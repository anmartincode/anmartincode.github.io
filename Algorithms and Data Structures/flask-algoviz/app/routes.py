from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/visualize/<structure>')
def visualize(structure):
    return render_template('visualization.html', structure=structure)

@bp.route('/api/step', methods=['POST'])
def api_step():
    # Placeholder for step logic
    return jsonify({'status': 'ok', 'step': request.json})

@bp.route('/api/benchmark', methods=['POST'])
def api_benchmark():
    # Placeholder for benchmark logic
    return jsonify({'status': 'ok', 'results': {}})

@bp.route('/api/export', methods=['POST'])
def api_export():
    # Placeholder for export logic
    return jsonify({'status': 'ok', 'csv': ''})
