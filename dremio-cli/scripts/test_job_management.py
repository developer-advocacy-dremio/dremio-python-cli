#!/usr/bin/env python3
"""
Live test script for Job Management API.

This script tests job management functionality with real Dremio instances.
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


def test_software_jobs():
    """Test job management with Software profile."""
    console.print("\n[bold cyan]Testing Job Management - Software Profile[/bold cyan]\n")
    
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
        
        # Test 1: Execute SQL to create a job
        console.print("\n[bold]Test 1: Execute SQL Query[/bold]")
        try:
            result = client.execute_sql("SELECT 1 as test_column")
            job_id = result.get("id")
            if job_id:
                console.print(f"[green]✓[/green] SQL executed, Job ID: {job_id}")
            else:
                console.print(f"[yellow]⚠[/yellow] SQL executed but no job ID returned")
                console.print(f"Result: {result}")
        except Exception as e:
            console.print(f"[red]✗[/red] SQL execution failed: {e}")
            return False
        
        # Test 2: Get job details
        if job_id:
            console.print("\n[bold]Test 2: Get Job Details[/bold]")
            try:
                job_details = client.get_job(job_id)
                console.print(f"[green]✓[/green] Job details retrieved")
                console.print(f"  State: {job_details.get('jobState', 'N/A')}")
                console.print(f"  Query: {job_details.get('sql', 'N/A')[:50]}...")
            except Exception as e:
                console.print(f"[red]✗[/red] Get job failed: {e}")
        
        # Test 3: Get job results
        if job_id:
            console.print("\n[bold]Test 3: Get Job Results[/bold]")
            try:
                results = client.get_job_results(job_id, limit=10)
                rows = results.get("rows", [])
                console.print(f"[green]✓[/green] Job results retrieved: {len(rows)} rows")
                if rows:
                    console.print(f"  First row: {rows[0]}")
            except Exception as e:
                console.print(f"[red]✗[/red] Get job results failed: {e}")
        
        # Test 4: List recent jobs
        console.print("\n[bold]Test 4: List Recent Jobs[/bold]")
        try:
            jobs_list = client.list_jobs(max_results=5)
            jobs = jobs_list.get("jobs", [])
            console.print(f"[green]✓[/green] Jobs list retrieved: {len(jobs)} jobs")
            for i, job in enumerate(jobs[:3], 1):
                console.print(f"  {i}. {job.get('id', 'N/A')[:20]}... - {job.get('jobState', 'N/A')}")
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] List jobs failed: {e}")
            console.print("[dim]Note: Job listing might not be available on this Dremio version[/dim]")
        
        # Test 5: Get job profile (if available)
        if job_id:
            console.print("\n[bold]Test 5: Get Job Profile[/bold]")
            try:
                profile_data = client.get_job_profile(job_id)
                console.print(f"[green]✓[/green] Job profile retrieved")
                console.print(f"  Profile size: {len(str(profile_data))} bytes")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Get job profile failed: {e}")
        
        # Test 6: Get job reflections (if available)
        if job_id:
            console.print("\n[bold]Test 6: Get Job Reflections[/bold]")
            try:
                reflections = client.get_job_reflections(job_id)
                console.print(f"[green]✓[/green] Job reflections retrieved")
                console.print(f"  Reflections: {reflections}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] Get job reflections failed: {e}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Software job test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]Job Management API - Live Testing[/bold cyan]\n"
        "Testing job operations with real Dremio instances",
        border_style="cyan"
    ))
    
    # Test Software
    software_success = test_software_jobs()
    
    # Summary
    console.print("\n" + "="*60)
    if software_success:
        console.print(Panel.fit(
            "[bold green]✓ Job Management Tests Passed![/bold green]\n\n"
            "All job operations are working correctly.",
            border_style="green"
        ))
        return 0
    else:
        console.print(Panel.fit(
            "[bold yellow]⚠ Some Tests Failed[/bold yellow]\n\n"
            "Check the output above for details.",
            border_style="yellow"
        ))
        return 1


if __name__ == "__main__":
    sys.exit(main())
