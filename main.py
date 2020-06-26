from random import randint
from random import choice
import sys
import names

# 10 | 100 | 1000 | 10000
symbole = ['♥','♠','♣','♦']
carteVierge = {"number": 0, "symbole": "x", "write": 'x'}

listesGenerate = []
maxPlayer = 5
minSold = 1000
maxSold = 5000
listesPlayers = {'user': {}, "player": []}

def showCartes(listeCartes):
    ligne1, ligne2, ligne3, ligneBase = "", "", "", ""
    for carte in listeCartes:
        ligne1 += "┌─────"+str(listeCartes[0]["write"])+"──┐"
        ligne2 += "│     "+str(listeCartes[0]["symbole"])+"    │"
        ligne3 += "└──"+str(listeCartes[0]["write"])+"─────┘"
        ligneBase += "│          │"


    print(ligne1)
    print(ligneBase)
    print(ligneBase)
    print(ligne2)
    print(ligneBase)
    print(ligneBase)
    print(ligne3)

def generateCarte(nbCarte = 2):
    listeCarte = []
    for i in range(nbCarte):
        global symbole, listesGenerate
        myCarte = {"number": randint(1, 13), "symbole": choice(symbole) }
        if len(listesGenerate) < 52:
            for cartes in listesGenerate:
                if myCarte["symbole"] == cartes["symbole"]: # +10
                    if (myCarte["number"]) == (cartes["number"]):
                        myCarte = generateCarte(1)[0]
        if myCarte["number"] > 10:
            if myCarte["number"] == 11:
                myCarte["write"] = "─V"+myCarte["symbole"]
            elif myCarte["number"] == 12:
                myCarte["write"] = "─D"+myCarte["symbole"]
            else:
                myCarte["write"] = "─R"+myCarte["symbole"]
        elif myCarte["number"] == 10:
            myCarte["write"] = "10"+myCarte["symbole"]
        else:
            myCarte["write"] = "─"+str(myCarte["number"])+myCarte["symbole"]
        listesGenerate.append(myCarte)
        listeCarte.append(myCarte)
    return listeCarte


def menu():
    global maxPlayer, minSold, maxSold, listesPlayers
    print("      |=====================|")
    print("|=====|                     |=====|")
    print("|                                 |")
    print("|               POKER             |")
    print("|                                 |")
    print("|=====|                     |=====|")
    print("      |=====================|")
    print("      |                     |")
    print("      |      (1) Solo       |")
    print("      |      (2) Multi      |")
    print("      |      (3) Leave      |")
    print("      |                     |")
    print("      =======================")
    choix = input('Entrez votre choix: ')
    if choix == '2':
        print("Le choix n'est pas accessible")
        menu()
    elif choix == '1':
        while True:
            choix = input('Nb de player (1 - '+str(maxPlayer)+') ')
            if choix.isnumeric() == False: 
                continue
            elif int(choix) < 1 or int(choix) > maxPlayer:
                continue
            else:
                sold = randint(minSold, maxSold)
                for i in range (int(choix)):
                    listesPlayers["player"].append({"name": names.get_full_name(), "sold": sold, id: i,"partie":[], "tauxRelance":5, "tauxCoucher":2})
                while True:
                    name = input('Entrez un nom: ')
                    if len(name) > 2:
                        end = True
                        for player in listesPlayers["player"]:
                            if player["name"] == name:
                                end = False
                        if end == True: 
                            listesPlayers["user"] = {"name": name, "sold": sold, "partie":[]}
                            break
                break
        game()
    elif choix == '3':
        sys.exit(0)
    else:
        menu()

def menuPlayer(partie):
    global listesPlayers
    print("=======================")
    print("|                     |")
    print("|  Name:"+listesPlayers["user"]["name"]+"        |")
    print("|  Sold:"+str(listesPlayers["user"]["sold"])+"€         |")
    print("|   Pot:"+str(partie["pot"])+"€            |")
    print("| Cagnotte:"+str(partie["cagnotte"])+"€         |")
    print("|                     |")
    print("=======================")
    print("|                     |")
    print("|      (0) Mes cartes |")
    # print("|      (1) Check      |")
    print("|      (1) Suivre     |")
    # print("|      (3) Relance    |")
    print("|      (2) Coucher    |")
    print("|                     |")
    print("=======================")
    while True:
        choix = input("Entrez votre choix: ")
        if choix == '0':
            showCartes(listesPlayers["user"]["partie"][partie["id"]-1]["carte"])
            continue
        elif choix == '1':
            listesPlayers["user"]["sold"] -= partie["pot"]
            print("Votre sold est actuellement de:"+str(listesPlayers["user"]["sold"])+"€")
            return True
        elif choix == '2':
            print('Vous vous etes coucher')
            return False
        else:
            continue


def partie(numPartie):
    global listesPlayers
    listesPlayers["user"]["partie"].append({"carte": generateCarte(), "miseTotal": 0, "gainTotal": 0, "isWin":False ,"down": False})
    for player in listesPlayers["player"]:
        player["partie"].append({"carte": generateCarte(), "miseTotal": 0, "gainTotal": 0, "isWin":False, "down": False})
    partie = {"id": numPartie, "pot":0, "cagnotte":0, "coucher": [], "carte": []}
    for manche in range(4):
        choix = menuPlayer(partie)
        if choix == False:
            return False
        for player in listesPlayers["player"]:
            if player ["tauxRelance"] > randint(0, 100):
                prime = randint(100, 300)
                print('Relance de '+player["name"]+" pour un montant de " +str(prime)+"€")
                player["sold"] -= prime
                partie["pot"] += prime
                choix = menuPlayer(partie)
                if choix == False:
                    return False
                else:
                    listesPlayer["user"]["sold"] -= prime
                    partie["pot"] += prime
                    print('Vous avez suivie de '+str(prime)+'€')
            elif player ["tauxCoucher"] > randint(0, 100):
                partie["coucher"].append(player)
        partie["cagnotte"] += partie["pot"]
        partie["pot"] = 0
        if manche == 1:
            partie["carte"] = generateCarte(3)
            showCartes(partie["carte"])
        elif manche == 2:
            partie["carte"].append(generateCarte(1))
            showCartes(partie["carte"])
        elif manche == 3:
            partie["carte"].append(generateCarte(1))
            showCartes(partie["carte"])    



def game():
    global listesPlayers
    nbPartie = 1
    while True:
        finish = False 
        if (len(listesPlayers["player"])+1) == 1:
            finish = True
        if finish == True:
            break
        partie(nbPartie)
        nbPartie += 1
        break
    

menu()


