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

## Development Workflow

### Claude Code Development Process
1. **Create Feature Branch**: Always create a new feature branch from master for any new feature development
   ```bash
   git checkout master
   git pull origin master
   git checkout -b feature/descriptive-feature-name
   ```

2. **Implement & Test**: Develop the feature with proper self-testing
   - Implement the requested functionality
   - Test all scenarios and edge cases
   - Ensure code quality and follows project conventions
   - Verify compatibility across all templates/styles

3. **Commit to Feature Branch**: Commit completed and tested code to the feature branch
   ```bash
   git add .
   git commit -m "feat: descriptive commit message with implementation details"
   git push -u origin feature/descriptive-feature-name
   ```

4. **User Verification**: Wait for user to verify and approve the feature

5. **Create PR**: Only create pull request after user requests it
   ```bash
   gh pr create --title "feat: Feature Title" --body "Detailed description"
   ```

### Important Notes
- **NEVER** commit directly to master branch
- **ALWAYS** create a new feature branch for each enhancement
- **ONLY** create PR when explicitly requested by user after verification
- Self-test thoroughly before committing
- Use descriptive branch names (e.g., `feature/export-pdf`, `feature/mobile-responsive`)
- **MAINTAIN** existing output file names when implementing new features:
  - `1_default_design.html` - Classic Gantt chart design
  - `2_minimal_design.html` - Ultra-clean minimal design  
  - `3_dark_design.html` - Professional dark theme
  - `4_colorful_design.html` - Vibrant, friendly design
  - `5_interactive_design.html` - Modern interactive design
  - `6_frappe_design.html` - Clean, modern Frappe-inspired design

## Memory Logs

- Memorized the commit code flow to understand project enhancement and versioning process