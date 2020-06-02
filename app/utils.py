from graphql_relay.node.node import from_global_id

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

def handle_image(image):
  """Save image to disk using timestamp.

  Parameters:
    image - image to save

  Returns:
    imageFilename - name of the file in ./images/
  """
  imageFilename = str(datetime.datetime.now())
  imageFilename = imageFilename.replace(' ', '--')
  imageFilename = imageFilename.replace('.', '-')
  imageFilename = imageFilename.replace(':', '-')
  imageFilename = imageFilename + ".png"
  imageFilePath = "./images/" + imageFilename

  image.save(imageFilePath)
  return imageFilename