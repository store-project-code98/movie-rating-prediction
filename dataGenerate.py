import selenium
from selenium import webdriver
import requests
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random
import time
import csv

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--incognito") 
# option.add_argument("--headless") headless option

driver = webdriver.Chrome(options=option)
with open('movie_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Review', 'Rating']) 

    url = "https://www.imdb.com/search/title/?groups=top_100"
    driver.get(url)

    for i in range(50):  
        movie_titles = driver.find_elements(By.XPATH, "//a[@class='ipc-title-link-wrapper']")
        
        title = movie_titles[i].find_element(By.XPATH, ".//h3[@class='ipc-title__text']").text
        relative_link = movie_titles[i].get_attribute('href')

        print(f"{i+1}. {title}")
        
        if relative_link.startswith('https://www.imdb.com'):
            full_url = relative_link 
        else:
            full_url = "https://www.imdb.com" + relative_link  
        
        print(f"Full URL: {full_url}")
        
        driver.get(full_url)
        full_url = full_url.split('?')[0]
        
        for rating in range(1, 11): 
            reviews_url = f"{full_url}reviews/?sort=user_rating%2Cdesc&rating={rating}"
            print(f"Reviews URL for rating {rating}: {reviews_url}")
            
            driver.get(reviews_url)
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                spoiler_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='Expand Spoiler']")
                
                for button in spoiler_buttons:
                    try:
                        if button.is_displayed():
                            driver.execute_script("arguments[0].scrollIntoView(true);", button)
                            
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                            
                            driver.execute_script("arguments[0].click();", button)
                            
                            print("Clicked a spoiler button")
                    except Exception as e:
                        print(f"Error clicking spoiler button: {e}")
                
            except Exception as e:
                print(f"Error during the first pass for movie {title} with rating {rating}: {e}")

            try:
                review_count = len(driver.find_elements(By.XPATH, "//div[@class='ipc-html-content-inner-div']"))
                for j in range(review_count): 
                    try:
                        rating_element = driver.find_element(By.XPATH, f"(//span[contains(@class, 'ipc-rating-star--rating')])[{j+1}]")
                        rating_value = rating_element.text if rating_element else "No rating found"
                    except:
                        rating_value = "No rating found"

                    try:
                        review_element = driver.find_element(By.XPATH, f"(//div[@class='ipc-html-content-inner-div'])[{j+1}]")
                        review_content = review_element.text if review_element else "No review content found"
                    except:
                        review_content = "No review content found"
                    
                    print(f"Review {j+1} Rating: {rating_value}/10")
                    print(f"Review {j+1} Content: {review_content}\n")
                    
                    writer.writerow([review_content, rating_value])

            except Exception as e:
                print(f"Error extracting reviews or ratings for movie {title} with rating {rating}: {e}")
        
        driver.get("https://www.imdb.com/search/title/?groups=top_100")

    driver.quit()

def randomize_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows = list(reader)  

    random.shuffle(rows)

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header) 
        writer.writerows(rows) 

input_file = 'movie_reviews.csv' 
output_file = 'imdb_reviews.csv'  

randomize_csv(input_file, output_file)
