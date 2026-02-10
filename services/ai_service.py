"""
AI Trainer Service - The "Analyst"
Queries match data and identifies player weaknesses.
"""

from collections import defaultdict
import json
import statistics
from sqlmodel import Session, select, desc
import google.generativeai as genai
from backend.core.config import settings
from backend.models.match import MatchParticipation
from backend.services.knowledge_base import search_knowledge

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)



def get_recent_matches(puuid: str, db: Session, limit: int = 20) -> list[MatchParticipation]:
    """Fetch the most recent N matches for a player."""
    statement = (
        select(MatchParticipation)
        .where(MatchParticipation.puuid == puuid)
        .order_by(desc(MatchParticipation.start_time))
        .limit(limit)
    )
    return db.exec(statement).all()


# ─── 1. Core Performance Stats ───────────────────────────────────────────────

def get_aggregate_stats(matches: list[MatchParticipation]) -> dict:
    """Calculate overall averages across all provided matches."""
    total = len(matches)
    if total == 0:
        return {}

    avg_kd = sum(m.kills / max(m.deaths, 1) for m in matches) / total
    avg_adr = sum(m.damage_dealt / m.rounds_played for m in matches) / total
    avg_acs = sum(m.combat_score / m.rounds_played for m in matches) / total
    avg_hs = sum(
        m.headshots / max(m.headshots + m.othershots, 1) * 100
        for m in matches
    ) / total
    deaths_per_round = sum(m.deaths / m.rounds_played for m in matches) / total
    win_rate = sum(1 for m in matches if m.result == "win") / total

    return {
        "avg_kd": round(avg_kd, 2),
        "avg_adr": round(avg_adr),
        "avg_acs": round(avg_acs),
        "avg_hs": round(avg_hs),
        "deaths_per_round": round(deaths_per_round, 2),
        "win_rate": round(win_rate, 2),
        "total_matches": total,
    }


# ─── 2. Map-Specific Win Rate ────────────────────────────────────────────────

def get_map_stats(matches: list[MatchParticipation]) -> list[dict]:
    """Group matches by map and compute per-map win rates."""
    maps = defaultdict(list)
    for m in matches:
        maps[m.map].append(m)

    map_stats = []
    for map_name, games in maps.items():
        if len(games) < 3:
            continue

        wins = sum(1 for g in games if g.result == "win")
        avg_kd = sum(g.kills / max(g.deaths, 1) for g in games) / len(games)
        avg_acs = sum(g.combat_score / g.rounds_played for g in games) / len(games)

        map_stats.append({
            "map": map_name,
            "games": len(games),
            "win_rate": round(wins / len(games), 2),
            "avg_kd": round(avg_kd, 2),
            "avg_acs": round(avg_acs),
        })

    return map_stats


# ─── 3. Agent Performance ────────────────────────────────────────────────────

def get_agent_stats(matches: list[MatchParticipation]) -> list[dict]:
    """Group matches by agent and compare performance."""
    agents = defaultdict(list)
    for m in matches:
        agents[m.agent_name].append(m)

    agent_stats = []
    for agent, games in agents.items():
        if len(games) < 2:
            continue

        wins = sum(1 for g in games if g.result == "win")
        avg_kd = sum(g.kills / max(g.deaths, 1) for g in games) / len(games)
        avg_acs = sum(g.combat_score / g.rounds_played for g in games) / len(games)

        agent_stats.append({
            "agent": agent,
            "games": len(games),
            "win_rate": round(wins / len(games), 2),
            "avg_kd": round(avg_kd, 2),
            "avg_acs": round(avg_acs),
        })

    return agent_stats


# ─── 4. Consistency Check ────────────────────────────────────────────────────

def get_consistency(matches: list[MatchParticipation]) -> dict:
    """Measure performance variance — high = inconsistent player."""
    if len(matches) < 3:
        return {"kd_std": 0, "acs_std": 0}

    kd_values = [m.kills / max(m.deaths, 1) for m in matches]
    acs_values = [m.combat_score / m.rounds_played for m in matches]

    return {
        "kd_std": round(statistics.stdev(kd_values), 2),
        "acs_std": round(statistics.stdev(acs_values), 2),
    }


# ─── 5. Impact Rating ────────────────────────────────────────────────────────

def get_impact_stats(matches: list[MatchParticipation]) -> dict:
    """How often does this player carry vs get carried?"""
    total = len(matches)
    if total == 0:
        return {}

    return {
        "avg_position": round(sum(m.position for m in matches) / total, 1),
        "top2_rate": round(sum(1 for m in matches if m.position <= 2) / total, 2),
        "bottom2_rate": round(sum(1 for m in matches if m.position >= 9) / total, 2),
        "mvp_count": sum(1 for m in matches if m.position == 1),
    }


# ─── 6. Trend Detection ──────────────────────────────────────────────────────

def get_trend(matches: list[MatchParticipation]) -> dict:
    """Compare last 5 games vs previous 15 to detect improvement/slump."""
    if len(matches) < 6:
        return {"kd_trend": 0, "acs_trend": 0, "direction": "not_enough_data"}

    recent = matches[:5]
    older = matches[5:]

    recent_kd = sum(m.kills / max(m.deaths, 1) for m in recent) / len(recent)
    older_kd = sum(m.kills / max(m.deaths, 1) for m in older) / len(older)

    recent_acs = sum(m.combat_score / m.rounds_played for m in recent) / len(recent)
    older_acs = sum(m.combat_score / m.rounds_played for m in older) / len(older)

    kd_diff = round(recent_kd - older_kd, 2)

    return {
        "kd_trend": kd_diff,
        "acs_trend": round(recent_acs - older_acs),
        "direction": "improving" if kd_diff > 0.1 else "slumping" if kd_diff < -0.1 else "stable",
    }


# ─── 7. THE FULL WEAKNESS DETECTOR ───────────────────────────────────────────

def detect_weaknesses(puuid: str, db: Session) -> dict:
    """
    Main entry point. Fetches last 20 matches, runs all analyses,
    and returns structured weakness data for the LLM to use.
    """
    matches = get_recent_matches(puuid, db, limit=20)

    if len(matches) < 3:
        return {"error": "Not enough matches to analyze (need at least 3)"}

    stats = get_aggregate_stats(matches)
    map_data = get_map_stats(matches)
    agent_data = get_agent_stats(matches)
    consistency = get_consistency(matches)
    impact = get_impact_stats(matches)
    trend = get_trend(matches)

    # ── Identify weaknesses ──
    weaknesses = []

    # K/D check
    if stats["avg_kd"] < 0.9:
        weaknesses.append({
            "type": "low_kd",
            "severity": "high",
            "message": f"Your K/D ({stats['avg_kd']}) is below 0.9 — you're dying more than you're killing.",
        })

    # Headshot check
    if stats["avg_hs"] < 20:
        weaknesses.append({
            "type": "low_headshot",
            "severity": "medium",
            "message": f"Your HS% ({stats['avg_hs']}%) is low — crosshair placement needs work.",
        })

    # Deaths per round
    if stats["deaths_per_round"] > 0.85:
        weaknesses.append({
            "type": "dying_too_much",
            "severity": "high",
            "message": f"You die {stats['deaths_per_round']} times per round — likely over-peeking or bad positioning.",
        })

    # Map weaknesses
    for m in map_data:
        if m["win_rate"] < 0.40:
            weaknesses.append({
                "type": "weak_map",
                "severity": "high",
                "message": f"Your {m['map']} win rate is {int(m['win_rate']*100)}% over {m['games']} games.",
                "map": m["map"],
            })

    # Agent weaknesses
    for a in agent_data:
        if a["avg_kd"] < stats["avg_kd"] * 0.8:
            weaknesses.append({
                "type": "weak_agent",
                "severity": "medium",
                "message": f"Your {a['agent']} K/D ({a['avg_kd']}) is significantly below your average ({stats['avg_kd']}).",
                "agent": a["agent"],
            })

    # Bottom-fragger check
    if impact["bottom2_rate"] > 0.30:
        weaknesses.append({
            "type": "low_impact",
            "severity": "high",
            "message": f"You're bottom-fragging in {int(impact['bottom2_rate']*100)}% of your games.",
        })

    # Consistency check
    if consistency["kd_std"] > 0.6:
        weaknesses.append({
            "type": "inconsistent",
            "severity": "medium",
            "message": f"Your K/D varies a lot (std: {consistency['kd_std']}). You're either popping off or feeding.",
        })

    # Trend check
    if trend["direction"] == "slumping":
        weaknesses.append({
            "type": "slumping",
            "severity": "medium",
            "message": f"Your K/D dropped by {abs(trend['kd_trend'])} over your last 5 games — possible tilt.",
        })

    # Sort by severity (high first)
    severity_order = {"high": 3, "medium": 2, "low": 1}
    weaknesses.sort(key=lambda w: severity_order[w["severity"]], reverse=True)

    return {
        "summary": stats,
        "maps": map_data,
        "agents": agent_data,
        "consistency": consistency,
        "impact": impact,
        "trend": trend,
        "weaknesses": weaknesses,
    }


# ─── 8. THE ORCHESTRATOR (Analyst + Librarian + Writer) ──────────────────────

def generate_coaching_report_stream(puuid: str, db: Session):
    """
    Orchestrates the full AI coaching process:
    1. Analyst: Analyzes matches to find weaknesses
    2. Librarian: Searches knowledge base for relevant tips
    3. Writer: Streams a personalized coaching report using Gemini
    """
    # 1. Analyst: Get stats and weaknesses
    data = detect_weaknesses(puuid, db)

    if "error" in data:
        yield f"Error: {data['error']}\n"
        return

    weaknesses = data["weaknesses"]
    stats = data["summary"]

    # 2. Librarian: Gather relevant coaching tips
    # We'll search for tips related to the top 3 weaknesses
    relevant_tips = []
    seen_content = set()

    for w in weaknesses[:3]:
        # Formulate a search query from the weakness
        query = f"tips for {w['type']} {w.get('agent', '')} {w.get('map', '')}"
        
        # Filter by agent/map if applicable
        agent_filter = w.get("agent")
        map_filter = w.get("map")

        results = search_knowledge(query, top_k=2, agent_filter=agent_filter, map_filter=map_filter)
        
        for tip in results:
            if tip["content"] not in seen_content:
                relevant_tips.append(tip)
                seen_content.add(tip["content"])

    # 3. Writer: Construct Prompt
    prompt = f"""
    You are a professional Valorant coach. Write a personalized training report for a player with the following stats.

    PLAYER PROFILE:
    - Average K/D: {stats.get('avg_kd')}
    - Headshot %: {stats.get('avg_hs')}% (Goal: >20%)
    - Win Rate: {int(stats.get('win_rate', 0)*100)}%
    - Deaths/Round: {stats.get('deaths_per_round')}

    IDENTIFIED WEAKNESSES:
    {json.dumps(weaknesses[:3], indent=2)}

    RELEVANT COACHING KNOWLEDGE (Use these tips!):
    {json.dumps([t['content'] for t in relevant_tips], indent=2)}

    INSTRUCTIONS:
    - Be encouraging but direct.
    - Start with a quick summary of their playstyle.
    - Focus on their top 3 weaknesses.
    - For each weakness, explain WHY it's bad and use the relevant coaching knowledge to give a SPECIFIC drill or tip.
    - Use formatting (bullet points, bold text) to make it readable.
    - Keep it under 300 words.
    """

    # 4. Stream Response
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            yield chunk.text

