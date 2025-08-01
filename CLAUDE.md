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

## Common Commands

```bash
# Quick generation (same output file each iteration)
python generate.py

# Quick generation with standalone version
python generate.py --standalone

# Advanced usage with custom output
python main.py data/sample_projects.csv output/custom.html

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

### After Any Enhancement
1. **Create Feature Branch**: Create feature branch from master (e.g., `feature/add-filtering`, `feature/export-pdf`)
2. **Commit Changes**: Create descriptive commit messages
3. **Push Feature Branch**: Push changes to remote feature branch
4. **Create PR**: Create pull request from feature branch to master

## Memory Logs

- Memorized the commit code flow to understand project enhancement and versioning process