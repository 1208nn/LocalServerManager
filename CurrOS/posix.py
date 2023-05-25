from pathlib import Path
appdata_path = Path.home() / (".config" if not Path.home().startswith("/Users/") else "")
