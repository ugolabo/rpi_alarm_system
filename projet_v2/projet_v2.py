import pygame
from pyowm import OWM
from pyowm.utils.config import get_default_config
import datetime
import requests


# Définir les paramètres
# Définir les couleurs (RGB)
BLANC = (255, 255, 255)
BLANCF = (235, 235, 235)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
GRISF = (88, 88, 88)
GRISP = (225, 225, 225)
VERT = (14, 209, 69)
BLEU = (63, 72, 204)
ROUGE = (236, 28, 36)
JAUNE = (255, 242, 0)

# Définir les constantes et
# les paramètres de départ
running = True
u_input = "" # le texte (code) entré
ÉTATS = ["DÉSARMÉ", "CODE...", "ARMÉ", "CODE...", "ALARME"] # état 0, 1, 2, 3, 4
état = 0 # état de départ
COULEURS = [VERT, BLEU, ROUGE, BLEU, JAUNE] # couleurs associées aux états
delta = datetime.timedelta(seconds=0) # initialisation du chronoDébut
delta_i = delta
début = datetime.datetime(2022, 1, 1, 0, 0, 0, 0) # idem
début_i = début
durée = 7 # secondes (temps max pour armer, désarmer, couper l'alarme)
code = "" # initialisation du code entré
BON_CODE = "baba" # code pour armer ou arrêter l'alarme et/ou désarmer 


# Paramétrer OWM
config_dict = get_default_config()
config_dict['language'] = 'fr'

try:
    # Ouvrir une connexion
    # ugolbt@gmail.com
    # H8BwPm47uhez
    owm = OWM('6a4e192151862f798ed5b2ff67b695b1', config_dict)
    mgr = owm.weather_manager()
    
    # Télécharger les observations
    observation = mgr.weather_at_place('Montreal,CA')
    w = observation.weather
    
    # Télécharger l'image
    image_meteo = f"http://openweathermap.org/img/wn/{w.weather_icon_name}.png"
    response = requests.get(image_meteo)
    
    # Sauvegarder l'image
    with open('meteo_image.png', 'wb') as fichier:
        fichier.write(response.content)
except:
    print("Ne peut ouvrir une connexion avec OWM.")


# Définir les fonctions
def btn1(screen, pos, texteBtn, couleur):
    """Créer un gros bouton (armer, désarmer, etc.)"""
    global large1
    global haut1
    large1 = 150
    haut1 = 150
    font = pygame.font.SysFont('liberationsans', 20, bold=True)
    pygame.draw.rect(screen, couleur, (pos[0], pos[1], large1, haut1), 0)
    pygame.draw.rect(screen, GRISF, (pos[0], pos[1], large1, haut1), 1)
    pygame.draw.rect(screen, GRIS, (pos[0]+20, pos[1]+20, large1-40, haut1-40), 0)
    #pygame.draw.rect(screen, GRISF, (pos[0]+20, pos[1]+20, large1-40, haut1-40), 1)
    txtBtn = font.render(texteBtn, True, GRISF)
    rectBtn = txtBtn.get_rect()
    rectBtn.center = (pos[0] + (large1-2)/2, pos[1] + (haut1-5)/2)
    screen.blit(txtBtn, rectBtn)
    
def btn2(screen, pos, texteBtn):
    """Créer des boutons pour entrer le code"""
    global large2
    global haut2
    large2 = 70
    haut2 = 70
    font = pygame.font.SysFont('hpsimplified', 48)
    pygame.draw.rect(screen, GRIS, (pos[0], pos[1], large2, haut2), 0)
    pygame.draw.rect(screen, GRISF, (pos[0]+5, pos[1]+5, large2-10, haut2-10), 1)
    txtBtn = font.render(texteBtn, True, GRISF)
    rectBtn = txtBtn.get_rect()
    rectBtn.center = (pos[0] + large2/2, pos[1] + (haut2-5)/2)
    screen.blit(txtBtn, rectBtn)

def surBtn1(posBtn, posSrs):
    """Créer un test si la souris survole un btn1"""
    xBtn = posBtn[0]
    yBtn = posBtn[1]
    xSrs = posSrs[0]
    ySrs = posSrs[1]
    return ((xBtn < xSrs) and ((xBtn + large1) > xSrs)) \
        and ((yBtn < ySrs) and ((yBtn + haut1) > ySrs))
        
def surBtn2(posBtn, posSrs):
    """Créer un test si la souris survole un btn2"""
    xBtn = posBtn[0]
    yBtn = posBtn[1]
    xSrs = posSrs[0]
    ySrs = posSrs[1]
    return ((xBtn < xSrs) and ((xBtn + large2) > xSrs)) \
        and ((yBtn < ySrs) and ((yBtn + haut2) > ySrs))

def chronoDébut():
    """Démarrer le chrono"""
    global delta
    global début
    delta = delta_i
    début = datetime.datetime.now()

def chronoPassage():
    """Mesurer les temps de passage du chrono démarré"""
    global delta
    passage = datetime.datetime.now()
    delta = passage - début

def réinitialiser(niv='moyen', ét=0):
    """Réinitialiser l'afficheur et des paramètres"""
    global état
    global delta
    global début
    global u_input
    global code
    if niv == 'simple':
        u_input, code = "", ""
    elif niv == 'moyen':
        état, u_input, code = ét, "", ""
    elif niv == 'élevé':
        état, delta, début, u_input, code = ét, delta_i, début_i, "", ""

# ce qui précède pourrait être importé dans un autre fichier
# pour employer les fonction qui précèdent
# sans ce qui suit ne soit exécuté
if __name__ == "__main__":
# ce qui suit n'est exécuté que si ce fichier est exécuté
    
    # Contruire l'instance de l'interface
    pygame.init()
    
    # Définir la taille de la fenêtre
    screen = pygame.display.set_mode([500, 450])
    
    
    # Démarrer l'application pygame
    while running:
        # Surveiller les évènements
        for event in pygame.event.get():
            # Cliquer sur le x de la fenêtre
            # pour quitter le programme
            if event.type == pygame.QUIT:
                running = False
            # évènements de la souris
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                xSrs, ySrs = pygame.mouse.get_pos()
                # évènements de la souris et des btn1
                # selon l'état...
                if surBtn1((40, 80), (xSrs, ySrs)) and état == 0:
                    print("bouton pour ARMER")
                    état = 1 # changer
                    chronoDébut() # démarrer
                elif surBtn1((40, 80), (xSrs, ySrs)) and état == 1:
                    print("bouton inutile; entrer le code!")
                elif surBtn1((40, 80), (xSrs, ySrs)) and état == 2:
                    print("bouton pour DÉSARMER inutile; entrer le code!")
                elif surBtn1((40, 80), (xSrs, ySrs)) and état == 3:
                    print("bouton inutile; entrer le code!")
                elif surBtn1((40, 80), (xSrs, ySrs)) and état == 4:
                    print("bouton pour ARRÊTER/DÉSARMER inutile; entrer le code!")
                # événements de la souris et des btn2
                if surBtn2((230, 165), (xSrs, ySrs)):
                    print("bouton a")
                    u_input += "a" # entrer
                if surBtn2((310, 165), (xSrs, ySrs)):
                    print("bouton b")
                    u_input += "b" # entrer
                if surBtn2((390, 165), (xSrs, ySrs)):
                    print("bouton c")
                    u_input += "c" # entrer
                if surBtn2((230, 245), (xSrs, ySrs)):
                    print("bouton x")
                    réinitialiser(niv='simple')
                if surBtn2((310, 245), (xSrs, ySrs)):
                    print("bouton <-")
                    u_input = u_input[0:-1] # effacer/reculer
                if surBtn2((390, 245), (xSrs, ySrs)):
                    print("bouton #")
                    code = u_input # confirmer/entrer
                    
        # Définir l'arriere-plan
        screen.fill(BLANCF)
    
        # Définir la barre supérieure
        pygame.draw.rect(screen, GRIS, (0, 0, 500, 70), 0)    # fond
        pygame.draw.rect(screen, GRISF, (10, 10, 480, 50), 1) # ligne
        
        # Définir la bordure
        pygame.draw.rect(screen, GRIS, (0, 0, 500, 450), 10) # bordure
        pygame.draw.rect(screen, NOIR, (0, 0, 500, 450), 1)  # ligne
    
        # Ajouter du texte à la barre supérieure
        font = pygame.font.SysFont('liberationsans', 20, bold=False)
        txt = font.render("Entrez votre code pour armer/désarmer le système",
                          True, GRISF)
        screen.blit(txt, (20, 22))
        
        # Définir le bouton de gauche (avec la fonction)
        btn1(screen, ((40, 80)), ÉTATS[état], COULEURS[état])
    
        # Définir la zone heure
        pygame.draw.rect(screen, GRISF, (40, 245, 150, 70), 0)
        # Capter le temps
        temps = datetime.datetime.now()
        tps_date = temps.strftime('%d-%m-%Y')
        tps_heure = temps.strftime('%Hh%M  %S')
        # Inscrire le temps
        font = pygame.font.SysFont('liberationsans', 20, bold=False)
        txt = font.render(tps_date,
                          True, BLANC)
        screen.blit(txt, (65, 255))
        txt = font.render(tps_heure,
                          True, BLANC)
        screen.blit(txt, (72, 280))
        # Redéfinir la zone heure pour afficher le chrono
        if (état == 1) or (état == 3):
            pygame.draw.rect(screen, GRISF, (40, 245, 150, 70), 0)
            font = pygame.font.SysFont('liberationsans', 20, bold=False)
            txt = font.render("chrono: " + str(delta.seconds) + " sec",
                              True, BLANC)
            screen.blit(txt, (55, 255))
            txt = font.render("max: " + str(durée) + " sec",
                              True, BLANC)
            screen.blit(txt, (78, 280))
        
        # Définir le logo (une image)
        logo = pygame.image.load("logo2.png")
        logo = pygame.transform.scale(logo, (174, 94))
        logo.convert()
        screen.blit(logo, (35, 330))
        
        # Définir l'afficheur du code
        pygame.draw.rect(screen, GRIS, (230, 80, 230, 70), 0)  # fond1
        pygame.draw.rect(screen, GRISF, (235, 85, 220, 60), 0) # fond2
        
        # Ajouter de l'interactivité (texte) à l'afficheur
        font = pygame.font.SysFont('hpsimplified', 48, bold=True)
        longueur = len(u_input)
        if longueur > 6:
            u_input = u_input[-1]
        else:
            décalage = longueur * 19
            txt = font.render(u_input, True, GRIS)
            screen.blit(txt, (420 - décalage, 95))    
        
        # Définir les boutons de droite (avec la fonction)
        btn2(screen, ((230, 160)), "a")
        btn2(screen, ((310, 160)), "b")
        btn2(screen, ((390, 160)), "c")
        btn2(screen, ((230, 245)), "x")
        btn2(screen, ((310, 245)), "<-")
        btn2(screen, ((390, 245)), "#")
    
        # Définir la zone météo et
        # afficher les données téléchargées (plus haut)
        # https://openweathermap.org/current
        pygame.draw.rect(screen, GRISF, (230, 330, 230, 100), 0)
        try:
            font = pygame.font.SysFont('liberationsans', 20, bold=False)
            txt = font.render(str( round(w.temperature('celsius')['temp'], 1))\
                              + '°C',
                              True, BLANC)
            screen.blit(txt, (250, 338))
            txt = font.render(str( round(w.humidity, 1))\
                              + '%',
                              True, BLANC)
            screen.blit(txt, (250, 366))
        
            txt = font.render(str( w.pressure['press'] / 10)\
                              + 'kPa',
                              True, BLANC)
            screen.blit(txt, (250, 393))
            logo = pygame.image.load("meteo_image.png")
            logo.convert()
            screen.blit(logo, (370, 325))
            txt = font.render(str( round(w.wind()['speed'], 1))\
                              + 'km/h',
                              True, BLANC)    
            screen.blit(txt, (355, 366))
            txt = font.render(str( round(w.wind()['deg'], 1))\
                              + '°',
                              True, BLANC)    
            screen.blit(txt, (355, 393))
        except:
            font = pygame.font.SysFont('liberationsans', 25, bold=False)
            txt = font.render("Ne peut ouvrir une connexion avec OWM\net afficher des résultats.",
                              True, BLANC)
            screen.blit(txt, (250, 338))
        
        # Gérer les états
        # états permanent 0, 2 et 4 (DÉSARMÉ, ARMÉ, ALARME)
        # états passagés 1 et 3 (CODE)
        if état == 0:
            pass
        elif état == 1:
            chronoPassage() # (re)lancer
            print(delta.seconds) # afficher le temps de passage
            if delta.seconds >= durée: # dépasser la durée
                réinitialiser(niv='élevé', ét=0)
            if code == BON_CODE: # vérifier l'entrée du code
                réinitialiser(niv='élevé', ét=2)
        elif état == 2:
            if code == BON_CODE: # vérifier l'entrée du code
                réinitialiser(niv='moyen', ét=0)
            elif code == "bbc": # code pour déclencher
                réinitialiser(niv='moyen', ét=3)
                chronoDébut() # démarrer
        elif état == 3:
            chronoPassage() # (re)lancer
            print(delta.seconds) # afficher le temps de passage
            if delta.seconds >= durée: # dépasser la durée
                réinitialiser(niv='élevé', ét=4)
            if code == BON_CODE: # vérifier l'entrée du code
                réinitialiser(niv='élevé', ét=0)
        elif état == 4:
            if code == BON_CODE: # vérifier l'entrée du code
                réinitialiser(niv='élevé', ét=0)
    
        # Mettre à jour l'affichage
        pygame.display.update()
    
    # Quitter correctement le programme
    pygame.quit()
