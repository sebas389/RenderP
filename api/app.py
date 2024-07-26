from flask import Flask, request, jsonify, render_template
import pandas as pd
from joblib import load
import datetime


app = Flask(__name__)

# Lista de todos los distritos en tu modelo
distritos = [
    'Ate Vitarte', 'Barranco', 'Bellavista', 'Breña', 'Carabayllo', 'Cercado de Lima', 'Chorrillos', 
    'Comas', 'Jesús María', 'La Molina', 'La Perla', 'La Victoria', 'Lince', 'Los Olivos', 'Magdalena', 
    'Miraflores', 'Pueblo Libre', 'San Borja', 'San Isidro', 'San Miguel', 'Surco', 'Surquillo'
]

model = load('./housing_prediction.joblib')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
     # Recoge los datos del formulario
    area = float(request.form.get('area'))
    bedrooms = int(request.form.get('bedrooms'))
    bathrooms = int(request.form.get('bathrooms'))
    garages = int(request.form.get('garages'))
    exterior_view = 1 if request.form.get('exterior_view') else 0
    age = float(request.form.get('age'))
    district = request.form.get('district')

     # Crear un diccionario con todas las columnas posibles
    current_year = datetime.datetime.now().year
    data = {
        "Year": current_year - age,
        "Quarter":3,
        "Exchange_rate":3.31644,
        "IPC": 120.303045,
        'Area': [area],
        'Bedrooms': [bedrooms],
        'Bathrooms': [bathrooms],
        'Garages': [garages],
        "Floor": 2,
        'Exterior_view': [exterior_view],
        'Age': [age],
    }


    # Agregar columnas para los distritos
    for d in distritos:
        data[d] = [1 if d == district else 0]

    # Crear un DataFrame con las columnas en el orden correcto
    columns = [
        'Year', 'Quarter', 'Exchange_rate', 'IPC', 'Area', 'Bedrooms', 'Bathrooms', 'Garages', 'Floor', 
        'Exterior_view', 'Age'] + distritos
    
     # Añadir las columnas de distritos al DataFrame
    input_data = pd.DataFrame(data, columns=columns)

    # print(input_data)
          
    prediction = model.predict(input_data)
    print(prediction)


    return jsonify({'price': prediction[0]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)