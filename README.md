# Système d'alarme avec un Raspberry Pi

## v1; système d'alarme avec bouton

**Objectif:** maitriser les fondements des nanoordinateurs (Raspberry Pi), des OS Linux (Raspbian, mais aussi Ubuntu, les CLI) et de montages, du langage Python embarqué, de concepts comme les rappels haut et bas, les fils d'exécution (*thread*), les évènements sur le système (bouton), la gestion du temps avec `time` et `datetime`, les extractions web avec `requests`, le protocole SMTP avec `smtplib`, et plus afin de construire des projets simples en IoT et de pouvoir collaborer avec des spécialistes de ces domaines dans des projets avancés.

Montage:

- un contact représentant une porte ou une fenêtre
  - lorsque le fil est branché, le circuit est fermé et l'état du contact est actif
  - lorsque le fil est débranché, le circuit est ouvert et l'état du contact est inactif
- un bouton
  - pour armer ou désarmer le système: état armé ou désarmé
- une DEL rouge allumée; système en état armé
- une DEL jaune clignotante; système en état d'alerte

Schéma Fritzing global avec un Raspberry Pi 3 (le projet a été fait avec un RPi4)

<img src="img/diagramme_fritzing.jpg" alt="">

| Schéma bouton | Schéma contact  | Schéma DEL  |
|:---|:---|:---|
| <img src="img/schema_bouton.jpg" alt="" width="200"> | <img src="img/schema_contact.jpg" alt="" width="200">  | <img src="img/schema_dels.jpg" alt="" width="200">  |

Diagramme d'états

<img src="img/diagramme_etat.jpg" alt="">

## v2; système d'alarme avec console Pygame

**Objectif:** poursuivre avec la programmation embarquée et s'initier à la programmation orientée objet en Python pour gérer les états et les changements d’état avec des classes et `enum`, la journalisation (*logging*) avec `logging`, les interface graphique (*GUI*) avec `pygame`, les images avec `PIL`, plus d’évènements sur le système (clavier, souris), plus d'extractions web avec `pyowm`, l'importation de données de fichiers YAML, la gestion de paquets et la configuration des fichiers et dossiers Python avec des fichiers comme `__init__.py` et `main.py` ou une ligne d'instruction comme  `__name__ == "__main__":` et plus.

| Clavier | Armer  |
|:---|:---|
| <img src="img/console1.gif" alt="" width="300">  | <img src="img/console2.gif" alt="" width="250"> |
| **Armer, déarmer**  | **Armer, déclencer, désarmer** |
| <img src="img/console3.gif" alt="" width="250">  | <img src="img/console4.gif" alt="" width="250"> |
