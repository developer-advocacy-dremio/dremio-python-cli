"""Source management commands."""

import click
from rich.console import Console

from dremio_cli.config import ProfileManager
from dremio_cli.client.factory import create_client
from dremio_cli.formatters.table import format_as_table
from dremio_cli.formatters.json import format_as_json
from dremio_cli.formatters.yaml import format_as_yaml

console = Console()


@click.group()
def source() -> None:
    """Source management operations."""
    pass


@source.command("list")
@click.pass_context
def list_sources(ctx) -> None:
    """List all sources."""
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
        
        # Get catalog and filter for sources
        data = client.get_catalog()
        items = data.get("data", [])
        
        # Filter for sources
        sources = [
            item for item in items
            if item.get("containerType") == "SOURCE" or item.get("type") == "SOURCE"
        ]
        
        # Format output
        output_format = ctx.obj.output_format
        if output_format == "json":
            console.print(format_as_json(sources))
        elif output_format == "yaml":
            console.print(format_as_yaml(sources))
        else:
            if sources:
                format_as_table(sources, title=f"Sources ({profile_name})")
            else:
                console.print("[yellow]No sources found[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()


@source.command("get")
@click.argument("source_id")
@click.option("--include", help="Include additional fields")
@click.pass_context
def get_source(ctx, source_id: str, include: str) -> None:
    """Get source by ID."""
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
        
        # Get source
        data = client.get_catalog_item(source_id, include=include)
        
        # Format output
        output_format = ctx.obj.output_format
        if output_format == "json":
            console.print(format_as_json(data))
        elif output_format == "yaml":
            console.print(format_as_yaml(data))
        else:
            format_as_table(data, title=f"Source: {source_id}")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()


@source.command("get-by-path")
@click.argument("source_name")
@click.option("--include", help="Include additional fields")
@click.pass_context
def get_source_by_path(ctx, source_name: str, include: str) -> None:
    """Get source by name/path."""
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
        
        # Get source by path
        data = client.get_catalog_item_by_path(source_name, include=include)
        
        # Format output
        output_format = ctx.obj.output_format
        if output_format == "json":
            console.print(format_as_json(data))
        elif output_format == "yaml":
            console.print(format_as_yaml(data))
        else:
            format_as_table(data, title=f"Source: {source_name}")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if ctx.obj.verbose:
            import traceback
            traceback.print_exc()
        raise click.Abort()
