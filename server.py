from flask import Flask, request, jsonify, send_from_directory
from text_summarizer import generate_hybrid_summary

# Create Flask app
app = Flask(__name__)


# Route for homepage
@app.route('/')
def home():
    return send_from_directory('.', 'home.html')


# Route for CSS
@app.route('/home_style.css')
def style():
    return send_from_directory('.', 'home_style.css')


# Route for JavaScript
@app.route('/home_script.js')
def script():
    return send_from_directory('.', 'home_script.js')


# Route for summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get text safely from frontend
        text = request.form.get('text', '')

        # If input is empty
        if text.strip() == "":
            return jsonify({'error': 'Please enter some text!'})

        # Generate hybrid summary
        summary = generate_hybrid_summary(text)

        # Send summary back to frontend
        return jsonify({'summary': summary})

    except Exception as e:
        # Print error in terminal for debugging
        print("Error occurred:", str(e))

        # Send error message to frontend
        return jsonify({'error': str(e)}), 500


# Run server on custom port
if __name__ == '__main__':
    app.run(debug=True, port=5003)