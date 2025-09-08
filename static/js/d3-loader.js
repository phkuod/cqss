/**
 * CQSS D3.js Loader Module
 * Centralized D3.js loading with consistent error handling and user experience
 */

(function(window) {
    'use strict';
    
    // Ensure config is available
    if (!window.CQSS_CONFIG) {
        console.error('CQSS_CONFIG not found. Please include config.js before d3-loader.js');
        return;
    }
    
    const config = window.CQSS_CONFIG;
    
    /**
     * D3.js Loader Class
     */
    class D3Loader {
        constructor() {
            this.loaded = false;
            this.loading = false;
            this.error = null;
            this.callbacks = [];
            this.retryCount = 0;
        }
        
        /**
         * Load D3.js library with promise-based API
         * @returns {Promise} Resolves when D3.js is loaded
         */
        load() {
            return new Promise((resolve, reject) => {
                // Already loaded
                if (this.loaded && typeof window.d3 !== 'undefined') {
                    resolve(window.d3);
                    return;
                }
                
                // Already failed
                if (this.error) {
                    reject(this.error);
                    return;
                }
                
                // Currently loading
                if (this.loading) {
                    this.callbacks.push({ resolve, reject });
                    return;
                }
                
                this.callbacks.push({ resolve, reject });
                this._loadLibrary();
            });
        }
        
        /**
         * Internal method to load the library
         */
        _loadLibrary() {
            this.loading = true;
            this.error = null;
            
            // Show loading indicator
            if (config.ui.showLoadingSpinner) {
                this._showLoadingIndicator();
            }
            
            const script = document.createElement('script');
            script.src = this._getLibraryPath();
            script.async = false;
            
            // Set up timeout
            const timeoutId = setTimeout(() => {
                this._handleError(new Error(config.messages.d3Timeout));
            }, config.loading.timeout);
            
            script.onload = () => {
                clearTimeout(timeoutId);
                this._handleSuccess();
            };
            
            script.onerror = () => {
                clearTimeout(timeoutId);
                this._handleLoadError();
            };
            
            document.head.appendChild(script);
        }
        
        /**
         * Get the appropriate library path based on configuration
         */
        _getLibraryPath() {
            const d3Config = config.libraries.d3;
            
            switch (config.environment.mode) {
                case 'local':
                    return d3Config.localPath;
                case 'cdn':
                    return d3Config.cdnPath;
                case 'auto':
                    return config.environment.offline ? d3Config.localPath : d3Config.cdnPath;
                default:
                    return d3Config.localPath;
            }
        }
        
        /**
         * Handle successful loading
         */
        _handleSuccess() {
            this.loading = false;
            this.loaded = true;
            this._hideLoadingIndicator();
            
            // Verify D3.js is actually available
            if (typeof window.d3 === 'undefined') {
                this._handleError(new Error('D3.js loaded but not available in global scope'));
                return;
            }
            
            // Resolve all pending callbacks
            this.callbacks.forEach(({ resolve }) => {
                resolve(window.d3);
            });
            this.callbacks = [];
            
            // Dispatch custom event
            window.dispatchEvent(new CustomEvent('d3Loaded', { 
                detail: { d3: window.d3 } 
            }));
            
            if (config.environment.debug) {
                console.log('D3.js loaded successfully:', window.d3.version);
            }
        }
        
        /**
         * Handle loading errors with retry logic
         */
        _handleLoadError() {
            if (this.retryCount < config.loading.retryAttempts) {
                this.retryCount++;
                if (config.environment.debug) {
                    console.log(`Retrying D3.js load (attempt ${this.retryCount}/${config.loading.retryAttempts})`);
                }
                
                setTimeout(() => {
                    this.loading = false;
                    this._loadLibrary();
                }, config.loading.retryDelay);
                return;
            }
            
            this._handleError(new Error(config.messages.d3LoadError));
        }
        
        /**
         * Handle terminal errors
         */
        _handleError(error) {
            this.loading = false;
            this.error = error;
            this._hideLoadingIndicator();
            
            // Show error message to user
            this._showErrorMessage(error.message);
            
            // Reject all pending callbacks
            this.callbacks.forEach(({ reject }) => {
                reject(error);
            });
            this.callbacks = [];
            
            // Dispatch error event
            window.dispatchEvent(new CustomEvent('d3LoadError', { 
                detail: { error: error } 
            }));
            
            console.error('D3.js loading failed:', error);
        }
        
        /**
         * Show loading indicator
         */
        _showLoadingIndicator() {
            if (document.getElementById('cqss-loading-indicator')) return;
            
            const indicator = document.createElement('div');
            indicator.id = 'cqss-loading-indicator';
            indicator.className = config.ui.loadingIndicatorClass;
            indicator.innerHTML = `
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: rgba(0,0,0,0.8);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    z-index: 10000;
                    font-family: 'Segoe UI', sans-serif;
                    text-align: center;
                ">
                    <div style="margin-bottom: 10px;">Loading visualization library...</div>
                    <div style="
                        width: 30px;
                        height: 30px;
                        border: 3px solid #333;
                        border-top: 3px solid #fff;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin: 0 auto;
                    "></div>
                    <style>
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                </div>
            `;
            document.body.appendChild(indicator);
        }
        
        /**
         * Hide loading indicator
         */
        _hideLoadingIndicator() {
            const indicator = document.getElementById('cqss-loading-indicator');
            if (indicator) {
                indicator.remove();
            }
        }
        
        /**
         * Show error message to user
         */
        _showErrorMessage(message) {
            if (document.getElementById('cqss-error-message')) return;
            
            const errorDiv = document.createElement('div');
            errorDiv.id = 'cqss-error-message';
            errorDiv.className = config.ui.errorClass;
            errorDiv.innerHTML = `
                <div style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #f44336;
                    color: white;
                    padding: 15px 20px;
                    border-radius: 8px;
                    max-width: 400px;
                    z-index: 10001;
                    font-family: 'Segoe UI', sans-serif;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                ">
                    <div style="font-weight: bold; margin-bottom: 5px;">⚠️ Loading Error</div>
                    <div style="font-size: 14px;">${message}</div>
                    <button onclick="this.parentElement.parentElement.remove()" style="
                        position: absolute;
                        top: 10px;
                        right: 10px;
                        background: none;
                        border: none;
                        color: white;
                        cursor: pointer;
                        font-size: 16px;
                    ">×</button>
                </div>
            `;
            document.body.appendChild(errorDiv);
            
            // Auto-remove after specified duration
            setTimeout(() => {
                if (errorDiv.parentElement) {
                    errorDiv.remove();
                }
            }, config.ui.errorDisplayDuration);
        }
        
        /**
         * Check if D3.js is already loaded
         */
        isLoaded() {
            return this.loaded && typeof window.d3 !== 'undefined';
        }
        
        /**
         * Get current loading state
         */
        getState() {
            return {
                loaded: this.loaded,
                loading: this.loading,
                error: this.error,
                retryCount: this.retryCount
            };
        }
    }
    
    // Create global instance
    window.CQSS_D3Loader = new D3Loader();
    
    // Convenience method for backward compatibility
    window.loadD3 = function(callback) {
        window.CQSS_D3Loader.load()
            .then(d3 => {
                if (typeof callback === 'function') {
                    callback(null, d3);
                }
            })
            .catch(error => {
                if (typeof callback === 'function') {
                    callback(error, null);
                }
            });
    };
    
})(window);