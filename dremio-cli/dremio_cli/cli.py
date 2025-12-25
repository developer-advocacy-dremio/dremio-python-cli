"""Main CLI module with command groups and REPL support."""

import sys
from typing import Optional

import click
from rich.console import Console

from dremio_cli.config import ProfileManager
from dremio_cli.commands import (
    catalog,
    profile,
    source,
    space,
    folder,
    table,
    view,
    sql,
    job,
    user,
    role,
    tag,
    wiki,
    grant,
)

console = Console()


class DremioContext:
    """Context object for CLI commands."""

    def __init__(self, profile_name: Optional[str] = None, output_format: str = "table"):
        self.profile_manager = ProfileManager()
        self.profile_name = profile_name or self.profile_manager.get_default_profile()
        self.output_format = output_format
        self.verbose = False


@click.group()
@click.option(
    "--profile",
    "-p",
    help="Profile to use for this command",
    type=str,
)
@click.option(
    "--output",
    "-o",
    help="Output format",
    type=click.Choice(["table", "json", "yaml"], case_sensitive=False),
    default="table",
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Quiet mode")
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    profile: Optional[str],
    output: str,
    verbose: bool,
    quiet: bool,
) -> None:
    """Dremio CLI - Manage Dremio Cloud and Dremio Software from the command line."""
    ctx.obj = DremioContext(profile_name=profile, output_format=output)
    ctx.obj.verbose = verbose
    
    if quiet:
        console.quiet = True


# Register command groups
cli.add_command(profile.profile)
cli.add_command(catalog.catalog)
cli.add_command(source.source)
cli.add_command(space.space)
cli.add_command(folder.folder)
cli.add_command(table.table)
cli.add_command(view.view)
cli.add_command(sql.sql)
cli.add_command(job.job)
cli.add_command(user.user)
cli.add_command(role.role)
cli.add_command(tag.tag)
cli.add_command(wiki.wiki)
cli.add_command(grant.grant)


@cli.command()
@click.pass_context
def repl(ctx: click.Context) -> None:
    """Start interactive REPL mode."""
    console.print("[bold green]Dremio CLI - Interactive Mode[/bold green]")
    console.print("Type 'help' for available commands, 'exit' or 'quit' to exit.\n")
    
    profile_name = ctx.obj.profile_name
    console.print(f"[dim]Using profile: {profile_name}[/dim]\n")
    
    while True:
        try:
            command = console.input("[bold cyan]dremio>[/bold cyan] ")
            command = command.strip()
            
            if not command:
                continue
                
            if command.lower() in ("exit", "quit"):
                console.print("[yellow]Goodbye![/yellow]")
                break
                
            # Parse and execute command
            try:
                # Remove 'dremio' prefix if present
                if command.startswith("dremio "):
                    command = command[7:]
                
                # Execute the command
                cli.main(command.split(), standalone_mode=False, obj=ctx.obj)
            except SystemExit:
                # Click raises SystemExit, we want to continue in REPL
                pass
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Goodbye![/yellow]")
            break


def main() -> None:
    """Main entry point."""
    try:
        cli()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
