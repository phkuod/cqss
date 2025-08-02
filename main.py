#!/usr/bin/env python3
"""
CQSS Gantt Chart Generator
Main entry point for generating Gantt charts from CSV project data
"""

import argparse
import sys
from pathlib import Path
from src.gantt_generator import GanttChartGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Generate static HTML Gantt chart from CSV project data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py data/sample_projects.csv
  python main.py data/sample_projects.csv output/my_gantt.html
  python main.py data/sample_projects.csv --standalone
  python main.py data/sample_projects.csv --style minimal --open
  python main.py data/sample_projects.csv --style dark --open
  python main.py data/sample_projects.csv --style colorful --open
  python main.py data/sample_projects.csv --style interactive --open

Available Styles:
  default     - Classic Gantt chart design
  frappe      - Clean, modern Frappe-inspired design
  minimal     - Ultra-clean minimal design (Notion/Linear style)
  dark        - Professional dark theme (GitHub/Figma style)
  colorful    - Vibrant, friendly design (Monday.com/Asana style)
  interactive - Modern interactive design with filters & click features
        """
    )
    
    parser.add_argument(
        'csv_file',
        help='Path to CSV file containing project data'
    )
    
    parser.add_argument(
        'output_file',
        help='Path for output HTML file (optional, defaults to output/gantt_chart.html)',
        nargs='?',
        default=None
    )
    
    parser.add_argument(
        '--template',
        help='Path to custom HTML template (optional)',
        default=None
    )
    
    parser.add_argument(
        '--standalone',
        help='Generate standalone HTML (no internet required)',
        action='store_true'
    )
    
    parser.add_argument(
        '--style',
        help='Gantt chart style (default, frappe, minimal, dark, colorful, interactive)',
        choices=['default', 'frappe', 'minimal', 'dark', 'colorful', 'interactive'],
        default='default'
    )
    
    parser.add_argument(
        '--open',
        help='Automatically open the generated chart in default browser',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)
    
    # Set default output file if not provided
    if args.output_file is None:
        if args.style == 'frappe':
            default_output = 'output/gantt_chart_frappe.html'
        elif args.style == 'minimal':
            default_output = 'output/gantt_chart_minimal.html'
        elif args.style == 'dark':
            default_output = 'output/gantt_chart_dark.html'
        elif args.style == 'colorful':
            default_output = 'output/gantt_chart_colorful.html'
        elif args.style == 'interactive':
            default_output = 'output/gantt_chart_interactive.html'
        elif args.standalone:
            default_output = 'output/gantt_chart_standalone.html'
        else:
            default_output = 'output/gantt_chart.html'
        args.output_file = default_output
    
    # Create output directory if needed
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate Gantt chart
        generator = GanttChartGenerator(template_path=args.template, standalone=args.standalone, style=args.style)
        generator.generate_chart(str(csv_path), str(output_path))
        
        print(f"\nSuccess! Open {output_path} in your web browser to view the Gantt chart.")
        
        # Auto-open in browser if requested
        if args.open:
            try:
                import webbrowser
                import os
                file_url = f"file:///{os.path.abspath(output_path).replace(os.sep, '/')}"
                webbrowser.open(file_url)
                print(f"Opening in default browser...")
            except Exception as browser_error:
                print(f"Could not open browser automatically: {browser_error}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()