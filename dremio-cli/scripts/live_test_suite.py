#!/usr/bin/env python3
"""
Comprehensive Live Test Suite for Dremio CLI.
Tests all commands against live Dremio Software and Cloud environments.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from dremio_cli.env import load_dotenv, get_env_override
from dremio_cli.utils.exceptions import ApiError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class IssueLogger:
    def __init__(self, issues_file: str = "planning/issues.md"):
        self.issues_file = Path(sys.path[0]).parent / issues_file
        self.issues = []

    def log_issue(self, command: str, error: str, context: str):
        self.issues.append({
            "command": command,
            "error": error,
            "context": context
        })
        console.print(f"[red]FAILED: {command}[/red]")
        console.print(f"  Error: {error}")

    def save(self):
        if not self.issues:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.issues_file, "a") as f:
            f.write(f"\n## Test Run: {timestamp}\n")
            for issue in self.issues:
                f.write(f"\n### {issue['command']}\n")
                f.write(f"- **Error**: {issue['error']}\n")
                f.write(f"- **Context**: {issue['context']}\n")

class LiveTestSuite:
    def __init__(self):
        self.logger = IssueLogger()
        load_dotenv()
        self.manager = ProfileManager()
        
    def setup_profiles(self) -> List[Dict[str, Any]]:
        """Setup profiles from environment variables."""
        profiles = []
        
        # Check for Software Profile
        if os.environ.get("DREMIO_SOFTWARE_BASE_URL"):
            console.print("[cyan]Found Software Configuration[/cyan]")
            profiles.append({
                "name": "software",
                "type": "software",
                "test_folder": os.environ.get("DREMIO_SOFTWARE_TEST_FOLDER", "dremio-catalog.home")
            })
            
        # Check for Cloud Profile
        if os.environ.get("DREMIO_CLOUD_BASE_URL"):
            console.print("[cyan]Found Cloud Configuration[/cyan]")
            profiles.append({
                "name": "cloud",
                "type": "cloud",
                "test_folder": os.environ.get("DREMIO_CLOUD_TEST_FOLDER", "@user") # Cloud usually uses @user or project ID
            })
            
        if not profiles:
            console.print("[yellow]No profiles found in .env. Please configure DREMIO_SOFTWARE_* or DREMIO_CLOUD_* variables.[/yellow]")
            sys.exit(1)
            
        return profiles

    def test_catalog_ops(self, client: Any, profile_name: str):
        console.print(f"\n[bold]Testing Catalog Ops ({profile_name})[/bold]")
        try:
            # List Catalog
            catalog = client.get_catalog()
            console.print(f"[green]✓[/green] List Catalog: Found {len(catalog.get('data', []))} items")
            
            # Get specific item (first one)
            if catalog.get('data'):
                item = catalog['data'][0]
                item_id = item['id']
                details = client.get_catalog_item(item_id)
                console.print(f"[green]✓[/green] Get Catalog Item: {item.get('path', [])}")
        except Exception as e:
            self.logger.log_issue("catalog", str(e), f"Profile: {profile_name}")

    def test_sql_execution(self, client: Any, profile_name: str, context: Optional[str] = None):
        console.print(f"\n[bold]Testing SQL Execution ({profile_name})[/bold]")
        query = "SELECT 1 as test_col"
        try:
            # Simple Select
            result = client.execute_sql(query, context=[context] if context else None)
            
            # Helper to safely get ID
            if isinstance(result, dict):
                job_id = result.get("id")
                console.print(f"[green]✓[/green] Execute SQL: Job {job_id}")
                
                # Get Results
                if job_id:
                     # Wait for job completion with ENGINE_START handling
                     max_retries = 30
                     for _ in range(max_retries):
                         job_info = client.get_job(job_id)
                         state = job_info.get("jobState")
                         if state == "COMPLETED":
                             break
                         elif state in ["FAILED", "CANCELED"]:
                             self.logger.log_issue("sql execution", f"Job failed: {state}", f"Profile: {profile_name}")
                             return
                         time.sleep(2) # Poll every 2s
                     
                     job_results = client.get_job_results(job_id)
                     rows = job_results.get("rows", [])
                     if len(rows) > 0 and rows[0].get("test_col") == 1:
                         console.print(f"[green]✓[/green] SQL Results Verified")
                     elif len(rows) == 0:
                         self.logger.log_issue("sql results", "No results returned", f"Profile: {profile_name}, Query: {query}")
                     else:
                         self.logger.log_issue("sql results", "Unexpected results", f"Profile: {profile_name}, Query: {query}")
            else:
                self.logger.log_issue("sql execution", f"Return type mismatch: {type(result)} - {result}", f"Profile: {profile_name}")

        except Exception as e:
             self.logger.log_issue("sql command", str(e), f"Profile: {profile_name}, Query: {query}")

    def test_source_ops(self, client: Any, profile_name: str):
        console.print(f"\n[bold]Testing Source Ops ({profile_name})[/bold]")
        try:
            # We usually find sources in catalog list where containerType is SOURCE
            catalog = client.get_catalog()
            sources = [x for x in catalog.get('data', []) if x.get('containerType') == 'SOURCE']
            console.print(f"[green]✓[/green] Found {len(sources)} sources")
            
            if sources:
                source = sources[0]
                # Test refresh (carefully, maybe skip full metadata refresh on prod)
                # console.print(f"Skipping refresh detail for safety on {source['id']}")
                pass

        except Exception as e:
            self.logger.log_issue("source read", str(e), f"Profile: {profile_name}")

    def test_reflection_ops(self, client: Any, profile_name: str):
        console.print(f"\n[bold]Testing Reflection Ops ({profile_name})[/bold]")
        try:
            # List Reflections
            reflections = client.list_reflections(summary=True)
            # Handle different return formats (list or dict with data)
            items = reflections.get('data', []) if isinstance(reflections, dict) else reflections
            console.print(f"[green]✓[/green] List Reflections: Found {len(items)} items")
            
            if items:
                 r_id = items[0]['id']
                 # Get details
                 details = client.get_reflection(r_id)
                 console.print(f"[green]✓[/green] Get Reflection: {r_id}")

        except Exception as e:
            self.logger.log_issue("reflection read", str(e), f"Profile: {profile_name}")

    def test_script_ops(self, client: Any, profile_name: str):
        console.print(f"\n[bold]Testing Script Ops ({profile_name})[/bold]")
        
        # Check support
        if not hasattr(client, "list_scripts"):
             console.print("[yellow]Scripts not supported on this client[/yellow]")
             return
             
        try:
            # List Scripts
            scripts = client.list_scripts()
            items = scripts.get('data', [])
            console.print(f"[green]✓[/green] List Scripts: Found {len(items)} items")
            
            # Create a test script
            script_name = f"Test Script {int(time.time())}"
            content = "SELECT 1"
            
            try:
                created = client.create_script(name=script_name, content=content)
                console.print(f"[green]✓[/green] Created Script: {script_name}")
                s_id = created.get("id")
                
                # Get
                if s_id:
                     got = client.get_script(s_id)
                     console.print(f"[green]✓[/green] Get Script: {got.get('name')}")
                     
                     # Update
                     client.update_script(s_id, name=f"{script_name} Updated", content="SELECT 2")
                     console.print(f"[green]✓[/green] Updated Script")
                     
                     # Delete
                     client.delete_script(s_id)
                     console.print(f"[green]✓[/green] Deleted Script")

            except Exception as e:
                 self.logger.log_issue("script crud", str(e), f"Profile: {profile_name}")

        except Exception as e:
            self.logger.log_issue("script list", str(e), f"Profile: {profile_name}")

    def test_space_folder_workflow(self, client: Any, profile_name: str, root_path: str):
        console.print(f"\n[bold]Testing Space/Folder Workflow ({profile_name})[/bold]")
        test_folder_name = f"cli_test_{int(time.time())}"
        
        # We need to construct the full path correctly.
        # root_path might be "dremio-catalog.alexmerced.testing"
        # We want to create "dremio-catalog.alexmerced.testing.cli_test_123"
        
        try:
            full_path_list = root_path.split(".") + [test_folder_name]
            
            # Create Folder
            folder_data = {"path": full_path_list, "description": "integration test"}
            try:
                created = client.create_folder(folder_data)
                console.print(f"[green]✓[/green] Created Folder: {test_folder_name}")
                folder_id = created.get("id")
                folder_tag = created.get("tag") # Optimistic locking
                
                # Cleanup
                if folder_id:
                     client.delete_folder(folder_id, tag=folder_tag)
                     console.print(f"[green]✓[/green] Deleted Folder: {test_folder_name}")

            except Exception as e:
                self.logger.log_issue("folder create/delete", str(e), f"Profile: {profile_name}, Path: {full_path_list}")

        except Exception as e:
             self.logger.log_issue("folder workflow setup", str(e), f"Profile: {profile_name}")

    def test_advanced_features(self, client: Any, profile_name: str):
        console.print(f"\n[bold]Testing Advanced Features ({profile_name})[/bold]")
        
        # Lineage
        try:
            # Try to get lineage for a known item (e.g. from catalog list)
            # We need a dataset ID.
            catalog = client.get_catalog()
            datasets = [x for x in catalog.get('data', []) if x.get('containerType') == 'DATASET']
            if not datasets:
                 # Try deeper if none at root
                 pass 
            
            if datasets:
                d_id = datasets[0]['id']
                if hasattr(client, "get_catalog_graph"):
                    graph = client.get_catalog_graph(d_id)
                    console.print(f"[green]✓[/green] Lineage Graph fetched for {d_id}")
                else:
                    console.print("[yellow]Lineage not supported on client[/yellow]")
        except Exception as e:
            self.logger.log_issue("lineage", str(e), f"Profile: {profile_name}")

        # Job Analyzer
        # We need a job ID. We can use one from recent SQL test if we stored it, 
        # but for now let's just trigger a quick new one.
        try:
            res = client.execute_sql("SELECT 1")
            job_id = res.get("id")
            if job_id and hasattr(client, "get_job"):
                # Analyze logic is client-side in CLI command, but here we verify we can fetch the data needed for it.
                # Actually, the analyze command uses client.get_job, so just verifying that works well enough.
                job = client.get_job(job_id)
                if job.get("jobState"):
                     console.print(f"[green]✓[/green] Job Analyzer Data available (Job {job_id})")
        except Exception as e:
            self.logger.log_issue("job analyzer", str(e), f"Profile: {profile_name}")

    def run(self):
        profiles = self.setup_profiles()
        
        for profile_config in profiles:
            p_name = profile_config['name']
            console.rule(f"Running Tests for Profile: {p_name}")
            
            # Manually load profile using logic similar to ProfileManager but direct from env for test isolation
            # Re-using the env loading logic by relying on standard Dremio env vars which factories use.
            # Assuming env variables are set, we just tell ProfileManager to use 'software' or 'cloud' name matching what we set in .env
            
            # Because we didn't inject into profiles.yaml, we rely on env vars being present 
            # and matching the naming convention expected by `dremio_cli.env`.
            # We already validated they exist in `setup_profiles`.
            
            # We need to forcefully get the profile from env
            from dremio_cli.env import get_profile_from_env
            p_data = get_profile_from_env(p_name) 
            
            if not p_data:
                 console.print(f"[red]Could not load profile data for {p_name}[/red]")
                 continue
                 
            try:
                # Factory create
                if profile_config['type'] == 'cloud':
                     from dremio_cli.client.cloud import CloudClient
                     # Extract fields
                     client = CloudClient(
                         base_url=p_data['base_url'],
                         project_id=p_data.get('project_id', ''),
                         token=p_data.get('auth', {}).get('token', '')
                     )
                else:
                     from dremio_cli.client.software import SoftwareClient
                     client = SoftwareClient(
                         base_url=p_data['base_url'],
                         token=p_data.get('auth', {}).get('token', '')
                     )

                # Execute Tests
                self.test_catalog_ops(client, p_name)
                self.test_sql_execution(client, p_name)
                self.test_sql_execution(client, p_name)
                self.test_source_ops(client, p_name)
                self.test_reflection_ops(client, p_name)
                self.test_script_ops(client, p_name)
                
                test_root = profile_config.get('test_folder')
                if test_root:
                    self.test_space_folder_workflow(client, p_name, test_root)
                else:
                    console.print("[yellow]Skipping folder tests (no test folder defined)[/yellow]")
                
                self.test_advanced_features(client, p_name)

            except Exception as e:
                self.logger.log_issue("client init", str(e), f"Profile: {p_name}")
                import traceback
                traceback.print_exc()

        # Save issues
        self.logger.save()
        console.rule("[bold]Test Suite Complete[/bold]")

if __name__ == "__main__":
    suite = LiveTestSuite()
    suite.run()
