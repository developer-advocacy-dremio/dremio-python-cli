
import os
import json
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class ResourceState:
    id: str
    path: List[str]
    type: str # DATASET, FOLDER, SPACE, SOURCE, VIEW (Specific)
    hash: str # Content hash for change detection
    metadata: Dict[str, Any]

class LocalState:
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.state_file = os.path.join(root_path, ".dremio_state.json")
        self.resources: Dict[str, ResourceState] = {} # Keyed by path string "space.folder.view"

    def load(self):
        """Load state from .dremio_state.json"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    for key, item in data.items():
                        self.resources[key] = ResourceState(**item)
            except Exception as e:
                print(f"Warning: Could not load state file: {e}")

    def save(self):
        """Save state to .dremio_state.json"""
        data = {k: asdict(v) for k, v in self.resources.items()}
        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)

    def update_resource(self, path_list: List[str], type: str, id: str, hash: str, metadata: Dict[str, Any]):
        key = ".".join(path_list)
        self.resources[key] = ResourceState(
            id=id,
            path=path_list,
            type=type,
            hash=hash,
            metadata=metadata
        )
    
    def get_resource(self, path_list: List[str]) -> Optional[ResourceState]:
        key = ".".join(path_list)
        return self.resources.get(key)

    def remove_resource(self, path_list: List[str]):
        key = ".".join(path_list)
        if key in self.resources:
            del self.resources[key]

    def scan_filesystem(self) -> Dict[str, Dict[str, Any]]:
        """
        Scans the root_dir for .yaml and .sql files to build a picture of local state.
        Returns a dict of resource definitions found on disk.
        """
        local_resources = {}
        for root, dirs, files in os.walk(self.root_path):
            # skipping .git, .dremio_state.json, etc is handled by not parsing them
            for file in files:
                if file.endswith(".yaml") and file != "dremio.yaml":
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, 'r') as f:
                            data = yaml.safe_load(f)
                            # We expect 'type' and 'path' in the yaml
                            if data and "type" in data and "path" in data:
                                path_key = ".".join(data["path"])
                                local_resources[path_key] = data
                                # If there is a sql file, read it
                                if "sql_file" in data:
                                    sql_path = os.path.join(root, data["sql_file"])
                                    if os.path.exists(sql_path):
                                        with open(sql_path, 'r') as sql_f:
                                            data["sql_content"] = sql_f.read()
                    except Exception as e:
                        print(f"Error reading {full_path}: {e}")
        return local_resources
