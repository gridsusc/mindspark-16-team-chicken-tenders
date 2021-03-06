from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from img_to_stl.test import test
from img_to_stl._3Dvoxel import _3Dvoxel
from os import listdir
from os.path import isfile, join
import math
import time


app = Flask(__name__)

app.secret_key = "secret key"

mypath = "./static"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def convert_image():
    # create a file object of the uploaded file
    file = request.files['file']
    # get name of the file
    filename = secure_filename(file.filename)
    # save the file in current directory
    file.save(os.path.join('.', filename))

    """
    pipeline description
    Runs test with input file, number of centers and iterations
    Then runs 3Dvoxel on the 2 images
    Outputs the stl file
    """
    test(input_image=filename, num_centers=4, iterations=20)
    _3Dvoxel()

    # print where the stl file is saved
    output_file_path = os.path.join(os.getcwd(), 'static/output'+str(math.trunc(time.time()))+'.stl')
    output_message = f'STL file generated and saved as {output_file_path}'

    # delete the copied image file
    os.remove(os.path.join('.', filename))

    # delete all preprocessing files
    os.remove(os.path.join('.', 'center_processing_0.png'))
    os.remove(os.path.join('.', 'center_processing_1.png'))
    os.remove(os.path.join('.', 'center_processing_2.png'))
    os.remove(os.path.join('.', 'center_processing_3.png'))
    os.remove(os.path.join('.', 'center_0.png'))
    os.remove(os.path.join('.', 'center_1.png'))
    os.remove(os.path.join('.', 'center_2.png'))
    os.remove(os.path.join('.', 'center_3.png'))
    os.remove(os.path.join('.', 'final.png'))

    return render_template('index.html', output_message=output_message)


@app.route('/library')
def library():
    onlyfiles = [{'name': f, 'key': f.split('.')[0]} for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.stl')]
    return render_template('library.html', files=onlyfiles)


@app.route('/download')
def download():
    # For windows you need to use drive name [ex: F:/Example.pdf]
    path = "./static/" + request.args.get('filename')

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
