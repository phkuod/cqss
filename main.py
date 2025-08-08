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
  python main.py data/sample_projects.csv --open

Always generates interactive Gantt charts with:
  - Advanced filtering (category, priority, team, search)
  - Auto-scroll to today functionality
  - Modern responsive design with tooltips
  - Export capabilities and project details modal
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
    
    # Style parameter removed - now always uses interactive template
    
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
        if args.standalone:
            default_output = 'output/gantt_chart_standalone.html'
        else:
            default_output = 'output/gantt_chart.html'
        args.output_file = default_output
    
    # Create output directory if needed
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate Gantt chart using interactive template
        generator = GanttChartGenerator(template_path=args.template, standalone=args.standalone)
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