import requests
from bs4 import BeautifulSoup
import tweepy
import pandas as pd
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Function to fetch top papers from Hugging Face
def fetch_top_papers_huggingface():
    url = "https://huggingface.co/papers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    papers = []
    for paper in soup.find_all('div', class_='paper-card')[:5]:
        title = paper.find('h4').text.strip()
        papers.append({"title": title})
    return papers

# Function to create a table image
def create_table_image(data):
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    plt.title("Top 5 AI Papers", fontsize=16)
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0.2)
    img_buffer.seek(0)
    return Image.open(img_buffer)

# Function to post to Twitter
def post_to_twitter(image_path, message):
    # Set up your Twitter API credentials
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    # Authenticate with Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Post the tweet with the image
    api.update_status_with_media(status=message, filename=image_path)

# Main script
if __name__ == "__main__":
    # Fetch top papers
    papers = fetch_top_papers_huggingface()

    # Create table image
    table_image = create_table_image(papers)
    
    # Save the image temporarily
    image_path = "top_papers_table.png"
    table_image.save(image_path)

    # Post to Twitter
    message = "Check out the top 5 AI papers from Hugging Face! #AI #MachineLearning"
    post_to_twitter(image_path, message)

    print("Tweet posted successfully!")