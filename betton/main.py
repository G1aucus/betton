#betton
#Carl Larsson
#v0.0.1

import funktioner
import slack
from itertools import islice

import schedule
import time

def dagens_matcher_med_odds():
    return 

match_fran_nu = 4

#datum, hemma, borta, oddshemma, oavgjort, oddsborta, ranking = funktioner.csvlas()

#rankingtop10 = list(islice(ranking.keys(), 5))
    
dagensbett = 1
def skicka_meddelande(): #for dagensbett in rankingtop10:
    matchText = "ManCity"+" vs "+"RealMadrid"
    medelande = funktioner.räkna_betts("ManCity","RealMadrid", 1, 1,0)
    #medelande = funktioner.räkna_betts(hemma[dagensbett],borta[dagensbett], oddshemma[dagensbett], oddsborta[dagensbett],oavgjort[dagensbett])
    slack.skicka_notis(matchText,medelande[0],medelande[1],medelande[2])


#def kolla_dagens_matcher():


# Schedule the task to run every day at a specific time (e.g., 3:00 AM)
#schedule.every().day.at("15:00").do(skicka_meddelande)

while True:
    # Run pending scheduled tasks
    #schedule.run_pending()
    skicka_meddelande()
    time.sleep(60)
    # Sleep for a while to avoid high CPU usage
    #time.sleep(1)