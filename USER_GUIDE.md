# CQSS Gantt Chart Generator - User Guide

Welcome to the comprehensive user guide for the CQSS Gantt Chart Generator! This guide will walk you through everything you need to know to create stunning Gantt charts for your projects.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding Templates](#understanding-templates)
3. [Data Preparation](#data-preparation)
4. [Chart Generation](#chart-generation)
5. [Interactive Features](#interactive-features)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)
8. [Tips & Best Practices](#tips--best-practices)

## Getting Started

### System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)
- **Storage**: ~50MB for installation and data

### Installation Steps

1. **Download the project**
   ```bash
   git clone https://github.com/yourusername/cqss-system.git
   cd cqss-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python generate.py
   ```
   This should create sample charts in the `output/` folder.

## Understanding Templates

The CQSS system offers 6 distinct visual templates, each designed for different use cases:

### 1. Default Design (`1_default_design.html`)
- **Best for**: Corporate presentations, formal reports
- **Style**: Professional, clean, traditional
- **Features**: Standard colors, clear typography, print-friendly

### 2. Modern Minimal (`2_minimal_design.html`)
- **Best for**: Focus on data, minimal interfaces
- **Style**: Ultra-clean, distraction-free, spacious
- **Features**: Subtle colors, maximum readability, elegant spacing

### 3. Dark Professional (`3_dark_design.html`)
- **Best for**: Dark mode environments, developer dashboards
- **Style**: Sleek dark theme, modern aesthetic
- **Features**: Easy on eyes, great for extended viewing, tech-focused

### 4. Colorful Friendly (`4_colorful_design.html`)
- **Best for**: Team dashboards, creative projects
- **Style**: Vibrant, approachable, fun with emojis
- **Features**: Color-coded categories, emoji indicators, team-friendly

### 5. Interactive Modern (`5_interactive_design.html`)
- **Best for**: Interactive dashboards, live demos
- **Style**: Advanced hover effects, smooth animations
- **Features**: Enhanced interactivity, polished animations, engaging UX

### 6. Frappe-inspired (`6_frappe_design.html`)
- **Best for**: Development projects, technical documentation
- **Style**: Clean GitHub-style, developer-focused
- **Features**: Subtle indicators, clean lines, technical aesthetic

## Data Preparation

### CSV File Structure

You can use two different formats depending on your project complexity:

#### Multi-Stage Format (Recommended for Complex Projects)

```csv
project_name,category,priority,description,team_lead,stages
"Website Redesign","Development","High","Complete redesign of company website","Alice Johnson","[{""name"":""Planning"",""start"":""2024-01-15"",""end"":""2024-02-15"",""progress"":100},{""name"":""Design"",""start"":""2024-02-15"",""end"":""2024-03-15"",""progress"":80},{""name"":""Development"",""start"":""2024-03-15"",""end"":""2024-05-15"",""progress"":40}]"
"Marketing Campaign","Marketing","Medium","Q2 product launch campaign","Bob Smith","[{""name"":""Research"",""start"":""2024-02-01"",""end"":""2024-02-15"",""progress"":100},{""name"":""Planning"",""start"":""2024-02-15"",""end"":""2024-03-01"",""progress"":90},{""name"":""Execution"",""start"":""2024-03-01"",""end"":""2024-04-15"",""progress"":60}]"
```

#### Legacy Format (Simple Two-Stage Projects)

```csv
project_name,category,priority,preparing_start,preparing_end,execution_end,progress_percent,description,team_lead
"Security Audit","Security","Critical","2024-01-01","2024-02-01","2024-03-15",75,"Complete security assessment","Charlie Wilson"
"Database Migration","Infrastructure","High","2024-02-15","2024-03-01","2024-04-30",30,"Migrate to new database system","Diana Prince"
```

### Data Guidelines

#### Required Fields

| Field | Description | Example | Notes |
|-------|-------------|---------|-------|
| `project_name` | Project identifier | "Website Redesign" | Keep under 50 characters for best display |
| `category` | Project type/department | "Development" | Used for filtering and organization |
| `priority` | Importance level | "High" | Must be: Critical, High, Medium, or Low |
| `description` | Brief project summary | "Complete site redesign" | Shown in tooltips and details |
| `team_lead` | Responsible person | "Alice Johnson" | Used for team filtering |

#### Multi-Stage Specific Fields

- **`stages`**: JSON array of stage objects with `name`, `start`, `end`, and `progress` fields

#### Legacy Format Specific Fields

- **`preparing_start`**: Preparation phase start date
- **`preparing_end`**: Preparation phase end date  
- **`execution_end`**: Final project completion date
- **`progress_percent`**: Overall completion percentage (0-100)

#### Date Format

All dates must use ISO format:
- **Simple**: `2024-03-15` 
- **With time**: `2024-03-15T14:30:00`

#### Progress Values

- Must be integers between 0 and 100
- Represents percentage completion
- Each stage can have individual progress values

## Chart Generation

### Quick Generation

The fastest way to get started:

```bash
# Generate all 6 templates with sample data
python generate.py

# Generate all 6 templates with your data
python generate.py data/your_projects.csv
```

This creates:
- `output/1_default_design.html`
- `output/2_minimal_design.html`
- `output/3_dark_design.html`
- `output/4_colorful_design.html`
- `output/5_interactive_design.html`
- `output/6_frappe_design.html`

### Custom Generation

For more control over output:

```bash
# Generate specific template
python main.py data/your_projects.csv output/my_chart.html --template templates/dark_professional_template.html

# Generate standalone version (no internet required)
python main.py data/your_projects.csv output/standalone_chart.html --standalone

# Generate all styles to custom directory
python generate_all_styles.py --output custom_output/
```

### Mock Data for Testing

Create realistic test data:

```bash
# Generate 25 projects over 3 months
python generate_mock_data.py

# Generate 50 projects over 6 months  
python generate_mock_data.py --projects 50 --months 6 --output data/large_test.csv

# Use the mock data
python generate.py data/mock_three_months.csv
```

## Interactive Features

### Timeline Navigation

#### Auto-scroll to Today
- Charts automatically center on today's date when opened
- Look for the red "Today" line indicating current date
- Perfect for tracking current project status

#### Manual Navigation
- **Mouse**: Click and drag to scroll horizontally
- **Keyboard**: Use arrow keys for precise navigation
- **Scroll wheel**: Horizontal scrolling over timeline
- **Today button**: Click to return to current date

#### Visual Indicators
- **Fade indicators**: Show when more content is available left/right
- **Scroll hints**: Appear briefly to guide new users
- **Smooth animations**: Enhanced scrolling experience

### Filtering System

#### Priority Filter
Filter projects by importance level:
- **Critical**: Red projects requiring immediate attention
- **High**: Orange projects with high importance
- **Medium**: Yellow projects with moderate priority
- **Low**: Green projects with lower priority

#### Category Filter
Organize projects by type:
- Development, Marketing, Security, Infrastructure, etc.
- Dynamically populated from your data
- Useful for focusing on specific departments

#### Team Filter
View projects by responsible team members:
- Filter by team lead or responsible person
- Great for individual performance tracking
- Helps in resource allocation planning

#### Progress Filter
Track completion status:
- **0-25%**: Projects just getting started
- **26-50%**: Projects in early phases
- **51-75%**: Projects well underway
- **76-100%**: Projects nearing completion

#### Search Filter
Real-time text search:
- Search across project names and descriptions
- Instant results as you type
- Case-insensitive matching

#### Active Filter Management
- **Filter badges**: See which filters are currently active
- **Clear individual**: Click ✕ on any filter badge to remove it
- **Clear all**: Reset all filters with one click
- **Live counter**: See "X of Y projects visible"

### Project Details

#### Hover Tooltips
- Hover over any project bar to see detailed information
- Shows all project stages, dates, and progress
- Non-intrusive overlay that follows mouse

#### Click Modals
- Click on project bars to open detailed modal
- Complete project information display
- Stage-by-stage breakdown with dates and progress
- Easy to close with Escape key or click outside

### Progress Visualization

#### Progress Bars
- Each project stage shows individual completion status
- Subtle background indicates incomplete work
- Clear percentage labels on each stage
- Consistent styling across all templates

#### Stage Indicators
- Color-coded stages by type (Planning: purple, Development: green, etc.)
- Visual progress indicators within each stage
- Clear stage names and durations

## Advanced Usage

### Creating Custom Templates

1. **Start with existing template**
   ```bash
   cp templates/gantt_template.html templates/my_custom_template.html
   ```

2. **Modify styling**
   - Update CSS variables for colors and fonts
   - Adjust layout and spacing
   - Customize hover effects and animations

3. **Test your template**
   ```bash
   python main.py data/sample_projects.csv output/test_custom.html --template templates/my_custom_template.html
   ```

### Batch Processing

Generate multiple charts from different data sources:

```bash
# Script to process multiple files
for file in data/*.csv; do
  filename=$(basename "$file" .csv)
  python main.py "$file" "output/${filename}_chart.html" --template templates/dark_professional_template.html
done
```

### Integration with External Systems

#### Export from Project Management Tools
Many tools can export to CSV format:
- **Jira**: Export issues to CSV, map fields appropriately
- **Asana**: Export project data with custom fields
- **Monday.com**: Export boards with timeline data
- **Excel/Google Sheets**: Direct CSV export

#### Web Integration
Embed generated charts in web applications:

```html
<iframe src="path/to/generated_chart.html" width="100%" height="600px" frameborder="0"></iframe>
```

### Performance Optimization

#### Large Datasets
- Recommended limit: 500 projects for smooth filtering
- For larger datasets, pre-filter data in CSV
- Consider splitting into multiple charts by time period

#### Fast Generation
```bash
# Use specific template instead of generating all
python main.py data/large_file.csv --template templates/modern_minimal_template.html

# Skip standalone generation for faster processing
python main.py data/large_file.csv output/chart.html
```

## Troubleshooting

### Common Issues

#### "File not found" errors
```bash
# Check file paths are correct
ls data/your_file.csv
# Use absolute paths if needed
python main.py /full/path/to/data/your_file.csv
```

#### CSV parsing errors
- Ensure all required columns are present
- Check for special characters in project names (use quotes)
- Validate date formats (YYYY-MM-DD)
- Verify JSON format in stages column for multi-stage projects

#### Charts not displaying properly
- Check browser console for JavaScript errors
- Ensure D3.js loads correctly (check internet connection for non-standalone)
- Verify data contains valid dates and numeric progress values

#### Performance issues
- Reduce number of projects if filtering is slow
- Use simpler templates for large datasets
- Close other browser tabs to free memory

### Data Validation

Check your CSV data:

```bash
# Validate CSV format
python -c "
import pandas as pd
df = pd.read_csv('data/your_file.csv')
print('Columns:', df.columns.tolist())
print('Shape:', df.shape)
print('First few rows:')
print(df.head())
"
```

### Debug Mode

Generate with verbose output:

```bash
python main.py data/your_file.csv --debug
```

## Tips & Best Practices

### Data Organization

#### Project Naming
- **Be descriptive**: "Website Redesign Q1 2024" instead of "Website"
- **Use consistent naming**: Establish naming conventions for your team
- **Keep it concise**: Names under 50 characters display better

#### Category Management
- **Standardize categories**: Use consistent category names across projects
- **Limit categories**: 5-10 categories work best for filtering
- **Use clear names**: "Development" instead of "Dev"

#### Progress Tracking
- **Update regularly**: Keep progress percentages current
- **Be realistic**: Avoid inflating completion percentages
- **Stage-specific**: Update each stage individually for multi-stage projects

### Visual Design

#### Template Selection
- **Match your brand**: Choose templates that align with your organization's style
- **Consider audience**: Use colorful templates for internal teams, minimal for executives
- **Think about usage**: Dark themes for monitoring dashboards, light for presentations

#### Color Coding
- **Consistent priorities**: Always use the same priority levels
- **Meaningful categories**: Ensure category names reflect actual work types
- **Team colors**: Consider assigning colors to teams for quick identification

### Workflow Integration

#### Regular Updates
```bash
# Create update script
#!/bin/bash
echo "Updating project charts..."
python main.py data/current_projects.csv output/current_dashboard.html --template templates/dark_professional_template.html
echo "Charts updated! Open output/current_dashboard.html"
```

#### Automated Generation
Set up scheduled generation:
- **Windows**: Use Task Scheduler
- **macOS/Linux**: Use cron jobs
- **CI/CD**: Integrate into deployment pipelines

#### Sharing Results
- **Static hosting**: Upload HTML files to web server
- **Email reports**: Attach generated charts to status emails  
- **Team dashboards**: Display charts on office monitors
- **Documentation**: Include charts in project documentation

### Performance Tips

#### Optimal Data Size
- **Sweet spot**: 20-100 projects for best performance
- **Quarterly views**: Focus on 3-month periods for detail
- **Annual overviews**: Use broader time ranges for strategy

#### Fast Iteration
- **Start simple**: Begin with legacy format, upgrade to multi-stage as needed
- **Template testing**: Use minimal template for quick testing
- **Mock data**: Use generated data during design phases

### Collaboration

#### Team Standards
- **Data format**: Establish team-wide CSV format standards
- **Update frequency**: Set regular update schedules
- **Template preferences**: Choose preferred templates for different use cases
- **Sharing methods**: Standardize how charts are shared and accessed

#### Version Control
- **Track changes**: Keep CSV files in version control
- **Document updates**: Use commit messages to explain project changes
- **Archive old versions**: Maintain historical project data

---

## Need More Help?

- **Documentation**: Check [API.md](API.md) for technical details
- **Examples**: Look in the `data/` folder for sample files
- **Issues**: Report problems on the project's issue tracker
- **Community**: Join discussions in the project forums

Happy charting! 🎉