# Auto-Browser Opening Feature

The CQSS Gantt Chart Generator now supports automatically opening the generated charts in your default web browser.

## Usage Options

### Option 1: Quick Generation (Auto-opens by default)
```bash
python generate.py
```
This will:
- Generate a Gantt chart from `data/extended_projects.csv`
- Save it to `output/gantt_chart.html`
- **Automatically open it in your default browser**

### Option 2: Main Script with `--open` flag
```bash
python main.py data/sample_projects.csv --open
python main.py data/sample_projects.csv --style interactive --open
python main.py data/sample_projects.csv output/my_chart.html --style frappe --open
```

## Examples

### Auto-open different styles:
```bash
# Generate and auto-open frappe style
python main.py data/extended_projects.csv --style frappe --open

# Generate and auto-open interactive style with filters
python main.py data/extended_projects.csv --style interactive --open

# Generate and auto-open clean modern style
python main.py data/extended_projects.csv --style minimal --open

# Generate and auto-open dark theme
python main.py data/extended_projects.csv --style dark --open
```

### Quick development workflow:
```bash
# Quick iteration - always opens in browser
python generate.py

# Test with different data
python generate.py data/current_projects.csv
```

## Technical Details

- Uses Python's `webbrowser` module for cross-platform browser opening
- Handles Windows file path conversion properly (`file:///` protocol)
- Graceful error handling if browser opening fails
- Works with all chart styles and templates

## Benefits

- **Faster development**: No need to manually navigate and open files
- **Immediate feedback**: See your changes instantly
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Fallback graceful**: If browser opening fails, you still get the file path

## Current Date Feature

All generated charts now show:
- **Current date line**: Blue vertical line marking today's position
- **Date marker**: Shows "Today YYYY/MM/DD" format above the timeline
- **Proper positioning**: Marker appears above the x-axis header (fixed positioning issue)
- **Consistent across all styles**: Works with all 7 template variations