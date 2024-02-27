import requests
import elo
from bs4 import BeautifulSoup


def matcher(datum):
    "Hittar vem som spelar på BBC"
    allt = []
    # Specify the URL of the website you want to scrape
    url = 'https://www.bbc.com/sport/football/scores-fixtures/'+datum
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')


##Den vill inte hitta alla lagen som spelar utan tar bara det första laget i listan


        # Find all classes with the name 'match'
        matches = soup.find_all(class_='qa-match-block')
        # Find and print the text within 'date' and 'time' classes within each 'match' class
        for matcher in matches:
            lag = matcher.find_all("span",class_='gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc')
            
            lag1flera = lag[0]
            lag2flera = lag[1]
            tidflera = matcher.find_all(class_='sp-c-fixture__number sp-c-fixture__number--time')
            liga = matcher.find(class_='gel-minion sp-c-match-list-heading')
            ligatext = liga.text.strip()
            # Print the text within 'date' and 'time' classes
            if lag1flera and lag2flera:
                
                for lag1_class, lag2_class, tid_class in zip(lag1flera, lag2flera, tidflera):
                    lag1text = lag1_class.text.strip()
                    lag2text = lag2_class.text.strip()
                    tidtext = tid_class.text.strip()
                    
                    if tidtext != "ft":
                        print(lag1text,lag2text)

                        elo1 = elo.elo_csv(lag1text)
                        elo2 = elo.elo_csv(lag2text)
                        källa = "csv"
                        if None == elo1 or None == elo2:
                            elo1 = elo.kolla_elo(lag1text)
                            elo2 = elo.kolla_elo(lag2text)
                            källa = "web"
                        if None != elo1 and None != elo2 and "error" != elo1 and "error" != elo2:
                            matchlista = [ligatext, tidtext,lag1text,lag2text, elo1, elo2, källa]
                            allt.append(matchlista)  
            else:
                print("How about no... :)")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return allt