import sqlite3
import hashlib
import time
import getpass
import random
import csv
import os
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt # Pour graphique
import seaborn as sns # Pour graphique
from colorama import Fore, Style
from tabulate import tabulate # Pour les tableaux dans charge d'entraînement

#variables
date_actuelle = date.today()

#dates maj
date_début_maj = date(2025, 7, 27)
date_fin_maj = date(2026, 7, 27)

date_début_bienvenue = date(2025, 7, 13)
date_fin_bienvenue = date(2025, 7, 17)

#dates saison
debut_printemps = date(date_actuelle.year, 3, 20) # .year pour enlever l'année, l'extraire
fin_printemps = date(date_actuelle.year, 6, 20)

debut_été = date(date_actuelle.year, 6, 21) 
fin_été = date(date_actuelle.year, 9, 21)

debut_automne = date(date_actuelle.year, 9, 22) 
fin_automne = date(date_actuelle.year, 12, 20)

debut_hiver = date(2025, 12, 21) 
fin_hiver = date(2026, 3, 19)

#date célèbres
date_jour_de_an = date(date_actuelle.year, 1, 1)
date_saint_valentin = date(date_actuelle.year, 2, 14)
date_halloween = date(date_actuelle.year, 10, 31)
date_noël = date(date_actuelle.year, 12, 25)
date_réveillon = date(date_actuelle.year, 12, 31)
date_fête_nationale = date(date_actuelle.year, 7, 14)
date_jour_de_la_femmes = date(date_actuelle.year, 3, 8)
date_anniversaire_sprintia = date(date_actuelle.year, 5, 20)
date_fête_du_travail = date(date_actuelle.year, 5, 1)
date_victoire_de_1945 = date(date_actuelle.year, 5, 8)
date_premiere_guerre_mondiale = date(date_actuelle.year, 11, 11)
date_toussaint = date(date_actuelle.year, 11, 1)
date_droits_de_homme = date(date_actuelle.year, 12, 10)
date_rentrée = date(date_actuelle.year, 9, 1)

def nettoyer_console():
    # Vérifie le système d'exploitation
    if os.name == 'nt':  # 'nt' signifie Windows
        _ = os.system('cls')
    else:  # Pour MacOS et Linux
        _ = os.system('clear')

def deconnexion():
    print("")
    print("👋 Vous avez été déconnecté.")
    time.sleep(1)
    menu_de_connection()

def maj():
    nettoyer_console()
    print("🆕 Une mise à jour est disponible 🆕")
    print("")
    print("➡️  Sprintia 1.4 est disponible")
    print("")
    print("1. 🔄 Lancer la mise à jour | 2. 🛑 Quitter")

    choix_jour_de_maj = input("Votre choix : ").strip()

    if choix_jour_de_maj == "1":
        print("")
        print("-- ⚙️  Mise à jour en cours ⚙️  --")
        print("⏳ Chargement ⏳")
        print("")
        time.sleep(5) #régler la durée de mise à jour !!!
        print("⬇️  Téléchargement : 25%")
        time.sleep(5)
        print("⬇️  Téléchargement : 50%")
        time.sleep(5)
        print("⬇️  Téléchargement : 75%")
        time.sleep(5)
        print("⬇️  Téléchargement : 100%")
        time.sleep(2)
        print("📦 Installation ⏳")
        time.sleep(5)
        print("")
        print(f"{Fore.GREEN}✅ Sprintia a été mis à jour{Style.RESET_ALL}")
        time.sleep(2)
        print("")
        print("🔄 Veuillez ouvrir le nouveau fichiers Sprintia 1.3")
        time.sleep(2)

    elif choix_jour_de_maj == "2":
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()

def modifier_mots_de_passe(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 🔒 Modification de votre mots de passe ✍️  --")
    print("")
    print("🔒 Votre saisie reste invisible pour garantir la confidentialité. 🛡️")
    new_password = getpass.getpass(prompt='Nouveau mots de passe : ').strip()
    new_password2 = getpass.getpass(prompt='Confirmez votre nouveau mots de passe : ').strip()
    if new_password == new_password2:
        password_encode = new_password.encode("UTF-8")

        try:
            if not new_password:
                print("")
                print(f"{Fore.RED}❌ Le mot de passe ne peuvent pas être vides.{Style.RESET_ALL}")
            else:
                if (password_valide(new_password)):
                    print(f"{Fore.GREEN}✅ Le mot de passe est valide{Style.RESET_ALL}")
                    sha256 = hashlib.sha256()
                    sha256.update(password_encode)
                    hashed_password = sha256.hexdigest()
                    con.execute("UPDATE Account SET password = ? WHERE id = ?", (hashed_password, account_id))
                    con.commit()
                    print("")
                    print(f"{Fore.GREEN}✅ Votre mots de passe à bien été modifié{Style.RESET_ALL}")
                    print("")
                    print("Vous pouvez maintenant vous connecter. ➡️")
                    time.sleep(1)
                    connection()
                
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue lors de la modification du mots de passe : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
    else:
        print(f"{Fore.RED}❌ Les mots de passe saisis ne correspondent pas.{Style.RESET_ALL}")

def modifier_nom_utilisateur(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 🔒 Modification de votre nom d'uilisateur ✍️  --")
    print("")
    new_username = input("Nouveau nom d'utilisateur : ").strip()
    new_username2 = input("Confirmez votre nouveau nom d'utilisateur : ").strip()

    if new_username == new_username2:
        try:
            if not new_username:
                print("")
                print(f"{Fore.RED}❌ Le nom d'utilisateur ne peut pas être vides.{Style.RESET_ALL}")
            else:
                con.execute("UPDATE Account SET username = ? WHERE id = ?", (username, account_id))
                con.commit()
                print("")
                print(f"{Fore.GREEN}✅ Votre nom d'utilisateur à bien été modifié{Style.RESET_ALL}")
                print("")
                print("Vous pouvez maintenant vous connecter. ➡️")
                time.sleep(1)
                connection()

        except sqlite3.IntegrityError as e: 
            print("")
            print(f"{Fore.RED}❌ Erreur d'intégrité à la base de données : {e}{Style.RESET_ALL}")
            print("Ce nom d'utilisateur est probablement déjà utilisé ou un problème de données est survenu.")
            print("Veuillez réessayer avec un autre nom d'utilisateur.")
            time.sleep(2)
            modifier_nom_utilisateur(account_id, username, password)
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue lors de la modification du mots de passe : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
    else:
        print(f"{Fore.RED}❌ Les mots de passe saisis ne correspondent pas.{Style.RESET_ALL}")

def connection():
    nettoyer_console()
    print("")
    print("-- 🌐 Connection 🌐 --")

    try:
        username = input("Nom d'utilisateur : ").strip() #enlève les espaces au début et à la fin
        print("🔒 Votre saisie reste invisible pour garantir la confidentialité. 🛡️")
        password = getpass.getpass(prompt='Mots de passe : ').encode('UTF-8')

        sha256 = hashlib.sha256()
        sha256.update(password)
        hashed_password = sha256.hexdigest()
        curseur.execute("SELECT id, username, password FROM Account WHERE username = ? AND password = ?", (username, hashed_password))
        result = curseur.fetchone()

        if not username or not password:
            print("")
            print(f"{Fore.RED}❌ Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.{Style.RESET_ALL}")
        if result:
            account_id = result[0]
            print("")
            print(f"{Fore.GREEN}✅ Vous êtes connectés en tant que {username}{Style.RESET_ALL}")
            time.sleep(1)
            accueil(account_id, username, password)
        else:
            print(f"{Fore.RED}❌ Identifiants incorrects. Veuillez réessayer.{Style.RESET_ALL}")
        
        time.sleep(1)
        connection()

    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste, veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue lors de la connexion : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    
    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        connection()
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        connection()

def mon_compte(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 👤 Mon compte 👤  --")
    print("")
    print(f"🆔 Votre ID : {account_id}")
    print(f"🧑 Votre nom d'utilisateur : {username}")
    time.sleep(0.5)
    
    print("")
    print("Choisissez une option ⬇️")
    print("")
    print("1. 🔒 Modifier mon mots de passe       | 2. 🧑 Modifier mon nom d'utilisateur")
    print("3. 📊 Changer de statut d'entraînement | 4. 🔙 Retour")

    choix_compte = input("Votre choix : ").strip()

    if choix_compte == "1":
        modifier_mots_de_passe(account_id, username, password)
    elif choix_compte == "2":
        modifier_nom_utilisateur(account_id, username, password)
    elif choix_compte == "3":
        print("1. 🏖️  Vacances | 2. 🤕 Blessure | 3. 🔄 Reprendre | 4. 🔙 Retour")

        sous_choix = input("Choix : ")

        if sous_choix == "1":
            activer_pause(account_id, username, password, "vacances")
        elif sous_choix == "2":
            activer_pause(account_id, username, password, "blessure")
        elif sous_choix == "3":
            arreter_pause(account_id, username, password)
        elif sous_choix == "4":
            mon_compte(account_id, username, password)
    elif choix_compte == "4":
        accueil(account_id, username, password)
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        mon_compte(account_id, username, password)

def conseils(account_id, username, password):
    nettoyer_console()
    result_conseil = random.randint(1, 20)

    print("")
    print("-- 💡 Conseils 💡 --")
    print("")

    try:
        if result_conseil == 1:
            print("➡️  Démarre en douceur : Commence petit, augmente l'intensité progressivement pour habituer ton corps sans te blesser.")
        elif result_conseil == 2:
            print("➡️  Fixe-toi des objectifs réalistes : Plutôt que de vouloir devenir un champion du monde en un mois, fixe-toi des petits objectifs que tu peux atteindre.")
        elif result_conseil == 3:
            print("➡️  Trouve une activité que tu aimes : Le sport, ça doit être un plaisir. Si tu détestes la course à pied, essaie la natation, le vélo,... Ce qui compte, c'est de bouger !")
        elif result_conseil == 4:
            print("➡️  Varie tes entraînements : Faire toujours la même chose peut devenir ennuyeux et ton corps s'habitue. Change d'activités, de lieux ou d'intensité pour rester stimulé.")
        elif result_conseil == 5:
            print("➡️  Échauffe-toi : Avant une séance de haute intensité, prends 5 minutes pour préparer tes muscles. Ça évite les blessures et ça améliore tes performances.")
        elif result_conseil == 6:
            print("➡️  Écoute ton corps : Si tu as mal, ne force pas. Le repos est aussi important que l'entraînement. Apprends à reconnaître les signaux de ton corps.")
        elif result_conseil == 7:
            print("➡️  Hydrate-toi : Bois de l'eau avant, pendant et après l'effort. C'est super important pour que ton corps fonctionne bien, surtout quand il fait chaud.")
        elif result_conseil == 8:
            print("➡️  Mange équilibré : Ce que tu manges a un impact direct sur ton énergie et ta récupération. Mange des fruits, des légumes, des protéines et des glucides complexes.")
        elif result_conseil == 9:
            print("➡️  Sois régulier : Mieux vaut faire 30 minutes de sport trois fois par semaine que 3 heures une seule fois de temps en temps. La régularité paie.")
        elif result_conseil == 10:
            print("➡️  Dors suffisamment : C'est pendant ton sommeil que tes muscles se réparent et se renforcent. Vise 7 à 9 heures par nuit.")
        elif result_conseil == 11:
            print("➡️  Prépare tes affaires la veille : Ça peut paraître bête, mais avoir tes affaires prêtes réduit les excuses pour ne pas faire ta séance.")
        elif result_conseil == 12:
            print("➡️  Fais des étirements avant de te coucher : Prends quelques minutes pour les étirer doucement. Ça permet de récupérer plus rapidement.")
        elif result_conseil == 13:
            print("➡️  Ne te compare pas aux autres : Compare-toi uniquement au toi d'hier.")
        elif result_conseil == 14:
            print("➡️  Utilise des outils : Sprintia et les montres connectées/sportives peuvent t'aider à progresser et à gérer ton entraînement.")
        elif result_conseil == 15:
            print("➡️  Apprends la technique : Maîtrise les bons mouvements pour être plus efficace et réduire les risques de blessures.")
        elif result_conseil == 16:
            print("➡️  Repos : Tes muscles ont besoin de récupérer et de se reconstruire, alors prévois des jours de repos.")
        elif result_conseil == 17:
            print("➡️  Récompense-toi : Célèbre tes petites victoires pour maintenir ta motivation et ton plaisir à long terme.")
        elif result_conseil == 18:
            print("➡️  Amuse-toi avant tout : Le sport doit rester une source de joie et de bien-être dans ta vie.")
        elif result_conseil == 19:
            print("➡️  Sois patient : Les résultats viennent avec le temps et la persévérance, alors ne te décourage pas.")
        elif result_conseil == 20:
            print("➡️  Augmente la difficulté Progressivement : donne à ton corps de nouveaux défis en augmentant doucement le temps, l'intensité ou le nombre de tes exercices.")
    
        time.sleep(0.5)
        print("")
        print("-- Autre --")
        print("")
        print("Choisissez une option ⬇️")
        print("")
        print("1. 🔄 Réessayer | 2. 🔙 Retour")

        choix_astuce = input("Votre choix : ").strip()

        if choix_astuce == "1":
            conseils(account_id, username, password)
        elif choix_astuce == "2":
            accueil(account_id, username, password)
        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
            time.sleep(1)
            conseils(account_id, username, password)
    
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        conseils(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print("❌ Sélection incorrecte, veuillez réessayer")
        time.sleep(1)
        conseils(account_id, username, password)

def inscription():
    nettoyer_console()
    print("")
    print("-- 🖋️  Inscription 🖋️  --")
    username = input("Nom d'utilisateur (requis) : ").strip() #enlève les espaces au début et à la fin
    print("🔒 Votre saisie reste invisible pour garantir la confidentialité. 🛡️")
    password = getpass.getpass(prompt='Mots de passe : ')
    password_encode = password.encode("UTF-8")

    try:
        if not username or not password:
            print("")
            print(f"{Fore.RED}❌ Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.{Style.RESET_ALL}")
        else:
            if (password_valide(password)):
                print(f"{Fore.GREEN}✅ Le mot de passe est valide{Style.RESET_ALL}")
                sha256 = hashlib.sha256()
                sha256.update(password_encode)
                hashed_password = sha256.hexdigest()
                curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                print("")
                print(f"{Fore.GREEN}✅ Votre compte a été enregistré{Style.RESET_ALL}")
                print("")
                print(f"{Fore.BLUE}Bienvenue {username} ! Vous pouvez désormais utiliser Sprintia.{Style.RESET_ALL}") #Ne pas oublier le f !
                print("Vous pouvez maintenant vous connecter. ➡️")
                time.sleep(1)
                connection()

    except sqlite3.IntegrityError as e: #Erreur de contrainte UNIQUE dans la ligne username dans la table Account
        print("")
        print(f"{Fore.RED}❌ Erreur d'intégrité à la base de données : {e}{Style.RESET_ALL}")
        print("Ce nom d'utilisateur est probablement déjà utilisé ou un problème de données est survenu.")
        print("Veuillez réessayer avec un autre nom d'utilisateur.")
    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue lors de l'inscription : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        inscription()
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        inscription()
    
def a_propos():
    nettoyer_console()
    print("")
    print("-- ℹ️  À propos ℹ️  --")
    print("")
    print("Sprintia est conçue pour vous aidés avant et après un entraînement")
    print("Version : 1.3.6 - Alpha")
    print("Dernière mise à jour : 19 Juillet 2025")
    print("➡️  Développé par Gabriel Chapet")
    print("📧 gabchap486@gmail.com")
    print("")
    print("1. 🆕 Nouveautés | 2. 🔙 Retour")

    choix_info = input("Votre choix : ").strip()

    if choix_info == "1":
        nouveautés_maj()
        
    elif choix_info == "2":
        menu_de_connection()
    
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        a_propos()

def nouveautés_maj():
    nettoyer_console()
    print("")
    print("-- 🆕 Nouveautés 🆕 --")
    print("")
    print("1️⃣  Tableau dans historique d'entraînement") 
    print("2️⃣  Gestions des objectifs") 
    print("3️⃣  Gestion de diverses données en fonction du sport")
    print("4️⃣  Gestion des événements/des compétitions") 
    print("5️⃣  Possiblité de mettre une description à votre activité") 
    print("6️⃣  Graphique charge d'entraînement")
    print("7️⃣  Profite d'une interface plus propre : chaque menu s'affiche désormais seul !") 
    print("8️⃣  Messages de confirmations, erreurs et résultats en couleur")
    print("9️⃣  Charge d'entraînement plus précise") 
    print("🔟 Possibilité de mettre son statut d'entraînement en mode blessure ou en mode vacances")
    print("")
    print("1. 🔙 Retour")

    choix_nouveauté = input("Votre choix : ").strip()

    if choix_nouveauté == "1":
        a_propos()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        nouveautés_maj()

def exportation_fichiers(account_id, username, password, historique_activité):
    nettoyer_console()
    try:
        données_csv = []
        for row in historique_activité: #'row' = lignes
            date_activité = datetime.strptime(row[0], '%Y-%m-%d')
            date_formatée = date_activité.strftime('%d-%m-%Y')

            données_csv.append({
                "Date": date_formatée,
                "Sport": row[1],
                "Durée (min)": row[2],
                "RPE": row[3],
                "Fatigue": row[4],
                "Douleur": row[5],
                "Climat": row[6],
                "Charge": row[7],
            })

        noms_colonnes = ["Date", "Sport", "Durée (min)", "RPE", "Fatigue", "Douleur", "Climat", "Charge"]

        format_du_fichier = input("Choissisez l'extension du fichiers (exemple : .txt, .csv,...) : ").strip()
        nom_du_fichier = input("Choisissez le nom du fichier : ").strip()
        nom_complet = nom_du_fichier + format_du_fichier

        with open(nom_complet, 'w', newline='', encoding='utf-8') as fichier_csv:
            writer = csv.DictWriter(fichier_csv, fieldnames=noms_colonnes)
            writer.writeheader() #Écrit le nom des colonnes
            writer.writerows(données_csv)

        print("")
        print(f"{Fore.GREEN}✅ Le fichier CSV a été sauvegardé sous le nom : {nom_complet}{Style.RESET_ALL}") #il faut gérer les erreurs!!!
        time.sleep(2)
        accueil(account_id, username, password)
            
    except IOError as e:
        print(f"{Fore.RED}❌ Erreur lors de l'exportation de vos données d'activité : {e}{Style.RESET_ALL}")
        print("Veuillez-vous assurer que d'avoir mis une extension du fichier à la fin du nom du fichiers.")
        print("")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        exportation_fichiers(account_id, username, password, historique_activité)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        exportation_fichiers(account_id, username, password, historique_activité)   

def historique_entraînement(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 🔁 Historique d'entraînement 🔁 --")
    print("")
    try:
        date_actuelle = date.today()
        choix_date = input("📅  Depuis quand souhaitez-vous consulter votre historique (JJ-MM-AAAA) : ").strip()
        date_conversion = datetime.strptime(choix_date, '%d-%m-%Y') #conversion format datetime

        période_str = date_conversion.strftime('%Y-%m-%d')

        curseur.execute("SELECT date_activité, sport, durée, distance, allure, rpe, fatigue, douleur, climat, charge, dénivelé FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, période_str))
        historique_activité = curseur.fetchall()

        if historique_activité:
            print("🔁 Votre historique d'entraînement :")
            catégorie = ["Date", "Sport", "Durée (min)",  "Distance (km)", "Allure (/km)", "RPE", "Fatigue", "Douleur", "Climat", "Charge", "Dénivelé (m)"]
            données_tableau = []
            for row in historique_activité: #row = ligne de données extraite de la base de données

                date_activité = datetime.strptime(row[0], '%Y-%m-%d')
                date_obj = date_activité.strftime('%d-%m-%Y')
                données_tableau.append([date_obj, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])

            print(tabulate(données_tableau, headers=catégorie, tablefmt="grid"))
        else:
            print(f"{Fore.RED}🚫 Aucune activité trouvée pour cette période.{Style.RESET_ALL}")

        time.sleep(0.5)
        print("")
        print("-- Autre --")
        print("")
        print("Choisissez une option ⬇️")
        print("")
        print("1. 📁 Exportez vos données d'activités | 2. 📅 Modifier la date | 3. 🔙 Retour")

        choix_historique_entainement = input("Votre choix : ").strip()
            
        if choix_historique_entainement == "1":
            exportation_fichiers(account_id, username, password, historique_activité)
        elif choix_historique_entainement == "2":
            historique_entraînement(account_id, username, password)
        elif choix_historique_entainement == "3":
            accueil(account_id, username, password)
        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
            time.sleep(1)
            historique_entraînement(account_id, username, password)
        
    except sqlite3.Error as e: #Erreur SQLite
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e: #Capture toutes les erreurs inattendue
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        historique_entraînement(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        historique_entraînement(account_id, username, password)

def ajouter_objectif(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- ➕ Ajouter un objectif 🎯 --")
    print("")
    sport = input("Sport (Requis): ").strip()
    date_str = input("Date (Requis) (JJ-MM-AAAA) : ").strip()
    date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
    date = date_conversion.strftime('%Y-%m-%d')

    objectif = input("Votre objectif (Requis) (ex : perte de poids, prise de muscle, s'améliorer, préparer une compétition) : ").strip()
    fréquence = input("À quelle fréquence comptes-tu t'entraîner ? (Ex: 1-2 fois par semaine,...) : ")
    niveau = input("Votre niveau actuel (débutant, intermédiaire, avancé) : ")
    statut = input("Nouveau statut (en cours, atteint, non atteint) : ")

    if not sport or not date_str or not objectif or not fréquence or not niveau:
        print(f"{Fore.RED}❌ Veuillez remplir tout les champs requis{Style.RESET_ALL}")
    else:
        try:
            curseur.execute("INSERT INTO Objectif (account_id, sport, date, objectif, fréquence, niveau_début, statut) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, sport, date, objectif, fréquence, niveau, statut))
            con.commit()
            print("")
            print(f"{Fore.GREEN}✅ Votre objectif a été enregistré, bonne chance !{Style.RESET_ALL}")
            time.sleep(1)
            accueil(account_id, username, password)
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue lors de l'inscription : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")

        time.sleep(2)
        print("")
        print("1. 🔄 Réessayer | 2. 🛑 Quitter")
        print("")

        choix_erreur = input("Votre choix : ").strip()

        if choix_erreur == "1":
            ajouter_objectif(account_id, username, password)
        elif choix_erreur == "2":
            print("")
            print("👋 Au revoir et à bientôt sur Sprintia !")
            con.close()
            exit()
        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
            time.sleep(1)
            ajouter_objectif(account_id, username, password)

def modifier_objectif(account_id, username, password):
    nettoyer_console()
    print("-- ✏️  Modifier un objectif ✏️  --")
    try:
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        if not result:
            print(f"{Fore.RED}🚫 Aucun objectif à modifier.{Style.RESET_ALL}")
            time.sleep(2)
            mes_objectifs(account_id, username, password)
        elif result:            
            catégorie = ["id", "Sport", "Date", "Objectif", "Statut"]
            données_tableau = []
            for row in result:
                données_tableau.append([row[0], row[1], row[2], row[3], row[4]])
                print(tabulate(données_tableau, headers=catégorie, tablefmt="grid"))

        choix = input("ID de l'objectif à modifier : ").strip()
        nouveau_statut = input("Nouveau statut : (⏳ en cours, ✅ atteint, ❌ non atteint) : ").strip().lower()
        try:
            if not choix.isdigit():
                print("L'ID est invalide.")
                return
            choix_id_saisi = int(choix)
            ids_objectifs_disponibles = [obj[0] for obj in result]

            if choix_id_saisi in ids_objectifs_disponibles:
                if nouveau_statut in ["en cours", "atteint", "non atteint"]:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("UPDATE Objectif SET statut = ? WHERE id = ? AND account_id = ?", (nouveau_statut, objectif_id_db, account_id))
                    con.commit()                
                    print(f"{Fore.GREEN}✅ Objectif mis à jour avec succès.{Style.RESET_ALL}")
                    time.sleep(1)
                    mes_objectifs(account_id, username, password)
                else:
                    print(f"{Fore.RED}❌ Statut invalide.{Style.RESET_ALL}")
                    time.sleep(1)
                    modifier_objectif(account_id, username, password)
            else:
                print(f"{Fore.RED}❌L'ID d'objectif saisi n'existe pas ou n'appartient pas à votre compte.{Style.RESET_ALL}")
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
        else:
            print(f"{Fore.RED}❌ Choix invalide.{Style.RESET_ALL}")
            time.sleep(1)
            modifier_objectif(account_id, username, password)

    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        modifier_objectif(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        modifier_objectif(account_id, username, password)

def supprimer_competition(account_id, username, password):
    nettoyer_console()
    print("-- 🗑️  Supprimer une compétition 🗑️  --")
    try:
        curseur.execute("SELECT id, nom, date FROM Compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        if not result:
            print(f"{Fore.RED}🚫 Aucune compétition à supprimer.{Style.RESET_ALL}")
            time.sleep(2)
            mes_objectifs(account_id, username, password)
        elif result:            
            catégorie = ["id", "Nom", "Date"]
            données_tableau = []
            for row in result:
                données_tableau.append([row[0], row[1], row[2]])
                print(tabulate(données_tableau, headers=catégorie, tablefmt="grid"))

        choix = input("ID de la compétition à supprimer : ").strip()
        try:
            if not choix.isdigit():
                print(f"{Fore.RED}❌ L'ID doit être un nombre.{Style.RESET_ALL}")
                return

            choix_id_saisi = int(choix)
            ids_competitions_disponibles = [comp[0] for comp in result]

            if choix_id_saisi in ids_competitions_disponibles:
                competition_id_db = choix_id_saisi
                curseur.execute("DELETE FROM Compétition WHERE id = ? AND account_id = ?", (competition_id_db, account_id))
                con.commit()
                print(f"{Fore.GREEN}✅ Compétition supprimée avec succès.{Style.RESET_ALL}")
                time.sleep(1)
                mes_objectifs(account_id, username, password)
            else:
                print(f"{Fore.RED}❌ L'ID de la compétition est invalide.{Style.RESET_ALL}")
                time.sleep(1)
                supprimer_competition(account_id, username, password)
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        supprimer_competition(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        supprimer_competition(account_id, username, password)

def supprimer_objectif(account_id, username, password):
    nettoyer_console()
    print("-- 🗑️  Supprimer un objectif 🗑️  --")
    try:
        curseur.execute("SELECT id, sport, date, objectif FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        if not result:
            print(f"{Fore.RED}🚫 Aucun objectif à supprimer.{Style.RESET_ALL}")
            time.sleep(2)
            mes_objectifs(account_id, username, password)
        elif result:            
            catégorie = ["id", "Sport", "Date", "Objectif", "Statut"]
            données_tableau = []
            for row in result:
                données_tableau.append([row[0], row[1], row[2], row[3], row[4]])
                print(tabulate(données_tableau, headers=catégorie, tablefmt="grid"))

        choix = input("ID de l'objectif à supprimer : ").strip()

        try:
            if not choix.isdigit():
                print("❌ L'ID doit est invalide.")
                return

            choix_id_saisi = int(choix)
            ids_objectifs_disponibles = [obj[0] for obj in result]

            if choix_id_saisi in ids_objectifs_disponibles:
                objectif_id_db = choix_id_saisi
                curseur.execute("DELETE FROM Objectif WHERE id = ? AND account_id = ?", (objectif_id_db, account_id))
                con.commit()
                print(f"{Fore.GREEN}✅ Objectif supprimé avec succès.{Style.RESET_ALL}")
                time.sleep(1)
                mes_objectifs(account_id, username, password)
            else:
                print(f"{Fore.RED}❌ L'ID d'objectif saisi n'existe pas ou n'appartient pas à votre compte.{Style.RESET_ALL}")
                time.sleep(1)
                supprimer_objectif(account_id, username, password)
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        supprimer_objectif(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        supprimer_objectif(account_id, username, password)

def mes_objectifs(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 🎯 Objectifs 🎯 --")
    print("")
    print("Mes objectifs ⬇️")
    print("")
    try:
        date_actuelle = date.today().isoformat() #pour convertir les dates en YYYY-MM-DD
        curseur.execute("SELECT sport, date, objectif, fréquence, niveau_début, statut FROM Objectif WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
        objectif_result = curseur.fetchall()

        if objectif_result:            
            catégorie = ["Sport", "Date", "Objectif", "Fréquence", "Niveau au début de l'objectif", "Statut"]
            données_tableau = []
            for row in objectif_result:
                données_tableau.append([row[0], row[1], row[2], row[3], row[4], row[5]])
            print(tabulate(données_tableau, headers=catégorie, tablefmt="grid"))
        else:
            print(f"{Fore.RED}🚫 Aucun objectif à venir trouvée.{Style.RESET_ALL}")

        time.sleep(2)
        print("")
        print("-- Autre --")
        print("")
        print("Choisissez une option ⬇️")
        print("")
        print("1. 🎯 Ajouter un objectif | 2. 🗑️  Supprimer un objectif | 3. ✏️  Modifier un objectif")
        print("                                     4. 🔙 Retour")

        choix_compétition = input("Votre choix : ").strip()
            
        if choix_compétition == "1":
            ajouter_objectif(account_id, username, password)
        elif choix_compétition == "2":
            supprimer_objectif(account_id, username, password)
        elif choix_compétition == "3":
            modifier_objectif(account_id, username, password)
        elif choix_compétition == "4":
            accueil(account_id, username, password)
        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
            time.sleep(1)
            mes_objectifs(account_id, username, password)  

    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        mes_objectifs(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        compétition(account_id, username, password)

def ajouter_compétition(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- ➕ Ajouter une compétition 🏆 --")
    print("")
    nom = input("Nom de compétition (Requis) : ").strip()
    date_str = input("Date (Requis) (JJ-MM-AAAA) : ").strip()
    date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
    date = date_conversion.strftime('%Y-%m-%d')

    sport = input("Sport (Requis): ").strip()
    objectif = input("Votre objectif (Requis) (ex : Courir 10km en 45 min) : ").strip()


    if not nom or not date_str or not sport or not objectif:
        print(f"{Fore.RED}❌ Veuillez remplir tout les champs requis{Style.RESET_ALL}")
    else:
        try:
            curseur.execute("INSERT INTO Compétition (account_id, nom, date, sport, objectif) VALUES (?, ?, ?, ?, ?)", (account_id, nom, date, sport, objectif))
            con.commit()
            print("")
            print(f"{Fore.GREEN}✅ Votre compétition a été enregistré, bonne chance !{Style.RESET_ALL}")
            time.sleep(1)
            accueil(account_id, username, password)
        except sqlite3.Error as e:
            print("")
            print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e:
            print(f"{Fore.RED}❌ Une erreur inattendue est survenue lors de l'inscription : {e}{Style.RESET_ALL}")
            print("Si le problème persiste veuillez contacter le développeur.")

        time.sleep(2)
        print("")
        print("1. 🔄 Réessayer | 2. 🛑 Quitter")
        print("")

        choix_erreur = input("Votre choix : ").strip()

        if choix_erreur == "1":
            ajouter_compétition(account_id, username, password)
        elif choix_erreur == "2":
            print("")
            print("👋 Au revoir et à bientôt sur Sprintia !")
            con.close()
            exit()
        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
            time.sleep(1)
            ajouter_compétition(account_id, username, password)

def activer_pause(account_id, username, password, type_pause):
    #Vérifie si une pause est déjà actif
    curseur.execute("SELECT id FROM Pauses WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    if curseur.fetchone():
        print(f"{Fore.RED}❌ Une pause est déjà active.{Style.RESET_ALL}")
        return

    #Active la pause
    #date('now') c'est une fonction SQLite
    curseur.execute("""INSERT INTO Pauses (account_id, type, date_debut)VALUES (?, ?, date('now'))""", (account_id, type_pause))
    con.commit()
    print(f"{Fore.GREEN}✅ Pause '{type_pause}' activée !{Style.RESET_ALL}")
    time.sleep(1)
    accueil(account_id, username, password)

def arreter_pause(account_id, username, password):
    #date('now') c'est une fonction SQLite
    curseur.execute("""UPDATE Pauses SET date_fin = date('now')WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    con.commit()
    print(f"{Fore.GREEN}✅ Reprise d'activité !{Style.RESET_ALL}")
    time.sleep(1)
    accueil(account_id, username, password)

def verifier_pause(account_id):
    #AND date_fin IS NULL = Cibler uniquement les pauses en cours (non terminés).
    curseur.execute("""SELECT type FROM Pauses WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    result = curseur.fetchone()
    return result[0] if result else None

def compétition(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 🏆 Compétition 🏆 --")
    print("")
    print("Mes compétitions ⬇️")
    print("")
    try:
        date_actuelle = date.today().isoformat() #pour convertir les dates en YYYY-MM-DD
        curseur.execute("SELECT nom, date, sport, objectif FROM Compétition WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
        compétition_result = curseur.fetchall()

        if compétition_result:            
            catégorie = ["Nom", "Date", "Sport", "Objectif"]
            données_tableau = []
            for row in compétition_result:
                données_tableau.append([row[0], row[1], row[2], row[3]])

            print(tabulate(données_tableau, headers=catégorie, tablefmt="grid"))
        else:
            print(f"{Fore.RED}🚫 Aucune compétition à venir trouvée.{Style.RESET_ALL}")

        time.sleep(2)
        print("")
        print("-- Autre --")
        print("")
        print("Choisissez une option ⬇️")
        print("")
        print("1. 🏆 Ajouter une compétition | 2. 🗑️  Supprimer une compétition | 3. 🔙 Retour")

        choix_compétition = input("Votre choix : ").strip()
            
        if choix_compétition == "1":
            ajouter_compétition(account_id, username, password)
        elif choix_compétition == "2":
            supprimer_competition(account_id, username, password)
        elif choix_compétition == "3":
            accueil(account_id, username, password)
        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
            time.sleep(1)
            compétition(account_id, username, password)  

    except sqlite3.Error as e: #Erreur SQLite
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e: #Capture toutes les erreurs inattendue
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        compétition(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        compétition(account_id, username, password)

def créer_activité(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- ✍🏻 Créer une activité ✍🏻 --")
    print("")

    try:
        while True:
            date_str = input("Quelle était la date de ton activité (JJ-MM-AAAA) : ").strip()
            try:
                date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
                date = date_conversion.strftime('%Y-%m-%d')
                break #pour fermer la boucle while True
            except ValueError:
                print(f"{Fore.RED}❌ Format de date invalide. Veuillez utiliser JJ-MM-AAAA.{Style.RESET_ALL}")

        sport = input("Quel sport as-tu pratiqué : ").strip()
        while True:
            try :
                durée = int(input("Quelle était la durée de ton activité (en min) : "))
                if durée < 0 :
                    print(f"{Fore.RED}❌ La durée doit être un nombre positif.{Style.RESET_ALL}")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}❌ Entrée invalide. Veuillez saisir un nombre entier pour la durée.{Style.RESET_ALL}")

        distance = None
        allure = None
        dénivelé = None

        if sport.lower() in ["course à pied", "course", "running", "run", "course a pied", 
                             "tapis de course", "athlétisme", "athletisme", "course sur piste", "marche", "marche à pied",
                             "marche a pied", "course d'orientation", "roller", "luge", "snowboard", "skateboard"]:
            while True:
                distance = float(input("Quelle distance as-tu parcourue (en km) (ex : 8.43) : "))
                try:
                    if distance < 0:
                        print(f"{Fore.RED}❌ La distance doit être un nombre supérieur à 0.{Style.RESET_ALL}")
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}❌ La distance doit être un nombre. Veuillez réesayer.{Style.RESET_ALL}")
            
            allure = durée / distance
            minutes = int(allure)
            secondes = int((allure - minutes) * 60)
            print(f"💡 Allure calculée : {minutes}:{secondes:02d} min/km") # le ":O2d" = 2 chiffres après la virgule

        elif sport.lower() in ["vélo", "velo", "cyclisme", "bike", "vélo élliptique", "velo elliptique",
                               "vélo d'intérieur", "velo d'interieur","vélo d'appartement", "velo d'appartement",
                               "vtt"]:
            while True:
                distance = float(input("Quelle distance as-tu parcourue (en km) : "))
                try:
                    if distance < 0:
                        print(f"{Fore.RED}❌ La distance doit être un nombre supérieur à 0.{Style.RESET_ALL}")
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}❌ La distance doit être un nombre. Veuillez réesayer.{Style.RESET_ALL}")

            vitesse_moyenne = distance / (durée / 60)
            allure = vitesse_moyenne
            print(f"💡 Vitesse moyenne calculée : {allure:.2f} km/h")
            
        elif sport.lower() in ["natation", "nage", "swimming", "rameur", "rameur intérieur", "rameur interieur",
                               "aviron", "canoë-kayak", "canoe-kayak", "voile", "planche à voile",
                               "planche a voile", "surf"]:
            while True:
                distance = float(input("Quelle distance as-tu nagée (en m) : "))
                try:
                    if distance < 0:
                        print(f"{Fore.RED}❌ La distance doit être un nombre supérieur à 0.{Style.RESET_ALL}")
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}❌ La distance doit être un nombre. Veuillez réesayer.{Style.RESET_ALL}")

            allure = (durée * 100) / distance
            minutes = int(allure)
            secondes = int((allure - minutes) * 60)
            print(f"💡 Allure calculée : {minutes}:{secondes:02d} min/100m")

        elif sport.lower() in ["ultra-trail", "randonnée", "randonnee","trail", "ski de fond", "ski alpin", 
                               "ski",]:
            while True:
                distance = float(input("Quelle distance as-tu parcourue (en km) : "))
                try:
                    if distance < 0:
                        print(f"{Fore.RED}❌ La distance doit être un nombre supérieur à 0.{Style.RESET_ALL}")
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}❌ La distance doit être un nombre. Veuillez réesayer.{Style.RESET_ALL}")

            allure = durée / distance
            minutes = int(allure)
            secondes = int((allure - minutes) * 60)
            print(f"💡 Allure calculée : {minutes}:{secondes:02d} min/km")
            while True:
                dénivelé = int(input("Quel est le dénivelé total de votre parcours (en m) : "))
                try:
                    if dénivelé < 0:
                        print(f"{Fore.RED}❌ Le dénivelé doit être un nombre supérieur à 0.{Style.RESET_ALL}")
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}❌ Le dénivelé doit être un nombre entier. Veuillez réesayer.{Style.RESET_ALL}")

        rpe = int(input("Note cet effort sur une échelle de 1 à 10 : "))
        if not 1 <= rpe <= 10:
            print(f"{Fore.RED}❌ Vous devez saisir un nombre entre 1 et 10{Style.RESET_ALL}")
            time.sleep(1)
            créer_activité(account_id, username, password)
        else:
            fatigue = int(input("Quel est ton niveau de fatigue sur une échelle de 1 à 10 après cette entraînement : "))
            if not 1 <= fatigue <= 10:
                print(f"{Fore.RED}❌ Vous devez saisir un nombre entre 1 et 10{Style.RESET_ALL}")
                time.sleep(1)
                créer_activité(account_id, username, password)
            else:
                douleur = int(input("As-tu des douleurs après cette séance (0= non, 1= un peu, 2= oui, 3= blessure) : "))
                if not 0 <= douleur <= 3:
                    print(f"{Fore.RED}❌ Vous devez saisir un chiffre entre 0 et 3{Style.RESET_ALL}")
                    time.sleep(1)
                    créer_activité(account_id, username, password)
                else:
                    climat = int(input("Climat (0= Normal, 1= Chaud, 2= Froid, 3= Difficile) : "))
                    if not 0 <= climat <= 3:
                        print(f"{Fore.RED}❌ Vous devez saisir un chiffre entre 0 et 3{Style.RESET_ALL}")
                        time.sleep(1)
                        créer_activité(account_id, username, password)
                    else:
                        description = input("Despription (pas obligatoire) : ")

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

                        curseur.execute("""
                            INSERT INTO Activité (date_activité, sport, durée, distance, allure, rpe, fatigue, douleur, climat, charge, account_id, description, dénivelé)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                        (date, sport, durée, distance, allure, rpe, fatigue, douleur, climat, charge_activité, account_id, description, dénivelé)) 
                        con.commit()
                        print("")
                        print(f"{Fore.GREEN}✅ Votre activité a été enregistré.{Style.RESET_ALL}")
                        time.sleep(1)
                        accueil(account_id, username, password)

    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")

    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        accueil(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        accueil(account_id, username, password)

def charge_entraînement(account_id, username, password):
    nettoyer_console()
    print("")
    print("-- 📈 Charge d'entraînement 📈 --")
    try:
        #date
        date_actuelle = date.today()

        ca = date_actuelle - timedelta(days=7)  #ca = charge aïgue
        ca_str = ca.strftime('%Y-%m-%d')
        curseur.execute("SELECT charge FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, ca_str))
        charges_aigue = [row[0] for row in curseur.fetchall()]

        cc = date_actuelle - timedelta(days=28)  #cc = charge chronique
        cc_str = cc.strftime('%Y-%m-%d')
        curseur.execute("SELECT date_activité, charge FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité ASC", (account_id, cc_str))
        data_pour_graphique = curseur.fetchall()

        #Calcul des moyennes
        charge_aigue = sum(charges_aigue) / len(charges_aigue) if charges_aigue else 0

        #On prend le 2ème élément des data pour graphique pour avoir les charges et ne pas prendre les dates
        charge_chronique = sum([row[1] for row in data_pour_graphique]) / len(data_pour_graphique) if data_pour_graphique else 0

        #Ratio de charge
        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None

        print("")
        print(f"📈 Charge aiguë (7 jours) : {charge_aigue:.1f}")
        print(f"📈 Charge chronique (28 jours) : {charge_chronique:.1f}")

        pause = verifier_pause(account_id)
        if pause == "blessure":
            print("⛑️ Mode blessure : suivi désactivé.")
            time.sleep(1.2)
            accueil(account_id, username, password)
        elif pause == "vacances":
            print("🏖️  Mode vacances : pas d'analyse.")
            time.sleep(1.2)
            accueil(account_id, username, password)

        if ratio is not None:
            print(f"📊 Ratio : {ratio:.2f}")
            print("")
            if ratio < 0.5:
                print(f"{Fore.BLUE}🛌 Récupération active : Charge très basse. Priorité à la régénération{Style.RESET_ALL}")
            elif 0.5 <= ratio <= 0.8:
                print(f"{Fore.CYAN}😴 Sous-entraînement : Vous pourriez augmenter légèrement l'intensité.{Style.RESET_ALL}")
            elif 0.8 <= ratio <= 0.9:
                print(f"{Fore.GREEN}🔄 Maintien : Charge adaptée pour conserver votre niveau.{Style.RESET_ALL}")
            elif 0.9 <= ratio <= 1.1:
                print(f"{Fore.GREEN}🟢 Progression optimale : Charge idéale pour améliorer vos performances{Style.RESET_ALL}")
            elif 1.1 < ratio <= 1.3:
                print(f"{Fore.YELLOW}💪 Progression élévée : Restez vigilant à la fatigue accumulée.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}⚠️  Surentraînement : Risque élevé de blessure. Repos nécessaire.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}🚫 Données insuffisantes pour calculer le ratio.{Style.RESET_ALL}")

        time.sleep(0.5)
        print("")
        print("1. 📊 Voir graphique | 2. 🔙 Retour")
        print("")

        choix_charge = input("Votre choix : ").strip()

        if choix_charge == "1":
            try:
                if data_pour_graphique:
                    dates_graphique = [datetime.strptime(row[0], '%Y-%m-%d') for row in data_pour_graphique]
                    charges_graphique = [row[1] for row in data_pour_graphique]

                    #graphique
                    plt.figure(figsize=(12, 4))
                    sns.lineplot(x=dates_graphique, y=charges_graphique, marker='o', color='blue') 

                    # On ajoute une ligne pointillée rouge pour montrer la moyenne de la charge chronique
                    plt.axhline(y=charge_chronique, color='red', linestyle='--')

                    plt.title("Évolution de la charge chronique")

                    # On nomme les axes du graphique
                    plt.xlabel("Date")
                    plt.ylabel("Charge chronique")
                    plt.show()
                else :
                    print("")
                    print(f"{Fore.RED}❌ Vous n'avez pas encore assez de données pour pouvoir avoir un graphique{Style.RESET_ALL}")

            except sqlite3.Error as e:
                print("")
                print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
                print("Si le problème persiste veuillez contacter le développeur.")
            except Exception as e:
                print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
                print("Si le problème persiste veuillez contacter le développeur.")

            time.sleep(2)
            print("")
            print("1. 🔄 Réessayer | 2. 🛑 Quitter")
            print("")

            choix_erreur = input("Votre choix : ").strip()

            if choix_erreur == "1":
                charge_entraînement(account_id, username, password)
            elif choix_erreur == "2":
                print("")
                print("👋 Au revoir et à bientôt sur Sprintia !")
                con.close()
                exit()
            else:
                print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
                time.sleep(1)
                charge_entraînement(account_id, username, password)
                
        elif choix_charge == "2":
            accueil(account_id, username, password)

        else:
            print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")

    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
    
    time.sleep(2)
    print("")
    print("1. 🔄 Réessayer | 2. 🛑 Quitter")
    print("")

    choix_erreur = input("Votre choix : ").strip()

    if choix_erreur == "1":
        charge_entraînement(account_id, username, password)
    elif choix_erreur == "2":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()
    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        charge_entraînement(account_id, username, password)

def password_valide(password):
    SpecialSymbol =['$', '@', '#', '%', '?', '!']
    val = True

    if len(password) < 6:
        print(f'{Fore.RED}❌ La longueur doit être d\'au moins 6 caractères{Style.RESET_ALL}')
        val = False

    if len(password) > 20:
        print(f'{Fore.RED}❌ La longueur ne doit pas dépasser 20 caractères{Style.RESET_ALL}')
        val = False

    if not any(char.isdigit() for char in password):
        print(f'{Fore.RED}❌ Le mot de passe doit contenir au moins un chiffre{Style.RESET_ALL}')
        val = False

    if not any(char.isupper() for char in password):
        print(f'{Fore.RED}❌ Le mot de passe doit contenir au moins une lettre majuscule{Style.RESET_ALL}')
        val = False

    if not any(char.islower() for char in password):
        print(f'{Fore.RED}❌ Le mot de passe doit contenir au moins une lettre minuscule{Style.RESET_ALL}')
        val = False

    if not any(char in SpecialSymbol for char in password):
        print(f'{Fore.RED}❌ Le mot de passe doit contenir au moins un des symboles spéciaux : $@#%?!{Style.RESET_ALL}')
        val = False
    if val:
        return val

def accueil(account_id, username, password):
    nettoyer_console()
    print("")
    print(f"{Fore.BLUE} Bonjour {username} ! {Style.RESET_ALL}")
    print("")
    print("-- 🏠 Accueil 🏠 --")
    print("")
    print("Choisissez une option ⬇️")
    print("")
    print("1. ✍🏻 Créer une activité   | 2. 🔁 Historique d'entraînement")
    print("3. 📈 Charge d'entraînement | 4. 🏆 Compétition")
    print("5. 🎯 Objectifs             | 6. 💡 Conseils")
    print("7. 👤 Mon Compte            | 8. ➡️  Déconnexion")
    print("                      9. 🛑 Quitter")

    choix_accueil = input("Votre choix : ").strip()

    if choix_accueil == "1":
        créer_activité(account_id, username, password)

    elif choix_accueil == "2":
        historique_entraînement(account_id, username, password)

    elif choix_accueil == "3":
        charge_entraînement(account_id, username, password)

    elif choix_accueil == "4":
        compétition(account_id, username, password)

    elif choix_accueil == "5":
        mes_objectifs(account_id, username, password)

    elif choix_accueil == "6":
        conseils(account_id, username, password)

    elif choix_accueil == "7":
        mon_compte(account_id, username, password)

    elif choix_accueil == "8":
        deconnexion()

    elif choix_accueil == "9":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()

    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(2)
        accueil(account_id, username, password)

def menu_de_connection():
    nettoyer_console()
    print("")
    print(Style.RESET_ALL)
    if debut_printemps  <= date_actuelle <= fin_printemps:
        print("-- 🌸  Bienvenue sur Sprintia ! 🌸 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif debut_été  <= date_actuelle <= fin_été:
        print("-- ☀️  Bienvenue sur Sprintia ! 🏖️  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif debut_automne  <= date_actuelle <= fin_automne:
        print("-- 🍂  Bienvenue sur Sprintia ! 🌰 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif debut_hiver  <= date_actuelle <= fin_hiver:
        print("-- ❄️  Bienvenue sur Sprintia ! ☃️  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_jour_de_an == date_actuelle:
        print("-- 🎉  Bienvenue sur Sprintia ! 📅 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_saint_valentin == date_actuelle:
        print("-- ❤️  Bienvenue sur Sprintia ! 🌹 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_halloween == date_actuelle:
        print("-- 🎃  Bienvenue sur Sprintia ! 👻 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_noël == date_actuelle:
        print("-- 🎅  Bienvenue sur Sprintia ! 🎄 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_réveillon == date_actuelle:
        print("-- 🎉  Bienvenue sur Sprintia ! 🥂 --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_fête_nationale == date_actuelle:
        print("-- 📅  Bienvenue sur Sprintia ! 🥳  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_jour_de_la_femmes == date_actuelle:
        print("-- ♀️   Bienvenue sur Sprintia ! 💜  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_anniversaire_sprintia == date_actuelle:
        print("-- 🎂  Bienvenue sur Sprintia ! 🥳  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_fête_du_travail == date_actuelle:
        print("-- 🛠️   Bienvenue sur Sprintia ! 📅  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_victoire_de_1945 == date_actuelle:
        print("-- 🕊️   Bienvenue sur Sprintia ! 📅  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_premiere_guerre_mondiale == date_actuelle:
        print("-- 🕊️   Bienvenue sur Sprintia ! 🕰️   --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_toussaint == date_actuelle:
        print("-- 🕯️   Bienvenue sur Sprintia ! 🙏  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_droits_de_homme == date_actuelle:
        print("-- ⚖️   Bienvenue sur Sprintia ! 📜  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    elif date_rentrée == date_actuelle:
        print("-- 🎒  Bienvenue sur Sprintia ! 📚  --")
        print("💪 Votre compagnon d'entraînement !")
        print("")
    else:
        print("-- 🏅 Bienvenue sur Sprintia ! 🏅 --")
        print("🏃 Votre compagnon d'entraînement !")
        print("")
    if date_début_maj <= date_actuelle <= date_fin_maj:
        maj()
    print("Choisissez une option ⬇️")
    print("")
    print("1. 🌐 Connection | 2. 🖋️  Inscription")
    print("3. ℹ️  À propos   | 4. 🛑  Quitter")

    choix = input("Votre choix : ").strip()

    if choix == "1":
        connection()

    elif choix == "2":
        inscription()

    elif choix == "3":
        a_propos()      
           
    elif choix == "4":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")
        con.close()
        exit()

    else:
        print(f"{Fore.RED}❌ Sélection incorrecte, veuillez réessayer{Style.RESET_ALL}")
        time.sleep(1)
        menu_de_connection()
                
    time.sleep(1)

def main():
    nettoyer_console()
    if date_début_bienvenue  <= date_actuelle <= date_fin_bienvenue:
        print("")
        print("👋 Bienvenue sur la nouvelle version de Sprintia !")
        print("🆕 Nous espérons que les nouvelles fonctionnalités vous plairont. ✨")
        print("Merci beaucoup pour votre soutien ! ❤️")
        time.sleep(3)
    menu_de_connection()

if __name__ == "__main__":
    try:
        con = sqlite3.connect("sport_data1.0.db")
        curseur = con.cursor()

        curseur.execute('''CREATE TABLE IF NOT EXISTS Account (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL)''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,allure INTEGER,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,description TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Compétition (id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT NOT NULL,date TEXT NOT NULL,sport TEXT NOT NULL,objectif TEXT NOT NULL,account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Objectif (id INTEGER PRIMARY KEY AUTOINCREMENT,sport TEXT NOT NULL,date TEXT NOT NULL,objectif TEXT NOT NULL,fréquence TEXT NOT NULL,niveau_début TEXT NOT NULL,statut TEXT, account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Pauses (id INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER NOT NULL,type TEXT CHECK(type IN ('vacances', 'blessure')),date_debut TEXT DEFAULT CURRENT_DATE,date_fin TEXT,FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        con.commit()

    except sqlite3.Error as e:
        print("")
        print(f"{Fore.RED}❌ Erreur lors de la connexion à la base de données : {e}{Style.RESET_ALL}")
        print("Si le problème persiste, veuillez contacter le développeur.")
        con.close()
        exit()
    except Exception as e:
        print(f"{Fore.RED}❌ Une erreur inattendue est survenue : {e}{Style.RESET_ALL}")
        print("Si le problème persiste veuillez contacter le développeur.")
        con.close()
        exit()

    main()