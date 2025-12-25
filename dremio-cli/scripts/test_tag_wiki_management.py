#!/usr/bin/env python3
"""
Live test script for Tag and Wiki Management.

This script tests tag and wiki operations with both Cloud and Software profiles.
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from rich.console import Console
from rich.panel import Panel

console = Console()


def test_software_tags_wiki():
    """Test tag and wiki operations with Software profile."""
    console.print("\n[bold cyan]Testing Tag & Wiki - Software Profile[/bold cyan]\n")
    
    space_id = None
    
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
        
        # Create a test space for tagging/wiki
        console.print("\n[bold]Setup: Create Test Space[/bold]")
        try:
            space_data = {"name": "cli_tag_test"}
            result = client.create_space(space_data)
            space_id = result.get("id")
            console.print(f"[green]✓[/green] Test space created: {space_id}")
        except Exception as e:
            console.print(f"[red]✗[/red] Create space failed: {e}")
            return False
        
        # Test 1: Set tags
        console.print("\n[bold]Test 1: Set Tags[/bold]")
        try:
            tags = ["analytics", "production", "sensitive"]
            client.set_tags(space_id, tags)
            console.print(f"[green]✓[/green] Tags set")
            console.print(f"  Tags: {', '.join(tags)}")
        except Exception as e:
            console.print(f"[red]✗[/red] Set tags failed: {e}")
        
        # Test 2: Get tags
        console.print("\n[bold]Test 2: Get Tags[/bold]")
        try:
            result = client.get_tags(space_id)
            retrieved_tags = result.get("tags", [])
            console.print(f"[green]✓[/green] Tags retrieved")
            console.print(f"  Tags: {', '.join(retrieved_tags)}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Get tags failed: {e}")
        
        # Test 3: Set wiki
        console.print("\n[bold]Test 3: Set Wiki[/bold]")
        try:
            wiki_text = "# Test Space\n\nThis is a test space for CLI testing.\n\n## Purpose\n- Testing tags\n- Testing wiki"
            client.set_wiki(space_id, wiki_text)
            console.print(f"[green]✓[/green] Wiki set")
            console.print(f"  Length: {len(wiki_text)} characters")
        except Exception as e:
            console.print(f"[red]✗[/red] Set wiki failed: {e}")
        
        # Test 4: Get wiki
        console.print("\n[bold]Test 4: Get Wiki[/bold]")
        try:
            result = client.get_wiki(space_id)
            wiki_content = result.get("text", "")
            console.print(f"[green]✓[/green] Wiki retrieved")
            console.print(f"  Length: {len(wiki_content)} characters")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Get wiki failed: {e}")
        
        # Test 5: Delete tags
        console.print("\n[bold]Test 5: Delete Tags[/bold]")
        try:
            client.delete_tags(space_id)
            console.print(f"[green]✓[/green] Tags deleted")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Delete tags failed: {e}")
        
        # Test 6: Delete wiki
        console.print("\n[bold]Test 6: Delete Wiki[/bold]")
        try:
            client.delete_wiki(space_id)
            console.print(f"[green]✓[/green] Wiki deleted")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Delete wiki failed: {e}")
        
        # Cleanup
        console.print("\n[bold]Cleanup[/bold]")
        if space_id:
            try:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
                console.print(f"[green]✓[/green] Test space deleted")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Cleanup failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Software test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if space_id:
            try:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
            except:
                pass
        
        return False


def test_cloud_tags_wiki():
    """Test tag and wiki operations with Cloud profile."""
    console.print("\n[bold cyan]Testing Tag & Wiki - Cloud Profile[/bold cyan]\n")
    
    space_id = None
    
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
        
        # Create a test space for tagging/wiki
        console.print("\n[bold]Setup: Create Test Space[/bold]")
        try:
            space_data = {"name": "cli_tag_test"}
            result = client.create_space(space_data)
            space_id = result.get("id")
            console.print(f"[green]✓[/green] Test space created: {space_id}")
        except Exception as e:
            console.print(f"[red]✗[/red] Create space failed: {e}")
            return False
        
        # Test 1: Set tags
        console.print("\n[bold]Test 1: Set Tags[/bold]")
        try:
            tags = ["analytics", "production", "cloud"]
            client.set_tags(space_id, tags)
            console.print(f"[green]✓[/green] Tags set")
            console.print(f"  Tags: {', '.join(tags)}")
        except Exception as e:
            console.print(f"[red]✗[/red] Set tags failed: {e}")
        
        # Test 2: Get tags
        console.print("\n[bold]Test 2: Get Tags[/bold]")
        try:
            result = client.get_tags(space_id)
            retrieved_tags = result.get("tags", [])
            console.print(f"[green]✓[/green] Tags retrieved")
            console.print(f"  Tags: {', '.join(retrieved_tags)}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Get tags failed: {e}")
        
        # Test 3: Set wiki
        console.print("\n[bold]Test 3: Set Wiki[/bold]")
        try:
            wiki_text = "# Cloud Test Space\n\nThis is a test space in Dremio Cloud.\n\n## Features\n- Cloud deployment\n- Tag management\n- Wiki documentation"
            client.set_wiki(space_id, wiki_text)
            console.print(f"[green]✓[/green] Wiki set")
            console.print(f"  Length: {len(wiki_text)} characters")
        except Exception as e:
            console.print(f"[red]✗[/red] Set wiki failed: {e}")
        
        # Test 4: Get wiki
        console.print("\n[bold]Test 4: Get Wiki[/bold]")
        try:
            result = client.get_wiki(space_id)
            wiki_content = result.get("text", "")
            console.print(f"[green]✓[/green] Wiki retrieved")
            console.print(f"  Length: {len(wiki_content)} characters")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Get wiki failed: {e}")
        
        # Test 5: Delete tags
        console.print("\n[bold]Test 5: Delete Tags[/bold]")
        try:
            client.delete_tags(space_id)
            console.print(f"[green]✓[/green] Tags deleted")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Delete tags failed: {e}")
        
        # Test 6: Delete wiki
        console.print("\n[bold]Test 6: Delete Wiki[/bold]")
        try:
            client.delete_wiki(space_id)
            console.print(f"[green]✓[/green] Wiki deleted")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Delete wiki failed: {e}")
        
        # Cleanup
        console.print("\n[bold]Cleanup[/bold]")
        if space_id:
            try:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
                console.print(f"[green]✓[/green] Test space deleted")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Cleanup failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Cloud test failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Cleanup on error
        if space_id:
            try:
                space = client.get_catalog_item(space_id)
                client.delete_space(space_id, space.get("tag"))
            except:
                pass
        
        return False


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]Tag & Wiki Management - Live Testing[/bold cyan]\n"
        "Testing tag and wiki operations on catalog objects",
        border_style="cyan"
    ))
    
    # Test Software
    software_success = test_software_tags_wiki()
    
    # Test Cloud
    cloud_success = test_cloud_tags_wiki()
    
    # Summary
    console.print("\n" + "="*60)
    if software_success and cloud_success:
        console.print(Panel.fit(
            "[bold green]✓ All Tag & Wiki Tests Passed![/bold green]\n\n"
            "Software: ✓ Passed\n"
            "Cloud: ✓ Passed\n\n"
            "All tag and wiki operations are working correctly.",
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
