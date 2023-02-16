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

Code source `projet_v1.py`:

- configurer le montage, le Rpi, les broches, les rappels, le destinataire du courriel, les fils d'exécution (*thread*), etc.
- veiller et gérer les évènements pour changer les états (contact branché/débranché, système armé/désarmé, état d'alerte ou non
  - appuyer sur le bouton arme ou désarme le système
  - brancher et débrancher le contact n'a aucun effet si le système est désarmé
  - quand le système est armé, la DEL rouge allume; débrancher le contact donne 3 secondes pour désarmer le système sinon l'alarme démarre, la DEL jaune clignote et un courriel est envoyé à un destinataire
  - quand l'alarme est enclenchée, brancher et débrancher le contact n'a plus d'effet
  - quand l'alarme est enclenchée, appuyer sur le bouton désarme le système et arrête l'alarme
