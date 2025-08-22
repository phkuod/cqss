#!/usr/bin/env python3
"""
Script to update all remaining Gantt chart templates for multi-stage support
while maintaining backward compatibility with legacy two-stage format.
"""

import re
import os
from pathlib import Path

def update_d3_template(template_path):
    """Update D3.js-based templates (like gantt_template.html)"""
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace hardcoded stage rendering with dynamic multi-stage support
    old_stage_pattern = r'// Add preparing stage bars[\s\S]*?\.style\(\'cursor\', \'pointer\'\)'
    new_stage_code = '''// Define stage colors for multi-stage support
        const stageColors = {
            'Planning': '#6f42c1',
            'Preparing': '#6f42c1', 
            'Analysis': '#17a2b8',
            'Research': '#17a2b8',
            'Design': '#20c997',
            'Wireframes': '#20c997',
            'Development': '#28a745',
            'Implementation': '#28a745',
            'Testing': '#ffc107',
            'Audit': '#ffc107',
            'Migration': '#fd7e14',
            'Deployment': '#dc3545',
            'Execution': '#007bff'
        };
        
        // Add stage bars dynamically
        projectGroups.each(function(d) {
            const group = d3.select(this);
            
            d.stages.forEach((stage, index) => {
                const isLastStage = index === d.stages.length - 1;
                const stageColor = stageColors[stage.name] || (index === 0 ? '#6f42c1' : priorityColors[d.priority] || '#6c757d');
                
                // Add stage background bar
                group.append('rect')
                    .attr('class', `stage-bar stage-${index}`)
                    .attr('x', xScale(parseTime(stage.start)))
                    .attr('y', (yScale.bandwidth() - barHeight) / 2)
                    .attr('width', xScale(parseTime(stage.end)) - xScale(parseTime(stage.start)))
                    .attr('height', barHeight)
                    .attr('fill', stageColor)
                    .attr('opacity', stage.progress_percent === 100 ? 0.8 : 0.3);
                
                // Add progress bar for stages with partial progress
                if (stage.progress_percent < 100 && stage.progress_percent > 0) {
                    group.append('rect')
                        .attr('class', `progress-bar stage-${index}`)
                        .attr('x', xScale(parseTime(stage.start)))
                        .attr('y', (yScale.bandwidth() - barHeight) / 2)
                        .attr('width', (xScale(parseTime(stage.end)) - xScale(parseTime(stage.start))) * (stage.progress_percent / 100))
                        .attr('height', barHeight)
                        .attr('fill', stageColor);
                }
            });
        });
        
        // Add interactive overlays for each project
        projectGroups.append('rect')
            .attr('class', 'interaction-overlay')
            .attr('x', d => xScale(parseTime(d.stages[0].start)))
            .attr('y', (yScale.bandwidth() - barHeight) / 2)
            .attr('width', d => xScale(parseTime(d.stages[d.stages.length - 1].end)) - xScale(parseTime(d.stages[0].start)))
            .attr('height', barHeight)
            .attr('fill', 'transparent')
            .style('cursor', 'pointer')'''
    
    content = re.sub(old_stage_pattern, new_stage_code, content, flags=re.DOTALL)
    
    # Update tooltip content for multi-stage
    old_tooltip_pattern = r'\.html\(`[\s\S]*?d\.execution_stage\.end\.split.*?\`\);'
    new_tooltip_code = '''.html(`
                        <div class="tooltip-title">${d.name}</div>
                        <div class="tooltip-item"><strong>Category:</strong> ${d.category}</div>
                        <div class="tooltip-item"><strong>Priority:</strong> ${d.priority}</div>
                        <div class="tooltip-item"><strong>Team Lead:</strong> ${d.team_lead}</div>
                        <div class="tooltip-item"><strong>Overall Progress:</strong> ${d.execution_stage.progress_percent}%</div>
                        <div class="tooltip-item"><strong>Description:</strong> ${d.description}</div>
                        <div class="tooltip-section"><strong>Stages:</strong></div>
                        ${d.stages.map(stage => 
                            '<div class="tooltip-item"><strong>' + stage.name + ':</strong> ' + stage.start.split('T')[0] + ' to ' + stage.end.split('T')[0] + ' (' + stage.progress_percent + '%)</div>'
                        ).join('')}
                    `);'''
    
    content = re.sub(old_tooltip_pattern, new_tooltip_code, content, flags=re.DOTALL)
    
    # Update project name positioning for multi-stage
    old_name_pattern = r'// Add project names to execution bars[\s\S]*?d\.name\.substring.*?\);'
    new_name_code = '''// Add project names centered across all stages
        projectGroups.append('text')
            .attr('x', d => {
                const startX = xScale(parseTime(d.stages[0].start));
                const endX = xScale(parseTime(d.stages[d.stages.length - 1].end));
                return startX + (endX - startX) / 2;
            })
            .attr('y', (yScale.bandwidth() - barHeight) / 2 + barHeight / 2 - 4)
            .attr('dy', '0.35em')
            .attr('text-anchor', 'middle')
            .style('font-size', '13px')
            .style('font-weight', 'bold')
            .style('fill', 'white')
            .style('text-shadow', '1px 1px 3px rgba(0,0,0,0.9)')
            .text(d => {
                const totalBarWidth = xScale(parseTime(d.stages[d.stages.length - 1].end)) - xScale(parseTime(d.stages[0].start));
                const maxChars = Math.floor(totalBarWidth / 8); // Estimate characters that fit
                return d.name.length > maxChars && maxChars > 3 ? 
                    d.name.substring(0, maxChars - 3) + '...' : d.name;
            });'''
    
    content = re.sub(old_name_pattern, new_name_code, content, flags=re.DOTALL)
    
    # Update progress labels for multi-stage
    old_progress_pattern = r'// Add progress percentage labels at end[\s\S]*?d\.execution_stage\.progress_percent.*?\);'
    new_progress_code = '''// Add stage progress labels for each stage
        projectGroups.each(function(d) {
            const group = d3.select(this);
            
            d.stages.forEach((stage, index) => {
                if (stage.progress_percent > 0 && stage.progress_percent < 100) {
                    const stageWidth = xScale(parseTime(stage.end)) - xScale(parseTime(stage.start));
                    const progressWidth = stageWidth * (stage.progress_percent / 100);
                    
                    if (progressWidth > 25) { // Only show if there's enough space
                        group.append('text')
                            .attr('x', xScale(parseTime(stage.start)) + progressWidth + 3)
                            .attr('y', (yScale.bandwidth() - barHeight) / 2 + barHeight / 2)
                            .attr('dy', '0.35em')
                            .attr('text-anchor', 'start')
                            .style('font-size', '10px')
                            .style('font-weight', 'bold')
                            .style('fill', '#343a40')
                            .style('text-shadow', '1px 1px 2px rgba(255,255,255,0.8)')
                            .text(`${stage.progress_percent}%`);
                    }
                }
            });
        });'''
    
    content = re.sub(old_progress_pattern, new_progress_code, content, flags=re.DOTALL)
    
    return content

def update_templates():
    """Update all templates for multi-stage support"""
    
    templates_dir = Path('templates')
    templates_to_update = [
        'dark_professional_template.html',
        'colorful_friendly_template.html', 
        'interactive_modern_template.html',
        'frappe_gantt_template.html'
    ]
    
    for template_name in templates_to_update:
        template_path = templates_dir / template_name
        if not template_path.exists():
            print(f"Template not found: {template_path}")
            continue
            
        print(f"Updating {template_name}...")
        
        try:
            # Read original content
            with open(template_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Create backup
            backup_path = template_path.with_suffix('.html.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Update for multi-stage support
            updated_content = update_d3_template(template_path)
            
            # Write updated content
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated {template_name} (backup saved as {backup_path.name})")
            
        except Exception as e:
            print(f"Error updating {template_name}: {str(e)}")
            continue

if __name__ == "__main__":
    print("Updating Gantt chart templates for multi-stage support...")
    update_templates()
    print("\nTemplate updates completed!")
    print("\nTo test the updates, run:")
    print("python main.py data/sample_multistage_projects.csv output/test_multistage_all.html --template templates/dark_professional_template.html")