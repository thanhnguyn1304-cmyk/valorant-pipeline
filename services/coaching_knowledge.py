"""
Valorant Coaching Knowledge Base
~200 coaching tips organized by category with metadata for filtering.
Each entry has: content (the tip), agent (or 'all'), map (or 'all'), category.
"""

COACHING_KNOWLEDGE = [
    # ─── AIM & CROSSHAIR PLACEMENT ───────────────────────────────────────────
    {
        "content": "If your headshot percentage is below 20%, focus on crosshair placement. Keep your crosshair at head height at all times, even when walking through empty areas. This builds muscle memory for where enemies will appear.",
        "agent": "all",
        "map": "all",
        "category": "aim",
    },
    {
        "content": "Practice your aim with 15-20 minutes of Deathmatch before ranked. Use Guardian-only DM to force yourself to aim for heads. After 2 weeks of this routine, your headshot percentage should improve by 5-10%.",
        "agent": "all",
        "map": "all",
        "category": "aim",
    },
    {
        "content": "If you consistently whiff the first bullet, slow down. Counter-strafing (tapping the opposite movement key before shooting) ensures your bullets are accurate. Practice this in the Range until it feels natural.",
        "agent": "all",
        "map": "all",
        "category": "aim",
    },
    {
        "content": "Pre-aim common angles as you walk around the map. Your crosshair should already be placed where an enemy's head will be when you peek. This reduces reaction time needed to land the first shot.",
        "agent": "all",
        "map": "all",
        "category": "aim",
    },
    {
        "content": "Spray transfer is important for clutch situations. In the practice range, line up 3 bots and practice killing all three with one spray. Control the recoil by pulling down and slightly in the opposite direction of the spray pattern.",
        "agent": "all",
        "map": "all",
        "category": "aim",
    },

    # ─── POSITIONING & GAME SENSE ─────────────────────────────────────────────
    {
        "content": "If you're dying more than 0.85 times per round, you're either over-peeking or holding bad angles. Play one angle, get a kill or info, then reposition. Never re-peek the same angle twice.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },
    {
        "content": "Off-angles win rounds. Instead of holding the obvious angle everyone expects, position slightly to the left or right. This gives you a split-second advantage because enemies pre-aim the common spot.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },
    {
        "content": "If your damage ratio (dealt vs taken) is below 1.0, you're getting hit before you can trade effectively. This usually means you're swinging too wide or taking fights where the enemy sees you first. Jiggle-peek to gather info instead.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },
    {
        "content": "In post-plant situations, don't push the enemy. You have time on your side. Hold an angle watching the bomb and force them to come to you. Playing passive in post-plant increases your win rate significantly.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },
    {
        "content": "When retaking a site, don't trickle in one by one. Coordinate with your team to push together from multiple angles. Trading kills is essential — if one teammate dies, the next should immediately refrag.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },
    {
        "content": "If you're bottom-fragging consistently, it might not be an aim issue. Check if you're rotating too late, playing too passively, or taking unnecessary duels. Sometimes impact is about staying alive rather than getting kills.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },
    {
        "content": "Play for information, not just kills. A well-timed callout about enemy positions is sometimes more valuable than a frag. Use sound cues and utility to gather info without exposing yourself.",
        "agent": "all",
        "map": "all",
        "category": "positioning",
    },

    # ─── ECONOMY ──────────────────────────────────────────────────────────────
    {
        "content": "Never force-buy every round. If the team loses pistol round, full save round 2 and buy round 3. A coordinated full buy beats a messy force buy. Track the team's economy and make buy calls together.",
        "agent": "all",
        "map": "all",
        "category": "economy",
    },
    {
        "content": "On eco rounds, play aggressive and close angles with Spectre or Sheriff. You need to get kills to have impact with lesser weapons. Don't play the same as you would with a Vandal.",
        "agent": "all",
        "map": "all",
        "category": "economy",
    },
    {
        "content": "If you win the pistol round, consider a light buy (Spectre + light armor) round 2 to maintain economy advantage while still being effective. Full saving after winning pistol is usually wasteful.",
        "agent": "all",
        "map": "all",
        "category": "economy",
    },

    # ─── MENTAL & CONSISTENCY ─────────────────────────────────────────────────
    {
        "content": "If your performance variance is high (some games 25 kills, others 5 kills), you likely tilt after bad rounds. Take a 3-second breath after dying. Don't immediately re-peek out of frustration.",
        "agent": "all",
        "map": "all",
        "category": "mental",
    },
    {
        "content": "If your K/D drops significantly in your last 5 games compared to your average, take a break. Playing through a slump usually makes it worse. Come back fresh after 30 minutes or the next day.",
        "agent": "all",
        "map": "all",
        "category": "mental",
    },
    {
        "content": "Warm up before ranked. Never queue for competitive as your first game of the day. Play 1-2 unrated or deathmatch games to get your aim and game sense warmed up.",
        "agent": "all",
        "map": "all",
        "category": "mental",
    },
    {
        "content": "Communication wins games. Even simple callouts like 'one low B main' can change the outcome of a round. If you're not comfortable talking, use text chat or the ping system at minimum.",
        "agent": "all",
        "map": "all",
        "category": "mental",
    },
    {
        "content": "Stop blaming teammates. Focus only on what YOU could have done differently each round. Review your deaths and ask: was that a fight I should have taken? Could I have played that differently?",
        "agent": "all",
        "map": "all",
        "category": "mental",
    },

    # ─── MAP-SPECIFIC TIPS ────────────────────────────────────────────────────
    # BIND
    {
        "content": "On Bind, use the teleporters aggressively on attack. Faking a teleporter sound can pull defenders out of position. Combo TP fakes with Hookah pushes for an easy B site take.",
        "agent": "all",
        "map": "Bind",
        "category": "map_strategy",
    },
    {
        "content": "On Bind defense, Hookah control is everything. If you lose Hookah, you lose B site. Use utility to hold it early and rotate through it to gather information about B main pushes.",
        "agent": "all",
        "map": "Bind",
        "category": "map_strategy",
    },
    {
        "content": "Bind A site is vulnerable to A short pushes. If you're defending A, don't play Showers too deep. Hold an angle where you can see both A short and A Bath entrances.",
        "agent": "all",
        "map": "Bind",
        "category": "map_strategy",
    },

    # ASCENT
    {
        "content": "On Ascent, mid control wins the map. If you consistently lose mid, the enemy has access to both sites. Prioritize taking mid with utility before committing to a site.",
        "agent": "all",
        "map": "Ascent",
        "category": "map_strategy",
    },
    {
        "content": "On Ascent defense, holding Market window gives you information on both mid and B main. This is a high-value position. Play it with a teammate covering your flank.",
        "agent": "all",
        "map": "Ascent",
        "category": "map_strategy",
    },
    {
        "content": "Ascent A site has many open angles which makes retakes difficult. When defending, play for time and utility. When attacking, clear site methodically — there are many corners to check.",
        "agent": "all",
        "map": "Ascent",
        "category": "map_strategy",
    },

    # HAVEN
    {
        "content": "Haven has three sites, which means defense is spread thin. On attack, default and look for the weak link. If one site has only one defender, that's your target.",
        "agent": "all",
        "map": "Haven",
        "category": "map_strategy",
    },
    {
        "content": "On Haven, the C site through Garage is dangerous. If you consistently die pushing Garage, try a C Long execute instead. Have a teammate smoke off Garage while the team pushes C Long.",
        "agent": "all",
        "map": "Haven",
        "category": "map_strategy",
    },
    {
        "content": "Haven mid doors give early information. If you're an attacker, taking mid control opens up splits to both A and C site. Use a smoke on mid window and push through courtyard.",
        "agent": "all",
        "map": "Haven",
        "category": "map_strategy",
    },

    # SPLIT
    {
        "content": "Split is a defender-sided map. On attack, you need coordinated executes with smokes and flashes. Don't dry-peek ramps or mid without utility — the angles favor defenders.",
        "agent": "all",
        "map": "Split",
        "category": "map_strategy",
    },
    {
        "content": "On Split, Heaven control is crucial for both sites. If you take A, immediately clear Heaven. If you take B, watch for players on top site. Post-plant positioning should always account for Heaven angles.",
        "agent": "all",
        "map": "Split",
        "category": "map_strategy",
    },

    # ICEBOX
    {
        "content": "On Icebox, the vertical angles make it unique. Always check above (rafters, pipes, containers). Many deaths come from not clearing vertical positions.",
        "agent": "all",
        "map": "Icebox",
        "category": "map_strategy",
    },
    {
        "content": "Icebox B site tube is a powerful position for defenders. If you keep dying to tube players, smoke it off before entering B site. Never push into tube without utility.",
        "agent": "all",
        "map": "Icebox",
        "category": "map_strategy",
    },

    # LOTUS
    {
        "content": "Lotus has rotating doors and destructible walls. Use destructible walls to create new angles mid-round. Many players forget about them, which can catch enemies off guard.",
        "agent": "all",
        "map": "Lotus",
        "category": "map_strategy",
    },
    {
        "content": "On Lotus, the three-site layout means rotations are key. If you hear the rotating doors spin, call it immediately — it tells you which direction the enemy is moving.",
        "agent": "all",
        "map": "Lotus",
        "category": "map_strategy",
    },

    # PEARL
    {
        "content": "Pearl is aim-heavy with long sight lines. If your headshot percentage is low, you'll struggle here. Play closer angles on Pearl and avoid long-range duels unless you have an Operator.",
        "agent": "all",
        "map": "Pearl",
        "category": "map_strategy",
    },

    # SUNSET
    {
        "content": "On Sunset, mid control is essential. The market area connects both sites, and whoever controls mid can rotate faster. Use utility to take mid before committing to a site hit.",
        "agent": "all",
        "map": "Sunset",
        "category": "map_strategy",
    },

    # ABYSS
    {
        "content": "On Abyss, the lack of barriers means falling off the map is a real danger. Be careful when moving near edges, especially during gunfights. Knockback abilities near edges can get environmental kills.",
        "agent": "all",
        "map": "Abyss",
        "category": "map_strategy",
    },

    # ─── AGENT-SPECIFIC TIPS ──────────────────────────────────────────────────
    # DUELISTS
    {
        "content": "As Jett, your value comes from creating space on entry. Dash into site, get a pick, and updraft to safety. If you're not entry-fragging as Jett, switch to a different agent — you're wasting her kit.",
        "agent": "Jett",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Jett's Cloudburst smokes are short duration but instant. Use them to cross angles safely or one-way smoke on defense. Don't waste them randomly — they're valuable for off-angle plays.",
        "agent": "Jett",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Reyna, you need kills to be useful. If you're not getting at least 1 kill per round, her kit does nothing. Consider switching to a more utility-focused agent if your K/D is consistently low on Reyna.",
        "agent": "Reyna",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Reyna's dismiss makes her the best agent for ego-peeking. Peek an angle, get a kill, immediately dismiss to safety. But if you're dying without getting kills, you're a liability to your team.",
        "agent": "Reyna",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Raze, your Paint Shells (grenades) are incredibly powerful for clearing corners. Always throw them into common hiding spots before pushing onto site. A well-placed grenade can get easy kills or force enemies out of position.",
        "agent": "Raze",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Raze's Blast Pack combo (satchel jump into Showstopper) is her signature play. Practice the timing in custom games — jump at the peak of the satchel boost for max distance and fire the rocket at the highest point.",
        "agent": "Raze",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Phoenix, use your flash for yourself and your team. Don't just throw it randomly — call it out so teammates can follow up. Curveball around corners before peeking for easy kills.",
        "agent": "Phoenix",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Neon, your sprint is for entry, not rotation. Use slide to take aggressive peeks and your wall to cut off sight lines when entering site. Neon with good movement is extremely hard to hit.",
        "agent": "Neon",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Yoru, your teleport should be placed in a safe spot before you peek. Get a kill or info, then teleport back to safety. Don't use it reactively — plan your escape before the fight starts.",
        "agent": "Yoru",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Iso, your shield ability is your best tool for taking duels. Activate it before peeking to absorb the first hit. This gives you a huge advantage in 1v1 situations. Always use it on entry.",
        "agent": "Iso",
        "map": "all",
        "category": "agent_tips",
    },

    # CONTROLLERS
    {
        "content": "As Omen, your smokes have global range. Smoke for your team's execute even if you're on the other side of the map. One-way smokes on defense are Omen's strongest tool — learn them for each site.",
        "agent": "Omen",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "If your K/D is low on Omen, remember you're a controller, not a duelist. Your primary job is smoking chokes, not taking fights. Smoke, flash for teammates, and play for trades.",
        "agent": "Omen",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Brimstone, your smokes are the longest lasting in the game. Use them to cut off rotations during a site execute, not just to block sight lines. Time your smokes to expire when your team needs to push.",
        "agent": "Brimstone",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Brimstone's Stim Beacon gives a fire rate boost to the whole team. Use it when pushing onto site — the extra fire rate helps win gunfights during executes.",
        "agent": "Brimstone",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Astra, your utility requires pre-planning. Place stars in key locations before the round starts. If you're reacting instead of planning, you're playing Astra wrong. Think two steps ahead.",
        "agent": "Astra",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Viper, your wall and smoke define the battlefield. On attack, use your wall to cut the site in half and isolate defenders. On defense, your poison cloud can deny an entire choke for the whole round.",
        "agent": "Viper",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Harbor, your cascade wall is a moving smoke that can push enemies off angles. Use it to walk onto site while your team follows behind. It's weaker than static smokes but more dynamic.",
        "agent": "Harbor",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Clove, your smokes can be cast after death. This means you should play aggressively early in the round — even if you die, you can still smoke for your team from the grave.",
        "agent": "Clove",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Clove's self-resurrect requires getting a kill or assist within a short time. Don't use it randomly — time it after getting an assist from a teammate's kill. The ult is strongest in chaotic fights.",
        "agent": "Clove",
        "map": "all",
        "category": "agent_tips",
    },

    # INITIATORS
    {
        "content": "As Sova, your recon arrow should be shot at the start of every round. Learn default recon lineups for each site. A well-placed recon dart gives your whole team wall-hacks for 3 seconds.",
        "agent": "Sova",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Sova's shock darts can clear corners without risking your life. Learn 2-3 lineups per map for common hiding spots. Double shock dart kills are devastating in post-plant.",
        "agent": "Sova",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Fade, use Haunt (eye) at the start of the round to reveal enemies, similar to Sova dart. But Fade's Prowler follows the trail, which is better for pushing specific angles that Haunt reveals.",
        "agent": "Fade",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Breach, your flashes and stun go through walls. This makes Breach the best agent for taking narrow corridors and choke points. Always flash through the wall before your team pushes through.",
        "agent": "Breach",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Skye, use your bird flash to gather info and blind enemies simultaneously. If the bird hits an enemy, it gives an audio cue. Use this to determine if an area is occupied before pushing.",
        "agent": "Skye",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As KAY/O, your suppression knife is a powerful tool for stopping enemy utility. Throw it into a site before executing to disable traps, smokes, and abilities. This makes retakes much harder for defenders.",
        "agent": "KAY/O",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Gekko, your creatures can be picked up and reused. Always try to recall your Dizzy (flash) and Wingman after using them. This gives you more utility than almost any other agent across a round.",
        "agent": "Gekko",
        "map": "all",
        "category": "agent_tips",
    },

    # SENTINELS
    {
        "content": "As Killjoy, your turret placement matters more than you think. Don't place it where enemies will see it immediately. Put it in a position where it shoots enemies in the back as they push past.",
        "agent": "Killjoy",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Killjoy's Lockdown ultimate forces enemies off a site entirely. Use it during retakes to force attackers to give up their post-plant positions. Don't use it in spots where enemies can easily destroy it.",
        "agent": "Killjoy",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Cypher, your tripwires are early warning systems. Place them in spots where enemies have to push through (doorways, corridors). The information from a triggered trip can save your whole team from a surprise push.",
        "agent": "Cypher",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Cypher's camera should watch flanks or unexpected angles. Don't put it in the most obvious spot. The longer it stays alive, the more information it provides. A good camera placement wins rounds.",
        "agent": "Cypher",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Chamber, your teleport anchors should be placed as escape routes. Take an aggressive peek, get a kill, and TP to safety. Chamber with a Tour De Force (Operator ultimate) holding long angles is extremely powerful.",
        "agent": "Chamber",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Sage, your wall is not just for blocking — it's for boosting teammates to off-angles. A Sage wall boost on defense can catch attackers completely off-guard. Learn creative wall placements for each site.",
        "agent": "Sage",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "Sage's slow orbs are criminally underused. Throw them in choke points when you hear a push. The slow + sound gives your team time to rotate and set up crossfires.",
        "agent": "Sage",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Deadlock, use your GravNet to slow pushes and her Barrier Mesh to block off areas. Deadlock excels at delaying enemy pushes and funneling them into specific paths.",
        "agent": "Deadlock",
        "map": "all",
        "category": "agent_tips",
    },
    {
        "content": "As Vyse, your utility can deny large areas. Her Shear ability is great for cutting off flanks, and Arc Rose provides excellent crowd control. Use her strategically to control key choke points during defense.",
        "agent": "Vyse",
        "map": "all",
        "category": "agent_tips",
    },

    # ─── ROLE-SPECIFIC TIPS ───────────────────────────────────────────────────
    {
        "content": "If you main duelists but have a low K/D, you're not fulfilling your role. Duelists are expected to entry frag and create space. If you can't do that consistently, try playing initiator instead — you can support without needing top fragging mechanics.",
        "agent": "all",
        "map": "all",
        "category": "role",
    },
    {
        "content": "Sentinel mains shouldn't chase kills. Your job is to hold a site and provide information. A sentinel that stays alive and gives callouts is more valuable than one who gets 2 kills and dies.",
        "agent": "all",
        "map": "all",
        "category": "role",
    },
    {
        "content": "As a controller, your team depends on your smokes. Dying with smokes still available is one of the worst things you can do. Stay alive and keep providing smokes throughout the round.",
        "agent": "all",
        "map": "all",
        "category": "role",
    },
    {
        "content": "Initiators should always use utility BEFORE their team pushes. Flash before entry, use recon before pushing, and stun common positions. If your team is dying on entry, you're not using your abilities early enough.",
        "agent": "all",
        "map": "all",
        "category": "role",
    },

    # ─── RANK-SPECIFIC ADVICE ─────────────────────────────────────────────────
    {
        "content": "In Iron to Bronze, focus only on crosshair placement and not dying. Don't worry about fancy utility usage or lineups. If you can consistently land headshots and reduce your deaths, you'll climb out of low ranks.",
        "agent": "all",
        "map": "all",
        "category": "rank_advice",
    },
    {
        "content": "In Silver to Gold, game sense becomes important. Learn to read the enemy's patterns — if they push B three rounds in a row, they'll probably push again or fake B. Start thinking about WHY enemies do things, not just reacting.",
        "agent": "all",
        "map": "all",
        "category": "rank_advice",
    },
    {
        "content": "In Platinum to Diamond, utility usage separates you from lower ranks. Learn 3-5 lineups per map for your agent. Coordinate utility combos with teammates (smoke + flash + push). Raw aim alone won't carry you above this rank.",
        "agent": "all",
        "map": "all",
        "category": "rank_advice",
    },
    {
        "content": "In Ascendant and above, team coordination and adaptability are key. You need to read the enemy's economy, track their utility, and adjust your strategy mid-game. Individual skill plateaus — teamwork scales.",
        "agent": "all",
        "map": "all",
        "category": "rank_advice",
    },

    # ─── CLUTCH & LATE ROUND PLAY ─────────────────────────────────────────────
    {
        "content": "In clutch situations (1vX), don't try to take all fights at once. Isolate each enemy into a 1v1. Use sound cues to track enemy positions and take them one at a time. Patience wins clutches.",
        "agent": "all",
        "map": "all",
        "category": "clutch",
    },
    {
        "content": "If your ACS drops in later rounds (rounds 20+), it suggests fatigue or tilt. In close games, stay hydrated, take deep breaths between rounds, and avoid autopiloting. Mental freshness wins overtime.",
        "agent": "all",
        "map": "all",
        "category": "clutch",
    },
    {
        "content": "When in a 1v1 post-plant, always play the bomb. As an attacker, hide near the bomb and listen for the defuse sound. As a defender, fake the defuse to bait out the attacker's peek.",
        "agent": "all",
        "map": "all",
        "category": "clutch",
    },

    # ─── AGENT + MAP COMBOS ───────────────────────────────────────────────────
    {
        "content": "Viper on Bind is extremely powerful. Her wall can cut B site in half, and her poison cloud can deny Hookah for the entire round. If you're struggling on Bind, consider picking Viper.",
        "agent": "Viper",
        "map": "Bind",
        "category": "agent_map_combo",
    },
    {
        "content": "Sova on Ascent is one of the best agent-map combinations. His recon dart can scan mid from safety, and his shock darts can clear Market and Tree corners. Learn Ascent-specific Sova lineups.",
        "agent": "Sova",
        "map": "Ascent",
        "category": "agent_map_combo",
    },
    {
        "content": "Killjoy on Split is a lockdown machine. Her turret and alarmbot can hold B site alone, letting your team stack A. Her ultimate can single-handedly win retakes on Split's tight sites.",
        "agent": "Killjoy",
        "map": "Split",
        "category": "agent_map_combo",
    },
    {
        "content": "Brimstone on Bind works well because the map is small enough for his smoke range. His molly can deny planting or defusing from safe positions, and stim beacon in Hookah fights gives a big advantage.",
        "agent": "Brimstone",
        "map": "Bind",
        "category": "agent_map_combo",
    },
    {
        "content": "Breach on Haven is very effective because Haven's corridors and doorways play perfectly into his through-wall abilities. His flash and stun can control Garage, A Long, and C Long without exposing himself.",
        "agent": "Breach",
        "map": "Haven",
        "category": "agent_map_combo",
    },
    {
        "content": "Cypher on Lotus excels due to the rotating doors. His tripwires on door paths catch rotators, and his camera can watch multiple angles through the unique map geometry.",
        "agent": "Cypher",
        "map": "Lotus",
        "category": "agent_map_combo",
    },
    {
    "content": "Sova is incredibly strong on Ascent due to the paper-thin walls. Pair his recon dart or drone with an Odin to easily wallbang enemies pushing B Main or A Main.",
    "agent": "Sova",
    "map": "Ascent",
    "category": "agent_map_combo"
  },
  {
    "content": "As Clove, your smokes can be cast after death, but their range is restricted to near your corpse. If you are going to take a risky duel, doing so in central areas like Mid allows you to continue smoking critical chokes on both sites post-mortem.",
    "agent": "Clove",
    "map": "all",
    "category": "agent_tips"
  },
  {
    "content": "On Breeze, a double controller setup with Viper and Astra or Omen gives you immense map control. Viper's wall cuts the large sightlines, while the secondary smoker handles localized chokes.",
    "agent": "Viper",
    "map": "Breeze",
    "category": "map_strategy"
  },
  {
    "content": "When holding an off-angle, stay completely still. Unnecessary movement (like jiggling) makes it harder for you to shoot accurately first. Let the element of surprise do the work.",
    "agent": "all",
    "map": "all",
    "category": "positioning"
  },
  {
    "content": "Use your keyboard movement to help your crosshair micro-adjustments. If your crosshair is slightly to the left of their head, step right instead of relying entirely on raw mouse flicks.",
    "agent": "all",
    "map": "all",
    "category": "aim"
  },
  {
    "content": "Scoreboard anxiety can cripple your confidence and cause you to overthink. If you find yourself tilting or hyper-focusing on your teammates' K/D ratios, unbind your scoreboard key for a few days to stay focused entirely on the current round.",
    "agent": "all",
    "map": "all",
    "category": "mental"
  },
  {
    "content": "As an initiator, understand if your agent provides 'info' (Sova, Fade) or 'flashes' (Breach, Skye). You must proactively communicate and set up your duelists with your utility before they entry, rather than using it selfishly or reacting too late.",
    "agent": "all",
    "map": "all",
    "category": "role"
  },
  {
    "content": "To break out of Ascendant into Immortal/Radiant, you need to stop auto-piloting and develop game sense. Start mentally tracking the enemy economy, ultimate points, and team composition gaps before the buy phase barrier drops.",
    "agent": "all",
    "map": "all",
    "category": "rank_advice"
  },
  {
    "content": "In a 1vX clutch situation, isolation is your best friend. Use your utility, positioning, and movement to force a series of 1v1 duels instead of wide-swinging into multiple enemies at once. Patience forces the enemy to get overconfident and make mistakes.",
    "agent": "all",
    "map": "all",
    "category": "clutch"
  },
  {
    "content": "If your team cannot afford a full buy, explicitly communicate a save. Try to keep your credits above 3900 so you can comfortably buy a rifle, heavy shields, and essential utility in the following round.",
    "agent": "all",
    "map": "all",
    "category": "economy"
  },
  {
    "content": "As Jett, your dash is your most valuable asset, but don't waste it defensively unless necessary. Use it proactively to break crosshairs by dashing into your initiator's utility (like a Sova dart or Fade haunt) to take space and force the defense to turn.",
    "agent": "Jett",
    "map": "all",
    "category": "agent_tips"
  },
  {
    "content": "On Bind, establishing early Shower control is crucial for Attackers. It prevents defenders from pushing up for free info and gives your team the threat of a fast A execute, which forces rotations and opens up B site.",
    "agent": "all",
    "map": "Bind",
    "category": "map_strategy"
  },
  {
    "content": "Stop holding static, head-level common angles where pre-fires happen. Play off-angles—either slightly wider or tighter than expected. Always secure an escape route so you can get one pick and fall back without getting traded.",
    "agent": "all",
    "map": "all",
    "category": "positioning"
  },
  {
    "content": "Omen is almost a necessity on Split. His Paranoia gets massive value through the walls in B Main or Mid Mail, and his ability to repeatedly throw one-way smokes in A Main completely shuts down fast attacker executes.",
    "agent": "Omen",
    "map": "Split",
    "category": "agent_map_combo"
  },
  {
    "content": "Crosshair placement isn't just about aiming at head height; it's about predicting enemy momentum. If you anticipate a wide swing (like a Neon or a highly aggressive Duelist), hold your crosshair further out from the wall to account for human reaction time.",
    "agent": "all",
    "map": "all",
    "category": "aim"
  },
  {
    "content": "Consistency stems from routine, not hype. Queueing while tilted is the fastest way to hemorrhage RR. If you lose two games in a row, take a 15-minute break to reset mentally. Don't carry the frustration of the last match into the pistol round of the next.",
    "agent": "all",
    "map": "all",
    "category": "mental"
  },
  {
    "content": "If you are playing a Sentinel, your job isn't just to passively anchor a site and die to a 5-man rush. If the enemies consistently hit the opposite site, communicate with your team to stack it, or aggressively push your main for early map control and information.",
    "agent": "all",
    "map": "all",
    "category": "role"
  },
  {
    "content": "To push out of Ascendant and break into Immortal/Radiant, mechanical skill is no longer enough. You must win micro-situations by trading your teammates efficiently and understanding default timings before the round even starts.",
    "agent": "all",
    "map": "all",
    "category": "rank_advice"
  },
  {
    "content": "In post-plant 1vX scenarios, play the spike, not the players. If you tap the bomb to fake a defuse, immediately hold an angle and listen for their running audio. Force them to panic and isolate the 1v1 duels.",
    "agent": "all",
    "map": "all",
    "category": "clutch"
  },
  {
    "content": "When your team is up 2-0 and the enemy is on a bonus or full eco round, group up and play as a pack. The worst thing you can do is give them isolated 1v1s where they can pick up a dropped rifle and swing the momentum of the half.",
    "agent": "all",
    "map": "all",
    "category": "economy"
  },
  {
    "content": "When double-satcheling as Raze, don't look straight down. Look slightly forward and down at an angle to maximize horizontal momentum rather than just vertical height, allowing you to break crosshairs faster when entering a site.",
    "agent": "Raze",
    "map": "all",
    "category": "agent_tips"
  },
  {
    "content": "Icebox Mid control is heavily underutilized in lower ranks. Sending one player to lurk under Tube or pressure Boiler forces the defense to anchor mid, relieving pressure from the main choke points on A and B.",
    "agent": "all",
    "map": "Icebox",
    "category": "map_strategy"
  },
  {
    "content": "Stop clearing angles with your W key. When you need to peek, use A or D to swing perpendicular to the angle. Diagonal movement makes you slower on the enemy's screen and easier to hit.",
    "agent": "all",
    "map": "all",
    "category": "positioning"
  },
  {
    "content": "Killjoy's B site defense on Ascent is meta for a reason, but it becomes predictable. To avoid getting your setup broken by Sova shocks or Kayo knives, alternate your turret between B Main wall, market, and CT every few rounds.",
    "agent": "Killjoy",
    "map": "Ascent",
    "category": "agent_map_combo"
  },
  {
    "content": "When clearing deep elevation changes (like A Ramps on Split or A Heaven on Haven), don't gradually adjust your crosshair up the ramp. Snap your crosshair directly to the expected head height of the new elevation before you fully expose yourself.",
    "agent": "all",
    "map": "all",
    "category": "aim"
  },
  {
    "content": "Radiant isn't about hitting every shot; it's about not spiraling when you miss. If you are having an off-aim day, switch your focus to hyper-communicating, playing heavy utility agents, and setting your teammates up for trades.",
    "agent": "all",
    "map": "all",
    "category": "mental"
  },
  {
    "content": "As a Controller, throwing a smoke right as the barrier drops tells the enemy exactly where you are and wastes 15 seconds of your smoke duration. Hold your smokes until your team is actually taking map control or the enemy is committing to a hit.",
    "agent": "all",
    "map": "all",
    "category": "role"
  },
  {
    "content": "Stop blaming your teammates for being hardstuck. Review your own VODs and look at your deaths. Ask yourself: 'Did I have to take that fight?' and 'Was my team in a position to trade me?' If the answer is no, the mistake was yours.",
    "agent": "all",
    "map": "all",
    "category": "rank_advice"
  },
  {
    "content": "In a 1v2 post-plant, if you get the first kill, immediately reposition. The second player will try to swing off the contact of the first. By moving, you force them to clear your old angle while you hold the crossfire.",
    "agent": "all",
    "map": "all",
    "category": "clutch"
  },
  {
    "content": "Understanding the 'bonus' round is critical. If you win pistol and round 2, round 3 is your bonus. Do not buy full rifles unless you survived. Keep your spectres, play close angles, and try to break the enemy's economy by securing 2-3 kills.",
    "agent": "all",
    "map": "all",
    "category": "economy"
  },
  {
    "content": "Cypher's camera shouldn't just be used for spotting the initial push. Place it high and deep on site so that when the enemy executes, you can tag them through your cages while they are actively planting or scaling.",
    "agent": "Cypher",
    "map": "all",
    "category": "agent_tips"
  },
  {
    "content": "On Sunset, Mid control dictates the entire half. Defenders must fight for Mid Tiles and Bottom Mid using utility, otherwise Attackers can freely pinch either site and force the defense into unwinnable retakes.",
    "agent": "all",
    "map": "Sunset",
    "category": "map_strategy"
  },
  {
    "content": "When holding a corner, play as far back from the wall as the geometry allows. Due to how perspective works, the player further from the angle will see the opponent's shoulder before the opponent sees them.",
    "agent": "all",
    "map": "all",
    "category": "positioning"
  },
  {
    "content": "Breach on Fracture is a nightmare for defenders. Use your Fault Line down A Main or B Main off cooldown at the start of the round to completely deny aggressive defender pushes and secure ultimate orbs for free.",
    "agent": "Breach",
    "map": "Fracture",
    "category": "agent_map_combo"
  },
  {
    "content": "If you are holding an angle with an Operator, don't hold the absolute edge of the wall. Give yourself a small gap to account for human reaction time, otherwise fast-swinging Neon or Jett players will pass your crosshair before you click.",
    "agent": "all",
    "map": "all",
    "category": "aim"
  },
  {
    "content": "Mute toxic teammates instantly. Do not argue with them. Engaging in an argument takes your mental bandwidth away from the game and ruins the vibe for the other three players. Communicate via pings if necessary.",
    "agent": "all",
    "map": "all",
    "category": "mental"
  },
  {
    "content": "If you play Sentinel, your life is heavily tied to flank watch. If you die first pushing mid for no reason, your team loses their trips/alarmbots, and the attackers are forced to play paranoid for the rest of the round.",
    "agent": "all",
    "map": "all",
    "category": "role"
  },
  {
    "content": "To climb efficiently, limit your agent pool. Playing 8 different agents across 4 roles means you are a master of none. Pick 2 agents in a primary role, and 1 backup agent in a secondary role, and master their micro-mechanics.",
    "agent": "all",
    "map": "all",
    "category": "rank_advice"
  },
  {
    "content": "When playing time in a 1v1 post-plant, jiggle peeking the spike is safer than wide swinging. Show just your shoulder to bait out their shot, then hide again. Every second they spend resetting their aim is a second closer to detonation.",
    "agent": "all",
    "map": "all",
    "category": "clutch"
  },
  {
    "content": "Track enemy ultimates during the buy phase. If the enemy Killjoy has lockdown, your team needs a plan to break it (Sova ult, Raze nade) or you must explicitly decide to play for a fast retake before the round even starts.",
    "agent": "all",
    "map": "all",
    "category": "economy"
  }
]
