from flask import Flask, render_template, redirect, url_for, request
from PIL import Image
import numpy as np
import requests as req

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form['url'] != '':
            res = req.get(request.form['image_url'])
            print(res.content)
        else:
            image = request.files['image_file']
        img = Image.open(image)
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=10)
        color_indeces = sorted(paletted.getcolors(
            img.width * img.height), reverse=True)
        palette = paletted.getpalette()
        print(palette)
        colors = ['#%02x%02x%02x' % tuple(palette[index[1]*3:index[1]*3+3])
                  for index in color_indeces]
        return render_template('index.html', image=image, colors=colors)
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=4000, debug=True)
