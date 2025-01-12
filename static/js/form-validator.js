class FormValidator {
    constructor(form) {
        this.form = form;
        this.init();
    }

    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.form.querySelectorAll('[data-validate]').forEach(field => {
            field.addEventListener('change', () => this.validateField(field));
            field.addEventListener('input', () => this.validateField(field));
        });
    }

    validateField(field) {
        const validations = field.dataset.validate.split(',');
        let isValid = true;
        let errorMessage = '';

        validations.forEach(validation => {
            const [rule, param] = validation.trim().split(':');
            
            if (!isValid) return; // Skip if already invalid

            switch (rule) {
                case 'required':
                    if (!field.value.trim()) {
                        isValid = false;
                        errorMessage = 'This field is required';
                    }
                    break;

                case 'pattern':
                    if (field.pattern && !new RegExp(field.pattern).test(field.value)) {
                        isValid = false;
                        errorMessage = field.dataset.patternMessage || 'Invalid format';
                    }
                    break;

                case 'cidr':
                    if (!this.validateCIDR(field.value)) {
                        isValid = false;
                        errorMessage = 'Invalid CIDR format';
                    }
                    break;

                case 'port':
                    const port = parseInt(field.value);
                    if (isNaN(port) || port < 0 || port > 65535) {
                        isValid = false;
                        errorMessage = 'Port must be between 0 and 65535';
                    }
                    break;

                case 'min':
                    if (parseFloat(field.value) < parseFloat(param)) {
                        isValid = false;
                        errorMessage = `Value must be at least ${param}`;
                    }
                    break;

                case 'max':
                    if (parseFloat(field.value) > parseFloat(param)) {
                        isValid = false;
                        errorMessage = `Value must not exceed ${param}`;
                    }
                    break;

                case 'aws-arn':
                    if (!this.validateAWSArn(field.value)) {
                        isValid = false;
                        errorMessage = 'Invalid AWS ARN format';
                    }
                    break;

                case 'aws-region':
                    if (!this.validateAWSRegion(field.value)) {
                        isValid = false;
                        errorMessage = 'Invalid AWS region format';
                    }
                    break;

                case 'json':
                    try {
                        JSON.parse(field.value);
                    } catch (e) {
                        isValid = false;
                        errorMessage = 'Invalid JSON format';
                    }
                    break;

                case 'domain':
                    if (!this.validateDomain(field.value)) {
                        isValid = false;
                        errorMessage = 'Invalid domain name format';
                    }
                    break;

                case 'aws-tag':
                    if (!this.validateAWSTag(field.value)) {
                        isValid = false;
                        errorMessage = 'Invalid AWS tag format (key=value)';
                    }
                    break;
            }
        });

        this.setFieldValidationState(field, isValid, errorMessage);
        return isValid;
    }

    // Validation helper methods
    validateCIDR(value) {
        const cidrPattern = /^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))$/;
        if (!cidrPattern.test(value)) return false;
        
        const parts = value.split('/')[0].split('.');
        return parts.every(part => parseInt(part) <= 255);
    }

    validateAWSArn(value) {
        const arnPattern = /^arn:aws:[a-zA-Z0-9\-]+:[a-zA-Z0-9\-]*:[0-9]{12}:.+$/;
        return arnPattern.test(value);
    }

    validateAWSRegion(value) {
        const regionPattern = /^[a-z]{2}-[a-z]+-[0-9]{1}$/;
        return regionPattern.test(value);
    }

    validateDomain(value) {
        const domainPattern = /^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$/;
        return domainPattern.test(value);
    }

    validateAWSTag(value) {
        const tagPattern = /^[a-zA-Z0-9+\-=._:/@]+=[a-zA-Z0-9+\-=._:/@]+$/;
        return tagPattern.test(value);
    }

    setFieldValidationState(field, isValid, errorMessage) {
        field.classList.toggle('is-invalid', !isValid);
        field.classList.toggle('is-valid', isValid);
        
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = errorMessage;
        }

        // Trigger custom event for field validation
        field.dispatchEvent(new CustomEvent('fieldValidated', {
            detail: { isValid, errorMessage }
        }));
    }

    validateForm() {
        let isValid = true;
        let firstInvalidField = null;

        this.form.querySelectorAll('[data-validate]').forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
                if (!firstInvalidField) firstInvalidField = field;
            }
        });

        if (firstInvalidField) {
            firstInvalidField.focus();
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        return isValid;
    }

    handleSubmit(e) {
        if (!this.validateForm()) {
            e.preventDefault();
            return false;
        }
        return true;
    }
} 