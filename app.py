from flask import Flask, render_template, request, jsonify
import weather

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    result = weather.main(city)  # Store the result (could be a tuple or an error message).

    if isinstance(result, tuple): #If main is executed properly
        report, qr_code_image = result
        return jsonify({'report': report, 'qr_code_image': qr_code_image.decode('utf-8')})
    else: #If error in main
        return jsonify({'report': result, 'error': True})  # Indicate an error to the frontend

if __name__ == '__main__':
    app.run(debug=True)
