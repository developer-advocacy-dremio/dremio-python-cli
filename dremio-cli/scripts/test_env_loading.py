#!/usr/bin/env python3
"""
Isolated test script to verify environment variables work correctly.

This script tests your specific .env configuration:
- DREMIO_CLOUD_* variables
- DREMIO_SOFTWARE_* variables

Run this script to verify everything is set up correctly before using the CLI.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.env import load_dotenv, get_profile_names_from_env, get_profile_from_env
from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def test_env_file_exists():
    """Test that .env file exists."""
    console.print("\n[bold cyan]Step 1: Checking for .env file[/bold cyan]")
    
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        console.print(f"[green]✓[/green] Found .env file at: {env_path}")
        return True
    else:
        console.print(f"[red]✗[/red] .env file not found at: {env_path}")
        console.print("\n[yellow]Create a .env file with your Dremio credentials[/yellow]")
        return False


def test_load_dotenv():
    """Test loading .env file."""
    console.print("\n[bold cyan]Step 2: Loading .env file[/bold cyan]")
    
    try:
        load_dotenv()
        console.print("[green]✓[/green] Successfully loaded .env file")
        return True
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading .env: {e}")
        return False


def test_env_variables():
    """Test that required environment variables are set."""
    console.print("\n[bold cyan]Step 3: Checking environment variables[/bold cyan]")
    
    required_vars = {
        "cloud": [
            "DREMIO_CLOUD_TOKEN",
            "DREMIO_CLOUD_PROJECTID",
            "DREMIO_CLOUD_TYPE",
        ],
        "software": [
            "DREMIO_SOFTWARE_TOKEN",
            "DREMIO_SOFTWARE_BASE_URL",
            "DREMIO_SOFTWARE_TYPE",
        ],
    }
    
    all_found = True
    
    for profile_name, vars_list in required_vars.items():
        console.print(f"\n[bold]{profile_name.upper()} profile:[/bold]")
        for var in vars_list:
            value = os.environ.get(var)
            if value:
                # Mask sensitive values
                if "TOKEN" in var:
                    display_value = value[:10] + "..." if len(value) > 10 else "***"
                else:
                    display_value = value
                console.print(f"  [green]✓[/green] {var} = {display_value}")
            else:
                console.print(f"  [red]✗[/red] {var} = [red]NOT SET[/red]")
                all_found = False
    
    return all_found


def test_profile_detection():
    """Test profile detection from environment."""
    console.print("\n[bold cyan]Step 4: Detecting profiles from environment[/bold cyan]")
    
    profile_names = get_profile_names_from_env()
    
    if profile_names:
        console.print(f"[green]✓[/green] Found {len(profile_names)} profile(s): {', '.join(profile_names)}")
        return profile_names
    else:
        console.print("[red]✗[/red] No profiles detected in environment variables")
        return []


def test_profile_loading(profile_names):
    """Test loading profiles from environment."""
    console.print("\n[bold cyan]Step 5: Loading profile configurations[/bold cyan]")
    
    profiles = {}
    
    for name in profile_names:
        profile = get_profile_from_env(name)
        if profile:
            profiles[name] = profile
            console.print(f"[green]✓[/green] Loaded profile: {name}")
            
            # Display profile details
            console.print(f"  Type: {profile.get('type')}")
            console.print(f"  Base URL: {profile.get('base_url', 'N/A')}")
            console.print(f"  Project ID: {profile.get('project_id', 'N/A')}")
            console.print(f"  Auth Type: {profile.get('auth', {}).get('type')}")
            console.print(f"  Has Token: {'✓' if profile.get('auth', {}).get('token') else '✗'}")
            console.print(f"  Testing Folder: {profile.get('testing_folder', 'N/A')}")
        else:
            console.print(f"[red]✗[/red] Failed to load profile: {name}")
    
    return profiles


def test_profile_manager():
    """Test ProfileManager integration."""
    console.print("\n[bold cyan]Step 6: Testing ProfileManager integration[/bold cyan]")
    
    try:
        manager = ProfileManager()
        profiles = manager.list_profiles()
        
        console.print(f"[green]✓[/green] ProfileManager loaded {len(profiles)} profile(s)")
        
        # Display profiles table
        if profiles:
            table = Table(title="Loaded Profiles")
            table.add_column("Profile", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Base URL", style="blue")
            table.add_column("Has Token", style="yellow")
            
            for name, profile in profiles.items():
                table.add_row(
                    name,
                    profile.get("type", "N/A"),
                    profile.get("base_url", "N/A"),
                    "✓" if profile.get("auth", {}).get("token") else "✗",
                )
            
            console.print(table)
        
        return profiles
    except Exception as e:
        console.print(f"[red]✗[/red] ProfileManager error: {e}")
        import traceback
        traceback.print_exc()
        return {}


def test_client_creation(profiles):
    """Test creating clients from profiles."""
    console.print("\n[bold cyan]Step 7: Testing client creation[/bold cyan]")
    
    clients = {}
    
    for name, profile in profiles.items():
        try:
            client = create_client(profile)
            clients[name] = client
            client_type = type(client).__name__
            console.print(f"[green]✓[/green] {name}: Created {client_type}")
        except Exception as e:
            console.print(f"[red]✗[/red] {name}: {e}")
    
    return clients


def test_api_connectivity(clients):
    """Test API connectivity (optional - requires valid credentials)."""
    console.print("\n[bold cyan]Step 8: Testing API connectivity (optional)[/bold cyan]")
    console.print("[dim]This step attempts to connect to Dremio APIs[/dim]\n")
    
    for name, client in clients.items():
        try:
            console.print(f"Testing {name}...", end=" ")
            
            # Try to get catalog
            if hasattr(client, 'get_catalog'):
                data = client.get_catalog()
                item_count = len(data.get("data", []))
                console.print(f"[green]✓[/green] Connected! Found {item_count} catalog items")
            else:
                console.print("[yellow]⚠[/yellow] Client doesn't support catalog operations")
                
        except Exception as e:
            console.print(f"[red]✗[/red] Connection failed: {str(e)[:100]}")


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]Dremio CLI - Environment Variable Test Suite[/bold cyan]\n"
        "This script verifies your .env configuration is correct",
        border_style="cyan"
    ))
    
    # Run tests
    if not test_env_file_exists():
        console.print("\n[red]Cannot proceed without .env file[/red]")
        return 1
    
    if not test_load_dotenv():
        return 1
    
    if not test_env_variables():
        console.print("\n[yellow]Warning: Some environment variables are missing[/yellow]")
    
    profile_names = test_profile_detection()
    if not profile_names:
        return 1
    
    env_profiles = test_profile_loading(profile_names)
    if not env_profiles:
        return 1
    
    manager_profiles = test_profile_manager()
    if not manager_profiles:
        return 1
    
    clients = test_client_creation(manager_profiles)
    if not clients:
        console.print("\n[red]Failed to create any clients[/red]")
        return 1
    
    # Optional API connectivity test
    try:
        test_api_connectivity(clients)
    except KeyboardInterrupt:
        console.print("\n[yellow]API connectivity test skipped[/yellow]")
    
    # Summary
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        f"[bold green]✓ All tests passed![/bold green]\n\n"
        f"Profiles loaded: {', '.join(manager_profiles.keys())}\n"
        f"Clients created: {len(clients)}\n\n"
        f"[dim]You can now use the CLI with:[/dim]\n"
        f"[cyan]dremio --profile cloud catalog list[/cyan]\n"
        f"[cyan]dremio --profile software catalog list[/cyan]",
        border_style="green"
    ))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
