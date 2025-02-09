from flask import Flask, request, render_template_string, send_file
import io

app = Flask(__name__)

# HTML template for the upload form
upload_form = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Upload Image</title>
  </head>
  <body>
    <h1>Upload an Image</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="image">
      <input type="submit" value="Upload">
    </form>
    {% if image_url %}
    <h2>Uploaded Image:</h2>
    <img src="{{ image_url }}" alt="Uploaded Image">
    {% endif %}
  </body>
</html>
'''

# Variable to store the uploaded image
uploaded_image = None

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    global uploaded_image
    image_url = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file part'
        file = request.files['image']
        if file.filename == '':
            return 'No selected file'
        if file:
            uploaded_image = file.read()
            image_url = '/image'
    return render_template_string(upload_form, image_url=image_url)

@app.route('/image')
def serve_image():
    if uploaded_image is None:
        return 'No image uploaded', 404
    return send_file(io.BytesIO(uploaded_image), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)