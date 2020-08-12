import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_file_upload.scalars import Upload
from app.models import Recipe, Image
from app import db
import app.utils as utils
import datetime

class RecipeAttribute:
    title = graphene.String(description="Title of the Recipe")
    category = graphene.String(description="Classification of Recipe")
    source_type = graphene.String(description="Source type: Book or Website")
    web_link = graphene.String(description="Link to source page")
    book_title = graphene.String(description="Title of the book containing the recipe")
    book_page = graphene.Int(description="Page number the recipe is on")
    rating = graphene.Int(description="The rating given by the user")
    notes = graphene.String(description="Any comments or notes")

class RecipeObject(SQLAlchemyObjectType, RecipeAttribute):
    """Recipe Node"""
    class Meta:
        model = Recipe
        interfaces = (graphene.relay.Node, )

class CreateRecipeInput(graphene.InputObjectType, RecipeAttribute):
    """Arguments to create a recipe"""
    bookImage = Upload(required=False)
    recipeImages = Upload(required=False)

class CreateRecipe(graphene.Mutation):
    """Mutation to create a recipe"""

    recipe = graphene.Field(lambda: RecipeObject, description="Recipe created by this mutation")

    class Arguments:
        input = CreateRecipeInput(required=True)
    
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        print(input)

        images = []
        # Handle recipe images. If it is a list, save all. If singleton, save it.
        if ('recipeImages' in data.keys() and type(data['recipeImages']) is list):
            for recipe_image in data['recipeImages']:
                if recipe_image:
                    image_filename = utils.handle_image(recipe_image)
                    images.append(Image(filename=image_filename, 
                                        date_added=datetime.datetime.now()))
            data.pop('recipeImages')
        elif ('recipeImages' in data.keys() and not type(data['recipeImages']) is None):
            images.append(Image(filename=utils.handle_image(data['recipeImages'])))
            data.pop('recipeImages')
        
        if ('bookImage' in data.keys() and not data['bookImage'] is None):
            data['book_image_path'] = utils.handle_image(data['bookImage'])
            data.pop('bookImage')
        
        recipe = Recipe(**data)
        # add relationship to images saved above
        recipe.images = images

        db.session.add(recipe)
        db.session.commit()

        return CreateRecipe(recipe=recipe)

class UpdateRecipeInput(graphene.InputObjectType, RecipeAttribute):
    """Arguments to update a recipe"""
    id = graphene.ID(required=True, description="Global ID of the recipe")
    bookImage = Upload(required=False)
    recipeImages = Upload(required=False)

class UpdateRecipe(graphene.Mutation):
    """Update a recipe"""
    recipe = graphene.Field(lambda: RecipeObject, description="Recipe updated by this mutation")

    class Arguments:
        input = UpdateRecipeInput(required=True)
    
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        print("Updating Recipe")
        print("input: %s" % input)
        images = []
        # Handle recipe images. If it is a list, save all. If singleton, save it.
        if ('recipeImages' in data.keys() and type(data['recipeImages']) is list):
            for recipe_image in data['recipeImages']:
                if recipe_image:
                    image_filename = utils.handle_image(recipe_image)
                    images.append(Image(filename=image_filename, 
                                        date_added=datetime.datetime.now()))
            data.pop('recipeImages')
        elif ('recipeImages' in data.keys() and not type(data['recipeImages']) is None):
            images.append(Image(filename=utils.handle_image(data['recipeImages'])))
            data.pop('recipeImages')
        
        if ('bookImage' in data.keys() and not data['bookImage'] is None):
            data['book_image_path'] = utils.handle_image(data['bookImage'])
        
        data.pop('bookImage')
        
        recipe = db.session.query(Recipe).filter_by(id=data['id'])
        recipe.update(data)
        db.session.commit()

        recipe = db.session.query(Recipe).filter_by(id=data['id']).first()
        for image in images:
            print(image)
            recipe.images.append(image)
        db.session.commit()

        return UpdateRecipe(recipe=recipe)

class DeleteRecipeInput(graphene.InputObjectType):
    """Arguments to delete a recipe. Only requires ID"""
    id = graphene.ID(required=True, description="Global ID of the recipe")

class DeleteRecipe(graphene.Mutation):
    """Delete a recipe"""
    ok = graphene.Boolean()

    class Arguments:
        input = DeleteRecipeInput(required=True)
    
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        recipe = db.session.query(Recipe).filter_by(id=data['id']).first()
        db.session.delete(recipe)
        db.session.commit()

        return DeleteRecipe(ok=True)
