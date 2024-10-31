# Import flask modules for web
from flask import Flask, render_template, request, jsonify
import weather 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    report = weather.main(city)
    print(f"Generated Report: {report}")
    return jsonify({'report': report})

if __name__ == '__main__':
    app.run(debug=True)