try:
        from  PIL  import  Image
except  ImportError:
        import  Image
import  pytesseract
import  re
def  getPlateNumber(img):
    text  =  pytesseract.image_to_string(img,  config="--psm  11")
    print('le texte vu par pytesseract ', text);
    #Trouve si la chaîne renvoyé par text contient une suite dans l'ordre suivant: une lettre suivie de 3 chiffres et finissant par 2 chiffres
    # Plaque Russe
    #reg = '[A-Z][0-9]{3}[A-Z]{2}'
    # Plaque QC
    #TODO adapter avec les possibilités suivantes:
    # https://saaq.gouv.qc.ca/immatriculation/categories-plaques-immatriculation
    reg = '[A-Z0-9]{3}\s[A-Z0-9]{3}'

    match = re.search(reg, text.upper())
    print('match: ', match)
    matricule = match.group()
    return matricule
if  __name__  ==  "__main__":
        print(getPlateNumber(Image.open("plaque.jpg")))
