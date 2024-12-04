from flask import Blueprint, render_template, request
from .analyze_transcript_gpt import analyze_transcript_gpt

analyzer_bp = Blueprint('analyzer', __name__, 
                       template_folder='./')

@analyzer_bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        transcript = request.form.get('transcript')
        results = analyze_transcript_gpt(transcript)
        return render_template('analyzer.html', results=results)
    return render_template('analyzer.html', results=None)