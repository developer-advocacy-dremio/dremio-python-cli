
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.client.software import SoftwareClient
from dremio_cli.client.auth import authenticate_with_username_password
from rich.console import Console
from dotenv import load_dotenv

console = Console()
load_dotenv()

def test_url_logic():
    console.rule("Testing URL Logic")
    
    # 1. Get raw config from env
    raw_url = os.getenv("DREMIO_SOFTWARE_BASE_URL") # likely .../api/v3
    token = os.getenv("DREMIO_SOFTWARE_TOKEN")
    
    if not raw_url:
        console.print("[red]DREMIO_SOFTWARE_BASE_URL not set in env.[/red]")
        return

    # Derive variants
    # normalized: ends with /api/v3 (what we expect input to be usually)
    # bare: root url (what user might input)
    
    if raw_url.endswith("/api/v3"):
        normalized_url = raw_url
        bare_url = raw_url[:-7]
    else:
        normalized_url = raw_url + "/api/v3"
        bare_url = raw_url.rstrip("/")

    console.print(f"Base Configuration:")
    console.print(f"  Existing Token (for Client test): {token[:10]}...")
    console.print(f"  Normalized URL: {normalized_url}")
    console.print(f"  Bare URL: {bare_url}")
    
    # Authenticate function requires username/password, which we might not have in env vars
    # checking DREMIO_USERNAME/PASSWORD
    username = os.getenv("DREMIO_USERNAME")
    password = os.getenv("DREMIO_PASSWORD")
    
    can_test_auth = username and password
    
    if can_test_auth:
        console.print("\n[bold]Test 1: Auth Logic (authenticate_with_username_password)[/bold]")
        
        # Test 1a: With Normalized URL
        try:
            console.print(f"  Testing with: {normalized_url}")
            t1 = authenticate_with_username_password(normalized_url, username, password)
            console.print("[green]  ✓ Success[/green]")
        except Exception as e:
            console.print(f"[red]  ✗ Failed: {e}[/red]")

        # Test 1b: With Bare URL
        try:
            console.print(f"  Testing with: {bare_url}")
            t2 = authenticate_with_username_password(bare_url, username, password)
            console.print("[green]  ✓ Success[/green]")
        except Exception as e:
            console.print(f"[red]  ✗ Failed: {e}[/red]")
    else:
        console.print("\n[yellow]Skipping Auth Logic test (credentials not found)[/yellow]")


    # Test 2: SoftwareClient Logic (get_catalog)
    console.print("\n[bold]Test 2: SoftwareClient Logic (get_catalog)[/bold]")
    
    # Test 2a: Init with Normalized URL
    try:
        console.print(f"  Testing Client init with: {normalized_url}")
        client1 = SoftwareClient(normalized_url, token)
        res1 = client1.get_catalog()
        console.print(f"[green]  ✓ Success (Found {len(res1.get('data', []))} items)[/green]")
    except Exception as e:
        console.print(f"[red]  ✗ Failed: {e}[/red]")

    # Test 2b: Init with Bare URL (The Refactor Test)
    try:
        console.print(f"  Testing Client init with: {bare_url}")
        client2 = SoftwareClient(bare_url, token)
        res2 = client2.get_catalog()
        console.print(f"[green]  ✓ Success (Found {len(res2.get('data', []))} items)[/green]")
    except Exception as e:
        console.print(f"[red]  ✗ Failed: {e}[/red]")

if __name__ == "__main__":
    test_url_logic()
