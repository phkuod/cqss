# CQSS Gantt Chart Generator

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Refactored](https://img.shields.io/badge/refactored-✨clean_architecture-green.svg)

**A powerful Python-based tool for generating interactive Gantt charts from CSV project data**

🚀 **v2.0 Major Refactoring**: 90% less code duplication, unified API, dependency injection architecture

[Features](#-features) • [Quick Start](#-quick-start) • [Templates](#-visual-templates) • [Documentation](#-documentation) • [Examples](#-examples)

</div>

## ✨ Features

### 🎨 **6 Beautiful Visual Templates**
- **Default Design**: Classic, professional Gantt chart
- **Modern Minimal**: Clean, ultra-minimalist design
- **Dark Professional**: Sleek dark theme for modern interfaces
- **Colorful Friendly**: Vibrant, approachable design with emojis
- **Interactive Modern**: Advanced interactions and hover effects
- **Frappe-inspired**: Clean, GitHub-style aesthetic

### 🔧 **Advanced Functionality**
- **Multi-Stage Projects**: Support for 2-10+ project stages with individual progress tracking
- **Smart Filtering**: Filter by priority, category, team, progress ranges, and search
- **Enhanced Timeline**: Auto-scroll to today, smooth scrolling with visual indicators
- **Progress Visualization**: Consistent, subtle progress bars across all templates
- **Mock Data Generation**: Create realistic test data for development and demos
- **Static HTML Output**: No web server required - just open in any browser

### 📊 **Project Management Features**
- **Two-Stage Compatibility**: Seamless support for legacy Preparing + Execution workflow
- **Priority-Based Coloring**: Visual priority levels (Critical, High, Medium, Low)
- **Interactive Tooltips**: Detailed project information on hover/click
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Today Line**: Always know where you are in the timeline

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cqss-system.git
   cd cqss-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Generate Your First Chart (v2.0 API)

```bash
# Simple generation with new clean API
python main_v2.py data/sample_projects.csv

# Choose your style
python main_v2.py data/sample_projects.csv --template dark

# Generate all templates at once
python main_v2.py data/sample_projects.csv --all-templates --open
```

**Or use the simple Python API:**
```python
from src.services import generate_chart

generate_chart('data/projects.csv', 'output/chart.html', 'colorful')
```

Open any of the generated files in `output/` to see your Gantt chart!

## 🎯 Usage

### Basic Usage

```bash
# Generate default template
python main.py data/sample_projects.csv

# Generate specific template
python main.py data/sample_projects.csv output/my_chart.html --template templates/dark_professional_template.html

# Generate all 6 templates at once
python generate_all_styles.py
```

### Advanced Options

```bash
# Generate standalone version (no internet required)
python main.py data/sample_projects.csv --standalone

# Generate with specific template and output
python main.py data/sample_projects.csv output/dark_chart.html --template templates/dark_professional_template.html

# Generate mock data for testing
python generate_mock_data.py --projects 30 --output data/my_test_data.csv
```

## 🎨 Visual Templates

| Template | File | Description | Best For |
|----------|------|-------------|----------|
| **Default** | `1_default_design.html` | Classic professional design | Corporate presentations, formal reports |
| **Minimal** | `2_minimal_design.html` | Ultra-clean, distraction-free | Focus on data, minimal interfaces |
| **Dark** | `3_dark_design.html` | Modern dark theme | Dark mode environments, developer tools |
| **Colorful** | `4_colorful_design.html` | Vibrant, friendly with emojis | Team dashboards, creative projects |
| **Interactive** | `5_interactive_design.html` | Advanced hover effects | Interactive dashboards, demos |
| **Frappe** | `6_frappe_design.html` | GitHub-inspired clean design | Development projects, technical docs |

## 📋 CSV Data Format

### Multi-Stage Format (Recommended)
```csv
project_name,category,priority,description,team_lead,stages
Project Alpha,Security,High,Multi-phase auth system,John Smith,"[{""name"":""Planning"",""start"":""2024-01-15"",""end"":""2024-02-15"",""progress"":100},{""name"":""Development"",""start"":""2024-02-15"",""end"":""2024-04-15"",""progress"":75}]"
```

### Legacy Format (Still Supported)
```csv
project_name,category,priority,preparing_start,preparing_end,execution_end,progress_percent,description,team_lead
Project Beta,Marketing,Medium,2024-01-01,2024-02-01,2024-04-01,60,Campaign launch,Jane Doe
```

### Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| `project_name` | Name of the project | "Website Redesign" |
| `category` | Project category | "Development" |
| `priority` | Priority level | "High" (Critical/High/Medium/Low) |
| `description` | Brief description | "Redesign company website" |
| `team_lead` | Responsible person | "Alice Johnson" |

**Multi-stage**: Use `stages` column with JSON array  
**Legacy**: Use `preparing_start`, `preparing_end`, `execution_end`, `progress_percent`

## 🛠️ Project Structure

```
cqss-system/
├── 📁 data/                     # CSV data files
│   ├── sample_projects.csv      # Legacy format example
│   ├── demo_multistage_projects.csv # Multi-stage example
│   └── mock_three_months.csv    # Generated test data
├── 📁 src/                      # Core source code
│   ├── data_processor.py        # CSV processing & validation
│   └── gantt_generator.py       # HTML generation engine
├── 📁 templates/                # HTML template files
│   ├── gantt_template.html      # Default template
│   ├── modern_minimal_template.html
│   ├── dark_professional_template.html
│   ├── colorful_friendly_template.html
│   ├── interactive_modern_template.html
│   └── frappe_gantt_template.html
├── 📁 output/                   # Generated HTML files
│   ├── 1_default_design.html
│   ├── 2_minimal_design.html
│   ├── 3_dark_design.html
│   ├── 4_colorful_design.html
│   ├── 5_interactive_design.html
│   └── 6_frappe_design.html
├── 📄 main.py                   # Primary CLI interface
├── 📄 generate.py               # Quick generation script
├── 📄 generate_mock_data.py     # Mock data generator
└── 📄 requirements.txt          # Python dependencies
```

## 🎯 Examples

### Example 1: Basic Project Timeline
```bash
# Create a simple 2-stage project chart
python main.py data/sample_projects.csv output/simple.html
```

### Example 2: Complex Multi-Stage Project
```bash
# Generate comprehensive multi-stage visualization
python main.py data/demo_multistage_projects.csv output/complex.html --template templates/interactive_modern_template.html
```

### Example 3: Dark Theme Dashboard
```bash
# Perfect for monitoring dashboards
python main.py data/mock_three_months.csv output/dashboard.html --template templates/dark_professional_template.html
```

## 🔍 Advanced Features

### Smart Filtering
- **Priority Filter**: Critical, High, Medium, Low
- **Category Filter**: Filter by project type
- **Team Filter**: Filter by team lead
- **Progress Filter**: 0-25%, 26-50%, 51-75%, 76-100%
- **Search**: Real-time text search across project names

### Timeline Navigation
- **Auto-scroll to Today**: Page centers on current date automatically
- **Today Button**: Manual navigation to current date
- **Smooth Scrolling**: Enhanced scroll experience with visual indicators
- **Keyboard Navigation**: Arrow keys for easy navigation

### Progress Visualization
- **Consistent Styling**: Unified progress bar appearance across all templates
- **Stage-Specific Progress**: Each stage shows individual completion status
- **Real-time Updates**: Progress bars reflect current project status

## 📚 Documentation

- [**API_v2.md**](API_v2.md) - Complete API reference for v2.0
- [**USER_GUIDE_v2.md**](USER_GUIDE_v2.md) - Comprehensive user guide
- [**CHANGELOG.md**](CHANGELOG.md) - Version history and updates
- [**CLAUDE.md**](CLAUDE.md) - Development guidelines and project instructions

### v2.0 Architecture Benefits

- **90% Less Code Duplication**: Templates share common `gantt-core.js` library
- **Dependency Injection**: Easy testing and component swapping
- **Protocol-Based Design**: Clean interfaces for extensibility
- **Unified Data Model**: No more legacy vs modern format confusion
- **Service Layer**: Proper separation of concerns
- **Comprehensive Testing**: Built-in mocks and performance benchmarks

## 🤝 Contributing

We welcome contributions! Please see our development guidelines in [CLAUDE.md](CLAUDE.md) for:
- Code style and conventions
- Development workflow
- Testing requirements
- Feature implementation process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [Report bugs or request features](https://github.com/yourusername/cqss-system/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/yourusername/cqss-system/discussions)
- **Documentation**: Check our [project documentation](CLAUDE.md)

---

<div align="center">

**Made with ❤️ by the CQSS Development Team**

[⭐ Star this project](https://github.com/yourusername/cqss-system) if you find it useful!

</div>