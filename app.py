from flask import Flask, render_template, request, jsonify
from jinja2.exceptions import TemplateNotFound
from config import RESOURCE_CONFIGS
from generators import generate_terraform_config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def index():
    return render_template('index.html', resources=RESOURCE_CONFIGS)

@app.route('/get_resource_form/<resource>')
def get_resource_form(resource):
    try:
        return render_template(f'resources/{resource}/form.html', 
                             config=RESOURCE_CONFIGS.get(resource, {}))
    except TemplateNotFound:
        return 'Form template not found', 404

@app.route('/get_config_fields/<resource_type>')
def get_config_fields(resource_type):
    return jsonify(RESOURCE_CONFIGS.get(resource_type, {}))

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    resource_type = data.get('resource_type')
    config = data.get('config', {})
    
    terraform_config = generate_terraform_config(resource_type, config)
    return jsonify({'config': terraform_config})

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    feedback = request.get_json()
    # Here you could save feedback to a database or send it via email
    return jsonify({'status': 'success', 'message': 'Thank you for your feedback!'})

if __name__ == '__main__':
    app.run(debug=True) 