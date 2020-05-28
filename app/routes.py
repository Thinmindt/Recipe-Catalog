from app import app
from app.schema import schema
from graphene_file_upload.flask import FileUploadGraphQLView
from flask import send_from_directory

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/image/<filename>')
def image_host(filename):
    return send_from_directory("../images", filename)

app.add_url_rule(
    '/graphql',
    view_func=FileUploadGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)