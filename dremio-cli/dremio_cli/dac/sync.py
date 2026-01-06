
import os
import yaml
import json
from typing import Optional, List, Dict, Any
from pathlib import Path
from dremio_cli.dac.config import DremioConfig
from dremio_cli.dac.state import LocalState
from dremio_cli.client.software import SoftwareClient
from dremio_cli.client.cloud import CloudClient
from dremio_cli.utils.console import console

class DremioSync:
    def __init__(self, config: DremioConfig, client, root_dir: str):
        self.config = config
        self.client = client
        self.root_dir = root_dir
        self.state = LocalState(root_dir)
        self.state.load()

    def pull(self):
        """
        Pull state from Dremio to local filesystem.
        """
        console.print(f"[bold blue]Syncing Pull...[/bold blue]")
        console.print(f"Scope: {self.config.scope.path} ({self.config.scope.type})")

        # 1. Resolve Root ID using scope path
        # Catalog API path lookup might behave differently on Cloud vs Software
        # Usually we can get by path.
        
        try:
            # We assume the user provided a valid top-level path or ID. 
            # If it's a path like "dremio-catalog.space", we can try to fetch it.
            # If it fails, we might need to search for it.
            
            # Special case for "dremio-catalog" or "sys" if root
            root_entity = self._fetch_entity_by_path(self.config.scope.path)
            if not root_entity:
                 console.print(f"[red]Could not find entity at path: {self.config.scope.path}[/red]")
                 return

            console.print(f"Found root entity: {root_entity.get('id')} ({root_entity.get('entityType', 'Unknown')})")
            
            # 2. Recursive Traversal
            self._traverse_and_sync(root_entity, parent_local_path=Path(self.root_dir))
            
            # 3. Save State
            self.state.save()
            console.print(f"[bold green]Pull Complete.[/bold green]")

        except Exception as e:
            console.print(f"[red]Sync failed: {e}[/red]")
            import traceback
            traceback.print_exc()

    def _fetch_entity_by_path(self, path: str):
        # Trying to fetch by path directly if client supports it or traverse from root
        try:
             return self.client.get_catalog_item(None, path=path.split("."))
        except:
             # Fallback: scan root catalog (expensive but reliable)
             # Note: standard get_catalog_item usually takes ID. 
             # SoftwareClient has distinct `get_catalog_item(id)` and `get_catalog_item_by_path(path)` logic implicitly?
             # Let's rely on `get_catalog_item` handling path lists or IDs if possible, 
             # but standard API is usually by ID.
             # We might need to resolve Path -> ID first.
             return self._resolve_path_to_entity(path)

    def _resolve_path_to_entity(self, path: str):
         # This logic needs to be robust.
         # 1. Try treating 'path' as ID (unlikely but possible)
         try:
             return self.client.get_catalog_item(path)
         except:
             pass
         
         # 2. Traverse from root to find it.
         parts = path.split(".") # dremio-catalog.space.folder
         # Root query
         current_container = self.client.get_catalog() # top level
         current_id = None
         
         # Assuming 'data' holds list of entities
         # top level usually has "dremio-catalog" (HOME) or spaces
         
         # For simplicity, if we are scoped to a SPACE, we expect it in root catalog
         target_name = parts[0] # dremio-catalog? or space name directly?
         # Software: "dremio-catalog" is Home? No, usually Sources/Spaces are top level.
         
         # Let's try to match parts
         found_entity = None
         
         # Helper to find in list
         def find_in_list(items, name):
             for x in items:
                 # path usually list ["space", "folder"]
                 # check last part of path or 'name' property
                 if x.get('path') and x['path'][-1] == name:
                     return x
                 if x.get('name') == name: # sometimes simple name
                     return x
             return None

         # Iterate path parts to drill down
         # Note: this is complex because 'dremio-catalog' might not be a real container in path list.
         # In older Dremio, '@user' is home.
         
         # Simplification: Assume user provides a ID or a path `Space.Folder`.
         # If `get_catalog_item` supports path lookup (which CLI client usually wraps), use it.
         # Our `client.get_catalog_item` calls specific API.
         # Let's try `by-path` endpoint if available (Software v3 has it).
         
         try:
             # Software v3 style
             res = self.client.get(f"catalog/by-path/{path.replace('.', '/')}")
             return res
         except:
             # Cloud might not have by-path easily.
             # Assume ID for now if path fails? 
             # Or ask user to provide ID in `dremio.yaml` for root?
             # Let's just assume we can list root and search.
             pass

         # Root scan
         items = self.client.get_catalog().get("data", [])
         
         # We need to walk `parts`
         # This is getting complicated for a single method. 
         # Let's assume for now that `path` in config allows either an ID or we find it at top level.
         
         # Try finding top level match
         for item in items:
             # Root item match?
             if item.get("path", [])[-1] == path:
                  return self.client.get_catalog_item(item['id'])
             if item.get("name") == path:
                  return self.client.get_catalog_item(item['id'])

         raise Exception(f"Could not resolve path '{path}' to an ID. Please use an ID in dremio.yaml or ensure path is correct.")

    def _traverse_and_sync(self, entity, parent_local_path: Path):
        """
        Recursive traverse.
        entity: The Dremio catalog object (Space, Folder, Dataset)
        parent_local_path: Local filesystem path where this entity belongs
        """
        entity_type = entity.get("entityType") # SPACE, FOLDER, DATASET
        entity_path = entity.get("path", [])
        entity_id = entity.get("id")
        entity_name = entity_path[-1] if entity_path else "unknown"
        
        # Determine local path
        # If we are at the ROOT of our scope, we don't create a folder for it, 
        # we treat `parent_local_path` AS the root.
        # UNLESS the user wants the root folder name.
        # Design doc says: `folder/` maps to `dremio-catalog.finance.folder`.
        # So sub-entities get folders.
        
        # Check if this entity IS the scope root
        is_root = ".".join(entity_path) == self.config.scope.path
        
        current_local_path = parent_local_path
        if not is_root and entity_type in ["SPACE", "FOLDER", "SOURCE"]:
             current_local_path = parent_local_path / entity_name
             if not current_local_path.exists():
                 current_local_path.mkdir(exist_ok=True)
                 
        if entity_type == "DATASET" and entity.get("type") == "VIRTUAL":
            # It's a view
            self._sync_view(entity, parent_local_path) # Views don't create folders, they sit in parent
            
        elif entity_type in ["SPACE", "FOLDER", "SOURCE"]:
            # Recurse
            # List children
            # Cloud/Software differences in Listing Children?
            # Creating a client wrapper or assuming get_catalog(id) returns children (it usually does for folders/spaces)
            
            # Re-fetch entity to get children if 'children' not in keys (sometimes listing gives thin objects)
            full_entity = self.client.get_catalog_item(entity_id) if "children" not in entity else entity
            children = full_entity.get("children", [])
            
            for child in children:
                self._traverse_and_sync(child, current_local_path)

    def _sync_view(self, view_entity, local_path: Path):
        # Fetch full details including SQL
        view_id = view_entity.get("id")
        full_view = self.client.get_catalog_item(view_id)
        
        name = full_view.get("path")[-1]
        sql = full_view.get("sql")
        context = full_view.get("sqlContext", [])
        
        # 1. Write SQL file
        sql_file = local_path / f"{name}.sql"
        with open(sql_file, "w") as f:
            f.write(sql)
            
        # 2. Write YAML metadata
        yaml_file = local_path / f"{name}.yaml"
        metadata = {
            "type": "VIEW",
            "path": full_view.get("path"),
            "context": context,
            "sql_file": f"{name}.sql"
            # TODO: add Reflections here if we fetch them
        }
        with open(yaml_file, "w") as f:
            yaml.dump(metadata, f)
            
        # 3. Update State
        # Calculate hash of SQL + Metadata for change detection
        content_hash = str(hash(sql + str(context))) # Simple hash for now
        self.state.update_resource(
            path_list=full_view.get("path"),
            type="VIEW",
            id=view_id,
            hash=content_hash,
            metadata=metadata
        )
        console.print(f"Synced View: {name}")

    def push(self, dry_run: bool = False):
        """
        Push local state to Dremio.
        """
        console.print(f"[bold blue]Syncing Push (Dry Run: {dry_run})...[/bold blue]")
        
        # 1. Scan Local Files
        local_resources = self.state.scan_filesystem()
        
        # 2. Compare with State/Remote
        # For simplicity in this iteration:
        # - Iterate local resources.
        # - If key not in self.state.resources -> CREATE
        # - If key in self.state.resources -> UPDATE (check hash later)
        # - If key in self.state but not in local -> DELETE (skip for now to be safe)
        
        changes = 0
        
        for key, data in local_resources.items():
            # Check if exists in state
            existing = self.state.get_resource(data["path"])
            
            if not existing:
                self._apply_create(data, dry_run)
                changes += 1
            else:
                # TODO: Check content hash for updates
                # For now assume no update if exists, or force update?
                # Let's compare SQL content
                old_hash = existing.hash
                new_content = data.get("sql_content", "") + str(data.get("context", []))
                new_hash = str(hash(new_content))
                
                if old_hash != new_hash:
                     self._apply_update(data, existing.id, dry_run)
                     changes += 1
        
        if changes == 0:
            console.print("No changes detected.")
        else:
            if not dry_run:
                self.state.save()
            console.print(f"[bold green]Push Complete. {changes} changes applied.[/bold green]")

    def _apply_create(self, data, dry_run):
        r_type = data.get("type")
        path = data.get("path")
        console.print(f"[green]+ CREATE[/green] {'.'.join(path)} ({r_type})")
        
        if dry_run: return

        if r_type == "VIEW":
            # Create View
            try:
                # API expects: {"path": [...], "sql": "...", "sqlContext": [...]}
                payload = {
                    "path": path,
                    "entityType": "dataset",
                    "type": "VIRTUAL_DATASET",
                    "sql": data.get("sql_content"),
                    "sqlContext": data.get("context", [])
                }
                # Use client.create_view (need to check if it exists or use catalog create)
                # SoftwareClient/CloudClient usually have `create_catalog_item` or `create_view`
                # Let's try `create_catalog_item` with type=VIRTUAL_DATASET
                
                # We need to ensure parent folder exists? 
                # Dremio creates folders implicitly? No.
                # Recursive folder creation needed? Yes.
                # Assuming folders exist for now or we create them.
                
                # Check for `create_view` helper
                if hasattr(self.client, "create_view"):
                     res = self.client.create_view(payload)
                else:
                     # Generic create
                     payload["entityType"] = "dataset"
                     payload["type"] = "VIRTUAL"
                     res = self.client.create_catalog(payload)
                
                # Update State
                new_id = res.get("id")
                new_hash = str(hash(data.get("sql_content", "") + str(data.get("context", []))))
                self.state.update_resource(path, "VIEW", new_id, new_hash, data)
                
            except Exception as e:
                console.print(f"[red]Failed to create {path}: {e}[/red]")

    def _apply_update(self, data, id, dry_run):
        path = data.get("path")
        console.print(f"[yellow]* UPDATE[/yellow] {'.'.join(path)}")
        
        if dry_run: return

        if data.get("type") == "VIEW":
            try:
                # Update View
                # Need tag/version usually. State might not have it if out of sync.
                # Fetch fresh first
                current = self.client.get_catalog_item(id)
                tag = current.get("tag")
                
                payload = {
                    "id": id,
                    "path": path,
                    "entityType": "dataset", # Software vs Cloud naming?
                    "type": "VIRTUAL",
                    "sql": data.get("sql_content"),
                    "sqlContext": data.get("context", []),
                    "tag": tag
                }
                
                self.client.update_catalog(id, payload, tag=tag)
                
                # Update State
                new_hash = str(hash(data.get("sql_content", "") + str(data.get("context", []))))
                self.state.update_resource(path, "VIEW", id, new_hash, data)

            except Exception as e:
                console.print(f"[red]Failed to update {path}: {e}[/red]")

