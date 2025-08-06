#!/usr/bin/env python3
"""
Generate All Gantt Chart Styles
Creates all 6 design variants from a single CSV input file
"""

import sys
import argparse
from pathlib import Path
from src.gantt_generator import GanttChartGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Generate all 6 Gantt chart design styles from CSV data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python generate_all_styles.py data/sample_projects.csv
  
Output Files:
  - output/1_default_design.html
  - output/2_minimal_design.html  
  - output/3_dark_design.html
  - output/4_colorful_design.html
  - output/5_interactive_design.html
  - output/6_frappe_design.html
        """
    )
    
    parser.add_argument(
        'csv_file',
        help='Path to CSV file containing project data'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory (default: output)',
        default='output'
    )
    
    parser.add_argument(
        '--open',
        help='Open all generated files in browser',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define style configurations
    styles = [
        {'name': 'default', 'output': '1_default_design.html', 'title': 'Default Design'},
        {'name': 'minimal', 'output': '2_minimal_design.html', 'title': 'Minimal Design'},
        {'name': 'dark', 'output': '3_dark_design.html', 'title': 'Dark Design'},
        {'name': 'colorful', 'output': '4_colorful_design.html', 'title': 'Colorful Design'},
        {'name': 'interactive', 'output': '5_interactive_design.html', 'title': 'Interactive Design'},
        {'name': 'frappe', 'output': '6_frappe_design.html', 'title': 'Frappe Design'}
    ]
    
    print(f"Generating all 6 Gantt chart styles from {csv_path}...")
    print(f"Output directory: {output_dir}")
    print()
    
    generated_files = []
    
    try:
        for style_config in styles:
            style_name = style_config['name']
            output_filename = style_config['output']
            style_title = style_config['title']
            
            output_path = output_dir / output_filename
            
            print(f"  Generating {style_title} ({style_name})...")
            
            # Create generator for this style
            generator = GanttChartGenerator(style=style_name)
            generator.generate_chart(str(csv_path), str(output_path))
            
            generated_files.append(output_path)
            print(f"    OK {output_path}")
        
        print()
        print(f"Success! Generated {len(generated_files)} Gantt chart files:")
        for file_path in generated_files:
            print(f"  - {file_path}")
        
        # Open files in browser if requested
        if args.open:
            try:
                import webbrowser
                import os
                print(f"\nOpening files in default browser...")
                for file_path in generated_files:
                    file_url = f"file:///{os.path.abspath(file_path).replace(os.sep, '/')}"
                    webbrowser.open(file_url)
                print(f"Opened {len(generated_files)} files in browser")
            except Exception as browser_error:
                print(f"Could not open browser automatically: {browser_error}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()