"""
Flask web application for monitoring dashboard.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from src.analytics import (
    get_complete_report,
    get_uptime_summary,
    get_performance_stats,
    detect_outages
)
from src.database import get_recent_checks, get_check_count
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = 'web-monitoring-secret-key-change-in-production'

@app.route('/')
def dashboard():
    """
    Main dashboard page.
    """
    try:
        # Get comprehensive report
        report = get_complete_report(hours=24)
        
        # Get recent checks for table
        recent_checks = get_recent_checks(limit=10)
        
        # Get flash messages from session
        check_result = session.pop('check_result', None)
        success_message = session.pop('success_message', None)
        error = session.pop('error', None)
        
        # Render dashboard template
        return render_template(
            'index.html',
            report=report,
            recent_checks=recent_checks,
            check_result=check_result,
            success_message=success_message,
            error=error
        )
    except Exception as e:
        return f"Error loading dashboard: {e}", 500


@app.route('/api/status')
def api_status():
    """
    API endpoint for current status (JSON).
    Useful for AJAX updates.
    """
    try:
        report = get_complete_report(hours=24)
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/uptime')
def api_uptime():
    """
    API endpoint for uptime data only.
    """
    try:
        uptime = get_uptime_summary()
        return jsonify(uptime)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recent')
def api_recent():
    """
    API endpoint for recent checks.
    """
    try:
        recent = get_recent_checks(limit=20)
        return jsonify(recent)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """
    Health check endpoint.
    """
    try:
        total_checks = get_check_count()
        return jsonify({
            'status': 'healthy',
            'total_checks': total_checks
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@app.route('/check', methods=['POST'])
def instant_check():
    """
    Instant URL check - user submits URL and gets immediate result.
    Uses POST-Redirect-GET pattern to prevent form resubmission.
    """
    try:
        from src.monitor import check_website
        from src.database import save_check
        
        # Get URL from form
        url = request.form.get('url', '').strip()
        
        # Validate URL
        if not url:
            session['error'] = "Please enter a URL"
            return redirect(url_for('dashboard'))
        
        # Add https:// if not present
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        
        # Check the website
        result = check_website(url, timeout=5)
        
        # Save to database
        save_check(result)
        
        # Store result in session for display after redirect
        session['check_result'] = result
        session['success_message'] = f"Checked {url} successfully!"
        
        # Redirect to dashboard (PRG pattern)
        return redirect(url_for('dashboard'))
            
    except Exception as e:
        session['error'] = f"Error checking URL: {str(e)}"
        return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("=" * 50)
    print("🌐 Starting Web Dashboard")
    print("=" * 50)
    print(f"📊 Dashboard URL: http://localhost:{port}")
    print("⌨️  Press Ctrl+C to stop")
    print("=" * 50)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )