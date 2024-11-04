from flask import Flask, render_template, request, jsonify
import weather

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    report, qr_code_image = weather.main(city)

    if report and qr_code_image:
        return jsonify({'report': report, 'qr_code_image': qr_code_image.decode('utf-8')})
    return jsonify({'report': report})

if __name__ == '__main__':
    app.run(debug=True)
