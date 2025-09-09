/**
 * CQSS Configuration Management
 * Central configuration for paths, versions, and environment settings
 */

window.CQSS_CONFIG = {
    // Library paths and versions
    libraries: {
        d3: {
            version: 'v7',
            localPath: '../static/js/d3.v7.min.js',
            cdnPath: 'https://d3js.org/d3.v7.min.js',
            fallbackPath: null
        }
    },
    
    // Environment settings
    environment: {
        mode: 'local', // 'local', 'cdn', 'auto'
        offline: true,
        debug: false
    },
    
    // Loading configuration
    loading: {
        timeout: 10000, // 10 seconds
        retryAttempts: 2,
        retryDelay: 1000, // 1 second
        showLoadingIndicator: true
    },
    
    // Error messages
    messages: {
        d3LoadError: 'Failed to load D3.js visualization library. Please ensure the file is accessible.',
        d3Timeout: 'D3.js library loading timed out. Please check the file location.',
        offlineMode: 'Running in offline mode. All resources are loaded locally.',
        noFallback: 'No fallback option available. Please check your configuration.'
    },
    
    // UI settings
    ui: {
        showLoadingSpinner: true,
        errorDisplayDuration: 5000, // 5 seconds
        loadingIndicatorClass: 'cqss-loading',
        errorClass: 'cqss-error'
    }
};