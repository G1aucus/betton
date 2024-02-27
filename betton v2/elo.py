import requests
from bs4 import BeautifulSoup
import time
import csv

def kolla_elo(lag):
    "Kollar elo för laget"
    elo = 0
        # Specify the URL of the website you want to scrape
    url = 'http://clubelo.com/'+lag.replace(" ", "")
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Specify the class of the elements you want to scrape
        target_class = 'astblatt'

        # Find the first element with the specified class
        first_element_with_class = soup.find(class_=target_class)

        # Check if the element is found
        if first_element_with_class:
            # Extract the content inside the first <b> tag within the element
            bold_text = first_element_with_class.find('b')
            
            # Print the text content of the first <b> tag
            if bold_text:
                elo = bold_text.text
                return elo
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}, url: {url}")
    return "error"


def elo_csv(lag):
    csv_file = csv.reader(open('C:/Users/carll/Desktop/betton v2/ELO lag.csv', "r",encoding="utf-8-sig"), delimiter=",")
    for row in csv_file:
        if lag == row[0]:
            print(row)
            return row[1]


def kolla_elo_elorationsnet():
    "Kollar elo för laget"
    elo = {}
        # Specify the URL of the website you want to scrape
    url = 'https://www.eloratings.net'
    response = requests.get(url)
    time.sleep(3)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first element with the specified class
        lag_alla = soup.find_all(class_="maintable slickgrid_219313 ui-widget")
        print(soup)
        for lag in lag_alla:
            vilketlag = lag.find(class_='slick-cell l1 r1 team-cell  narrow-layout')
            lagetselo = lag.find(class_='slick-cell l2 r2 rating-cell  narrow-layout')

            # Print the text within 'date' and 'time' classes
            if vilketlag and lagetselo:
                for lag_class, elo_class in zip(vilketlag, lagetselo):
                    lagtext = lag_class.text.strip()
                    elotext = elo_class.text.strip()
                    
                    elo[lagtext] = elotext  
            else:
                print("How about no... Again :(")
        return elo
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return "error"