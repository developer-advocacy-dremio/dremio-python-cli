"""Table management commands."""

import click
from rich.console import Console

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from dremio_cli.formatters.table import format_as_table
from dremio_cli.formatters.json import format_as_json
from dremio_cli.formatters.yaml import format_as_yaml

console = Console()


@click.group()
def table() -> None:
    """Table management operations."""
    pass


@table.command("get")
@click.argument("table_id")
@click.option("--include", help="Include additional fields")
@click.pass_context
def get_table(ctx, table_id: str, include: str) -> None:
    """Get table by ID."""
    try:
        # Get profile
        manager = ProfileManager()
        profile_name = ctx.obj.profile_name
        profile = manager.get_profile(profile_name)
        
        if not profile:
            console.print(f"[red]Profile '{profile_name}' not found[/red]")
            raise click.Abort()
        
        # Create client
        client = create_client(profile)
        
        # Get table
        data = client.get_catalog_item(table_id, include=include)
        
        # Format output
        output_format = ctx.obj.output_format
        if output_format == "json":
            console.print(format_as_json(data))
        elif output_format == "yaml":
            console.print(format_as_yaml(data))
        else:
            format_as_table(data, title=f"Table: {table_id}")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()


@table.command("get-by-path")
@click.argument("path")
@click.option("--include", help="Include additional fields")
@click.pass_context
def get_table_by_path(ctx, path: str, include: str) -> None:
    """Get table by path."""
    try:
        # Get profile
        manager = ProfileManager()
        profile_name = ctx.obj.profile_name
        profile = manager.get_profile(profile_name)
        
        if not profile:
            console.print(f"[red]Profile '{profile_name}' not found[/red]")
            raise click.Abort()
        
        # Create client
        client = create_client(profile)
        
        # Get table by path
        data = client.get_catalog_item_by_path(path, include=include)
        
        # Format output
        output_format = ctx.obj.output_format
        if output_format == "json":
            console.print(format_as_json(data))
        elif output_format == "yaml":
            console.print(format_as_yaml(data))
        else:
            format_as_table(data, title=f"Table: {path}")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()
