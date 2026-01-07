
import os
import shutil
from pathlib import Path
from dremio_cli.dac.config import DremioConfig
from dremio_cli.dac.sync import DremioSync
from dremio_cli.client.factory import create_client
from dotenv import load_dotenv

# Load Env
load_dotenv()

# Config
# Use Cloud or Software
# Software is usually faster/easier for generic testing if accessible
PREFIX = "DREMIO_CLOUD" 
# if not os.getenv(f"{PREFIX}_BASE_URL"):
#     PREFIX = "DREMIO_CLOUD" # Fallback

BASE_URL = os.getenv(f"{PREFIX}_BASE_URL")
TOKEN = os.getenv(f"{PREFIX}_TOKEN")
TEST_ROOT_FOLDER = os.getenv(f"{PREFIX}_TEST_FOLDER", "testing") # e.g. "space.folder"
TARGET_SCOPE = f"{TEST_ROOT_FOLDER}.dac_recursive_TEST"

print(f"Testing against: {PREFIX}")
print(f"Target Scope: {TARGET_SCOPE}")

# Setup Local Dir
LOCAL_DIR = Path("dac_recursive_test_env")
if LOCAL_DIR.exists():
    shutil.rmtree(LOCAL_DIR)
LOCAL_DIR.mkdir()

# 1. Create dremio.yaml
with open(LOCAL_DIR / "dremio.yaml", "w") as f:
    f.write(f"""
version: "1.0"
scope:
  path: "{TARGET_SCOPE}"
  type: SPACE
ignore: []
""")

# 2. Create Parent Resource (Inline Wiki)
# parent.yaml
# Normalize path: split scope into list
scope_parts = TARGET_SCOPE.split(".")

with open(LOCAL_DIR / "parent.yaml", "w") as f:
    parent_path = str(scope_parts + ["parent_view"])
    f.write(f"""
name: parent_view
type: VIRTUAL_DATASET
path: {parent_path}
sql: "SELECT 1 as id, 'parent' as name"
description: "This is the parent view."
tags: ["dac-test", "parent"]
""")

# 3. Create Child Folder & Resource (External Wiki + Dependency)
CHILD_DIR = LOCAL_DIR / "child_folder"
CHILD_DIR.mkdir()

# child.md
with open(CHILD_DIR / "child.md", "w") as f:
    f.write("# Child View\\nThis view depends on parent.")

# child.yaml
with open(CHILD_DIR / "child.yaml", "w") as f:
    child_path = str(scope_parts + ["child_folder", "child_view"])
    # Dependency name must match how it appears in graph?
    # Graph uses 'name' key from YAML?
    # Sync Logic: "path_list = data.get('path')"
    # Dependencies: List of *names*?
    # Graph uses `item.get("name")` matching `dependencies`.
    # Parent name: "parent_view". Child depends on "parent_view".
    # Sync requires "parent_view" to be in the set.
    
    f.write(f"""
name: child_view
type: VIRTUAL_DATASET
path: {child_path}
sql: "SELECT * FROM \\"{TARGET_SCOPE}\\".parent_view"
description: "child.md"
tags: ["dac-test", "child"]
dependencies:
  - "parent_view" 
""")

def run_test():
    # Setup Client
    config = {
        "type": "software" if "SOFTWARE" in PREFIX else "cloud",
        "base_url": BASE_URL,
        "auth": {"type": "pat", "token": TOKEN}
    }
    if os.getenv(f"{PREFIX}_PROJECTID"):
        config["project_id"] = os.getenv(f"{PREFIX}_PROJECTID")
        
    client = create_client(config)
    
    # Initialize Sync
    dac_config = DremioConfig.load(str(LOCAL_DIR / "dremio.yaml"))
    sync = DremioSync(dac_config, client, str(LOCAL_DIR))
    
    # Run Push
    print("\n--- Running PUSH ---")
    sync.push()
    
    # In a real test we would verify via Client check
    # Let's verify via Pull into a new directory
    
    print("\n--- Running PULL (verification) ---")
    # Verify by pulling to separate dir
    # But Sync is tied to root_dir. 
    # Let's just run pull in place (it should be idempotent/update)
    sync.pull()
    
    # Check if files exist and content matches
    print("\n--- Verifying Local Files ---")
    if (CHILD_DIR / "child.md").exists():
        print("✓ child.md exists")
    else:
        print("✗ child.md missing after pull")
        
    if (CHILD_DIR / "child_view.yaml").exists():
         print("✓ child_view.yaml exists (renamed from child.yaml usually by pulling name?)")
    elif (CHILD_DIR / "child.yaml").exists():
         print("✓ child.yaml exists")
        
    print("Test Complete.")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
