from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import weather  # Assuming weather.py is in the same directory

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    try:
        city = request.form['city']
        report = weather.main(city)
        print(f"Generated Report: {report}")
        return jsonify({'report': report})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
