
# Samuel Lajoie, Maxime Gazzé, Miguel Boka et Edgar Pereda Puig
# remplacer le fichier eng.traineddata par https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata
# le ficher ce trouve dans le même folder que tessdata (emplacement relatif à l'ordinateur)
import imutils, cv2, os, requests, sys, env, cadrant, photo, time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from Plaque import getPlateNumber  #quand vous faites 3.c enlever le commentaire
from pymongo import MongoClient
from gpiozero import Button, Buzzer
sys.path.insert(0, '../iteration_1')
from iteration1 import command
from datetime import date

def iterationCode():
    try:
        #Client et collection mangodb
        client = MongoClient("mongodb+srv://gaspard:savoureux@cluster0.qnkai.mongodb.net/Stationnement?retryWrites=true&w=majority")
        db = client.Stationnement
        collection_employees = db.employees
        collection_visites = db.visites

        #Compléter le code ici et appeler le classifieur Haarcascade
        photo.takePlaque()
        img = cv2.imread('plaque.jpg')
        #img = cv2.imread('car5.jpg')
        kernel = cv2.CascadeClassifier('../Data/plaque_russe_haarcascade.xml')

        # Edge detection
        ratio = img.shape[0] / 500.0
        orig = img.copy()
        img = imutils.resize(img, height=500)
        # Convert image to grayscale, blur and find edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)
        # Cropping the image
        contours = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None
        for c in contours:
            # Approximate contours
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            if(len(approx) == 4):
                screenCnt = approx
                break

        if screenCnt is None:
            print("No countour detected")
        else:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)

        (x, y) = np.where(mask == 255)
        (topX, topY) = (np.min(x), np.min(y))
        (bottomX, bottomY) = (np.max(x), np.max(y))
        cropped = gray[topX:bottomX+1, topY:bottomY+1]

        # noise removal
        def remove_noise(img):
            return cv2.medianBlur(img, 5)

        # thresholding
        def thresholding(img):
            return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # dilation
        def dilate(img):
            kernel = np.ones((5, 5), np.uint8)
            return cv2.dilate(img, kernel, iterations=1)

        # erosion
        def erode(img):
            kernel = np.ones((5, 5), np.uint8)
            return cv2.erode(img, kernel, iterations=1)

        cropped =   erode(dilate(thresholding(remove_noise(cropped))))
        cv2.imwrite('cropped.jpg', cropped)
        #Obtiens la matricule et interroge la bd pour vérifier l'existance de l'employé
        matricule = str(getPlateNumber(cropped))
        employe = collection_employees.find_one({"immatriculation": matricule})

        #Renvoie la matricule, le nom complet et l'accès au stationnement d'un employé
        msg ="\n matricule: {} \n employé: {} {} \n access: {}".format(matricule, employe['nom'], employe['prenom'], employe['stationnement'])

        if employe:
            print(msg)
        else:
            print('matricule n\'appartient pas a un employé')

        # la key doit être retourner avec un fichier que vous devez appelez env.py tel quel:
        #def getKey():
        #    return "Mettre_votre_clée_ici"

        #Event avec le bouton choisis
        event_name1 = "send_email"
        key = env.getKey()
        ifttt_hook1 = f"https://maker.ifttt.com/trigger/{event_name1}/with/key/{key}"
        bouton = Button(21)
        buzzer = Buzzer(4)

        command.visite(matricule)

        #Recyclage de l'iteration1 pour obtenir le nombre de visite de la journee
        today = date.today().strftime("%Y-%m-%d")
        nbVisites = str(command.nbVisites("day", today))

        #Permet d'obtenir les digits en string avec a chaque fois un nombre de 4 charactere
        digits = ""
        for digitZero in range(4 - len(nbVisites)):
            digits += "0"

        for digit in range(len(nbVisites)):
            digits += str(nbVisites[digit])

        #envoie un texto et affiche le nombre de visite de la journee
        requests.post(ifttt_hook2)
        return digits
    except:
        return None
