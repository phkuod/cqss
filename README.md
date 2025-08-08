# CQSS Gantt Chart Generator

A Python-based tool for generating interactive Gantt charts from CSV project data. Creates static HTML files with D3.js visualizations that can be viewed without a web server.

## Features

- **Two-stage project visualization**: Preparing stage and execution stage with different colors
- **Progress tracking**: Visual progress bars showing completion percentage
- **Advanced filtering**: Filter by category, priority, team, and search text
- **Auto-scroll to today**: Automatically centers timeline on current date
- **Interactive features**: Tooltips, project details modal, click interactions
- **Export capabilities**: Built-in export functionality for charts
- **Priority-based coloring**: Color-coded by project priority (Critical, High, Medium, Low)
- **Static HTML output**: No web server required, just open in browser
- **Modern responsive design**: Professional appearance that works on all screen sizes

## Installation

1. Clone or download this repository
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Generation (Same Output File Each Time)
```bash
# Generate interactive Gantt chart to output/gantt_chart.html
python generate.py

# Generate standalone version (no internet required)
python generate.py data/extended_projects.csv --standalone

# Or use the batch file on Windows
generate.bat
```

### Advanced Usage
```bash
# Basic usage with default output location
python main.py data/sample_projects.csv

# Specify custom output file
python main.py data/sample_projects.csv output/my_chart.html

# Generate standalone version
python main.py data/sample_projects.csv --standalone

# Auto-open in browser after generation
python main.py data/sample_projects.csv --open
```

## CSV Data Format

Your CSV file must contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| project_name | Name of the project | "Project Alpha" |
| category | Project category | "Security" |
| priority | Priority level | "High" (Critical/High/Medium/Low) |
| preparing_start | Preparation start date | "2024-01-15" |
| preparing_end | Preparation end date | "2024-02-15" |
| execution_end | Execution end date | "2024-05-15" |
| progress_percent | Current progress (0-100) | 75 |
| description | Brief description | "Implement new auth system" |
| team_lead | Responsible person | "John Smith" |

See `data/sample_projects.csv` for a complete example.

## Project Structure

```
cqss-system/
├── data/                   # CSV data files
│   ├── sample_projects.csv # Example data
│   └── README.md          # Data format documentation
├── src/                   # Source code
│   ├── data_processor.py  # CSV processing and validation
│   └── gantt_generator.py # HTML generation
├── templates/             # HTML templates
│   └── interactive_modern_template.html
├── output/               # Generated HTML files
├── main.py              # Main application entry point
└── requirements.txt     # Python dependencies
```

## Customization

### Colors
Priority colors can be modified in the HTML template:
- Critical: Red (#dc3545)
- High: Orange (#fd7e14) 
- Medium: Yellow (#ffc107)
- Low: Green (#28a745)

### Template
You can create custom HTML templates based on `templates/interactive_modern_template.html` and use them with the `--template` option. The system now uses a single, feature-complete interactive template by default.

## Output

The generated HTML file includes:
- Interactive Gantt chart with responsive timeline
- Advanced filtering controls (category, priority, team, search)
- Auto-scroll to today functionality with smooth animations
- Project details modal with comprehensive information
- Hover tooltips and click interactions
- Export capabilities for different formats
- Modern, professional design optimized for all devices

## Example

Run with sample data:
```bash
python main.py data/sample_projects.csv output/example.html
```

Then open `output/example.html` in your web browser to see the interactive Gantt chart.
