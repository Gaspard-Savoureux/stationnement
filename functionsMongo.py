# Samuel Lajoie, Maxime Gazzé, Miguel Boka et Edgar Pereda Puig
# Lancer le code avec python3 -i iteration1.py
# Les différentes commandes sont:
# command.createUpdate()
# command.stationnement()
# command.visite()
# command.nbVisites(cible) e.g command.nbVisites("employe") | command.nbVisites("day") | command.nbVisites("week") | command.nbVisites("month")
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import re

client = MongoClient("mongodb+srv://gaspard:savoureux@cluster0.qnkai.mongodb.net/Stationnement?retryWrites=true&w=majority")
db = client.Stationnement
collection_visites = db.visites
collection_employees = db.employees

class iteration1:

    #fonction pour créé ou mettre à jour un utilisateur
    def createUpdate(self):
        action = input('Create or Update? insert C or U: ')

        prenom = input('Entrez le prenom: ')
        nom = input('Entrez le nom: ')

        myQuery = {"nom": nom, "prenom": prenom}

        existant = collection_employees.find_one(myQuery)

        #Message erreur
        if ((action == 'U' or action == 'u') and not existant):
            print('employé inexistant')
        elif ((action == 'C' or action =='c') and existant):
            print('employé existant')

        if ((action == 'C' or action =='c') and not existant):
            #create employe(e)
            dept = input('Entrez le departement: ')
            poste = input('Entrez le poste: ')
            stationnement = bool(input('Stationnement  true/false: '))
            immatriculation = input('Entrez l\'immatriculation du vehicule : ')
            collection_employees.insert_one(
                {"nom": nom,
                "prenom": prenom,
                "departement": dept,
                "poste": poste,
                "stationnement": stationnement,
                "immatriculation": immatriculation})
        elif ((action == 'U' or action == 'u') and existant):
            #update employe(e) aux options répondues par "y"
            changeNom = input('Changez le nom? y/n: ')
            if changeNom == 'y' or changeNom == 'Y':
                nom = input('Entrez le nom: ')
                collection_employees.update_one(myQuery, {"$set": { "nom": nom }})

            changePrenom = input('Changez le prenom? y/n: ')
            if changePrenom == 'y' or changePrenom == 'Y':
                prenom = input('Entrez le nom: ')
                shit = collection_employees.update_one(myQuery, {"$set": { "prenom": prenom }})
                print(shit)

            changeDept = input('Changez le departement? y/n: ')
            if changeDept == 'y' or changeDept == 'Y':
                dept = input('Entrez le departement: ')
                collection_employees.update_one(myQuery, {"$set": { "departement": dept }})

            changePoste = input('Changez le poste? y/n: ')
            if changePoste == 'y' or changePoste == 'Y':
                poste = input('Entrez le poste: ')
                collection_employees.update_one(myQuery, {"$set": { "poste": poste }})

            changeStationnement = input('Changez le status du stationnement? y/n: ')
            if changeStationnement == 'y' or changeStationnement == 'Y':
                stationnement = str(input('Stationnement  true/false: ')).lower()
                if(stationnement == 'false'):
                    stationnement = False
                else:
                    stationnement = True
                collection_employees.update_one(myQuery, {"$set": { "stationnement": stationnement }})

            changeImmatri = input('Changez l\'immatriculation? y/n: ')
            if changeImmatri == 'y' or changeImmatri == 'Y':
                immatriculation = input('Entrez l\'immatriculation du vehicule : ')
                collection_employees.update_one(myQuery, {"$set": { "immatriculation": immatriculation }})

    #Fonction qui retourne les informations conçernant le stationnement d'un véhicule selon son immatriculation
    def stationnement(self):
        immatricule = input('Immatriculation: ')

        user = collection_employees.find_one({"immatriculation": immatricule})

        if user:
            prenom = user["prenom"]
            nom = user["nom"]
            stationnement = user["stationnement"]

            print('employe: %s %s \naccess: %r' %(prenom, nom, stationnement))
        else:
            print('employe inexistant')

    #Fonction qui cummul les visites
    def visite(self, immatricule):
        #immatricule = input('Immatriculation de la personne visitante: ').upper()
        immatricule = immatricule.upper()
        reg = '[A-Z][0-9]{3}[A-Z]{2}'
        match = re.search(reg, immatricule)
        if match is None: return "matricule non conforme"
        now = datetime.now().strftime("%Y-%m-%d")

        myQuery1 = {"immatriculation": immatricule}
        myQuery2 = {"immatriculation": immatricule, "date": now}

        employee_exist = collection_employees.find_one(myQuery1)
        visites_exist = collection_visites.find(myQuery2)

        condition1 = employee_exist != None and visites_exist == None
        condition2 = employee_exist != None and visites_exist != None

        if(condition1):
            #créer une première visite si un(e) employé(e) existe et que c'est ça première visite
            collection_visites.insert_one({ "date": now, "visites": 1, "immatriculation": immatricule})
        elif(condition2):
            #Si un(e) employé(e) existe et qu'il a déjà visité
            visite = {"date": "2001-01-01"}
            for i in range(collection_visites.count_documents(myQuery2)):
                date1 = datetime.strptime(visites_exist[i]["date"], "%Y-%m-%d")
                date2 = datetime.strptime(visite["date"], "%Y-%m-%d")
                if( date1 > date2):
                    visite = visites_exist[i]

            if(visite["date"] == now):
                #si l'employé(e) visite le stationnement à nouveau dans une même journée, effectue la mise à jour
                collection_visites.update_one(myQuery2, {"$set": { "visites": (visite["visites"] + 1) }})
            elif(visite["date"] != now):
                #Si l'employé(e) visite le stationnement pour la première fois une nouvelle journée, crée une nouvelle entrez
                collection_visites.insert_one({ "date": now, "visites": 1, "immatriculation": immatricule})
        return "l'employé(e) n'existe probablement pas"
    #Fonction qui retourne le nombre de visites selon le critère ciblé
    def nbVisites(self, option, cibleDate):
        #msg = "Entrez la date de la journée désiré (ex:2001-01-01)(yyyy-mm-dd): "
        #Code si l'option choisie est "employe"
        if(option == "employe"):
            matricule = input("Entrez le matricule de la personne ciblé: ")
            myQuery = {"immatriculation": matricule}
            listMatricules = collection_visites.find(myQuery)
            nbVisites = 0
            for i in range(collection_visites.count_documents(myQuery)):
                nbVisites += int(listMatricules[i]["visites"])
            print("Le nombre total de visite: ", nbVisites)
            return nbVisites
        #Code si l'option choisie est "day"
        elif(option == "day"):
            #day = input(msg)
            myQuery = {"date": cibleDate}
            listDay = collection_visites.find(myQuery)
            nbVisites = 0
            for i in range(collection_visites.count_documents(myQuery)):
                nbVisites += int(listDay[i]["visites"])
            print("Le nombre total de visite: ", nbVisites)
            return nbVisites
        #Code si l'option choisie est "week"
        elif(option == "week"):
            day = cibleDate.split("-")
            myQuery = {
                "date": {
                "$regex": day[0] + "-" + day[1],
                "$options" :'i' # case-insensitive
                }
            }
            listDay = collection_visites.find(myQuery)
            nbVisites = 0
            for i in range(collection_visites.count_documents(myQuery)):
                current_day = datetime.strptime(listDay[i]["date"], "%Y-%m-%d")
                firstDay = datetime.strptime("-".join(day), "%Y-%m-%d")
                td = timedelta(7)
                lastDay = firstDay + td
                if(current_day >= firstDay and current_day <= lastDay):
                    nbVisites += int(listDay[i]["visites"])
            print("Le nombre total de visite pendant la semaine du ", day, ": ", nbVisites)
            return nbVisites
        #Code si l'option choisie est "month"
        elif(option == "month"):
            day = cibleDate.split("-")
            myQuery = {
                "date": {
                "$regex": day[0] + "-" + day[1],
                "$options" :'i' # case-insensitive
                }
            }
            listDay = collection_visites.find(myQuery)
            nbVisites = 0
            for i in range(collection_visites.count_documents(myQuery)):
                nbVisites += int(listDay[i]["visites"])
            print("Le nombre total de visite pendant le mois,", day[1], ": ", nbVisites)

command = iteration1()
