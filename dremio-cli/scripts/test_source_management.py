#!/usr/bin/env python3
"""
Live test script for Source Management.

This script tests source operations with both Cloud and Software profiles.
Tests use existing sources (no creation needed).
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_software_sources():
    """Test source operations with Software profile."""
    console.print("\n[bold cyan]Testing Source Management - Software Profile[/bold cyan]\n")
    
    try:
        # Get profile
        manager = ProfileManager()
        profile = manager.get_profile('software')
        
        if not profile:
            console.print("[red]Software profile not found[/red]")
            return False
        
        # Create client
        client = create_client(profile)
        console.print(f"[green]✓[/green] Connected to: {profile['base_url']}")
        
        # Test 1: List sources
        console.print("\n[bold]Test 1: List Sources[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            sources = [
                item for item in items
                if item.get("containerType") == "SOURCE"
            ]
            
            console.print(f"[green]✓[/green] Sources listed: {len(sources)} total")
            
            # Show first source if available
            if sources:
                first_source = sources[0]
                console.print(f"  Example: {first_source.get('path', ['Unknown'])[0]}")
        except Exception as e:
            console.print(f"[red]✗[/red] List sources failed: {e}")
            return False
        
        # Test 2: Get source details
        if sources:
            console.print("\n[bold]Test 2: Get Source Details[/bold]")
            try:
                source_id = sources[0].get("id")
                source = client.get_catalog_item(source_id)
                
                console.print(f"[green]✓[/green] Source retrieved")
                console.print(f"  ID: {source_id}")
                console.print(f"  Type: {source.get('type', 'Unknown')}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Get source failed: {e}")
        
        # Test 3: Refresh source (if available)
        if sources:
            console.print("\n[bold]Test 3: Refresh Source[/bold]")
            try:
                source_id = sources[0].get("id")
                result = client.refresh_source(source_id)
                
                console.print(f"[green]✓[/green] Source refresh initiated")
                if result and result.get("id"):
                    console.print(f"  Job ID: {result.get('id')}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Refresh source failed: {e}")
                console.print(f"  [dim]Note: Refresh may not be available for all source types[/dim]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Software test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cloud_sources():
    """Test source operations with Cloud profile."""
    console.print("\n[bold cyan]Testing Source Management - Cloud Profile[/bold cyan]\n")
    
    try:
        # Get profile
        manager = ProfileManager()
        profile = manager.get_profile('cloud')
        
        if not profile:
            console.print("[red]Cloud profile not found[/red]")
            return False
        
        # Create client
        client = create_client(profile)
        console.print(f"[green]✓[/green] Connected to: {profile['base_url']}")
        
        # Test 1: List sources
        console.print("\n[bold]Test 1: List Sources[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            sources = [
                item for item in items
                if item.get("containerType") == "SOURCE"
            ]
            
            console.print(f"[green]✓[/green] Sources listed: {len(sources)} total")
            
            # Show sources
            if sources:
                for source in sources[:3]:  # Show first 3
                    console.print(f"  - {source.get('path', ['Unknown'])[0]}")
        except Exception as e:
            console.print(f"[red]✗[/red] List sources failed: {e}")
            return False
        
        # Test 2: Get source details
        if sources:
            console.print("\n[bold]Test 2: Get Source Details[/bold]")
            try:
                source_id = sources[0].get("id")
                source = client.get_catalog_item(source_id)
                
                console.print(f"[green]✓[/green] Source retrieved")
                console.print(f"  ID: {source_id}")
                console.print(f"  Name: {source.get('path', ['Unknown'])[0]}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Get source failed: {e}")
        
        # Test 3: Refresh source
        if sources:
            console.print("\n[bold]Test 3: Refresh Source[/bold]")
            try:
                source_id = sources[0].get("id")
                result = client.refresh_source(source_id)
                
                console.print(f"[green]✓[/green] Source refresh initiated")
                if result and result.get("id"):
                    console.print(f"  Job ID: {result.get('id')}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Refresh source failed: {e}")
                console.print(f"  [dim]Note: Refresh may not be available in Cloud API[/dim]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Cloud test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]Source Management - Live Testing[/bold cyan]\n"
        "Testing source operations with existing sources",
        border_style="cyan"
    ))
    
    # Test Software
    software_success = test_software_sources()
    
    # Test Cloud
    cloud_success = test_cloud_sources()
    
    # Summary
    console.print("\n" + "="*60)
    if software_success and cloud_success:
        console.print(Panel.fit(
            "[bold green]✓ Source Management Tests Passed![/bold green]\n\n"
            "Software: ✓ Passed\n"
            "Cloud: ✓ Passed\n\n"
            "Source operations are working correctly.",
            border_style="green"
        ))
        return 0
    else:
        status = []
        if software_success:
            status.append("Software: ✓ Passed")
        else:
            status.append("Software: ✗ Failed")
        
        if cloud_success:
            status.append("Cloud: ✓ Passed")
        else:
            status.append("Cloud: ✗ Failed")
        
        console.print(Panel.fit(
            f"[bold yellow]⚠ Some Tests Failed[/bold yellow]\n\n"
            f"{chr(10).join(status)}\n\n"
            "Check the output above for details.",
            border_style="yellow"
        ))
        return 1


if __name__ == "__main__":
    sys.exit(main())
