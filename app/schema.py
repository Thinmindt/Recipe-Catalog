import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models import User, Recipe
from app import db
from typing import Union

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )

class RecipeObject(SQLAlchemyObjectType):
    class Meta:
        model = Recipe
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

class CreateRecipe(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        type = graphene.String(required=True)
        web_link = graphene.String()
        book_title = graphene.String()
        book_page = graphene.Int()
        book_picture = graphene.String()
        notes = graphene.String()
        rating = graphene.Int()
    
    recipe = graphene.Field(lambda: RecipeObject)

    def mutate(self, info, title, type, web_link, 
               book_title, book_page, book_picture, 
               notes, rating):
        recipe = Recipe(title=title, type=type, web_link=web_link, 
                        book_title=book_title, book_page=book_page,
                        book_image_path=book_picture, notes=notes, 
                        rating=rating)
        db.session.add(recipe)
        db.session.commit()
        return CreateRecipe(recipe=recipe)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_users = SQLAlchemyConnectionField(UserObject)
    all_recipes = SQLAlchemyConnectionField(RecipeObject)
    recipe = graphene.Field(
        RecipeObject,
        recipeId = graphene.Argument(type=graphene.String, required=False)
    )

    @staticmethod
    def resolve_recipe(args, info, recipeId: Union[int, None] = None):
        query = RecipeObject.get_query(info=info)
        
        if recipeId:
            query.filter(Recipe.id == recipeId)
        
        recipe = query.first()
        return recipe

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_recipe = CreateRecipe.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)