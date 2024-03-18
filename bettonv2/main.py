#Fixa så att den skickar bettsen en timme innan

import time
import datetime
import schedule

import matcher
import requests 
#datum = "2024-02-24"

def bettsnotis(betts, tips):
  
  #Kollar hur bra bettsen var
  gårdagensmatchermedresultat = matcher.gårdagensmatcher(str(datetime.date.today()+datetime.timedelta(-1)), betts)
  totalvinst = 0
  for match in range(len(gårdagensmatchermedresultat)): 
    if gårdagensmatchermedresultat[match] == betts[match][4]:
      totalvinst += 1

  #räknar ut effektivitet
  endagsvinst = totalvinst/len(betts)
  tips += len(betts)

  sjudagars.pop(0)
  sjudagars.append(endagsvinst)
  mavinst = round(sum(sjudagars)/7,2)

  datum = str(datetime.date.today()+datetime.timedelta(1))
  dagensmatcher = matcher.matcher(datum)

  #Sätter nya betts
  betts = []

  for vilkenMatch in range(len(dagensmatcher)): 
      if abs(int(dagensmatcher[vilkenMatch][4])-int(dagensmatcher[vilkenMatch][5])) > 10:
        a = 2
        b = 3
        if int(dagensmatcher[vilkenMatch][4])<int(dagensmatcher[vilkenMatch][5]):
          a = 3
          b = 2
        vinstsannolikhet = (1 - 1 / (10 ** ((int(dagensmatcher[vilkenMatch][a+2]) - int(dagensmatcher[vilkenMatch][b+2])) / 400) + 1)) * 100
        if vinstsannolikhet >= 60:
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
    

  meddelande += str(
              "\n\n\nResultat en dag: " + str(endagsvinst*100) + "%" +
              "\nSju dagars vinst: " + str(round(mavinst*100,2)) + "%")

  print(meddelande)
  requests.post("https://ntfy.sh/betton", 
          data=meddelande.encode('utf-8'), 
          headers={
          "Title": "Betton "+datum, 
          "Icon": "https://passagen.se/wp-content/uploads/2024/01/fordelar-nackdelar-casinosajter-utan-svensk-licens.png",
          "Priority": "urgent",
          "Tags": "soccer"
      })

endagsvinst = 0
tips = 0
sjudagars = [0,0,0,0,0,0,0]

betts = [['Europa League', '17:45', 'Rangers', 'Benfica', 'Benfica', 369, 'web', '67.0%'], ['League Two', '20:00', 'Salford City', 'Stockport County', 'Stockport County', 328, 'csv', '65.58']]

bettsnotis(betts, tips)


#schedule.every().day.at("23:55").do(bettsnotis(betts, tips, lifetimevinst, mavinst))

while True: 
  #schedule.run_pending()
  #bettsnotis(betts, tips, lifetimevinst, mavinst)
  time.sleep(86400) #Var 24 timme
  