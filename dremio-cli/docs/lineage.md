# Lineage Visualization

Visualize the dependencies between datasets.

## Commands

### Show Lineage

Show the upstream parents of a dataset.

```bash
alt-dremio-cli lineage show <CATALOG_ID> [OPTIONS]
```

**Options:**
- `--format [tree|json|mermaid]` - Output format (Default: tree)

**Examples:**
```bash
# Tree view (Terminal)
alt-dremio-cli lineage show dremio-catalog.space.view

# Mermaid Graph (for markdown)
alt-dremio-cli lineage show dremio-catalog.space.view --format mermaid
```
