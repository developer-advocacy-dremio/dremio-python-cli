# Favorite Queries

Manage and re-run your favorite SQL queries.

## Commands

### Add Favorite

Save a query as a favorite.

```bash
alt-dremio-cli favorite add <NAME> [OPTIONS]
```

**Options:**
- `--sql TEXT` - The SQL query to save (Required)
- `--description TEXT` - A brief description of the query

**Examples:**
```bash
alt-dremio-cli favorite add daily_sales --sql "SELECT * FROM sales WHERE date = CURRENT_DATE"
alt-dremio-cli favorite add top_users --sql "SELECT * FROM users ORDER BY score DESC LIMIT 10" --description "Top 10 users by score"
```

### List Favorites

List all saved favorite queries.

```bash
alt-dremio-cli favorite list [OPTIONS]
```

**Examples:**
```bash
alt-dremio-cli favorite list
alt-dremio-cli --output json favorite list
```

### Run Favorite

Execute a saved favorite query.

```bash
alt-dremio-cli favorite run <NAME>
```

**Examples:**
```bash
alt-dremio-cli favorite run daily_sales
```

### Delete Favorite

Remove a query from favorites.

```bash
alt-dremio-cli favorite delete <NAME>
```

**Examples:**
```bash
alt-dremio-cli favorite delete daily_sales
```
