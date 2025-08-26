import sqlite3
import hashlib
import time
from datetime import datetime, date, timedelta

date_actuelle = date.today()
date_maj = date(2027, 6, 29)
date_fin_maj = date(2026, 6, 29)

con = sqlite3.connect("sport_data1.0.db")
curseur = con.cursor()

def menu_de_connection():
    print("Choisissez une option :")
    print("")
    print("1. Se connecter")
    print("2. S'inscrire")
    print("3. Nouveautés - Actu")
    print("4. À propos")

    choix = input("Votre choix : ")

    if choix == "1":
        print("")
        print("-- Connection --")
        username = input("Nom d'utilisateur : ")
        password = input("Mots de passe : ").encode('UTF-8')

        sha256 = hashlib.sha256()
        sha256.update(password)
        hashed_password = sha256.hexdigest() # Hache le mot de passe qui a été entré
        curseur.execute("SELECT id, username, password FROM Account WHERE username = ? AND password = ?", (username, hashed_password))
        result = curseur.fetchone()
        if result:
            account_id = result[0]
            print("")
            print(f"Vous êtes connectés en tant que {username}") #Ne pas oublier le f !
            accueil(account_id)
        else:
            print("Identifiants incorrects. Veuillez réessayer.")
            con.close

    elif choix == "2":
        print("")
        print("-- Inscription --")
        username = input("Nom d'utilisateur (requis) : ")
        password = input("Mots de passe (requis) : ").encode("UTF-8")
        if not username or not password:
            print("")
            print("Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
        else:
            sha256 = hashlib.sha256()
            sha256.update(password)
            hashed_password = sha256.hexdigest() # Hacher le mot de passe
            curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
            con.commit()
            print("")
            print(f"Bienvenue {username} ! Vous pouvez désormais utiliser Sprintia.") #Ne pas oublier le f !
            print("Vous pouvez maintenant vous connecter.")
            con.close

    elif choix == "3":
        print("")
        print("Bonjour, nous sommes ravis que vous utilisiez Sprintia !")
        print("Merci de faire partie de l'aventure Sprintia ! Ensemble, atteignons de nouveaux sommets !")
        print("Merci de votre confiance.")
        print("")
        print("Actu :")
        print("La mise à jour de Sprintia 1.1 arrive ce dimanche (26 Juin 2025)")
        print("")
        print("Préparez-vous à découvrir Sprintia 1.1, la nouvelle version qui va améliorer votre expérience !")
        print("Elle intègre '✨ GlyphFlow 🚀', une interface repensée pour une utilisation plus fluide et plus joli.")
        print("Nous avons également mis l'accent sur le renforcement de la sécurité de vos données et")
        print("l'optimisation de la gestion des erreurs, pour une performance toujours plus fiable.")
        print("")
        print("Nouveautés (version 1.0) : ")
        print("1. Charge d'entraînement : Analysez dès maintenant l'impact de vos activités.")
        print("2. Hachage des mots de passe : Vos mots de passe sont hachés, ajoutant une couche de sécurité cruciale.")

    elif choix == "4":
        print("")
        print("-- Informations sur le logiciel --")
        print("")
        print("Sprintia est conçue pour vous aidés avant et après un entraînement")
        print("Version : 1.0.4 - Alpha")
        print("Dernière mise à jour : 26 Juin 2025")
        print("Développé par Gabriel Chapet")
        print("Mon adresse mail : gabchap486@gmail.com")

    else:
        print("Sélection incorrecte, veuillez réessayer")

def charge_entraînement(account_id):
    #date
    date_actuelle = date.today()

    ca = date_actuelle - timedelta(days=7)  #ca = charge aïgue
    ca_str = ca.strftime('%Y-%m-%d')
    curseur.execute("SELECT charge FROM Activité WHERE account_id = ? AND date >= ?", (account_id, ca_str))
    charges_aigue = [row[0] for row in curseur.fetchall()]

    #Charge Aïgue
    cc = date_actuelle - timedelta(days=28)  #cc = charge chronique
    cc_str = cc.strftime('%Y-%m-%d')
    curseur.execute("SELECT charge FROM Activité WHERE account_id = ? AND date >= ?", (account_id, cc_str))
    charges_chronique = [row[0] for row in curseur.fetchall()] #Extrait les valeurs de 'charge' dans une liste

    #Calcul des moyennes
    charge_aigue = sum(charges_aigue) if charges_aigue else 0
    charge_chronique = sum(charges_chronique) / len(charges_chronique) if charges_chronique else 0

    #Ratio de charge
    if charge_chronique > 0:
        ratio = charge_aigue / charge_chronique
    else:
        ratio = None

    print("")
    print(f"- Charge aiguë (7 jours) : {charge_aigue:.1f}")
    print(f"- Charge chronique (28 jours) : {charge_chronique:.1f}")
    if ratio is not None:
        print(f"- Ratio ACR : {ratio:.2f}")
        if ratio < 0.8:
            print("Sous-entraînement")
        elif 0.8 <= ratio <= 1.3:
            print("Zone optimale, parfait")
        elif 1.3 < ratio <= 1.5:
            print("Charge élevée, prudence !")
        else:
            print("Surentraînement ! Risque de blessure !")
    else:
        print("Données insuffisantes pour calculer le ratio.")

#Menu d'accueil
def accueil(account_id):
    while True:
        print("")
        print("-- Accueil --")
        print("")
        print("1. Créer une activité")
        print("2. Charge d'entraînement")
        print("3. Quitter")

        choix_accueil = input("Votre choix : ")

        if choix_accueil == "1":
            print("")
            print("-- Création d'une activité --")
            print("")
            #convertir les dates
            date_str = input("Quelle était la date de ton activité (JJ-MM-AAAA) : ")
            #Je dois d’abord convertir la chaîne date_str en un objet datetime pour que ça fonctionne
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')#conversion str -> datetime
            date = date_conversion.strftime('%Y-%m-%d')#conversion datetime -> str formatée

            sport = input("Quel sport as-tu pratiqué : ")
            durée = int(input("Quelle était la durée de ton activité (en min) : ")) #Ne pas oublier de convertir en entier
            rpe = int(input("Note cet effort sur une échelle de 1 à 10 : "))
            fatigue = int(input("Quel est ton niveau de fatigue sur une échelle de 1 à 10 après cette entraînement : "))
            douleur = int(input("As-tu des douleurs après cette séance (0= non, 1= un peu, 2= oui, 3= blessure) : "))
            climat = int(input("Climat (0= Normal, 1= Chaud, 2= Froid, 3= Difficile) : "))

            #calcul de charge
            charge_de_base = durée*rpe

            score_de_fatigue = 1+(fatigue-5)*0.05

            if douleur == 0:
                charge_d = charge_de_base*0.9
            elif douleur == 1:
                charge_d = charge_de_base*1.05
            elif douleur == 2:
                charge_d = charge_de_base*1.2
            else:
                charge_d = charge_de_base*1.4

            if climat == 0:
                charge_c = charge_d*0.95
            elif climat == 1:
                charge_c = charge_d*1.1
            elif climat == 2:
                charge_c = charge_d*1.05
            else:
                charge_c = charge_d*1.2

            charge_activité = score_de_fatigue*charge_c

            curseur.execute("INSERT INTO Activité (date, sport, durée, rpe, fatigue, douleur, climat, account_id, charge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (date, sport, durée, rpe, fatigue, douleur, climat, account_id, charge_activité))          
            con.commit()
            print("")
            print("Votre activité a été enregistré.")

        elif choix_accueil == "2":
            print("")
            print("-- Analyse de la charge d'entraînement --")
            charge_entraînement(account_id)

        elif choix_accueil == "3":
            print("Au revoir et à bientôt sur Sprintia !")
            con.close
            break

        else:
            print("Sélection incorrecte, veuillez réessayer")

#menu de connection 
print("")
print("-- Bienvenue sur Sprintia ! --")
print("Votre compagnon d'entraînement !")
print("")
if date_maj <= date_actuelle <= date_fin_maj:
    print("Une mise à jour est disponible")
    print("Sprintia 1.1 est disponible")
    print("")
    print("1. Lancer la mise à jour")
    print("2. Quitter")

    choix_jour_de_maj = input("Votre choix : ")

    if choix_jour_de_maj == "1":
        print("-- Mise à jour en cours --")
        print("Chargement...")
        time.sleep(5)
        print("Téléchargement : 25%")
        time.sleep(5)
        print("Téléchargement : 50%")
        time.sleep(5)
        print("Téléchargement : 75%")
        time.sleep(5)
        print("Téléchargement : 100%")
        time.sleep(2)
        print("Installation...")
        time.sleep(5)
        print("")
        print("Sprintia a été mis à jour")
        time.sleep(2)
        print("")
        print("Veuillez ouvrir le nouveau fichiers Sprintia 1.1")

    elif choix_jour_de_maj == "2":
        print("Au revoir et à bientôt sur Sprintia !")

    else:
        print("Sélection incorrecte, veuillez réessayer")

else:
    menu_de_connection()