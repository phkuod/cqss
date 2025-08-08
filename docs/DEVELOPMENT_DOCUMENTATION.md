# CQSS Development Documentation

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [API Reference](#api-reference)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Contributing Guidelines](#contributing-guidelines)
9. [Troubleshooting](#troubleshooting)

## 1. Getting Started

### Prerequisites
- **Python 3.7+** (Recommended: Python 3.9 or higher)
- **pip** package manager
- **Git** for version control
- **Modern web browser** for viewing generated charts

### Quick Installation
```bash
# Clone the repository
git clone <repository-url>
cd cqss-system

# Install Python dependencies
pip install -r requirements.txt

# Verify installation with sample data
python generate.py
```

### Dependencies
```
pandas>=1.3.0          # Data processing and CSV handling
jinja2>=3.0.0          # Template engine for HTML generation
pathlib                # Modern path handling (built-in Python 3.4+)
argparse               # Command-line interface (built-in)
json                   # JSON data handling (built-in)
datetime               # Date/time operations (built-in)
```

## 2. Development Environment Setup

### Recommended Development Stack
- **IDE**: VS Code with Python extension
- **Python Environment**: Virtual environment or conda
- **Browser**: Chrome/Firefox with developer tools
- **Version Control**: Git with conventional commits

### Setting Up Virtual Environment
```bash
# Create virtual environment
python -m venv cqss-env

# Activate (Windows)
cqss-env\Scripts\activate

# Activate (macOS/Linux)
source cqss-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### VS Code Configuration
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./cqss-env/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "files.associations": {
        "*.html": "jinja-html"
    }
}
```

## 3. Project Structure

### Directory Layout
```
cqss-system/
├── src/                    # Core application modules
│   ├── __init__.py        # Package initialization
│   ├── data_processor.py  # CSV processing and validation
│   └── gantt_generator.py # HTML generation logic
├── templates/             # Jinja2 HTML templates
│   └── interactive_modern_template.html
├── data/                  # Sample and test data
│   ├── sample_projects.csv
│   ├── mock_three_months.csv
│   └── README.md         # Data format documentation
├── output/               # Generated HTML files
│   └── gantt_chart.html  # Primary output file
├── static/               # Static assets
│   └── js/
│       └── d3.v7.min.js  # D3.js library for offline use
├── docs/                 # Documentation files
│   ├── DESIGN_DOCUMENTATION.md
│   └── DEVELOPMENT_DOCUMENTATION.md
├── tests/                # Unit and integration tests
├── main.py               # Full CLI entry point
├── generate.py           # Quick generation script
├── generate_mock_data.py # Mock data generator
├── requirements.txt      # Python dependencies
├── CLAUDE.md            # Claude Code instructions
└── README.md            # Project overview
```

### Core Module Descriptions

#### `src/data_processor.py`
- **Purpose**: CSV data processing and validation
- **Key Classes**: `ProjectDataProcessor`
- **Responsibilities**: Data loading, validation, transformation to JSON format
- **Output**: Structured project data suitable for D3.js visualization

#### `src/gantt_generator.py`
- **Purpose**: HTML generation using Jinja2 templates
- **Key Classes**: `GanttChartGenerator`
- **Responsibilities**: Template rendering, data embedding, file output
- **Features**: Unified template approach, standalone mode support

## 4. Development Workflow

### Standard Development Process
1. **Feature Branch**: Create branch from `master`
   ```bash
   git checkout master
   git pull origin master
   git checkout -b feature/new-feature-name
   ```

2. **Development**: Implement and test locally
   ```bash
   # Quick testing
   python generate.py
   
   # Full testing with custom data
   python main.py data/sample_projects.csv output/test.html --open
   ```

3. **Commit**: Use conventional commit messages
   ```bash
   git add .
   git commit -m "feat: add new filtering capability"
   ```

4. **Push and PR**: Push to remote and create pull request
   ```bash
   git push -u origin feature/new-feature-name
   gh pr create --title "feat: New Feature" --body "Description"
   ```

### Common Development Commands

#### Quick Generation (Development)
```bash
# Generate with mock data (auto-opens browser)
python generate.py

# Generate with specific CSV file
python generate.py data/sample_projects.csv

# Generate standalone version (no internet required)
python generate.py data/sample_projects.csv --standalone
```

#### Full CLI Usage
```bash
# Basic generation
python main.py data/sample_projects.csv

# Custom output location
python main.py data/sample_projects.csv output/custom_name.html

# Auto-open in browser
python main.py data/sample_projects.csv --open

# Standalone mode
python main.py data/sample_projects.csv --standalone
```

#### Mock Data Generation
```bash
# Generate 25 projects spanning 3 months
python generate_mock_data.py --projects 25 --output data/test_data.csv

# Generate with specific parameters
python generate_mock_data.py --projects 50 --start-date 2024-01-01 --months 6
```

### Testing During Development
```bash
# Test data processor directly
cd src && python data_processor.py

# Test generator directly
cd src && python gantt_generator.py

# Run with different data files
python main.py data/mock_three_months.csv output/test.html
```

## 5. API Reference

### ProjectDataProcessor Class

#### Constructor
```python
processor = ProjectDataProcessor()
```

#### Methods

**`load_csv(file_path: str) -> pd.DataFrame`**
- Loads and validates CSV file
- **Parameters**: `file_path` - Path to CSV file
- **Returns**: Validated pandas DataFrame
- **Raises**: `ValueError` for validation errors

**`process_to_gantt_data(df: pd.DataFrame) -> List[Dict[str, Any]]`**
- Converts DataFrame to Gantt chart format
- **Parameters**: `df` - Validated DataFrame
- **Returns**: List of project dictionaries with stage information

**`get_date_range(data: List[Dict[str, Any]]) -> Dict[str, str]`**
- Calculates overall project date range
- **Parameters**: `data` - Processed project data
- **Returns**: Dictionary with `min_date` and `max_date`

**`export_to_json(data: List[Dict[str, Any]], output_path: str) -> None`**
- Exports processed data to JSON file
- **Parameters**: `data` - Project data, `output_path` - Output file path

### GanttChartGenerator Class

#### Constructor
```python
generator = GanttChartGenerator(
    template_path: str = None,
    standalone: bool = False,
    style: str = "interactive"
)
```

#### Methods

**`generate_chart(csv_file_path: str, output_path: str) -> None`**
- Complete chart generation from CSV to HTML
- **Parameters**: `csv_file_path` - Input CSV, `output_path` - Output HTML file

**`generate_from_processed_data(project_data: list, date_range: dict, output_path: str) -> None`**
- Generate chart from pre-processed data
- **Parameters**: `project_data` - Processed data, `date_range` - Date range info, `output_path` - Output file

## 6. Testing

### Manual Testing Checklist
- [ ] CSV data validation with invalid files
- [ ] Date range validation and edge cases
- [ ] Progress percentage validation (0-100)
- [ ] Template rendering with various data sizes
- [ ] Browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] Responsive design on different screen sizes
- [ ] Interactive features (filtering, scrolling, tooltips)

### Test Data Creation
```python
# Create test CSV data
import pandas as pd

test_data = {
    'project_name': ['Test Project'],
    'category': ['Testing'],
    'priority': ['High'],
    'preparing_start': ['2024-01-01'],
    'preparing_end': ['2024-01-15'],
    'execution_end': ['2024-03-01'],
    'progress_percent': [50],
    'description': ['Test project for validation'],
    'team_lead': ['Test Lead']
}

df = pd.DataFrame(test_data)
df.to_csv('data/test_data.csv', index=False)
```

### Error Testing Scenarios
1. **Missing required columns** in CSV
2. **Invalid date formats** (non-YYYY-MM-DD)
3. **Progress percentages** outside 0-100 range
4. **Illogical date sequences** (end before start)
5. **Empty CSV files**
6. **Non-existent file paths**

## 7. Deployment

### Static HTML Deployment
Generated HTML files are completely self-contained and can be:
- **Hosted on any web server** (Apache, Nginx, IIS)
- **Served from file system** (file:// URLs)
- **Deployed to CDN** (AWS S3, Netlify, Vercel)
- **Embedded in applications** (iframes, webviews)

### Build Process for Distribution
```bash
# Generate with all dependencies embedded
python main.py data/production_data.csv output/production_chart.html --standalone

# Verify standalone mode works offline
# (Disconnect internet and open in browser)
```

### Production Considerations
- **Data Security**: Ensure sensitive project data is not exposed
- **Performance**: Test with large datasets (100+ projects)
- **Browser Support**: Verify compatibility with target browsers
- **Responsive Design**: Test on target device types

## 8. Contributing Guidelines

### Code Style
- **Python**: Follow PEP 8 conventions
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Use Google-style docstrings
- **Comments**: Focus on why, not what

### Git Workflow
- **Branch Naming**: `feature/description`, `fix/issue-description`
- **Commit Messages**: Use conventional commits format
- **Pull Requests**: Include description and testing notes

### Template Modifications
- **CSS**: Use CSS custom properties for easy theming
- **JavaScript**: Maintain ES6+ compatibility
- **D3.js**: Follow D3.js best practices for performance
- **Responsive**: Test on multiple screen sizes

### Adding New Features
1. **Update data processor** if new CSV fields needed
2. **Modify template** for new visualizations
3. **Update documentation** including this file
4. **Test thoroughly** with various datasets
5. **Consider backwards compatibility**

## 9. Troubleshooting

### Common Issues

#### "CSV file not found" Error
```bash
# Check current directory
ls -la data/

# Use absolute path
python main.py /full/path/to/data.csv
```

#### "Missing required columns" Error
```python
# Check CSV headers
import pandas as pd
df = pd.read_csv('data/your_file.csv')
print(df.columns.tolist())

# Required columns:
required = [
    'project_name', 'category', 'priority', 'preparing_start', 
    'preparing_end', 'execution_end', 'progress_percent', 
    'description', 'team_lead'
]
```

#### "Invalid date format" Error
```python
# Ensure dates are in YYYY-MM-DD format
# Incorrect: 01/15/2024, 15-Jan-2024
# Correct: 2024-01-15
```

#### Template Not Found Error
```bash
# Verify template exists
ls -la templates/interactive_modern_template.html

# Use custom template
python main.py data/sample.csv --template custom_template.html
```

#### Browser Display Issues
- **Clear browser cache** if changes not appearing
- **Check browser console** for JavaScript errors
- **Verify D3.js library** is loaded correctly
- **Test in incognito mode** to avoid extension conflicts

### Performance Optimization

#### Large Datasets (100+ projects)
- **Data Processing**: Uses pandas for efficient processing
- **Template Rendering**: Jinja2 optimized for large templates
- **Browser Performance**: D3.js handles large SVG efficiently
- **Memory Usage**: Monitor with large datasets

#### Slow Generation Times
```bash
# Profile data processing
python -m cProfile -o profile.stats main.py data/large_dataset.csv
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('time').print_stats(10)"
```

### Debug Mode
Enable verbose logging for troubleshooting:
```python
# Add to main.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help
1. **Check CLAUDE.md** for project-specific guidance
2. **Review error messages** for specific issues
3. **Test with sample data** to isolate problems
4. **Check browser developer tools** for frontend issues
5. **Verify Python version** and dependencies

This development documentation provides comprehensive guidance for developers working on the CQSS system, from initial setup through deployment and troubleshooting.