
import os
import sys
import shutil
from pathlib import Path
from dremio_cli.config import ProfileManager
from dremio_cli.dac.config import DremioConfig
from dremio_cli.dac.sync import DremioSync

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.client.software import SoftwareClient
from dremio_cli.client.cloud import CloudClient
from rich.console import Console

console = Console()

def run_test():
    console.print("[bold]Running Dremio-as-Code Manual Test[/bold]")
    
    # 1. Setup Test Environment (Use Env Vars provided by User)
    # We will simulate a project directory in `tests/dac_test_project`
    test_project_dir = Path("tests/dac_test_project")
    if test_project_dir.exists():
        shutil.rmtree(test_project_dir)
    test_project_dir.mkdir(parents=True)
    
    # Create dremio.yaml
    # We need to decide which env to test. Let's test SOFTWARE first as it has "Spaces".
    # User provided: DREMIO_SOFTWARE_TEST_FOLDER=dremio-catalog.alexmerced.testing
    
    # Check if Software env vars exist (they should be in .env, but script doesn't read .env automatically unless we tell it)
    from dotenv import load_dotenv
    load_dotenv()
    
    base_url = os.getenv("DREMIO_SOFTWARE_BASE_URL")
    token = os.getenv("DREMIO_SOFTWARE_TOKEN")
    folder_path = os.getenv("DREMIO_SOFTWARE_TEST_FOLDER") # e.g. "dremio-catalog.alexmerced.testing"
    
    if not (base_url and token and folder_path):
        console.print("[yellow]Software env vars missing. Trying Cloud...[/yellow]")
        base_url = os.getenv("DREMIO_CLOUD_BASE_URL")
        token = os.getenv("DREMIO_CLOUD_TOKEN")
        folder_path = os.getenv("DREMIO_CLOUD_TEST_FOLDER") # "testing"
        is_cloud = True
        if not (base_url and token and folder_path):
             console.print("[red]No environment variables found for testing.[/red]")
             return
    else:
        is_cloud = False

    console.print(f"Testing against: {base_url} (Cloud: {is_cloud})")
    console.print(f"Scope: {folder_path}")

    # Create dremio.yaml
    yaml_content = f"""
version: "1.0"
scope:
  path: "{folder_path}"
  type: "SPACE" 
ignore:
  - "*.tmp"
"""
    with open(test_project_dir / "dremio.yaml", "w") as f:
        f.write(yaml_content)

    # 2. Initialize Client
    if is_cloud:
        client = CloudClient(base_url, token, os.getenv("DREMIO_CLOUD_PROJECTID"))
    else:
        client = SoftwareClient(base_url, token)

    # 3. Create a Test View in Dremio (to have something to Pull)
    # Ensure the root exists. 
    # For Cloud "testing" might be a project-level source? No, "Space".
    # Let's try to list catalog to see if it exists.
    try:
        # Create a dummy view at current_scope.view1
        # We need to execute SQL to create view? Or use create_view/create_catalog
        # Let's rely on `execute_sql` as it's easiest.
        
        view_name = "dac_test_view"
        full_view_path = f"{folder_path}.{view_name}"
        create_sql = f"CREATE OR REPLACE VIEW \"{folder_path}\".\"{view_name}\" AS SELECT 1 as val"
        
        # We might need to handle quoting better for "dremio-catalog.alexmerced.testing"
        # If it's dot separated, we might need to quote parts.
        # Simplest: Just try to pull whatever is there first.
        
        # console.print("Creating test view...")
        # client.execute_sql(create_sql) 
        pass 
    except Exception as e:
        console.print(f"Setup warning: {e}")

    # 4. Test Pull
    console.rule("Testing PULL")
    config = DremioConfig.load(str(test_project_dir / "dremio.yaml"))
    syncer = DremioSync(config, client, str(test_project_dir))
    syncer.pull()
    
    # Verify files exist
    found_files = list(test_project_dir.glob("**/*.yaml"))
    console.print(f"Files found: {len(found_files)}")
    for f in found_files:
        console.print(f" - {f.relative_to(test_project_dir)}")
        
    # 5. Test Push (Modification)
    console.rule("Testing PUSH")
    # Find a view yaml (if any) and modify it
    # note: if pull found nothing, create a local file
    
    dummy_view_name = "local_new_view"
    dummy_sql = f"{test_project_dir}/{dummy_view_name}.sql"
    dummy_yaml = f"{test_project_dir}/{dummy_view_name}.yaml"
    
    with open(dummy_sql, "w") as f:
        f.write("SELECT 2 as val")
        
    with open(dummy_yaml, "w") as f:
        # Write valid YAML for DAC
        # path is relative to scope? No, path in YAML is full path usually.
        # But we want to map it to file structure.
        # State uses full path.
        # Config has scope path.
        full_path_list = folder_path.split(".") + [dummy_view_name]
        
        import yaml
        yaml.dump({
            "type": "VIEW",
            "path": full_path_list,
            "sql_file": f"{dummy_view_name}.sql",
            "context": []
        }, f)
        
    # Re-init syncer to reload state/scan
    syncer = DremioSync(config, client, str(test_project_dir))
    syncer.push(dry_run=False)
    
    # 6. Verify Push created/updated view
    # Try to fetch it
    try:
        # check if exists
        # client.get_catalog_item_by_path ...
        console.print("[green]Verification: Check Dremio UI for 'local_new_view'[/green]")
    except:
        pass

if __name__ == "__main__":
    run_test()
