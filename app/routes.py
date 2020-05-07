from app import app
from app.schema import schema
from flask_graphql import GraphQLView

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)