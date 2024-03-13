from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import numpy as np
import pickle
import json

app = Flask(__name__,template_folder = 'template',static_folder='static')

# Define absolute file paths
model_path = "C:\\Users\\91784\\Desktop\\Hack_career\\Flask\\.venv\\model.pkl"
columns_path = "C:\\Users\\91784\\Desktop\\Hack_career\\Flask\\.venv\\my_columns.json"

# Load model and columns with error handling
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(columns_path, 'r') as f:
        columns = json.load(f)
except FileNotFoundError:
    print("Error: Files not found. Please check file paths.")
    exit(1)

# Define routes
@app.route('/')
def index_copy():
    return render_template("index copy.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    education = request.form['education']
    skills1 = request.form['skills1']
    skills2 = request.form['skills2']
    eng_lvl = int(request.form['eng_lvl'])
    cgpa = float(request.form['cgpa']) # Handle potential missing value

    # Create input features array
    input_features = np.zeros(len(columns['columns']))
    input_features[0] = eng_lvl
    input_features[1] = cgpa 

    # Find the index of education and skills in the column list
    edu_index = columns['columns'].index(education)
    skills1_index = columns['columns'].index(skills1)
    skills2_index = columns['columns'].index(skills2)

    # Set the corresponding indices to 1
    input_features[edu_index] = 1
    input_features[skills1_index] = 1
    input_features[skills2_index] = 1

    # Predict career
    predicted_career = model.predict([input_features])
    print("Predicted : ", predicted_career)

    return render_template("result.html", prediction_text="Predicted career is {}".format(predicted_career))


if __name__ == '__main__':
    app.run(debug=True)

