import os
from flask import Flask, request, jsonify, render_template, send_file
import numpy as np
import pandas as pd
import pickle
from utils import data_validation

# Define paths relative to the script location
model_path = os.path.join('data', 'model.pkl')
features_metadata_path = os.path.join('data', 'features_metadata.pkl')

# Load the model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load feature metadata from pickle file
with open(features_metadata_path, 'rb') as file:
    features_metadata = pickle.load(file)

# Load features data types from metadata
features_dtypes_tuple = [(feature, metadata['dtype']) for feature, metadata in features_metadata.items()]

# Flask-APP
app = Flask(__name__, template_folder='../templates')

# Rendering the html index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/features', methods=['GET'])
def get_features():
    return jsonify({'features_dtypes': features_dtypes_tuple})

@app.route('/predict', methods=['POST'])
def make_single_prediction():
    try:
        data = request.json
        user_feature_values, warnings = data_validation(data, features_metadata)
        X_new = pd.DataFrame([user_feature_values], columns=features_metadata.keys())
        Y_new_hat = model.predict(X_new)
        output = np.round(Y_new_hat[0], 2)
        return jsonify({'predicted_price': output, 'warnings': warnings})
    except ValueError as ve:
        return jsonify({'error': str(ve)})
    except Exception as e:
        return jsonify({'error': str(e)})

# Helper function to check allowed file extensions
def file_type(file_path):
    return file_path.split('/')[-1].split('.')[-1].lower()

def allowed_file(file_path):
    allowed_files_types = ['csv']
    return file_type(file_path) in allowed_files_types

def predict_multiple_features(file_path):
    try:
        if file_type(file_path) == 'csv': 
            user_features_df = pd.read_csv(file_path)
            index_list, prediction_list, all_warnings = [], [], []
            for index, row in user_features_df.iterrows():
                user_data = row.to_dict()
                try:
                    user_feature_values, row_warnings = data_validation(user_data, features_metadata)
                    X_new = pd.DataFrame([user_feature_values], columns=features_metadata.keys())
                    prediction = model.predict(X_new)[0]
                    index_list.append(index)
                    prediction_list.append(np.round(prediction, 2))
                    all_warnings.extend(row_warnings)
                except ValueError as ve:
                    return None, {'error': str(ve)}
                except Exception as e:
                    return None, {'error': str(e)}
            predictions_df = pd.DataFrame({'index': index_list, 'predictions': prediction_list})
            return predictions_df, {'warnings': all_warnings}
    except Exception as e:
        return None, {'error': str(e)}

@app.route('/batch_predict', methods=['POST'])
def make_multiple_predictions():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if allowed_file(file.filename):
            # Save the uploaded user data file
            user_data_filename = file.filename
            uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'user-data')
            os.makedirs(uploads_dir, exist_ok=True)
            user_data_path = os.path.join(uploads_dir, user_data_filename)
            file.save(user_data_path)
            
            # Process the file and generate predictions
            predictions_df, result = predict_multiple_features(user_data_path)
            if 'error' in result:
                return jsonify(result), 400

            warnings = result.get('warnings', [])
            
            # Save the predictions file
            predictions_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'predictions')
            os.makedirs(predictions_dir, exist_ok=True)
            predictions_path = os.path.join(predictions_dir, f'predictions_{user_data_filename}')
            predictions_df.to_csv(predictions_path, index=False)
            
            # Return the predictions file as a download    
            return send_file(predictions_path, as_attachment=True, download_name=f'predictions_{user_data_filename}')
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
