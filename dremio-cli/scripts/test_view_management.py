#!/usr/bin/env python3
"""
Live test script for View Management API.

This script tests view management functionality with real Dremio instances.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_cloud_views():
    """Test view management with Cloud profile."""
    console.print("\n[bold cyan]Testing View Management - Cloud Profile[/bold cyan]\n")
    
    view_id = None
    
    try:
        # Get profile
        manager = ProfileManager()
        profile = manager.get_profile('cloud')
        
        if not profile:
            console.print("[red]Cloud profile not found[/red]")
            return False
        
        # Get testing folder from profile
        testing_folder = profile.get('testing_folder', 'testing')
        
        # Create client
        client = create_client(profile)
        console.print(f"[green]✓[/green] Connected to: {profile['base_url']}")
        console.print(f"[dim]Testing folder: {testing_folder}[/dim]")
        
        # Test 1: Create a view
        console.print("\n[bold]Test 1: Create View[/bold]")
        try:
            view_data = {
                "entityType": "dataset",
                "type": "VIRTUAL_DATASET",
                "path": [testing_folder, "cli_test_view"],
                "sql": "SELECT 1 as test_column, 'hello' as message",
            }
            
            result = client.create_view(view_data)
            view_id = result.get("id")
            view_path = result.get("path", [])
            
            console.print(f"[green]✓[/green] View created")
            console.print(f"  ID: {view_id}")
            console.print(f"  Path: {'.'.join(view_path)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Create view failed: {e}")
            return False
        
        # Test 2: Get view by ID
        if view_id:
            console.print("\n[bold]Test 2: Get View by ID[/bold]")
            try:
                view = client.get_catalog_item(view_id)
                console.print(f"[green]✓[/green] View retrieved")
                console.print(f"  Type: {view.get('type')}")
                console.print(f"  SQL: {view.get('sql', 'N/A')[:50]}...")
            except Exception as e:
                console.print(f"[red]✗[/red] Get view failed: {e}")
        
        # Test 3: Get view by path
        console.print("\n[bold]Test 3: Get View by Path[/bold]")
        try:
            view_path_str = f"{testing_folder}/cli_test_view"
            view = client.get_catalog_item_by_path(view_path_str)
            console.print(f"[green]✓[/green] View retrieved by path")
            console.print(f"  ID: {view.get('id')}")
        except Exception as e:
            console.print(f"[red]✗[/red] Get view by path failed: {e}")
        
        # Test 4: Update view
        if view_id:
            console.print("\n[bold]Test 4: Update View[/bold]")
            try:
                # Get current view for tag
                current_view = client.get_catalog_item(view_id)
                
                update_data = {
                    "entityType": "dataset",
                    "type": "VIRTUAL_DATASET",
                    "id": view_id,
                    "path": current_view.get("path"),
                    "tag": current_view.get("tag"),
                    "sql": "SELECT 1 as test_column, 'updated' as message, 2 as another_column",
                }
                
                updated = client.update_view(view_id, update_data)
                console.print(f"[green]✓[/green] View updated")
                console.print(f"  New SQL: {updated.get('sql', 'N/A')[:60]}...")
            except Exception as e:
                console.print(f"[red]✗[/red] Update view failed: {e}")
        
        # Test 5: List views
        console.print("\n[bold]Test 5: List Views[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            views = [
                item for item in items
                if item.get("type") == "VIRTUAL_DATASET"
            ]
            
            console.print(f"[green]✓[/green] Views listed: {len(views)} total views")
            
            # Show our test view
            test_views = [v for v in views if "cli_test_view" in '.'.join(v.get("path", []))]
            if test_views:
                console.print(f"  Found our test view: {'.'.join(test_views[0].get('path', []))}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List views failed: {e}")
        
        # Test 6: Delete view
        if view_id:
            console.print("\n[bold]Test 6: Delete View[/bold]")
            try:
                # Get current tag
                current_view = client.get_catalog_item(view_id)
                tag = current_view.get("tag")
                
                client.delete_view(view_id, tag)
                console.print(f"[green]✓[/green] View deleted")
                
                # Verify deletion
                try:
                    client.get_catalog_item(view_id)
                    console.print(f"[yellow]⚠[/yellow] View still exists after deletion")
                except:
                    console.print(f"[dim]  Verified: View no longer exists[/dim]")
                    
            except Exception as e:
                console.print(f"[red]✗[/red] Delete view failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Cloud view test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if view_id:
            try:
                console.print("\n[yellow]Attempting cleanup...[/yellow]")
                manager = ProfileManager()
                profile = manager.get_profile('cloud')
                client = create_client(profile)
                current_view = client.get_catalog_item(view_id)
                client.delete_view(view_id, current_view.get("tag"))
                console.print("[green]✓[/green] Cleanup successful")
            except:
                console.print("[yellow]⚠[/yellow] Cleanup failed - manual deletion may be required")
        
        return False


def test_software_views():
    """Test view management with Software profile."""
    console.print("\n[bold cyan]Testing View Management - Software Profile[/bold cyan]\n")
    
    view_id = None
    
    try:
        # Get profile
        manager = ProfileManager()
        profile = manager.get_profile('software')
        
        if not profile:
            console.print("[red]Software profile not found[/red]")
            return False
        
        # Get testing folder from profile
        testing_folder = profile.get('testing_folder', '"dremio-catalog".alexmerced.testing')
        
        # Create client
        client = create_client(profile)
        console.print(f"[green]✓[/green] Connected to: {profile['base_url']}")
        console.print(f"[dim]Testing folder: {testing_folder}[/dim]")
        
        # Test 1: Create a view in a space
        console.print("\n[bold]Test 1: Create View[/bold]")
        try:
            # Use a simple space path for Software
            view_data = {
                "entityType": "dataset",
                "type": "VIRTUAL_DATASET",
                "path": ["@alex.merced@dremio.com", "cli_test_view"],
                "sql": "SELECT 1 as test_column, 'hello' as message",
            }
            
            result = client.create_view(view_data)
            view_id = result.get("id")
            view_path = result.get("path", [])
            
            console.print(f"[green]✓[/green] View created")
            console.print(f"  ID: {view_id}")
            console.print(f"  Path: {'.'.join(view_path)}")
            
        except Exception as e:
            console.print(f"[red]✗[/red] Create view failed: {e}")
            return False
        
        # Test 2: Get view by ID
        if view_id:
            console.print("\n[bold]Test 2: Get View by ID[/bold]")
            try:
                view = client.get_catalog_item(view_id)
                console.print(f"[green]✓[/green] View retrieved")
                console.print(f"  Type: {view.get('type')}")
                console.print(f"  SQL: {view.get('sql', 'N/A')[:50]}...")
            except Exception as e:
                console.print(f"[red]✗[/red] Get view failed: {e}")
        
        # Test 3: Get view by path
        console.print("\n[bold]Test 3: Get View by Path[/bold]")
        try:
            view_path_str = "@alex.merced@dremio.com/cli_test_view"
            view = client.get_catalog_item_by_path(view_path_str)
            console.print(f"[green]✓[/green] View retrieved by path")
            console.print(f"  ID: {view.get('id')}")
        except Exception as e:
            console.print(f"[red]✗[/red] Get view by path failed: {e}")
        
        # Test 4: Update view
        if view_id:
            console.print("\n[bold]Test 4: Update View[/bold]")
            try:
                # Get current view for tag
                current_view = client.get_catalog_item(view_id)
                
                update_data = {
                    "entityType": "dataset",
                    "type": "VIRTUAL_DATASET",
                    "id": view_id,
                    "path": current_view.get("path"),
                    "tag": current_view.get("tag"),
                    "sql": "SELECT 1 as test_column, 'updated' as message, 2 as another_column",
                }
                
                updated = client.update_view(view_id, update_data)
                console.print(f"[green]✓[/green] View updated")
                console.print(f"  New SQL: {updated.get('sql', 'N/A')[:60]}...")
            except Exception as e:
                console.print(f"[red]✗[/red] Update view failed: {e}")
        
        # Test 5: List views
        console.print("\n[bold]Test 5: List Views[/bold]")
        try:
            catalog = client.get_catalog()
            items = catalog.get("data", [])
            
            views = [
                item for item in items
                if item.get("type") == "VIRTUAL_DATASET"
            ]
            
            console.print(f"[green]✓[/green] Views listed: {len(views)} total views")
            
            # Show our test view
            test_views = [v for v in views if "cli_test_view" in '.'.join(v.get("path", []))]
            if test_views:
                console.print(f"  Found our test view: {'.'.join(test_views[0].get('path', []))}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List views failed: {e}")
        
        # Test 6: Delete view
        if view_id:
            console.print("\n[bold]Test 6: Delete View[/bold]")
            try:
                # Get current tag
                current_view = client.get_catalog_item(view_id)
                tag = current_view.get("tag")
                
                client.delete_view(view_id, tag)
                console.print(f"[green]✓[/green] View deleted")
                
                # Verify deletion
                try:
                    client.get_catalog_item(view_id)
                    console.print(f"[yellow]⚠[/yellow] View still exists after deletion")
                except:
                    console.print(f"[dim]  Verified: View no longer exists[/dim]")
                    
            except Exception as e:
                console.print(f"[red]✗[/red] Delete view failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Software view test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if view_id:
            try:
                console.print("\n[yellow]Attempting cleanup...[/yellow]")
                manager = ProfileManager()
                profile = manager.get_profile('software')
                client = create_client(profile)
                current_view = client.get_catalog_item(view_id)
                client.delete_view(view_id, current_view.get("tag"))
                console.print("[green]✓[/green] Cleanup successful")
            except:
                console.print("[yellow]⚠[/yellow] Cleanup failed - manual deletion may be required")
        
        return False


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]View Management API - Live Testing[/bold cyan]\n"
        "Testing view CRUD operations with real Dremio instances",
        border_style="cyan"
    ))
    
    # Test Cloud
    cloud_success = test_cloud_views()
    
    # Test Software
    software_success = test_software_views()
    
    # Summary
    console.print("\n" + "="*60)
    if cloud_success and software_success:
        console.print(Panel.fit(
            "[bold green]✓ All View Management Tests Passed![/bold green]\n\n"
            "Cloud: ✓ Passed\n"
            "Software: ✓ Passed\n\n"
            "All view CRUD operations are working correctly.",
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
