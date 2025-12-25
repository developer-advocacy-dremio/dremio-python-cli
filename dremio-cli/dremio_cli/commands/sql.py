"""SQL execution commands."""

import click
from rich.console import Console
from pathlib import Path

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from dremio_cli.formatters.table import format_as_table
from dremio_cli.formatters.json import format_as_json
from dremio_cli.formatters.yaml import format_as_yaml

console = Console()


@click.group()
def sql() -> None:
    """SQL execution operations."""
    pass


@sql.command("execute")
@click.argument("query", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Execute SQL from file")
@click.option("--context", help="SQL context (comma-separated path)")
@click.pass_context
def execute_sql(ctx, query: str, file: str, context: str) -> None:
    """Execute SQL query.
    
    Examples:
        dremio sql execute "SELECT * FROM MyTable LIMIT 10"
        dremio sql execute --file query.sql
        dremio sql execute "SELECT * FROM table" --context "MySpace"
    """
    try:
        # Get query from file or argument
        if file:
            with open(file, "r") as f:
                query = f.read()
        
        if not query:
            console.print("[red]Error: No query provided. Use argument or --file option[/red]")
            raise click.Abort()
        
        # Get profile
        manager = ProfileManager()
        profile_name = ctx.obj.profile_name
        profile = manager.get_profile(profile_name)
        
        if not profile:
            console.print(f"[red]Profile '{profile_name}' not found[/red]")
            raise click.Abort()
        
        # Create client
        client = create_client(profile)
        
        # Parse context
        sql_context = None
        if context:
            sql_context = [c.strip() for c in context.split(",")]
        
        # Execute SQL
        if hasattr(client, 'execute_sql'):
            with console.status(f"[bold green]Executing query on {profile_name}..."):
                result = client.execute_sql(query, context=sql_context)
        else:
            console.print("[red]SQL execution not supported for this profile type[/red]")
            raise click.Abort()
        
        # Format output
        output_format = ctx.obj.output_format
        
        if output_format == "json":
            console.print(format_as_json(result))
        elif output_format == "yaml":
            console.print(format_as_yaml(result))
        else:
            # Display job info and results
            job_id = result.get("id")
            if job_id:
                console.print(f"\n[dim]Job ID: {job_id}[/dim]")
            
            # Check for rows in result
            rows = result.get("rows", [])
            if rows:
                format_as_table(rows, title="Query Results")
            else:
                console.print("[yellow]Query executed successfully (no rows returned)[/yellow]")
                console.print(f"\n[dim]Result:[/dim]")
                console.print(result)
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()
