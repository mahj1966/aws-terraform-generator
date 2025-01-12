class TerraformGenerator {
    constructor() {
        this.selectedResource = null;
        this.currentConfig = {};
        this.formValidator = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.querySelectorAll('.resource-card').forEach(card => {
            card.addEventListener('click', () => this.handleResourceSelect(card));
        });
    }

    handleResourceSelect(card) {
        this.selectedResource = card.dataset.resource;
        document.querySelectorAll('.resource-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        this.loadConfigurationForm();
    }

    async loadConfigurationForm() {
        try {
            // Load resource-specific form template
            const formResponse = await fetch(`/get_resource_form/${this.selectedResource}`);
            if (!formResponse.ok) {
                throw new Error(`HTTP error! status: ${formResponse.status}`);
            }
            const formHtml = await formResponse.text();
            
            // Load field configurations
            const fieldsResponse = await fetch(`/get_config_fields/${this.selectedResource}`);
            if (!fieldsResponse.ok) {
                throw new Error(`HTTP error! status: ${fieldsResponse.status}`);
            }
            const fields = await fieldsResponse.json();

            this.renderForm(formHtml, fields);
        } catch (error) {
            console.error('Error loading form:', error);
            // Show error message to user
            const form = document.getElementById('resourceForm');
            if (form) {
                form.innerHTML = `<div class="alert alert-danger">Error loading form: ${error.message}</div>`;
            }
        }
    }

    renderForm(formHtml, fields) {
        const form = document.getElementById('resourceForm');
        if (!form) {
            console.error('Form element not found');
            return;
        }

        // Clear existing form content
        form.innerHTML = formHtml;

        // Initialize form validator
        this.formValidator = new FormValidator(form);

        // Initialize tooltips
        var tooltipTriggerList = [].slice.call(form.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                trigger: 'hover focus',
                placement: 'right'
            });
        });

        // Add event listeners to form fields
        form.querySelectorAll('input, select, textarea').forEach(input => {
            input.addEventListener('change', (e) => this.handleFieldChange(e));
        });

        // Show the form sections
        document.getElementById('configurationForm').style.display = 'block';
        document.getElementById('terraformOutput').style.display = 'block';
    }

    handleFieldChange(event) {
        const { name, value, type } = event.target;
        
        // Handle different input types
        if (type === 'checkbox') {
            this.currentConfig[name] = event.target.checked;
        } else if (type === 'number') {
            this.currentConfig[name] = parseFloat(value) || 0;
        } else if (event.target.multiple) {
            this.currentConfig[name] = Array.from(event.target.selectedOptions).map(opt => opt.value);
        } else {
            this.currentConfig[name] = value;
        }

        if (this.formValidator.validateField(event.target)) {
            this.generateTerraformConfig();
        }
    }

    async generateTerraformConfig() {
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    resource_type: this.selectedResource,
                    config: this.currentConfig
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            const outputElement = document.getElementById('configOutput');
            if (outputElement) {
                outputElement.textContent = data.config;
            }
        } catch (error) {
            console.error('Error generating config:', error);
            // Show error message to user
            const outputElement = document.getElementById('configOutput');
            if (outputElement) {
                outputElement.textContent = `Error generating configuration: ${error.message}`;
            }
        }
    }
}

// Initialize the application
const app = new TerraformGenerator();

// Add clipboard functionality
function copyToClipboard() {
    const configText = document.getElementById('configOutput').textContent;
    navigator.clipboard.writeText(configText).then(() => {
        alert('Configuration copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy configuration');
    });
}

// Add feedback handling
function submitFeedback(event) {
    event.preventDefault();
    const form = event.target.closest('.feedback-form');
    const feedback = form.querySelector('textarea').value;
    const section = form.closest('.tab-pane').id;

    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            section: section,
            feedback: feedback,
            helpful: form.dataset.helpful
        })
    })
    .then(response => response.json())
    .then(data => {
        form.innerHTML = '<div class="alert alert-success">Thank you for your feedback!</div>';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add search functionality
function initializeSearch() {
    const searchInput = document.getElementById('docSearch');
    if (!searchInput) return;

    searchInput.addEventListener('input', debounce(function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const content = document.querySelectorAll('.tab-pane');
        
        content.forEach(section => {
            const text = section.textContent.toLowerCase();
            const matches = text.includes(searchTerm);
            
            if (searchTerm === '') {
                section.innerHTML = section.originalContent || section.innerHTML;
                return;
            }
            
            if (!section.originalContent) {
                section.originalContent = section.innerHTML;
            }
            
            if (matches) {
                const regex = new RegExp(searchTerm, 'gi');
                section.innerHTML = section.originalContent.replace(regex, match => 
                    `<span class="highlight">${match}</span>`
                );
            }
        });
    }, 300));
}

// Initialize all features
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
} 