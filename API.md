# API Documentation

This document provides detailed technical information for developers who want to extend or integrate with the CQSS Gantt Chart Generator.

## Core Modules

### `src/data_processor.py`

Handles CSV data processing, validation, and transformation for D3.js consumption.

#### Key Functions

```python
def process_csv_data(csv_file_path: str) -> tuple[list, dict]:
    """
    Process CSV file and return project data and date range information.
    
    Args:
        csv_file_path (str): Path to the CSV file
        
    Returns:
        tuple: (processed_projects, date_range_info)
            - processed_projects: List of project dictionaries
            - date_range_info: Dict with min_date and max_date
    """
```

```python  
def detect_format(df: pandas.DataFrame) -> str:
    """
    Detect whether CSV uses legacy or multi-stage format.
    
    Args:
        df: Pandas DataFrame from CSV
        
    Returns:
        str: 'multistage' or 'legacy'
    """
```

```python
def process_multistage_format(df: pandas.DataFrame) -> list:
    """
    Process multi-stage format CSV data.
    
    Args:
        df: DataFrame with 'stages' column containing JSON arrays
        
    Returns:
        list: Processed project data with stages array
    """
```

### `src/gantt_generator.py`

Generates HTML output using Jinja2 templates and processed data.

#### Key Functions

```python
def generate_gantt_html(project_data: list, date_range: dict, 
                       template_path: str = None, standalone: bool = False) -> str:
    """
    Generate HTML content for Gantt chart.
    
    Args:
        project_data: Processed project data from data_processor
        date_range: Date range information  
        template_path: Path to HTML template file
        standalone: Whether to embed D3.js directly
        
    Returns:
        str: Generated HTML content
    """
```

## Data Structures

### Project Data Format

Each project in the processed data has this structure:

```python
{
    "id": "project_1",
    "name": "Project Alpha",
    "category": "Security", 
    "priority": "High",
    "description": "Multi-phase authentication system",
    "team_lead": "John Smith",
    
    # Multi-stage data
    "stages": [
        {
            "name": "Planning",
            "start": "2024-01-15T00:00:00",
            "end": "2024-02-15T00:00:00",
            "progress_percent": 100,
            "duration_days": 31
        },
        {
            "name": "Development", 
            "start": "2024-02-15T00:00:00",
            "end": "2024-04-15T00:00:00",
            "progress_percent": 75,
            "duration_days": 59
        }
    ],
    
    # Legacy compatibility fields (auto-generated)
    "preparing_stage": {
        "start": "2024-01-15T00:00:00",
        "end": "2024-02-15T00:00:00", 
        "progress_percent": 100
    },
    "execution_stage": {
        "start": "2024-02-15T00:00:00",
        "end": "2024-04-15T00:00:00",
        "progress_percent": 75
    }
}
```

### Date Range Format

```python
{
    "min_date": "2024-01-15T00:00:00",
    "max_date": "2024-05-15T00:00:00"
}
```

## Template System

### Template Variables

Templates receive these Jinja2 variables:

- `project_data`: List of processed project dictionaries
- `date_range`: Date range information dictionary

### Stage Color Mapping

Templates use this JavaScript object for stage colors:

```javascript
const stageColors = {
    'Planning': '#6f42c1',
    'Preparing': '#6f42c1', 
    'Analysis': '#17a2b8',
    'Research': '#17a2b8',
    'Design': '#20c997',
    'Wireframes': '#20c997',
    'Development': '#28a745',
    'Implementation': '#28a745',
    'Testing': '#ffc107',
    'Audit': '#ffc107',
    'Migration': '#fd7e14',
    'Deployment': '#dc3545',
    'Execution': '#007bff'
};
```

### Priority Colors

```javascript
const priorityColors = {
    'Critical': '#dc3545',
    'High': '#fd7e14', 
    'Medium': '#ffc107',
    'Low': '#28a745'
};
```

## Extension Points

### Adding New Templates

1. Create new HTML template in `templates/` directory
2. Use existing templates as reference for required JavaScript functions
3. Implement these core functions:
   - Dynamic stage rendering with `d.stages.forEach()`
   - Filter functionality 
   - Tooltip and modal interactions
   - Timeline navigation features

### Custom Stage Types

To add new stage types:

1. Update `stageColors` object in template
2. Add stage name recognition in data processor
3. Update documentation

### Custom Data Sources

To support data sources other than CSV:

1. Create new processor module following `data_processor.py` pattern  
2. Ensure output matches the project data structure format
3. Update main.py to support new input types

## Utility Scripts

### `generate_mock_data.py`

Generate test data for development and demos.

```python
def generate_mock_projects(num_projects: int = 25, 
                         months_span: int = 3) -> pandas.DataFrame:
    """
    Generate realistic mock project data.
    
    Args:
        num_projects: Number of projects to generate
        months_span: Time span in months around today
        
    Returns:
        DataFrame: Mock project data
    """
```

### `update_templates_multistage.py`

Update legacy templates to support multi-stage format.

## Error Handling

### Common Exceptions

```python
class CSVFormatError(Exception):
    """Raised when CSV format is invalid or unsupported."""
    pass

class DateParsingError(Exception):
    """Raised when date fields cannot be parsed."""
    pass
    
class TemplateNotFoundError(Exception):
    """Raised when specified template file doesn't exist."""
    pass
```

### Validation Rules

- Project names must be non-empty strings
- Dates must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- Priority must be one of: Critical, High, Medium, Low
- Progress percentages must be 0-100 integers
- Stage arrays must contain valid JSON with required fields

## Performance Considerations

### Large Datasets

- Tested with 100+ projects
- Filtering is client-side JavaScript (suitable for <500 projects)
- For larger datasets, consider server-side filtering

### Browser Compatibility

- Requires modern browser with D3.js v7 support
- ES6+ JavaScript features used
- Responsive CSS Grid and Flexbox

## Development Workflow

### Adding Features

1. Create feature branch from master
2. Implement changes with tests
3. Update relevant templates  
4. Update documentation
5. Submit for review

### Testing

- Test with both legacy and multi-stage CSV formats
- Verify all 6 templates work correctly
- Test filtering and interaction features
- Validate responsive design

## Integration Examples

### Custom Web Application

```python
from src.data_processor import process_csv_data
from src.gantt_generator import generate_gantt_html

# Process your data
projects, date_range = process_csv_data('your_data.csv')

# Generate HTML
html_content = generate_gantt_html(
    projects, 
    date_range, 
    template_path='templates/dark_professional_template.html'
)

# Serve or save the HTML
with open('output.html', 'w') as f:
    f.write(html_content)
```

### REST API Integration

```python
from flask import Flask, jsonify
from src.data_processor import process_csv_data

app = Flask(__name__)

@app.route('/api/projects')
def get_projects():
    projects, date_range = process_csv_data('data/projects.csv')
    return jsonify({
        'projects': projects,
        'date_range': date_range
    })
```