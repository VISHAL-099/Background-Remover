from flask import Flask, render_template, request, send_from_directory
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Define the desired width and height for the resized image
RESIZE_WIDTH = 300
RESIZE_HEIGHT = 300

@app.route('/output_image')
def output_image():
    return send_from_directory('static', 'output.png', as_attachment=True)

@app.route('/download_output')
def download_output():
    return send_from_directory('static', 'output.png', as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    input_image = None
    output_buffer = None

    if request.method == 'POST':
        input_file = request.files['input_file']
        if input_file and allowed_file(input_file.filename):
            try:
                # Attempt to open the image file
                input_image = Image.open(input_file)

                # Process the image
                output_image = remove(input_image)

                # Resize the output image
                output_image = output_image.resize((RESIZE_WIDTH, RESIZE_HEIGHT))

                # Save output image to a file in the 'static' folder
                output_image.save("static/output.png", format="PNG")

                # Save output image to a BytesIO object
                output_buffer = BytesIO()
                output_image.save(output_buffer, format="PNG")
                output_buffer.seek(0)

            except Exception as e:
                # Handle image processing errors
                print(f"Error processing image: {e}")

    return render_template('index.html', input_image=input_image, output_buffer=output_buffer)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

if __name__ == '__main__':
    app.run(debug=True)
