import requests
from bs4 import BeautifulSoup
from io import BytesIO
from google.cloud import vision

def get_text_from_url(cloud_client, _url):
    
    """Downloads an image from a URL and extracts text from it."""
    # Get the URL response
    url_response = requests.get(_url)
    
    # Check if the response is an image
    if 'image/' in url_response.headers['Content-Type']:
        print("Downloading recipe image data...")
        
        # Download the image data from the URL and extract the text with google cloud vision
        image_data = BytesIO(url_response.content)
        recipe_raw_text = text_detect(cloud_client, image_data)
        return recipe_raw_text
    else:
        print("Downloading recipe text from URL...")
        soup = BeautifulSoup(url_response.content, 'html.parser')
        recipe_page_body = soup.body
        recipe_raw_text = recipe_page_body.get_text()
    
    return recipe_raw_text
        
def text_detect(cloud_client, image_data):
    """Extracts text from an image."""
    
    print("Extracting text from image...")
    image = vision.Image(content=image_data.read())
    response = cloud_client.text_detection(image=image)
    texts = response.text_annotations
    text_list = []
    for text in texts:
        text_list.append(text.description)

    if response.error.message:
        print(response.error.message)
        return None
    else:
        return " ".join(text_list)

