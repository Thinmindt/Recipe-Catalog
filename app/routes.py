from app import app
from app.schema import schema
from graphene_file_upload.flask import FileUploadGraphQLView
from flask import send_from_directory, send_file
from PIL import Image
from resizeimage import resizeimage
import os
from io import BytesIO

@app.route('/')
@app.route('/index')
def index():
    """Leaving this here"""
    return "Hello, World!"

@app.route('/image/<filename>')
def image_host(filename):
    """Returns raw image from the images/ directory
    """
    return send_from_directory(os.path.join("..", "images"), filename)

@app.route('/image/<filename>/h+w/<height>/<width>')
def image_host_resized(filename, height, width):
    """resize image at images/<filename> with the given
    width and height. Does not crop or change image aspect ratio.
    """
    path = os.path.join("images", filename)
    img_io = BytesIO()
    with open(path, "rb") as f:
        with Image.open(f) as image:
            resized_image = resizeimage.resize_contain(image, [int(width), int(height)])
            resized_image.save(img_io, 'PNG', quality=70)
            img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

app.add_url_rule(
    '/graphql',
    view_func=FileUploadGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)