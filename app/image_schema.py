import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_file_upload.scalars import Upload
from app.models import Image
from app import db
import app.utils as utils

class ImageAttribute:
    filename = graphene.String(description="File name in image folder")
    id_recipe = graphene.ID(description="Global ID of associated recipe")
    date_added = graphene.DateTime(description="Date the image was added")

class ImageObject(SQLAlchemyObjectType, ImageAttribute):
    """ Image node """
    class Meta:
        model = Image
        interfaces = (graphene.relay.Node, )

class DeleteImageInput(graphene.InputObjectType):
    """Arguments to delete an image. Only requires the ID."""
    id = graphene.ID(required=True, description="Global ID of the image")

class DeleteImage(graphene.Mutation):
    """Delete Image"""
    ok = graphene.Boolean()

    class Arguments:
        input = DeleteImageInput(required=True)
    
    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        image = db.session.query(Image).filter_by(id=data['id']).first()
        
        print("Deleting image: %s" % image)
        db.session.delete(image)
        db.session.commit()

        return DeleteImage(ok=True)