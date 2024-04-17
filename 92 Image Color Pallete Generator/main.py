from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO
import requests as req
from base64 import b64encode

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        image = ''

        # Get image bytes from url/file
        if request.form['image_url'] != '':
            try:
                res = req.get(request.form['image_url'])
                res.raise_for_status()
                image = BytesIO(res.content)
            except req.HTTPError:
                error = f'{res.status_code}: Invalid image URL'
                return render_template('index.html', error=error)
            except Exception:
                error = 'Invalid image URL'
                return render_template('index.html', error=error)
        elif 'image_file' in request.files:
            image = BytesIO(request.files['image_file'].read())

        # Get most prominent colors
        try:
            print(request.files['image_file'].filename)
            img = Image.open(image)
            paletted = img.convert('P', palette=Image.ADAPTIVE, colors=10)
            color_indeces = sorted(paletted.getcolors(
                img.width * img.height), reverse=True)
            palette = paletted.getpalette()
            colors = ['#%02x%02x%02x'.title() % tuple(palette[index[1]*3:index[1]*3+3])
                      for index in color_indeces]
            return render_template('index.html', image='data:image/png;base64,' + b64encode(image.getvalue()).decode('ascii'), colors=colors)
        except:
            return render_template('index.html', error='Could not open image')

    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    app.run(port=4000, debug=True)
