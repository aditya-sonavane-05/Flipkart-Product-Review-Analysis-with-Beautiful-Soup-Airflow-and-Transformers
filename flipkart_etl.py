
import pandas as pd 
import json
from datetime import datetime
import s3fs 
import requests
from bs4 import BeautifulSoup
import emoji

def run_flipkart_etl():
    # Scrape reviews from Flipkart
    flipkart_base_url = "https://www.flipkart.com/apple-iphone-7-jet-black-128-gb/product-reviews/itmen6dakdgkpy6n?pid=MOBEMK62VCQ2UMT8&lid=LSTMOBEMK62VCQ2UMT8IY1JYN&sortOrder=MOST_HELPFUL&certifiedBuyer=false&aid=overall&page="

    # Number of pages you want to scrape from Flipkart
    num_pages =30

    flipkart_all_reviews = []  # List to store all the reviews from Flipkart

    for page in range(1, num_pages+1):
        flipkart_url = flipkart_base_url + str(page)
        flipkart_response = requests.get(flipkart_url)
        flipkart_soup = BeautifulSoup(flipkart_response.text, "html.parser")
        flipkart_reviews = flipkart_soup.find_all("div", class_="_27M-vq")

        for review in flipkart_reviews:
            review_info = review.find_all("p", class_="_2sc7ZR")
            reviewer_name = review_info[0].text.strip()  # Scrape reviewer name
            review_title = review.find("p", class_="_2-N8zT").text.strip()
            review_paragraph = review.find("div", class_="t-ZTKy").text.strip()
            star_rating = review.find("div", class_="_3LWZlK").text.strip()
            review_date = review_info[1].text.strip()  # Scrape review date
            review_paragraph = emoji.demojize(review_paragraph)

            flipkart_all_reviews.append((reviewer_name, review_title, review_paragraph, star_rating, review_date))
    df = pd.DataFrame(flipkart_all_reviews, columns=["Reviewer Name", "Review Title", "Review Paragraph", "Star Rating", "Review Date"])
    df.to_csv("s3://aditya-airflow-proj/something.csv")
