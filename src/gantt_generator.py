import json
from pathlib import Path
from jinja2 import Template
from .data_processor import ProjectDataProcessor

class GanttChartGenerator:
    """
    Generates static HTML Gantt chart from processed project data
    """
    
    def __init__(self, template_path: str = None, standalone: bool = False, style: str = "interactive"):
        if template_path is None:
            # Always use the interactive modern template - it's the most feature-complete
            template_name = 'interactive_modern_template.html'
            template_path = Path(__file__).parent.parent / 'templates' / template_name
        
        self.template_path = Path(template_path)
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
    
    def generate_chart(self, csv_file_path: str, output_path: str) -> None:
        """
        Generate complete Gantt chart HTML file from CSV data
        
        Args:
            csv_file_path: Path to CSV file containing project data
            output_path: Path where the HTML file will be saved
        """
        # Process the data
        processor = ProjectDataProcessor()
        df = processor.load_csv(csv_file_path)
        project_data = processor.process_to_gantt_data(df)
        date_range = processor.get_date_range(project_data)
        
        # Load template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Create Jinja2 template
        template = Template(template_content)
        
        # Render template with data
        html_content = template.render(
            project_data=json.dumps(project_data, indent=2),
            date_range=json.dumps(date_range, indent=2)
        )
        
        # Write output file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Gantt chart generated successfully: {output_file}")
        print(f"Processed {len(project_data)} projects")
        print(f"Date range: {date_range['min_date']} to {date_range['max_date']}")
    
    def generate_from_processed_data(self, project_data: list, date_range: dict, output_path: str) -> None:
        """
        Generate Gantt chart from already processed data
        
        Args:
            project_data: List of processed project dictionaries
            date_range: Dictionary with min_date and max_date
            output_path: Path where the HTML file will be saved
        """
        # Load template
        with open(self.template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Create Jinja2 template
        template = Template(template_content)
        
        # Render template with data
        html_content = template.render(
            project_data=json.dumps(project_data, indent=2),
            date_range=json.dumps(date_range, indent=2)
        )
        
        # Write output file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Gantt chart generated successfully: {output_file}")

# Example usage and main function
if __name__ == "__main__":
    generator = GanttChartGenerator()
    
    # Generate chart from sample data
    csv_path = Path(__file__).parent.parent / 'data' / 'sample_projects.csv'
    output_path = Path(__file__).parent.parent / 'output' / 'gantt_chart.html'
    
    try:
        generator.generate_chart(str(csv_path), str(output_path))
    except Exception as e:
        print(f"Error generating Gantt chart: {str(e)}")
        raise