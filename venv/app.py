from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    try:
        location_response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        location_data = location_response.json()
        city = location_data.get('city', 'Unknown')

        weather_response = requests.get(f'https://api.weatherapi.com/v1/current.json?key=fe575f1cbe3e4cd6835210220240707&q={city}')
        weather_data = weather_response.json()
        temperature = weather_data['current']['temp_c']

        return jsonify({
            'client_ip': client_ip,
            'location': city,
            'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}' 
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch location or weather data'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

