# Changelog

All notable changes to the CQSS Gantt Chart Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-08-22

### Added
- **6 Visual Templates**: Complete redesign with 6 distinct Gantt chart templates
  - Default Design (1_default_design.html)
  - Modern Minimal (2_minimal_design.html)  
  - Dark Professional (3_dark_design.html)
  - Colorful Friendly (4_colorful_design.html)
  - Interactive Modern (5_interactive_design.html)
  - Frappe-inspired (6_frappe_design.html)
- **Multi-Stage Project Support**: Projects can now have 2-10+ stages with individual progress tracking
- **Enhanced Filtering System**: Filter by priority, category, team, and progress ranges
- **Improved Progress Visualization**: Lighter, more consistent progress bar backgrounds across all templates
- **Advanced Timeline Features**:
  - Enhanced timeline header scrolling with visual indicators
  - Auto-scroll to today's date on page load
  - Smooth scroll animations and navigation hints
- **Mock Data Generation**: Generate realistic 3-month project data for testing
- **Template Update System**: Automated script to update all templates with new features

### Changed
- **Progress Bar Styling**: Updated from `rgba(0,0,0,0.4)` to `rgba(0,0,0,0.2)` for better visibility
- **Template Architecture**: Migrated from single template to 6 specialized designs
- **Data Processing**: Enhanced to support both legacy 2-stage and new multi-stage formats
- **Filter UI**: Redesigned filter controls with active filter badges and clear functionality

### Fixed
- **Timeline Header Scrolling**: Fixed synchronization issues across all templates
- **Filter Functionality**: Resolved content accumulation and infinite loop issues
- **Today Line Positioning**: Fixed visual duplication and positioning bugs
- **Template Consistency**: Ensured all 6 templates have consistent behavior and styling

### Technical Improvements
- Backward compatibility maintained for existing CSV formats
- Improved error handling and validation
- Enhanced code organization and documentation
- Added comprehensive testing coverage for all templates

## [1.0.0] - Previous Release

### Added
- Basic Gantt chart generation from CSV data
- Two-stage project visualization (Preparing + Execution)
- Priority-based color coding
- Interactive tooltips and click handlers
- Static HTML output with D3.js visualization
- Responsive design for different screen sizes

### Features
- CSV data import and validation
- Progress tracking with visual progress bars
- Hover tooltips with project details
- Priority levels: Critical, High, Medium, Low
- Standalone HTML generation (no server required)