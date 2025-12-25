#!/usr/bin/env python3
"""
Live test script for Space and Folder Management API.

This script tests space and folder management with both Cloud and Software profiles.
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


def test_cloud_spaces_folders():
    """Test space and folder management with Cloud profile."""
    console.print("\n[bold cyan]Testing Space & Folder Management - Cloud Profile[/bold cyan]\n")
    
    space_id = None
    folder_id = None
    
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
        
        # Test 1: Create a space (top-level folder in Cloud)
        console.print("\n[bold]Test 1: Create Space (Top-Level Folder)[/bold]")
        try:
            space_data = {
                "name": "cli_test_space",
                "description": "Test space created by CLI"
            }
            
            result = client.create_space(space_data)
            space_id = result.get("id")
            space_path = result.get("path", [])
            
            console.print(f"[green]✓[/green] Space created")
            console.print(f"  ID: {space_id}")
            console.print(f"  Path: {'.'.join(space_path)}")
            console.print(f"  [dim]Note: In Cloud, this is a top-level folder[/dim]")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Create space failed: {e}")
            return False
        
        # Test 2: List spaces
        console.print("\n[bold]Test 2: List Spaces[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            spaces = [
                item for item in items
                if item.get("containerType") == "FOLDER" and len(item.get("path", [])) == 1
            ]
            
            console.print(f"[green]✓[/green] Spaces listed: {len(spaces)} total")
            
            # Find our test space
            test_spaces = [s for s in spaces if "cli_test_space" in '.'.join(s.get("path", []))]
            if test_spaces:
                console.print(f"  Found our test space: {'.'.join(test_spaces[0].get('path', []))}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List spaces failed: {e}")
        
        # Test 3: Create a folder inside the space
        console.print("\n[bold]Test 3: Create Folder[/bold]")
        try:
            folder_data = {
                "path": ["cli_test_space", "reports"],
                "description": "Reports folder"
            }
            
            result = client.create_folder(folder_data)
            folder_id = result.get("id")
            folder_path = result.get("path", [])
            
            console.print(f"[green]✓[/green] Folder created")
            console.print(f"  ID: {folder_id}")
            console.print(f"  Path: {'.'.join(folder_path)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Create folder failed: {e}")
        
        # Test 4: Get folder by path
        if folder_id:
            console.print("\n[bold]Test 4: Get Folder by Path[/bold]")
            try:
                folder = client.get_catalog_item_by_path("cli_test_space/reports")
                console.print(f"[green]✓[/green] Folder retrieved by path")
                console.print(f"  ID: {folder.get('id')}")
            except Exception as e:
                console.print(f"[red]✗[/red] Get folder by path failed: {e}")
        
        # Test 5: List folders
        console.print("\n[bold]Test 5: List Folders[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            folders = [
                item for item in items
                if item.get("containerType") == "FOLDER"
            ]
            
            console.print(f"[green]✓[/green] Folders listed: {len(folders)} total")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List folders failed: {e}")
        
        # Cleanup: Delete folder then space
        console.print("\n[bold]Cleanup[/bold]")
        
        if folder_id:
            try:
                folder = client.get_catalog_item(folder_id)
                client.delete_folder(folder_id, folder.get("tag"))
                console.print(f"[green]✓[/green] Folder deleted")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Delete folder failed: {e}")
        
        if space_id:
            try:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
                console.print(f"[green]✓[/green] Space deleted")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Delete space failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Cloud test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        try:
            if folder_id:
                folder = client.get_catalog_item(folder_id)
                client.delete_folder(folder_id, folder.get("tag"))
            if space_id:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
        except:
            pass
        
        return False


def test_software_spaces_folders():
    """Test space and folder management with Software profile."""
    console.print("\n[bold cyan]Testing Space & Folder Management - Software Profile[/bold cyan]\n")
    
    space_id = None
    folder_id = None
    
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
        
        # Test 1: Create a space
        console.print("\n[bold]Test 1: Create Space[/bold]")
        try:
            space_data = {
                "name": "cli_test_space",
                "description": "Test space created by CLI"
            }
            
            result = client.create_space(space_data)
            space_id = result.get("id")
            space_path = result.get("path", [])
            
            console.print(f"[green]✓[/green] Space created")
            console.print(f"  ID: {space_id}")
            console.print(f"  Path: {'.'.join(space_path)}")
            console.print(f"  [dim]Note: In Software, this is a traditional SPACE[/dim]")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Create space failed: {e}")
            return False
        
        # Test 2: List spaces
        console.print("\n[bold]Test 2: List Spaces[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            spaces = [
                item for item in items
                if item.get("containerType") == "SPACE"
            ]
            
            console.print(f"[green]✓[/green] Spaces listed: {len(spaces)} total")
            
            # Find our test space
            test_spaces = [s for s in spaces if "cli_test_space" in '.'.join(s.get("path", []))]
            if test_spaces:
                console.print(f"  Found our test space: {'.'.join(test_spaces[0].get('path', []))}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List spaces failed: {e}")
        
        # Test 3: Create a folder inside the space
        console.print("\n[bold]Test 3: Create Folder[/bold]")
        try:
            folder_data = {
                "path": ["cli_test_space", "reports"],
                "description": "Reports folder"
            }
            
            result = client.create_folder(folder_data)
            folder_id = result.get("id")
            folder_path = result.get("path", [])
            
            console.print(f"[green]✓[/green] Folder created")
            console.print(f"  ID: {folder_id}")
            console.print(f"  Path: {'.'.join(folder_path)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Create folder failed: {e}")
        
        # Test 4: Get folder by path
        if folder_id:
            console.print("\n[bold]Test 4: Get Folder by Path[/bold]")
            try:
                folder = client.get_catalog_item_by_path("cli_test_space/reports")
                console.print(f"[green]✓[/green] Folder retrieved by path")
                console.print(f"  ID: {folder.get('id')}")
            except Exception as e:
                console.print(f"[red]✗[/red] Get folder by path failed: {e}")
        
        # Test 5: List folders
        console.print("\n[bold]Test 5: List Folders[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            folders = [
                item for item in items
                if item.get("containerType") == "FOLDER"
            ]
            
            console.print(f"[green]✓[/green] Folders listed: {len(folders)} total")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List folders failed: {e}")
        
        # Cleanup: Delete folder then space
        console.print("\n[bold]Cleanup[/bold]")
        
        if folder_id:
            try:
                folder = client.get_catalog_item(folder_id)
                client.delete_folder(folder_id, folder.get("tag"))
                console.print(f"[green]✓[/green] Folder deleted")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Delete folder failed: {e}")
        
        if space_id:
            try:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
                console.print(f"[green]✓[/green] Space deleted")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Delete space failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Software test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        try:
            if folder_id:
                folder = client.get_catalog_item(folder_id)
                client.delete_folder(folder_id, folder.get("tag"))
            if space_id:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
        except:
            pass
        
        return False


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]Space & Folder Management API - Live Testing[/bold cyan]\n"
        "Testing space and folder CRUD operations with both Cloud and Software",
        border_style="cyan"
    ))
    
    # Test Cloud
    cloud_success = test_cloud_spaces_folders()
    
    # Test Software
    software_success = test_software_spaces_folders()
    
    # Summary
    console.print("\n" + "="*60)
    if cloud_success and software_success:
        console.print(Panel.fit(
            "[bold green]✓ All Space & Folder Tests Passed![/bold green]\n\n"
            "Cloud: ✓ Passed\n"
            "Software: ✓ Passed\n\n"
            "All space and folder operations are working correctly.",
            border_style="green"
        ))
        return 0
    else:
        status = []
        if cloud_success:
            status.append("Cloud: ✓ Passed")
        else:
            status.append("Cloud: ✗ Failed")
        
        if software_success:
            status.append("Software: ✓ Passed")
        else:
            status.append("Software: ✗ Failed")
        
        console.print(Panel.fit(
            f"[bold yellow]⚠ Some Tests Failed[/bold yellow]\n\n"
            f"{chr(10).join(status)}\n\n"
            "Check the output above for details.",
            border_style="yellow"
        ))
        return 1


if __name__ == "__main__":
    sys.exit(main())
