"""
Echo-Sync entry point.

Usage:
    python -m echo_sync.main                # Voice mode (requires microphone)
    python -m echo_sync.main --demo-keyboard # Keyboard demo mode

Responsibilities:
- Load settings
- Start the app
- Catch fatal errors
- Print accessible terminal status for debugging
"""

import argparse
import logging
import sys

from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Configure logging with rich output."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                show_path=False,
            )
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="echo-sync",
        description=(
            "Echo-Sync: An inclusive, screen-free NUI media player "
            "for blind and motor-impaired users."
        ),
    )
    parser.add_argument(
        "--demo-keyboard",
        action="store_true",
        help="Use keyboard input instead of microphone (demo mode)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose debug logging",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for Echo-Sync."""
    args = parse_args()
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # Load settings
        from echo_sync.config.settings import load_settings

        console.print("[dim]Loading configuration...[/dim]")
        settings = load_settings()

        # Validate critical settings
        if settings.openai_api_key == "your_api_key_here":
            console.print(
                "[yellow]⚠ No OpenAI API key configured.[/yellow]\n"
                "[dim]Set OPENAI_API_KEY in your .env file for AI features.[/dim]\n"
                "[dim]Keyboard demo mode will still work with rule-based commands.[/dim]"
            )

        # Show mode
        mode = "keyboard demo" if args.demo_keyboard else "voice"
        console.print(f"[dim]Mode: {mode}[/dim]")
        console.print(f"[dim]Player: {settings.player}[/dim]")
        console.print(f"[dim]AI Model: {settings.ai_model}[/dim]")

        # Create and run the app
        from echo_sync.app import EchoSyncApp

        app = EchoSyncApp(
            settings=settings,
            demo_keyboard=args.demo_keyboard,
        )
        app.run()

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)

    except Exception as e:
        logger.exception("Fatal error: %s", e)
        console.print(f"\n[red]Fatal error: {e}[/red]")
        console.print(
            "[dim]Check the logs for details. "
            "If this persists, try --demo-keyboard mode.[/dim]"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
