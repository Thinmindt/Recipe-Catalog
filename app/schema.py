import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from app.models import User, Recipe
from app import db
from typing import Union
from base64 import b64decode
import app.utils as utils

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

class RecipeAttribute:
    title = graphene.String(description="Title of the Recipe")
    type = graphene.String(description="Source type: Book or Website")
    web_link = graphene.String(description="Link to source page")
    book_title = graphene.String(description="Title of the book containing the recipe")
    book_page = graphene.Int(description="Page number the recipe is on")
    book_image_path = graphene.String(description="Path to image of the recipe")
    rating = graphene.Int(description="The rating given by the user")
    notes = graphene.String(description="Any comments or notes")

class RecipeObject(SQLAlchemyObjectType, RecipeAttribute):
    """Recipe Node"""
    class Meta:
        model = Recipe
        interfaces = (graphene.relay.Node, )

class CreateRecipeInput(graphene.InputObjectType, RecipeAttribute):
    """Arguments to create a recipe"""
    pass

class CreateRecipe(graphene.Mutation):
    """Mutation to create a recipe"""

    recipe = graphene.Field(lambda: RecipeObject, description="Recipe created by this mutation")

    class Arguments:
        input = CreateRecipeInput(required=True)
    
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        recipe = Recipe(**data)
        db.session.add(recipe)
        db.session.commit()

        return CreateRecipe(recipe=recipe)

class UpdateRecipeInput(graphene.InputObjectType, RecipeAttribute):
    """Arguments to update a recipe"""
    id = graphene.ID(required=True, description="Global ID of the recipe")

class UpdateRecipe(graphene.Mutation):
    """Update a recipe"""
    recipe = graphene.Field(lambda: RecipeObject, description="Recipe updated by this mutation")

    class Arguments:
        input = UpdateRecipeInput(required=True)
    
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        
        recipe = db.session.query(Recipe).filter_by(id=data['id'])
        recipe.update(data)
        db.session.commit()
        recipe = db.session.query(Recipe).filter_by(id=data['id']).first()
        
        return UpdateRecipe(recipe=recipe)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_recipes = SQLAlchemyConnectionField(RecipeObject)
    recipe = graphene.relay.Node.Field(RecipeObject)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_recipe = CreateRecipe.Field()
    update_recipe = UpdateRecipe.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)