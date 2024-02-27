import time
import datetime
import schedule

import matcher
import requests 
#datum = "2024-02-24"

def bettsnotis():
  datum = str(datetime.date.today()+datetime.timedelta(dagar))
  print("\n"+datum) 
  dagensmatcher = matcher.matcher(datum)
  betts = []

  for vilkenMatch in range(len(dagensmatcher)): 
      if abs(int(dagensmatcher[vilkenMatch][4])-int(dagensmatcher[vilkenMatch][5])) > 10:
        a = 2
        b = 3
        if int(dagensmatcher[vilkenMatch][4])<int(dagensmatcher[vilkenMatch][5]):
          a = 3
          b = 2
        vinstsannolikhet = (1 - 1 / (10 ** ((int(dagensmatcher[vilkenMatch][a+2]) - int(dagensmatcher[vilkenMatch][b+2])) / 400) + 1)) * 100
        betts.append([dagensmatcher[vilkenMatch][0],str(dagensmatcher[vilkenMatch][1]), dagensmatcher[vilkenMatch][2], dagensmatcher[vilkenMatch][3], dagensmatcher[vilkenMatch][a], abs(int(dagensmatcher[vilkenMatch][4])-int(dagensmatcher[vilkenMatch][5])), dagensmatcher[vilkenMatch][6], str(round(vinstsannolikhet, 2))])

  betts.sort(key=lambda x: x[7], reverse=True)

  meddelande = ""

  for i in range(len(betts)):
    print(betts[i])
    meddelande += str(
              "\n\n\n"+betts[i][0] +" kl "+ betts[i][1] + 
              "\n" +
              betts[i][2] + "  VS  " + betts[i][3] + 
              "\nBetta på " + betts[i][4] + 
              "\nVinstsannolikhet " + betts[i][7] + "%" + 
              "\nKälla " + betts[i][6])


  requests.post("https://ntfy.sh/betton", 
          data=meddelande.encode('utf-8'), 
          headers={
          "Title": "Betton "+datum, 
          "Icon": "https://passagen.se/wp-content/uploads/2024/01/fordelar-nackdelar-casinosajter-utan-svensk-licens.png",
          "Priority": "urgent",
          "Tags": "soccer"
      })


dagar = 1
# Schedule the job to run every day at 10:00 AM
schedule.every().day.at("10:00").do(bettsnotis)

while True:
  schedule.run_pending()
  time.sleep(60)  # Check every minute

  #pushnotis.skicka("Dagens betts",datum)

  #print(elo.kolla_elo_elorationsnet())