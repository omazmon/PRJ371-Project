import requests
from flask import Flask, render_template, request, jsonify
import bcrypt
import pyodbc
import uuid

app = Flask(__name__)

# Database connection setup
conn_str = "DRIVER={SQL Server};SERVER=Mthokozisi-2\SQLEXPRESS;DATABASE=AgriDrone;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


def generate_user_id():
    # Generate a unique user ID using UUID
    user_id = str(uuid.uuid4())
    return user_id


@app.route('/')
def index():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Generate user ID (you can use any method to generate a unique ID, for example, UUID)
    user_id = generate_user_id()

    try:
        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert user data into the database
        cursor.execute(
            'INSERT INTO Users (UserID, FirstName, LastName, Username, Password, Role) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, first_name, last_name, username, hashed_password, role))
        conn.commit()

        return jsonify({'success': True, 'message': 'Registration successful!'})
    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while registering the user.'})


# External weather API endpoint (example: OpenWeatherMap API)
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/"
WEATHER_API_KEY = "06e1969da55a4b51d0b4447dcd9c92eb"

crops_data = {
    "wheat": {
        "temperature_range": [15, 25],  # Celsius
        "rainfall_range": [50, 100]  # mm
    },
    "corn": {
        "temperature_range": [20, 30],  # Celsius
        "rainfall_range": [100, 200]  # mm
    },
    # Add more crops and their suitable conditions here
}


# Endpoint for weather forecast
@app.route('/api/weather', methods=['GET'])
def get_weather_forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is missing"}), 400

    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Get temperature in Celsius
    }

    response = requests.get(WEATHER_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
        return jsonify({"weather": weather}), 200
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500


# Endpoint for crop analysis
@app.route('/api/crop-analysis', methods=['GET'])
def crop_analysis():
    crop = request.args.get('crop')
    temperature = float(request.args.get('temperature'))
    rainfall = float(request.args.get('rainfall'))

    if not crop or crop.lower() not in crops_data:
        return jsonify({"error": "Invalid or missing crop parameter"}), 400

    suitable_conditions = crops_data[crop.lower()]
    temp_range = suitable_conditions["temperature_range"]
    rainfall_range = suitable_conditions["rainfall_range"]

    is_suitable = temp_range[0] <= temperature <= temp_range[1] and rainfall_range[0] <= rainfall <= rainfall_range[1]

    return jsonify({"is_suitable": is_suitable}), 200


if __name__ == "__main__":
    app.run(debug=True)
