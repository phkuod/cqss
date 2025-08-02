# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CQSS (Cyber Query Security System) is a Gantt Chart Generator that creates interactive project timeline visualizations from CSV data. The system generates static HTML files with D3.js-powered Gantt charts that can be viewed without a web server.

## Development Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Test with sample data:
```bash
python main.py data/sample_projects.csv output/test_chart.html
```

## Architecture

### Core Components

- **`src/data_processor.py`**: CSV processing, validation, and data transformation for D3.js
- **`src/gantt_generator.py`**: HTML generation using Jinja2 templates and processed data
- **`templates/gantt_template.html`**: D3.js-based interactive Gantt chart template
- **`main.py`**: CLI entry point with argument parsing

### Data Flow

1. CSV → pandas DataFrame → validation
2. DataFrame → JSON format for D3.js consumption
3. JSON + HTML template → static HTML file with embedded data
4. D3.js renders interactive Gantt chart in browser

### Key Features

- Two-stage project visualization (preparing + execution stages)
- Progress tracking with visual progress bars
- Priority-based color coding (Critical/High/Medium/Low)
- Interactive tooltips and click handlers for project details
- **Enhanced Timeline Header Scrolling** - Smooth horizontal scrolling with visual indicators
- **Auto-scroll to Today** - Page automatically centers on today's date when loaded
- **Advanced Project Filtering** - Filter by category, priority, team, and search text
- **Mock Data Generation** - Generate realistic 3-month project data for testing

## Common Commands

```bash
# Quick generation with mock data (includes all new features)
python generate.py

# Generate mock data for testing (3-month range around today)
python generate_mock_data.py --projects 30 --output data/mock_projects.csv

# Quick generation with standalone version
python generate.py --standalone

# Advanced usage with custom output and specific template
python main.py data/mock_three_months.csv output/custom.html --template templates/modern_minimal_template.html

# Generate Gantt chart from CSV (uses defaults)
python main.py data/sample_projects.csv

# Run data processor directly (for testing)
cd src && python data_processor.py

# Run generator directly (for testing)  
cd src && python gantt_generator.py
```

## CSV Data Requirements

Required columns: project_name, category, priority, preparing_start, preparing_end, execution_end, progress_percent, description, team_lead

Date format: YYYY-MM-DD
Progress: 0-100 integer
Priority: Critical, High, Medium, Low

## New Features (Latest Update)

### 1. Mock Data Generation
Generate realistic project data spanning 3 months around today's date:
```bash
python generate_mock_data.py --projects 25 --output data/mock_projects.csv
```
- Generates diverse project categories (Software Development, Marketing Campaign, Product Launch, Infrastructure, Research & Analysis)
- Realistic team assignments and priorities
- Progress calculations based on current date
- Unique project names with industry-relevant terminology

### 2. Auto-scroll to Today
- Page automatically scrolls to center today's date when loaded
- Smooth scroll animations with visual feedback
- "📅 Today" button for manual navigation
- Respects timeline boundaries and handles edge cases

### 3. Advanced Project Filtering
Interactive filter controls for:
- **Category Filter**: Dropdown with all available project categories
- **Priority Filter**: Critical, High, Medium, Low priority levels
- **Team Filter**: Dropdown with all team leads from the data
- **Search Filter**: Real-time text search across project names and descriptions
- **Clear All**: Reset all filters with one click
- **Live Results**: Shows "X of Y projects visible" counter

### 4. Enhanced Timeline Header Scrolling
- **Synchronized Scrolling**: Header and content scroll together perfectly
- **Visual Scroll Indicators**: Fade effects on left/right edges when more content is available
- **Modern Scrollbar Styling**: Thin, custom-colored scrollbars for professional appearance
- **Touch-friendly**: Optimized for mobile and tablet scrolling
- **Smart Hints**: Scroll hints that fade after first user interaction

### After Any Enhancement
1. **Create Feature Branch**: Create feature branch from master (e.g., `feature/add-filtering`, `feature/export-pdf`)
2. **Commit Changes**: Create descriptive commit messages
3. **Push Feature Branch**: Push changes to remote feature branch
4. **Create PR**: Create pull request from feature branch to master

## Memory Logs

- Memorized the commit code flow to understand project enhancement and versioning process