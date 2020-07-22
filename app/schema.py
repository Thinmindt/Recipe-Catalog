import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from app.models import User, Recipe, Image, RecipeCategory
from app import db
from typing import Union
from base64 import b64decode
import app.utils as utils
from graphene_file_upload.scalars import Upload
from app.recipe_schema import RecipeObject, CreateRecipe, DeleteRecipe, UpdateRecipe

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, username, email, password):
        user = User(username=username, email=email)

        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user)

class RecipeCategoryAttribute:
    name = graphene.String(description="Name of Category")

class RecipeCategoryObject(SQLAlchemyObjectType, RecipeCategoryAttribute):
    """ Recipe Category node """
    class Meta: 
        model = RecipeCategory
        interfaces = (graphene.relay.Node, )

class ImageAttribute:
    filename = graphene.String(description="File name in image folder")
    id_recipe = graphene.ID(description="Global ID of associated recipe")
    date_added = graphene.DateTime(description="Date the image was added")

class ImageObject(SQLAlchemyObjectType, ImageAttribute):
    """ Image node """
    class Meta:
        model = Image
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_recipes = SQLAlchemyConnectionField(RecipeObject)
    recipe = graphene.relay.Node.Field(RecipeObject)
    images = SQLAlchemyConnectionField(ImageObject)
    image = graphene.relay.Node.Field(ImageObject)
    recipe_categories = SQLAlchemyConnectionField(RecipeCategoryObject)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_recipe = CreateRecipe.Field()
    update_recipe = UpdateRecipe.Field()
    delete_recipe = DeleteRecipe.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)