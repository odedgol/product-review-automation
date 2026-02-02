#!/usr/bin/env python3
"""
Product Review Video Automation
Main entry point for generating product review videos

Usage:
    python main.py --product owala_freesip --language hebrew
    python main.py --demo  # Run with example data, no API keys needed
"""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scrapers.product_scraper import get_product_data, format_product_for_script
from generators.script_generator import ScriptGenerator, get_example_script
from generators.voice_generator import get_voice_generator, MockVoiceGenerator
from generators.video_generator import get_video_generator, SimpleVideoGenerator

console = Console()


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║       🎬 Product Review Video Automation System 🎬            ║
    ║                                                               ║
    ║   Automatically generate YouTube product review videos        ║
    ║   with AI-powered scripts, voice-over, and video editing      ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue"))


def run_demo():
    """Run demo with pre-generated content (no API keys needed)"""
    
    console.print("\n[bold green]🚀 Running Demo Mode[/bold green]")
    console.print("No API keys required - using pre-generated content\n")
    
    # Step 1: Get product data
    console.print("[bold]Step 1:[/bold] Loading product data...")
    product = get_product_data("owala_freesip")
    
    table = Table(title="Product Information")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Name", product.name)
    table.add_row("Brand", product.brand)
    table.add_row("Price", f"${product.price}")
    table.add_row("Rating", f"{product.rating}/5")
    table.add_row("Reviews", f"{product.review_count:,}")
    console.print(table)
    
    # Step 2: Get script
    console.print("\n[bold]Step 2:[/bold] Loading pre-generated script...")
    script = get_example_script()
    
    console.print(f"  ✓ Script loaded: {script['word_count']} words")
    console.print(f"  ✓ Language: {script['language']}")
    console.print(f"  ✓ Sections: {', '.join(script['sections'].keys())}")
    
    # Show script preview
    console.print("\n[bold]Script Preview:[/bold]")
    console.print(Panel(
        script['full_script'][:500] + "...",
        title="תסריט הסרטון",
        border_style="green"
    ))
    
    # Step 3: Estimate voice-over cost
    console.print("\n[bold]Step 3:[/bold] Estimating voice-over cost...")
    voice_gen = MockVoiceGenerator()
    cost = voice_gen.estimate_cost(script['full_script'])
    console.print(f"  ✓ Character count: {len(script['full_script']):,}")
    console.print(f"  ✓ Estimated ElevenLabs cost: [green]${cost:.2f}[/green]")
    
    # Step 4: Generate storyboard
    console.print("\n[bold]Step 4:[/bold] Generating video storyboard...")
    video_gen = SimpleVideoGenerator()
    
    storyboard_path = video_gen.generate_storyboard(
        product_name=product.name,
        product_images=product.images,
        script_sections=script['sections'],
        pros=product.pros,
        cons=product.cons,
        score=8.5,
        output_filename="owala_freesip_storyboard.md"
    )
    
    console.print(f"  ✓ Storyboard saved to: [cyan]{storyboard_path}[/cyan]")
    
    # Summary
    console.print("\n" + "="*60)
    console.print(Panel(
        """
[bold green]✅ Demo Complete![/bold green]

Generated files:
• output/owala_freesip_storyboard.md - Video storyboard

[bold]To generate actual videos, you need:[/bold]
1. ElevenLabs API key (for voice-over)
2. Anthropic API key (for custom scripts)
3. MoviePy installed (for video rendering)

[bold]Next steps:[/bold]
1. Copy .env.example to .env
2. Add your API keys
3. Run: python main.py --product owala_freesip
        """,
        title="Summary",
        border_style="green"
    ))
    
    return storyboard_path


def run_full_pipeline(product_id: str, language: str = "hebrew"):
    """Run full pipeline with API calls"""
    
    console.print(f"\n[bold green]🚀 Running Full Pipeline[/bold green]")
    console.print(f"Product: {product_id}, Language: {language}\n")
    
    # Check for API keys
    import os
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[yellow]Warning: ANTHROPIC_API_KEY not set. Using example script.[/yellow]")
    if not os.getenv("ELEVENLABS_API_KEY"):
        console.print("[yellow]Warning: ELEVENLABS_API_KEY not set. Voice generation will be mocked.[/yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        # Step 1: Product data
        task = progress.add_task("Loading product data...", total=1)
        product = get_product_data(product_id)
        progress.update(task, completed=1)
        
        # Step 2: Script generation
        task = progress.add_task("Generating script...", total=1)
        
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                script_gen = ScriptGenerator()
                product_info = format_product_for_script(product)
                script = script_gen.generate_script(
                    product_info=product_info,
                    language=language,
                )
            except Exception as e:
                console.print(f"[yellow]Script generation failed: {e}. Using example.[/yellow]")
                script = get_example_script()
        else:
            script = get_example_script()
        
        progress.update(task, completed=1)
        
        # Step 3: Voice generation
        task = progress.add_task("Generating voice-over...", total=1)
        voice_gen = get_voice_generator()
        
        if isinstance(voice_gen, MockVoiceGenerator):
            audio_path = voice_gen.generate_voice(
                script['full_script'],
                output_filename=f"{product_id}_voiceover.txt"
            )
        else:
            audio_path = voice_gen.generate_voice(
                script['full_script'],
                output_filename=f"{product_id}_voiceover.mp3"
            )
        
        progress.update(task, completed=1)
        
        # Step 4: Video generation
        task = progress.add_task("Generating video...", total=1)
        video_gen = get_video_generator()
        
        if isinstance(video_gen, SimpleVideoGenerator):
            output_path = video_gen.generate_storyboard(
                product_name=product.name,
                product_images=product.images,
                script_sections=script['sections'],
                pros=product.pros,
                cons=product.cons,
                score=8.5,
                output_filename=f"{product_id}_storyboard.md"
            )
        else:
            output_path = video_gen.generate_full_video(
                product_name=product.name,
                product_images=[],  # Would need to download images
                pros=product.pros,
                cons=product.cons,
                score=8.5,
                recommendation="מומלץ בחום!",
                audio_path=str(audio_path) if audio_path.suffix == ".mp3" else None,
                output_filename=f"{product_id}_review.mp4"
            )
        
        progress.update(task, completed=1)
    
    console.print(f"\n[bold green]✅ Pipeline Complete![/bold green]")
    console.print(f"Output: [cyan]{output_path}[/cyan]")
    
    return output_path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Product Review Video Automation System"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo mode with pre-generated content"
    )
    parser.add_argument(
        "--product",
        type=str,
        default="owala_freesip",
        help="Product ID to review"
    )
    parser.add_argument(
        "--language",
        type=str,
        choices=["hebrew", "english"],
        default="hebrew",
        help="Language for the script"
    )
    parser.add_argument(
        "--list-products",
        action="store_true",
        help="List available products"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.list_products:
        console.print("\n[bold]Available Products:[/bold]")
        console.print("  • owala_freesip - Owala FreeSip Water Bottle 24oz")
        console.print("\n[dim]More products coming soon...[/dim]")
        return
    
    if args.demo:
        run_demo()
    else:
        run_full_pipeline(args.product, args.language)


if __name__ == "__main__":
    main()
