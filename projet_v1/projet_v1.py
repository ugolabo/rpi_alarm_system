import RPi.GPIO as GPIO
import time
import datetime
import smtplib
import destinataire

# définir les paramètres
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# tout réinitialiser
GPIO.cleanup()

# définir les broches
# action
BTN_ARMER = 16  # action HIGH:désarmer/LOW:armer (off/on)
# désactiver le 2e bouton; cette ligne ci-dessous et les autres plus loin
#BTN_COUPER = 12 # action HIGH:rien faire/LOW:couper alarme (off/on)
# etat
DEL_RG = 22   # état LOW:désarmé/HIGH:armé (off/on)
DEL_JN = 18   # état LOW:rien/HIGH:alarme (off/on)
CONTACT = 21  # état LOW:en contact/HIGH:bris de contact (off/on)

# paramétrer la limite de temps pour démarrer l'alarme
DELTA_LIMITE = 3 # secondes

# importer le courriel d'origine et le mdp
with open("idmdp.txt", "r") as f:
    contenu = f.readlines()
#print(contenu)
"""
Ce fichier texte doit contenir 2 lignes (à la ligne 1 et 2):
courriel@gmail.com
motdepasse
"""
print("--------------------")

# paramétrer le destinataire
DESTINATAIRE = destinataire.DEST

# états initiaux des composants
print("--------------------")
print("états initiaux des composants")
print("0: DEL éteinte\n1: bouton/contact en rappel haut")
print("--------------------")
# construire les instances de boutons
# en rappels haut (résistance): HIGH
GPIO.setup(BTN_ARMER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(BTN_COUPER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# tester
print("BTN_ARME:", GPIO.input(BTN_ARMER))
#print("BTN_ATT:", GPIO.input(BTN_COUPER))

# construire les instances de DEL
GPIO.setup(DEL_RG, GPIO.OUT)
GPIO.setup(DEL_JN, GPIO.OUT)
# (re)paramétrer les états initiaux
GPIO.output(DEL_RG, GPIO.LOW)
GPIO.output(DEL_JN, GPIO.LOW)
# tester
print("DEL_RG:", GPIO.input(DEL_RG))
print("DEL_JN:", GPIO.input(DEL_JN))

# construire les instances de contact
# voir le cas particulier
GPIO.setup(CONTACT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# tester
print("CONTACT:", GPIO.input(CONTACT))


print("====================")

# états initiaux
print("journal des activités et des états")
print("--------------------")
# si l'état de CONTACT est HIGH
if (GPIO.input(CONTACT) == 1):
    print("en contact avec système DÉSARMÉ")
# si l'état de CONTACT est LOW
elif (GPIO.input(CONTACT) == 0):
    print("contact brisé avec système DÉSARMÉ")
else:
    pass


# définir la fonction pour BTN_ARME
# en rappel haut, le bouton est HIGH
# presser donne LOW et l'action FALLING
def actArmer(ev=None):
    """Armer ou désarmer le système ou couper l'alarme et désarmer le système"""
    print("bouton pressé")
    # si l'état de DEL_RG et DEL_JN est HIGH
    if (GPIO.input(DEL_RG) == 1) and (GPIO.input(DEL_JN) == 1):
        # mettre à LOW
        GPIO.output(DEL_JN, GPIO.LOW)
        GPIO.output(DEL_RG, GPIO.LOW)
        print("ALARME coupée et système DÉSARMÉ")
    # si l'état de DEL_RG est HIGH
    elif GPIO.input(DEL_RG) == 1:
        # mettre à LOW
        GPIO.output(DEL_RG, GPIO.LOW)
        print("système DÉSARMÉ")
    else:
        # mettre à HIGH
        GPIO.output(DEL_RG, GPIO.HIGH)
        print("système ARMÉ")
    # déclarer les variables globales
    global delta
    global debut
    # (ré)initialiser le delta
    delta = 0.0
    # démarrer le chronomètre
    debut = datetime.datetime.now()

# briser le contact donnne HIGH et l'action RISING
def actBriserContact(ev=None):
    """Briser le contact ou remettre en contact avec un système armé ou désarmé"""
    # si l'état de CONTACT est HIGH, DEL_RG est HIGH
    if (GPIO.input(CONTACT) == 0) and (GPIO.input(DEL_RG) == 1) and (GPIO.input(DEL_JN) == 0):
        print("contact brisé avec système ARMÉ")
        actChronometrer()
    # si l'état de CONTACT est HIGH, DEL_RG est LOW
    elif (GPIO.input(CONTACT) == 0) and (GPIO.input(DEL_RG) == 0):
        print("contact brisé avec système DÉSARMÉ")
    # si l'état de CONTACT est LOW, DEL_RG est HIGH
    elif (GPIO.input(CONTACT) == 1) and (GPIO.input(DEL_RG) == 1):
        print("en contact avec système ARMÉ")
    # si l'état de CONTACT est LOW, DEL_RG est LOW
    elif (GPIO.input(CONTACT) == 1) and (GPIO.input(DEL_RG) == 0):
        print("en contact avec système DÉSARMÉ")

def actChronometrer():
    """Démarrer le chronomètre"""
    # déclarer les variables globales
    global delta
    global debut
    # (ré)initialiser le delta
    delta = 0.0
    # démarrer le chronomètre
    debut = datetime.datetime.now()
    print("chronomètre démarré")

def actEnvoyer():
    """Envoyer une courriel"""
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # paramétrer le serveur
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        # entrer le courriel et mdp importé
        smtp.login(contenu[0], contenu[1])
        
        # composer le courriel
        subject = 'ALARME'
        body = 'Une alarme est declenchee.'
        
        msg = f"Subject: {subject}\n\n{body}"

        # envoyer le courriel
        smtp.sendmail(contenu[0],
                      DESTINATAIRE,
                      msg)

def actDemarrerAlarme():
    """Démarrer l'alarme"""
    # si l'état de DEL_JN est LOW
    if GPIO.input(DEL_JN) == 0:
        # mettre à HIGH
        GPIO.output(DEL_JN, GPIO.HIGH)
        # envoyer un courriel
        actEnvoyer()
        print("ALARME démarrée")
    else:
        pass

# pendant que le boucle while tourne
# le système veille à une action...
# appuyer sur le bouton change son état (évènement)
# FALLING: event edge-type detection, HIGH -> LOW
# RISING: event edge-type detection, LOW -> HIGH
# BOTH: ...
GPIO.add_event_detect(BTN_ARMER, GPIO.BOTH, callback=actArmer, bouncetime=500)
GPIO.add_event_detect(CONTACT, GPIO.BOTH, callback=actBriserContact, bouncetime=500)
#GPIO.add_event_detect(BTN_COUPER, GPIO.BOTH, callback=actCouperAlarme, bouncetime=500)

while True:
    # attendre un événement
    time.sleep(0.5)
    # si l'état de CONTACT est HIGH, DEL_RG est HIGH, DEL_JN est LOW
    if (GPIO.input(CONTACT) == 0) and (GPIO.input(DEL_RG) == 1) and (GPIO.input(DEL_JN) == 0):
        # calculer le delta temporel depuis le debut du bris de contact
        # en secondes
        delta = (datetime.datetime.now() - debut).seconds
        # imprimer le cumulatif du delta en secondes
        if delta < DELTA_LIMITE:
            print(delta)        
        elif delta >= DELTA_LIMITE:
            print(delta)
            actDemarrerAlarme()
        else:
            pass
    if (GPIO.input(DEL_JN) == 1):
        GPIO.output(DEL_JN, GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(DEL_JN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(DEL_JN, GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(DEL_JN, GPIO.HIGH)
    else:
        pass