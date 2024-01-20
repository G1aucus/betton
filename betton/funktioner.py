import requests
from bs4 import BeautifulSoup
#import csv


def kolla_elo(lag):
    "Kollar elo för laget"
    elo = 0
        # Specify the URL of the website you want to scrape
    url = 'http://clubelo.com/'+lag
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
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    return "error"

def make_betting_decision(diff_team1, diff_team2, lag1, lag2):
    # Make a betting decision based on the differences
    if diff_team1 > diff_team2:
        return "Betta på " + str(lag1)
    elif diff_team1 < diff_team2:
        return "Betta på "  + str(lag2)
    else:
        return "Ingen tydlig rekomendation"

def calculate_expected_probability(elo_team1, elo_team2, odds_team1, odds_team2):
    # Calculate the expected probability based on Elo ratings and odds
    expected_prob_team1 = 1 / (1 + 10**((elo_team2 - elo_team1) / 400))
    expected_prob_team2 = 1 / (1 + 10**((elo_team1 - elo_team2) / 400))

    # Normalize the probabilities based on the provided odds
    norm_factor = 1 / (1 / expected_prob_team1 + 1 / expected_prob_team2)

    norm_prob_team1 = expected_prob_team1 / norm_factor
    norm_prob_team2 = expected_prob_team2 / norm_factor

    # Calculate implied probabilities from odds
    implied_prob_team1 = 1 / odds_team1
    implied_prob_team2 = 1 / odds_team2

    # Calculate the difference between implied and expected probabilities
    diff_team1 = norm_prob_team1 - implied_prob_team1
    diff_team2 = norm_prob_team2 - implied_prob_team2

    return norm_prob_team1, norm_prob_team2, implied_prob_team1, implied_prob_team2, diff_team1, diff_team2


#def csvlas():
    # Specify the file path
    file_path = 'C:/Users/carll/Documents/betton/fixtures.csv'

    datum = []
    hemma = []
    borta = []
    oddshemma = []
    oddsborta = []
    oavgjort = []

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Iterate through each row in the CSV file
        for row in csv_reader:                                                      #ta bort den första raden och de sista.
            datum.append(row[0])
            hemma.append(row[2])
            borta.append(row[3])
            oavgjort.append(float(row[10]))
            oddshemma.append(float(row[11])+float(row[12])+float(row[13])+float(row[14])+float(row[15])+float(row[16]))
            oddsborta.append(float(row[4])+float(row[5])+float(row[6])+float(row[7])+float(row[8])+float(row[9]))
    
    ranking = {}

    for pos in range(len(oddsborta)):
        lag = ""
        lag = pos
        if oddshemma[pos] < oddsborta[pos]:
            ranking[lag] = oddsborta[pos] - oddshemma[pos]
        else:
            ranking[lag] = oddshemma[pos] - oddsborta[pos]
    
    sorted_ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))

    return datum, hemma, borta, oddshemma, oavgjort, oddsborta, sorted_ranking

def räkna_betts(lag1, lag2, odds_team1, odds_team2, odds_ingen):
    "main för att räkna betts"
    print(lag1,"vs", lag2)
    meddelande = ""
    elo_team1 = 0
    elo_team2 = 0

    team1 = lag1.replace(' ', '')
    team2 = lag2.replace(' ', '')

    try:
        elo_team1 = int(kolla_elo(team1))
        elo_team2 = int(kolla_elo(team2))
    except:
        elo_team1 = 1
        elo_team2 = 1

    result = calculate_expected_probability(elo_team1, elo_team2, odds_team1, odds_team2)

    print("Elo:")
    print("Team 1:", elo_team1)
    print("Team 2:", elo_team2)

    print("\nNormalized Probabilities:")
    print("Team 1:", result[0])
    print("Team 2:", result[1])

    print("\nImplied Probabilities from Odds:")
    print("Team 1:", result[2])
    print("Team 2:", result[3])

    print("\nDifference (Expected - Implied):")
    print("Team 1:", result[4])
    print("Team 2:", result[5])

    # Make a betting decision
    betting_decision = make_betting_decision(result[4], result[5], team1, team2)
    print("\nBetting Decision:", betting_decision)
    
    if elo_team1 != 1 or elo_team2 != 1:
        dataText = str(team1)+": "+str(elo_team1)+"\n"+str(team2)+": "+str(elo_team2)
    else:
        dataText = "Hittar ingen elo. :("
    normsanText = str(team1)+": "+str(round(odds_team1*100, 3))+"\nOavgjort: "+str(round(odds_ingen*100, 3))+"\n"+str(team2)+": "+str(round(odds_team2*100, 3))
    bettText = betting_decision

    return dataText, normsanText, bettText