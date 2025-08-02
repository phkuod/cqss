#!/usr/bin/env python3
"""
Quick Gantt Chart Generator
Generates to the same output file each time for easy iteration
"""

import sys
from pathlib import Path
from src.gantt_generator import GanttChartGenerator

def main():
    # Default settings - try mock data first, fallback to extended data
    if Path("data/mock_three_months.csv").exists():
        csv_file = "data/mock_three_months.csv"  # Use fresh mock data by default
    else:
        csv_file = "data/extended_projects.csv"  # Fallback to extended data
    
    output_file = "output/gantt_chart.html"
    standalone = False
    style = "default"
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        if sys.argv[2] == "--standalone":
            standalone = True
            output_file = "output/gantt_chart_standalone.html"
        elif sys.argv[2] == "--frappe":
            style = "frappe"
            output_file = "output/gantt_chart_frappe.html"
    
    # Validate input file
    csv_path = Path(csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        print(f"Available files:")
        data_dir = Path("data")
        if data_dir.exists():
            for f in data_dir.glob("*.csv"):
                print(f"  - {f}")
        sys.exit(1)
    
    # Create output directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Generate Gantt chart
        style_text = f" ({style} style)" if style != "default" else ""
        print(f"Generating Gantt chart{style_text} from {csv_file}...")
        generator = GanttChartGenerator(standalone=standalone, style=style)
        generator.generate_chart(str(csv_path), str(output_path))
        
        print(f"\nSuccess! Chart saved to: {output_path}")
        print(f"  Open {output_path} in your browser to view")
        
        # Try to open automatically
        try:
            import webbrowser
            import os
            file_url = f"file:///{os.path.abspath(output_path).replace(os.sep, '/')}"
            webbrowser.open(file_url)
            print(f"  Opening in default browser...")
        except Exception as browser_error:
            print(f"  Could not open browser automatically: {browser_error}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()