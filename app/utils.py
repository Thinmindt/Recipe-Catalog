"""Basic utility functions that may be reused across the server.

Includes:
  Conversion from Graphene input object into a Python dictionary
  Filesystem interface functions for image files
"""
from graphql_relay.node.node import from_global_id
import datetime
import uuid
import os
from app.models import Image


def input_to_dictionary(input):
  """Convert Graphene inputs into a dictionary

  Parameters:
    input - from Graphene query
  
  Returns: 
    dictionary formatted for interacting with sqlalchemy
  """
  dictionary = {}
  for key in input:
    # Convert GraphQL global id to database id
    if key[-2:] == 'id':
      input[key] = from_global_id(input[key])[1]
    dictionary[key] = input[key]
  return dictionary

def resolve_image_filepath(filename):
  """Create relative path for an image file from the filename

  Parameters:
    filename - name of the file not including the path
  
  Returns:
    filepath - relative path for an image file
  """
  return os.path.join(".", "images", filename)

def handle_image(image):
  """Save image to disk using timestamp.

  Parameters:
    image - image to save

  Returns:
    imageFilename - name of the file in ./images/
  """
  imageFilename = str(uuid.uuid1())
  imageFilename = imageFilename.replace(' ', '--')
  imageFilename = imageFilename.replace('.', '-')
  imageFilename = imageFilename.replace(':', '-')
  imageFilename = imageFilename + ".png"
  imageFilePath = resolve_image_filepath(filename)

  image.save(imageFilePath)
  return imageFilename

def delete_image(filename):
  """Delete image file using provided filename

  Parameters: 
    filename - name of file not including path
  
  Returns: 
    boolean - True if success, false if fail
  """
  imageFilePath = resolve_image_filepath(filename)
  if os.path.exists(imageFilePath):
    try:
      os.remove(imageFilePath)
      return True
    except OSError as e:
      print("ERROR: %s" % e)
      return False
  print("ERROR: File does not exist")
  return False
  

def delete_images_without_database_reference(dryRun = False):
  """Deletes any files in the server image directory 
  that doesn't have an associated image object reference
  in the database. 
  Use this to clean up the image folder after running 
  tests or periodically in case of server error during 
  image deletion.  

  Parameters:
    dryRun - Set to true if you don't want to actually delete the files
  
  Returns:
    boolean - True if success, false if fail
  """
  #get list of filenames from database
  db_images = Image.query.all()
  db_filenames = [image.filename for image in db_images]
  
  #walk files and delete
  for root, dirs, files in os.walk(os.path.join('.', 'images')):
    for filename in files: 
      if filename not in db_filenames:
        print("%s is not in database. Deleting it." % filename)
        if (not dryRun):
          delete_image(filename)
      else:
        print("%s is in the database. Save it." % filename)