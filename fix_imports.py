import os

root_dir = r"c:\Users\Yoga\ValorTracker\ValorTracker\backend"

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py") and file != "fix_imports.py":
            filepath = os.path.join(subdir, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content.replace("from backend.", "from ")
            new_content = new_content.replace("import backend.", "import ")
            
            if new_content != content:
                print(f"Modifying {filepath}")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
