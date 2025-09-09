/**
 * CQSS D3.js Common Functionality
 * Shared components and utilities for all Gantt chart templates
 */

(function(window) {
    'use strict';
    
    // D3.js dependency will be checked during initialization
    // This allows the file to load without D3.js being immediately available
    
    /**
     * Common Filter Management
     */
    window.CQSS_FilterManager = {
        currentFilters: {},
        
        /**
         * Initialize filter functionality
         */
        init: function() {
            this.setupFilterEventListeners();
            this.populateFilterOptions();
        },
        
        /**
         * Set up event listeners for all filter controls
         */
        setupFilterEventListeners: function() {
            // Category filter
            const categoryFilter = document.getElementById('categoryFilter');
            if (categoryFilter) {
                categoryFilter.addEventListener('change', () => this.applyFilters());
            }
            
            // Priority filter  
            const priorityFilter = document.getElementById('priorityFilter');
            if (priorityFilter) {
                priorityFilter.addEventListener('change', () => this.applyFilters());
            }
            
            // Team filter
            const teamFilter = document.getElementById('teamFilter');
            if (teamFilter) {
                teamFilter.addEventListener('change', () => this.applyFilters());
            }
            
            // Search filter
            const searchFilter = document.getElementById('searchFilter');
            if (searchFilter) {
                searchFilter.addEventListener('input', () => this.applyFilters());
            }
            
            // Clear filters button
            const clearFiltersBtn = document.getElementById('clearFilters');
            if (clearFiltersBtn) {
                clearFiltersBtn.addEventListener('click', () => this.clearAllFilters());
            }
        },
        
        /**
         * Populate filter dropdown options from data
         */
        populateFilterOptions: function() {
            if (!window.allProjectData) return;
            
            // Get unique values
            const categories = [...new Set(window.allProjectData.map(p => p.category))].sort();
            const priorities = [...new Set(window.allProjectData.map(p => p.priority))].sort();
            const teams = [...new Set(window.allProjectData.map(p => p.team_lead))].sort();
            
            // Populate category filter
            this.populateSelect('categoryFilter', categories, 'All Categories');
            
            // Populate priority filter
            this.populateSelect('priorityFilter', priorities, 'All Priorities');
            
            // Populate team filter
            this.populateSelect('teamFilter', teams, 'All Teams');
        },
        
        /**
         * Helper to populate select elements
         */
        populateSelect: function(elementId, options, defaultText) {
            const select = document.getElementById(elementId);
            if (!select) return;
            
            // Clear existing options except the first (default)
            select.innerHTML = `<option value="">${defaultText}</option>`;
            
            // Add options
            options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option;
                optionElement.textContent = option;
                select.appendChild(optionElement);
            });
        },
        
        /**
         * Apply all filters to the data
         */
        applyFilters: function() {
            if (!window.allProjectData) return;
            
            // Get current filter values
            this.currentFilters = {
                category: document.getElementById('categoryFilter')?.value || '',
                priority: document.getElementById('priorityFilter')?.value || '',
                team: document.getElementById('teamFilter')?.value || '',
                search: document.getElementById('searchFilter')?.value.toLowerCase() || ''
            };
            
            // Filter the data
            window.filteredProjectData = window.allProjectData.filter(project => {
                // Category filter
                if (this.currentFilters.category && project.category !== this.currentFilters.category) {
                    return false;
                }
                
                // Priority filter
                if (this.currentFilters.priority && project.priority !== this.currentFilters.priority) {
                    return false;
                }
                
                // Team filter
                if (this.currentFilters.team && project.team_lead !== this.currentFilters.team) {
                    return false;
                }
                
                // Search filter
                if (this.currentFilters.search) {
                    const searchableText = `${project.project_name} ${project.description}`.toLowerCase();
                    if (!searchableText.includes(this.currentFilters.search)) {
                        return false;
                    }
                }
                
                return true;
            });
            
            // Update filter results count
            this.updateFilterResults();
            
            // Trigger chart re-render
            if (typeof window.renderChart === 'function') {
                window.renderChart();
            }
        },
        
        /**
         * Clear all filters
         */
        clearAllFilters: function() {
            // Reset filter controls
            ['categoryFilter', 'priorityFilter', 'teamFilter', 'searchFilter'].forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    element.value = '';
                }
            });
            
            // Reset filtered data to show all
            window.filteredProjectData = [...window.allProjectData];
            this.currentFilters = {};
            
            // Update display
            this.updateFilterResults();
            
            // Trigger chart re-render
            if (typeof window.renderChart === 'function') {
                window.renderChart();
            }
        },
        
        /**
         * Update the filter results counter
         */
        updateFilterResults: function() {
            const resultsElement = document.getElementById('filterResults');
            if (resultsElement && window.filteredProjectData && window.allProjectData) {
                const visibleCount = window.filteredProjectData.length;
                const totalCount = window.allProjectData.length;
                resultsElement.textContent = `${visibleCount} of ${totalCount} projects visible`;
            }
        }
    };
    
    /**
     * Common Modal Management
     */
    window.CQSS_ModalManager = {
        currentModal: null,
        
        /**
         * Initialize modal functionality
         */
        init: function() {
            this.setupModalEventListeners();
        },
        
        /**
         * Set up modal event listeners
         */
        setupModalEventListeners: function() {
            // Close modal when clicking outside
            document.addEventListener('click', (event) => {
                if (event.target.classList.contains('modal') && this.currentModal) {
                    this.closeModal();
                }
            });
            
            // Close modal with escape key
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Escape' && this.currentModal) {
                    this.closeModal();
                }
            });
            
            // Close button
            document.addEventListener('click', (event) => {
                if (event.target.classList.contains('modal-close')) {
                    this.closeModal();
                }
            });
        },
        
        /**
         * Show project details modal
         */
        showProjectModal: function(project) {
            const modal = document.getElementById('projectModal');
            if (!modal) return;
            
            // Populate modal content
            document.getElementById('modal-project-name').textContent = project.project_name || 'Unknown Project';
            document.getElementById('modal-category').textContent = project.category || 'N/A';
            document.getElementById('modal-priority').textContent = project.priority || 'N/A';
            document.getElementById('modal-team').textContent = project.team_lead || 'N/A';
            document.getElementById('modal-progress').textContent = `${project.progress_percent || 0}%`;
            document.getElementById('modal-description').textContent = project.description || 'No description available';
            
            // Show stages if available
            if (project.stages && project.stages.length > 0) {
                const stagesContainer = document.getElementById('modal-stages');
                if (stagesContainer) {
                    stagesContainer.innerHTML = '';
                    project.stages.forEach(stage => {
                        const stageDiv = document.createElement('div');
                        stageDiv.className = 'modal-stage';
                        stageDiv.innerHTML = `
                            <strong>${stage.name}</strong><br>
                            ${stage.start} to ${stage.end}<br>
                            Progress: ${stage.progress || 0}%
                            ${stage.status ? `<br>Status: ${stage.status}` : ''}
                        `;
                        stagesContainer.appendChild(stageDiv);
                    });
                }
            }
            
            // Show modal
            modal.style.display = 'flex';
            this.currentModal = modal;
        },
        
        /**
         * Close current modal
         */
        closeModal: function() {
            if (this.currentModal) {
                this.currentModal.style.display = 'none';
                this.currentModal = null;
            }
        }
    };
    
    /**
     * Common Chart Utilities
     */
    window.CQSS_ChartUtils = {
        /**
         * Get color for priority level
         */
        getPriorityColor: function(priority) {
            const colors = {
                'Critical': '#ff4444',
                'High': '#ff8800',
                'Medium': '#4CAF50',
                'Low': '#2196F3'
            };
            return colors[priority] || '#666666';
        },
        
        /**
         * Get color for project status
         */
        getStatusColor: function(status) {
            const colors = {
                'critical': '#ff4444',
                'warning': '#ff9800',
                'delayed': '#ff5722',
                'completed': '#4CAF50',
                'normal': '#2196F3'
            };
            return colors[status] || '#2196F3';
        },
        
        /**
         * Format date for display
         */
        formatDate: function(dateString) {
            if (!dateString) return 'N/A';
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
        },
        
        /**
         * Calculate days between dates
         */
        daysBetween: function(start, end) {
            const startDate = new Date(start);
            const endDate = new Date(end);
            return Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
        },
        
        /**
         * Get project status based on dates and progress
         */
        getProjectStatus: function(project) {
            const now = new Date();
            const endDate = new Date(project.execution_end || project.end_date);
            const progress = project.progress_percent || 0;
            
            if (progress >= 100) return 'Completed';
            if (now > endDate) return 'Overdue';
            if (progress > 0) return 'In Progress';
            return 'Not Started';
        },
        
        /**
         * Create loading indicator
         */
        showLoadingIndicator: function(container) {
            const loading = document.createElement('div');
            loading.className = 'cqss-loading-chart';
            loading.innerHTML = `
                <div style="text-align: center; padding: 50px;">
                    <div style="font-size: 18px; margin-bottom: 20px;">Loading chart...</div>
                    <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                </div>
                <style>
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                </style>
            `;
            container.appendChild(loading);
            return loading;
        },
        
        /**
         * Remove loading indicator
         */
        hideLoadingIndicator: function(container) {
            const loading = container.querySelector('.cqss-loading-chart');
            if (loading) {
                loading.remove();
            }
        }
    };
    
    /**
     * Initialize all common functionality
     */
    window.CQSS_InitCommon = function() {
        // Ensure D3.js is loaded before initializing
        if (typeof window.d3 === 'undefined') {
            console.error('D3.js is required for CQSS common functionality');
            throw new Error('D3.js must be loaded before initializing common functionality');
        }
        
        CQSS_FilterManager.init();
        CQSS_ModalManager.init();
        
        console.log('CQSS Common functionality initialized');
    };
    
})(window);