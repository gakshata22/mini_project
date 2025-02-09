from flask import Flask, request, render_template, redirect, url_for
import cv2
import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)


cnn_model = load_model('cnn_feature_extractor.h5')
model1_pipeline = joblib.load('model_pipeline.pkl')
le = joblib.load('label_encoder.pkl')
print("Classes in Label Encoder:", le.classes_)

SIZE = 128
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    image_url = None
    result = None
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', result="No file uploaded.")
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', result="No file selected.")
        
        if file:
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  
            
            
            img = cv2.imread(file_path)
            if img is not None:
                img = cv2.resize(img, (SIZE, SIZE))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = img / 255.0
                img = np.expand_dims(img, axis=0)
                
               
                features = cnn_model.predict(img)
                print("Features shape in Flask app:", features.shape)
                
                prediction = model1_pipeline.predict(features)
                prediction_label = le.inverse_transform([prediction[0]])
                
                
                result = 'Melanoma Detected' if prediction_label[0] in ['Malignant', 'melanoma'] else 'No Melanoma'
            
            
            image_url = url_for('static', filename=f'uploads/{filename}')
    
    return render_template('index.html', result=result, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)