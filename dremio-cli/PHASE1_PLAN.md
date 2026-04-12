# Phase 1 Development Plan

## ✅ Completed: Environment Variable Support

### What's Done
- [x] Created `env.py` module with `DREMIO_{PROFILE}_{KEY}` pattern support
- [x] Created `client/factory.py` for automatic client instantiation
- [x] Updated `ProfileManager` to merge env vars with YAML profiles
- [x] Environment variables take precedence over YAML
- [x] Support for `.env` file loading
- [x] Created test script `scripts/test_env_loading.py`

### Your Profiles Now Available
Based on your `.env` file, you now have:

**cloud** profile:
- Type: cloud
- Token: ✓
- Project ID: 788baab4-3c3b-42da-9f1d-5cc6dc03147d
- Testing Folder: testing

**software** profile:
- Type: software  
- Base URL: https://v26.dremio.org
- Token: ✓
- Testing Folder: "dremio-catalog".alexmerced.testing

## 🎯 Next Steps: Phase 1 Implementation

### Step 1: Test Environment Loading (Do This First!)
```bash
cd dremio-cli
python scripts/test_env_loading.py
```

This will verify your profiles load correctly from `.env`.

### Step 2: Implement Catalog Commands (Priority 1)
**File**: `dremio_cli/commands/catalog.py`

Commands to implement:
- `alt-dremio-cli catalog list [--profile cloud|software]`
- `alt-dremio-cli catalog get <id>`
- `alt-dremio-cli catalog get-by-path <path>`

**Why First**: Most fundamental operation, needed for everything else.

### Step 3: Implement SQL Execution (Priority 2)
**File**: `dremio_cli/commands/sql.py`

Commands to implement:
- `alt-dremio-cli sql execute "SELECT ..."`
- `alt-dremio-cli sql execute --file query.sql`
- Support for `--output json|yaml|table`

**Why Second**: Critical for testing and validation.

### Step 4: Implement Source Commands (Priority 3)
**File**: `dremio_cli/commands/source.py`

Commands to implement:
- `alt-dremio-cli source list`
- `alt-dremio-cli source get <id>`
- `alt-dremio-cli source get-by-path <name>`

**Why Third**: Needed to explore your data sources.

### Step 5: Implement Table Commands (Priority 4)
**File**: `dremio_cli/commands/table.py`

Commands to implement:
- `alt-dremio-cli table get <id>`
- `alt-dremio-cli table get-by-path <path>`
- `alt-dremio-cli table create --from-file config.json`

**Why Fourth**: For working with tables in your testing folders.

### Step 6: Integration Testing (Priority 5)
**File**: `tests/test_integration.py`

Test scenarios:
- List catalog on both cloud and software
- Execute SQL on both profiles
- Create/read/delete tables in testing folders
- Verify output formatting

## 📝 Implementation Template

Here's a template for implementing commands:

```python
# dremio_cli/commands/catalog.py
import click
from rich.console import Console

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from dremio_cli.formatters.table import format_as_table
from dremio_cli.formatters.json import format_as_json
from dremio_cli.formatters.yaml import format_as_yaml

console = Console()

@click.group()
def catalog() -> None:
    """Catalog operations."""
    pass

@catalog.command("list")
@click.pass_context
def list_catalog(ctx) -> None:
    """List catalog contents."""
    try:
        # Get profile
        manager = ProfileManager()
        profile_name = ctx.obj.profile_name
        profile = manager.get_profile(profile_name)
        
        if not profile:
            console.print(f"[red]Profile '{profile_name}' not found[/red]")
            return
        
        # Create client
        client = create_client(profile)
        
        # Make API call
        data = client.get_catalog()
        
        # Format output
        output_format = ctx.obj.output_format
        if output_format == "json":
            console.print(format_as_json(data))
        elif output_format == "yaml":
            console.print(format_as_yaml(data))
        else:
            format_as_table(data.get("data", []), title="Catalog")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
```

## 🧪 Testing Workflow

1. **Test with Cloud Profile**:
```bash
alt-dremio-cli --profile cloud catalog list
alt-dremio-cli --profile cloud sql execute "SELECT * FROM testing LIMIT 5"
```

2. **Test with Software Profile**:
```bash
alt-dremio-cli --profile software catalog list
alt-dremio-cli --profile software sql execute "SELECT * FROM \"dremio-catalog\".alexmerced.testing LIMIT 5"
```

3. **Test Different Output Formats**:
```bash
alt-dremio-cli --profile cloud catalog list --output json
alt-dremio-cli --profile cloud catalog list --output yaml
alt-dremio-cli --profile cloud catalog list --output table
```

## 📊 Success Criteria for Phase 1

- [ ] Environment variables load correctly from `.env`
- [ ] Can list catalog on both cloud and software
- [ ] Can execute SQL on both profiles
- [ ] Can view sources
- [ ] Can work with tables in testing folders
- [ ] All output formats work (table, JSON, YAML)
- [ ] Error handling works gracefully
- [ ] Integration tests pass

## ⏱️ Estimated Timeline

- **Day 1**: Test env loading, implement catalog commands
- **Day 2**: Implement SQL execution
- **Day 3**: Implement source commands
- **Day 4**: Implement table commands
- **Day 5**: Integration testing and bug fixes
- **Day 6-7**: Documentation and polish

## 🚀 Quick Start Command

To get started immediately:

```bash
cd dremio-cli
pip install -e .
python scripts/test_env_loading.py
```

Then start implementing catalog commands!
