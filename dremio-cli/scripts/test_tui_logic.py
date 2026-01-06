
import os
import sys
from pathlib import Path
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.client.factory import create_client
from dotenv import load_dotenv
from rich.console import Console

console = Console()
load_dotenv()

def get_env_config(prefix):
    """Get config from env vars with prefix."""
    ptype = os.getenv(f"{prefix}_TYPE")
    if not ptype: return None
    
    config = {
        "type": ptype,
        "base_url": os.getenv(f"{prefix}_BASE_URL"),
        "auth": {}
    }
    
    token = os.getenv(f"{prefix}_TOKEN")
    user = os.getenv(f"{prefix}_USERNAME")
    pwd = os.getenv(f"{prefix}_PASSWORD")
    pid = os.getenv(f"{prefix}_PROJECTID")
    
    if pid: config["project_id"] = pid
    
    if token:
        config["auth"]["type"] = "pat"
        config["auth"]["token"] = token
    elif user and pwd:
        config["auth"]["type"] = "username_password"
        config["auth"]["username"] = user
        config["auth"]["password"] = pwd
        
    return config

def test_tui_logic(prefix):
    console.rule(f"Testing TUI Logic: {prefix}")
    
    config = get_env_config(prefix)
    if not config:
        console.print(f"[yellow]Skipping {prefix}: variables not set[/yellow]")
        return

    try:
        client = create_client(config)
        
        # 1. Simulate CatalogTree.load_roots
        console.print("1. Fetching Roots (get_catalog)...")
        roots = client.get_catalog()
        data = roots.get("data", [])
        console.print(f"[green]✓ Found {len(data)} root items[/green]")
        
        if not data:
            console.print("[red]✗ No roots found, stopping.[/red]")
            return
            
        # Debug types
        types = set(i.get("type") for i in data)
        console.print(f"Found types: {types}")

        # 2. Simulate CatalogTree.load_children
        # We need to find a dataset to test preview
        dataset = None
        
        # Iterate through containers to find one with children
        # Limit to checking first 5 containers to avoid long wait
        for container in [c for c in data if c["type"] in ["SPACE", "SOURCE", "HOME", "CONTAINER"]][:5]:
            cid = container["id"]
            cpath = ".".join(container["path"])
            console.print(f"2. Checking container '{cpath}'...")
            
            try:
                details = client.get_catalog_item(cid)
                children = details.get("children", [])
                
                # Check for dataset
                ds = next((c for c in children if c["type"] in ["DATASET", "VIRTUAL_DATASET", "PHYSICAL_DATASET", "VIEW", "TABLE"]), None)
                if ds:
                    dataset = ds
                    console.print(f"[green]  ✓ Found dataset: {dataset['path']}[/green]")
                    break
            except:
                console.print(f"  [yellow]⚠ Failed to access {cpath}[/yellow]")

        if dataset:
            ds_path = ".".join([f'"{p}"' for p in dataset["path"]])
            console.print(f"3. Fetching Preview for '{ds_path}'...")
            
            # Fetch Details first (Schema/SQL)
            ds_details = client.get_catalog_item(dataset["id"])
            console.print(f"[green]✓ Fetched Metadata (Fields: {len(ds_details.get('fields', []))})[/green]")

            # Execute Preview SQL
            res = client.execute_sql(f"SELECT * FROM {ds_path} LIMIT 5")
            rows = res.get("rows", [])
            console.print(f"[green]✓ Fetched Preview ({len(rows)} rows)[/green]")
        else:
            console.print("[yellow]⚠ No dataset found in first 5 containers to test preview.[/yellow]")

    except Exception as e:
        console.print(f"[red]✗ Test Failed: {e}[/red]")
        # print stack string
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test Software (DREMIO_SOFTWARE_*)
    test_tui_logic("DREMIO_SOFTWARE")
    
    # Test Cloud (DREMIO_CLOUD_*)
    test_tui_logic("DREMIO_CLOUD")
