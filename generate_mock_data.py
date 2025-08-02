#!/usr/bin/env python3
"""
Mock Data Generator for CQSS Gantt Chart System
Generates realistic project data spanning 3 months around today's date
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict

def generate_mock_data(num_projects: int = 25, output_file: str = "data/mock_projects.csv") -> None:
    """
    Generate mock project data for 3 months around today's date
    
    Args:
        num_projects: Number of projects to generate
        output_file: Output CSV file path
    """
    
    # Define project categories and their typical characteristics
    categories = {
        "Software Development": {
            "teams": ["DevOps Team", "Frontend Team", "Backend Team", "QA Team", "Mobile Team"],
            "priorities": ["Critical", "High", "Medium"],
            "prep_days": (7, 21),
            "exec_days": (14, 90)
        },
        "Marketing Campaign": {
            "teams": ["Marketing Team", "Content Team", "Design Team", "Social Media Team"],
            "priorities": ["High", "Medium", "Low"],
            "prep_days": (5, 14),
            "exec_days": (10, 60)
        },
        "Product Launch": {
            "teams": ["Product Team", "Engineering Team", "Marketing Team", "Sales Team"],
            "priorities": ["Critical", "High"],
            "prep_days": (14, 30),
            "exec_days": (30, 120)
        },
        "Infrastructure": {
            "teams": ["DevOps Team", "Security Team", "Platform Team", "SRE Team"],
            "priorities": ["Critical", "High", "Medium"],
            "prep_days": (3, 14),
            "exec_days": (7, 45)
        },
        "Research & Analysis": {
            "teams": ["Research Team", "Data Team", "Analytics Team", "Strategy Team"],
            "priorities": ["Medium", "Low"],
            "prep_days": (7, 21),
            "exec_days": (21, 90)
        }
    }
    
    # Project name templates
    project_templates = {
        "Software Development": [
            "API {feature} Implementation", "Mobile App {feature}", "{platform} Integration",
            "Database Migration {version}", "Security {component} Update", "Performance Optimization {area}",
            "User Authentication {system}", "Payment Gateway {integration}", "Microservice {service} Development"
        ],
        "Marketing Campaign": [
            "Q{quarter} {brand} Campaign", "{season} Product Launch", "Social Media {platform} Strategy",
            "Email Marketing {segment}", "Brand Awareness {region}", "Customer Acquisition {channel}",
            "Product Demo {series}", "Influencer Partnership {brand}", "Content Marketing {theme}"
        ],
        "Product Launch": [
            "{product} v{version} Launch", "New Feature {name} Release", "{market} Expansion",
            "Beta Testing {product}", "Go-to-Market {strategy}", "Product Roadmap {quarter}",
            "Customer Onboarding {flow}", "Partnership {partner} Integration"
        ],
        "Infrastructure": [
            "Cloud Migration {service}", "Server Upgrade {environment}", "Monitoring System {tool}",
            "Backup Solution {strategy}", "Network Security {audit}", "CI/CD Pipeline {improvement}",
            "Container Orchestration {platform}", "Database Scaling {solution}"
        ],
        "Research & Analysis": [
            "Market Research {segment}", "Competitor Analysis {quarter}", "User Behavior {study}",
            "Performance Analytics {report}", "Customer Feedback {analysis}", "Trend Analysis {industry}",
            "ROI Assessment {project}", "Strategic Planning {initiative}"
        ]
    }
    
    # Generate base date (today) and 3-month range
    today = datetime.now()
    start_range = today - timedelta(days=30)  # 1 month before today
    end_range = today + timedelta(days=60)    # 2 months after today
    
    projects = []
    used_names = set()
    
    for i in range(num_projects):
        # Select random category
        category = random.choice(list(categories.keys()))
        cat_info = categories[category]
        
        # Generate unique project name
        template = random.choice(project_templates[category])
        replacements = {
            "feature": random.choice(["Dashboard", "Analytics", "Reporting", "Search", "Chat", "Profile"]),
            "platform": random.choice(["AWS", "Azure", "GCP", "Kubernetes", "Docker"]),
            "version": f"{random.randint(1,5)}.{random.randint(0,9)}",
            "quarter": f"Q{random.randint(1,4)}",
            "brand": random.choice(["Premium", "Essential", "Pro", "Enterprise", "Starter"]),
            "season": random.choice(["Spring", "Summer", "Fall", "Winter"]),
            "segment": random.choice(["B2B", "B2C", "Enterprise", "SMB", "Consumer"]),
            "region": random.choice(["APAC", "EMEA", "Americas", "Global", "Regional"]),
            "channel": random.choice(["Digital", "Social", "Email", "Direct", "Partner"]),
            "product": random.choice(["Platform", "Suite", "Engine", "System", "Framework"]),
            "name": random.choice(["Advanced", "Smart", "Automated", "Enhanced", "Unified"]),
            "market": random.choice(["US", "European", "Asian", "Global", "Emerging"]),
            "strategy": random.choice(["Aggressive", "Conservative", "Balanced", "Innovative"]),
            "service": random.choice(["Storage", "Compute", "Network", "Security", "Analytics"]),
            "environment": random.choice(["Production", "Staging", "Development", "Testing"]),
            "tool": random.choice(["Prometheus", "Grafana", "DataDog", "NewRelic", "Splunk"]),
            "improvement": random.choice(["V2", "Enhanced", "Optimized", "Streamlined"]),
            "solution": random.choice(["Horizontal", "Vertical", "Hybrid", "Cloud-Native"]),
            "study": random.choice(["Study", "Research", "Analysis", "Investigation"]),
            "report": random.choice(["Report", "Dashboard", "Insights", "Metrics"]),
            "analysis": random.choice(["Analysis", "Review", "Assessment", "Evaluation"]),
            "industry": random.choice(["Tech", "Finance", "Healthcare", "Retail", "Manufacturing"]),
            "project": random.choice(["Initiative", "Project", "Program", "Campaign"]),
            "initiative": random.choice(["2024", "Strategic", "Digital", "Innovation"]),
            "series": random.choice(["Series", "Collection", "Suite", "Package"]),
            "theme": random.choice(["Q1", "Q2", "Q3", "Q4", "2024", "Annual"]),
            "partner": random.choice(["Strategic", "Technology", "Channel", "Enterprise"]),
            "flow": random.choice(["V2", "Enhanced", "Streamlined", "Automated"]),
            "audit": random.choice(["2024", "Annual", "Quarterly", "Comprehensive"]),
            "component": random.choice(["Framework", "Module", "System", "Infrastructure"]),
            "area": random.choice(["Database", "API", "Frontend", "Backend"]),
            "system": random.choice(["V2", "Enhanced", "Multi-factor", "Enterprise"]),
            "integration": random.choice(["V2", "Enhanced", "Secure", "Modern"])
        }
        
        project_name = template.format(**replacements)
        
        # Ensure unique names
        counter = 1
        original_name = project_name
        while project_name in used_names:
            project_name = f"{original_name} {counter}"
            counter += 1
        used_names.add(project_name)
        
        # Generate dates
        prep_min, prep_max = cat_info["prep_days"]
        exec_min, exec_max = cat_info["exec_days"]
        
        # Random start date within range
        total_range_days = (end_range - start_range).days
        max_project_days = exec_max + prep_max
        
        if total_range_days > max_project_days:
            days_from_start = random.randint(0, total_range_days - max_project_days)
        else:
            days_from_start = random.randint(0, max(1, total_range_days - 30))  # Ensure some overlap
        
        prep_start = start_range + timedelta(days=days_from_start)
        
        # Preparation phase
        prep_duration = random.randint(prep_min, prep_max)
        prep_end = prep_start + timedelta(days=prep_duration)
        
        # Execution phase (starts right after preparation)
        exec_start = prep_end
        exec_duration = random.randint(exec_min, exec_max)
        exec_end = exec_start + timedelta(days=exec_duration)
        
        # Generate realistic progress based on how much time has passed
        if exec_end < today:
            # Project finished - 100% progress
            progress = 100
        elif exec_start > today:
            # Project not started yet - 0% progress
            progress = 0
        else:
            # Project in progress - calculate based on time elapsed
            total_exec_days = (exec_end - exec_start).days
            elapsed_days = (today - exec_start).days
            base_progress = min(95, int((elapsed_days / total_exec_days) * 100))
            # Add some randomness
            progress = max(5, min(95, base_progress + random.randint(-10, 15)))
        
        # Select team and priority
        team_lead = random.choice(cat_info["teams"])
        priority = random.choice(cat_info["priorities"])
        
        # Generate description
        descriptions = [
            f"Strategic {category.lower()} initiative focused on improving operational efficiency and user experience.",
            f"Cross-functional {category.lower()} project aimed at enhancing system capabilities and performance.",
            f"Critical {category.lower()} effort to modernize infrastructure and streamline processes.",
            f"Innovative {category.lower()} solution designed to address key business requirements.",
            f"Comprehensive {category.lower()} project targeting scalability and reliability improvements."
        ]
        
        project = {
            "project_name": project_name,
            "category": category,
            "priority": priority,
            "preparing_start": prep_start.strftime("%Y-%m-%d"),
            "preparing_end": prep_end.strftime("%Y-%m-%d"),
            "execution_end": exec_end.strftime("%Y-%m-%d"),
            "progress_percent": progress,
            "description": random.choice(descriptions),
            "team_lead": team_lead
        }
        
        projects.append(project)
    
    # Sort projects by start date for better visualization
    projects.sort(key=lambda x: x["preparing_start"])
    
    # Write to CSV
    fieldnames = ["project_name", "category", "priority", "preparing_start", "preparing_end", 
                  "execution_end", "progress_percent", "description", "team_lead"]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(projects)
    
    print(f"Generated {len(projects)} mock projects")
    print(f"Date range: {projects[0]['preparing_start']} to {projects[-1]['execution_end']}")
    print(f"Output file: {output_file}")
    
    # Print summary statistics
    category_counts = {}
    priority_counts = {}
    progress_stats = []
    
    for project in projects:
        category_counts[project['category']] = category_counts.get(project['category'], 0) + 1
        priority_counts[project['priority']] = priority_counts.get(project['priority'], 0) + 1
        progress_stats.append(project['progress_percent'])
    
    print(f"\nSummary:")
    print(f"Categories: {dict(category_counts)}")
    print(f"Priorities: {dict(priority_counts)}")
    print(f"Average Progress: {sum(progress_stats)/len(progress_stats):.1f}%")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate mock project data for CQSS Gantt Chart")
    parser.add_argument("--projects", "-p", type=int, default=25, help="Number of projects to generate (default: 25)")
    parser.add_argument("--output", "-o", type=str, default="data/mock_projects.csv", help="Output file path (default: data/mock_projects.csv)")
    
    args = parser.parse_args()
    
    generate_mock_data(args.projects, args.output)