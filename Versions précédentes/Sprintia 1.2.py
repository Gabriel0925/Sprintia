import sqlite3
import hashlib
import time
import getpass
import random
import csv
from datetime import date, datetime, timedelta

#variables
date_actuelle = date.today()

#dates maj
date_début_maj = date(2025, 7, 13)
date_fin_maj = date(2026, 7, 13)

date_début_bienvenue = date(2025, 7, 6)
date_fin_bienvenue = date(2025, 7, 10)

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

def maj():
    print("🆕 Une mise à jour est disponible 🆕")
    print("")
    print("➡️  Sprintia 1.3 est disponible")
    print("")
    print("1. ▶️  Lancer la mise à jour 🔄")
    print("2. 🛑 Quitter 🛑")

    choix_jour_de_maj = input("Votre choix : ")

    if choix_jour_de_maj == "1":
        print("")
        print("-- ⚙️  Mise à jour en cours ⚙️  --")
        print("⏳ Chargement ⏳")
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
        print("✅ Sprintia a été mis à jour")
        time.sleep(2)
        print("")
        print("🔄 Veuillez ouvrir le nouveau fichiers Sprintia 1.3")
        time.sleep(2)

    elif choix_jour_de_maj == "2":
        print("👋 Au revoir et à bientôt sur Sprintia !")

def modifier_mots_de_passe(account_id, username, password):
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
                print("❌ Le mot de passe ne peuvent pas être vides.")
            else:
                if (password_valide(new_password)):
                    print("✅ Le mot de passe est valide")
                    sha256 = hashlib.sha256()
                    sha256.update(password_encode)
                    hashed_password = sha256.hexdigest()
                    con.execute("UPDATE Account SET password = ? WHERE id = ?", (hashed_password, account_id))
                    con.commit()
                    print("")
                    print("✅ Votre mots de passe à bien été modifié")
                    print("")
                    print("Vous pouvez maintenant vous connecter. ➡️")
                    time.sleep(2)
                    connection()
                
        except sqlite3.Error as e:
            print("")
            print(f"❌ Erreur lors de la connexion à la base de données : {e}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
        except Exception as e:
            print(f"❌ Une erreur inattendue est survenue lors de la modification du mots de passe : {e}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
    else:
        print("❌ Les mots de passe saisis ne correspondent pas.")

def modifier_nom_utilisateur(account_id, username, password):
    print("")
    print("-- 🔒 Modification de votre nom d'uilisateur ✍️  --")
    print("")
    new_username = input("Nouveau nom d'utilisateur : ").strip()
    new_username2 = input("Confirmez votre nouveau nom d'utilisateur : ").strip()

    if new_username == new_username2:
        try:
            if not new_username:
                print("")
                print("❌ Le nom d'utilisateur ne peut pas être vides.")
            else:
                con.execute("UPDATE Account SET username = ? WHERE id = ?", (username, account_id))
                con.commit()
                print("")
                print("✅ Votre nom d'utilisateur à bien été modifié")
                print("")
                print("Vous pouvez maintenant vous connecter. ➡️")
                time.sleep(2)
                connection()

        except sqlite3.IntegrityError as e: 
            print("")
            print(f"❌ Erreur d'intégrité à la base de données : {e}")
            print("Ce nom d'utilisateur est probablement déjà utilisé ou un problème de données est survenu.")
            print("Veuillez réessayer avec un autre nom d'utilisateur.")
            time.sleep(2)
            modifier_nom_utilisateur(account_id, username, password)
        except sqlite3.Error as e:
            print("")
            print(f"❌ Erreur lors de la connexion à la base de données : {e}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
        except Exception as e:
            print(f"❌ Une erreur inattendue est survenue lors de la modification du mots de passe : {e}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            modifier_mots_de_passe(account_id, username,password)
    else:
        print("❌ Les mots de passe saisis ne correspondent pas.")

def connection():
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
            print("❌ Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
        if result:
            account_id = result[0]
            print("")
            print(f"✅ Vous êtes connectés en tant que {username}")
            time.sleep(1)
            accueil(account_id, username, password)
        else:
            print("❌ Identifiants incorrects. Veuillez réessayer.")
            time.sleep(2)
            connection()
    except sqlite3.Error as e:
        print("")
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        print("Si le problème persiste, veuillez contacter le développeur.")
        time.sleep(2)
        connection()

    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue lors de la connexion : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        connection()

def mon_compte(account_id, username, password):
    print("")
    print("-- 👤 Mon compte 👤  --")
    print("")
    print(f"🆔 Votre ID : {account_id}")
    print(f"🧑 Votre nom d'utilisateur : {username}")
    time.sleep(2)
    
    print("")
    print("Choisissez une option ⬇️")
    print("")
    print("1. 🔒 Modifier mon mots de passe ✍️")
    print("2. 🧑 Modifier mon nom d'utilisateur ✍️")
    print("3. 🔙 Retour")

    choix_compte = input("Votre choix : ")

    if choix_compte == "1":
        modifier_mots_de_passe(account_id, username, password)
    elif choix_compte == "2":
        modifier_nom_utilisateur(account_id, username, password)
    elif choix_compte == "3":
        accueil(account_id, username, password)
    else:
        print("❌ Sélection incorrecte, veuillez réessayer")
        time.sleep(1)
        mon_compte(account_id, username, password)

def conseils(account_id, username, password):
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
    
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        conseils(account_id, username, password)

    time.sleep(2)
    print("")
    print("-- Autre --")
    print("")
    print("Choisissez une option ⬇️")
    print("")
    print("1. 🔄 Réessayer 🔄")
    print("2. 🔙 Retour")

    choix_astuce = input("Votre choix : ")

    if choix_astuce == "1":
        conseils(account_id, username, password)
    elif choix_astuce == "2":
        accueil(account_id, username, password)
    else:
        print("❌ Sélection incorrecte, veuillez réessayer")
        time.sleep(1)
        conseils(account_id, username, password)

    time.sleep(2)

def inscription():
    print("")
    print("-- 🖋️  Inscription 🖋️  --")
    username = input("Nom d'utilisateur (requis) : ").strip() #enlève les espaces au début et à la fin
    print("🔒 Votre saisie reste invisible pour garantir la confidentialité. 🛡️")
    password = getpass.getpass(prompt='Mots de passe : ')
    password_encode = password.encode("UTF-8")

    try:
        if not username or not password:
            print("")
            print("❌ Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
        else:
            if (password_valide(password)):
                print("✅ Le mot de passe est valide")
                sha256 = hashlib.sha256()
                sha256.update(password_encode)
                hashed_password = sha256.hexdigest()
                curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                print("")
                print("✅ Votre compte a été enregistré")
                print("")
                print(f"Bienvenue {username} ! Vous pouvez désormais utiliser Sprintia.") #Ne pas oublier le f !
                print("Vous pouvez maintenant vous connecter. ➡️")
                time.sleep(1)
                connection()
            
        time.sleep(2)

    except sqlite3.IntegrityError as e: #Erreur de contrainte UNIQUE dans la ligne username dans la table Account
        print("")
        print(f"❌ Erreur d'intégrité à la base de données : {e}")
        print("Ce nom d'utilisateur est probablement déjà utilisé ou un problème de données est survenu.")
        print("Veuillez réessayer avec un autre nom d'utilisateur.")
        time.sleep(2)
        inscription()
    except sqlite3.Error as e:
        print("")
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        inscription()
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue lors de l'inscription : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        inscription()
    
def a_propos():
    print("")
    print("-- ℹ️  À propos ℹ️  --")
    print("")
    print("Sprintia est conçue pour vous aidés avant et après un entraînement")
    print("Version : 1.2.1 - Alpha")
    print("Dernière mise à jour : 06 Juillet 2025")
    print("➡️  Développé par Gabriel Chapet")
    print("📧 gabchap486@gmail.com")
    print("")
    print("1. 🆕 Nouveautés 🆕")
    print("2. 🔙 Retour")

    choix_info = input("Votre choix : ")

    if choix_info == "1":
        nouveautés_maj()
        
    elif choix_info == "2":
        menu_de_connection()
    
    else:
        print("❌ Sélection incorrecte, veuillez réessayer")
        time.sleep(2)
        a_propos()

def nouveautés_maj():
    print("")
    print("-- 🆕 Nouveautés 🆕 --")
    print("")
    print("1️⃣ Modularité du (Code avec des fonctions)")
    print("2️⃣ Accès à l'historique des entraînements")
    print("3️⃣ Exportation des Données d'Activités (CSV/JSON/...)")
    print("4️⃣ Modification du mots de passe du compte") 
    print("5️⃣ Modification du nom d'utilisateur")
    print("6️⃣ Accès aux informations du compte de l'utilisateur") 
    print("7️⃣ Astuce entrainement dans Accueil")
    print("8️⃣ Masquage des entrées de mot de passe")
    print("9️⃣ Accueil contextuel")
    print("")
    print("1. 🔙 Retour")

    choix_nouveauté = input("Votre choix : ")

    if choix_nouveauté == "1":
        a_propos()
    else:
        print("❌ Sélection incorrecte, veuillez réessayer")
        time.sleep(2)
        nouveautés_maj()

def exportation_fichiers(account_id, username, password, historique_activité):
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
            print(f"✅ Le fichier CSV a été sauvegardé sous le nom : {nom_complet}") #il faut gérer les erreurs!!!
            time.sleep(2)
            accueil(account_id, username, password)
            
        except IOError as e:
            print(f"❌ Erreur lors de l'exportation de vos données d'activité : {e}")
            print("Veuillez-vous assurer que d'avoir mis une extension du fichier à la fin du nom du fichiers.")
            print("")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            historique_entraînement(account_id, username, password)

        except Exception as e:
            print(f"❌ Une erreur inattendue est survenue : {e}")
            print("Si le problème persiste veuillez contacter le développeur.")
            time.sleep(2)
            historique_entraînement(account_id, username, password)    

def historique_entraînement(account_id, username, password):
    print("")
    print("-- 🔁 Historique d'entraînement 🔁 --")
    print("")
    try:
        date_actuelle = date.today()
        choix_date = input("📅  Depuis quand souhaitez-vous consulter votre historique (JJ-MM-AAAA) : ").strip()
        date_conversion = datetime.strptime(choix_date, '%d-%m-%Y') #conversion format datetime

        période_str = date_conversion.strftime('%Y-%m-%d')

        curseur.execute("SELECT date_activité, sport, durée, rpe, fatigue, douleur, climat, charge FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, période_str))
        historique_activité = curseur.fetchall()

        if historique_activité:
            print("🔁 Votre historique d'entraînement :")
            print("")
            for row in historique_activité: #row = ligne de données extraite de la base de données

                date_activité = datetime.strptime(row[0], '%Y-%m-%d')
                date_obj = date_activité.strftime('%d-%m-%Y')

                print(f"Date: {date_obj}, Sport: {row[1]}, Durée: {row[2]} min, RPE: {row[3]}, Fatigue: {row[4]}, Douleur: {row[5]}, Climat: {row[6]}, Charge: {row[7]:.1f}")
        else:
            print("🚫 Aucune activité trouvée pour cette période.")
        
    except sqlite3.Error as e: #Erreur SQLite
        print("")
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        accueil(account_id, username, password)
    except Exception as e: #Capture toutes les erreurs inattendue
        print(f"❌ Une erreur inattendue est survenue : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        accueil(account_id, username, password)

    time.sleep(2)
    print("")
    print("-- Autre --")
    print("")
    print("Choisissez une option ⬇️")
    print("")
    print("1. 📁 Exportez vos données d'activités 📁")
    print("2. 📅 Modifier la date pour consulter ton historique 📅")
    print("3. 🔙 Retour")

    choix_historique_entainement = input("Votre choix : ")
        
    if choix_historique_entainement == "1":
        exportation_fichiers(account_id, username, password, historique_activité)
    elif choix_historique_entainement == "2":
        charge_entraînement(account_id, username, password)
    elif choix_historique_entainement == "3":
        accueil(account_id, username, password)

def créer_activité(account_id, username, password):
    print("")
    print("-- ✍🏻 Créer une activité ✍🏻 --")
    print("")

    try:
        #convertir les dates
        date_str = input("Quelle était la date de ton activité (JJ-MM-AAAA) : ").strip()
        #Je dois d’abord convertir la chaîne date_str en un objet datetime pour que ça fonctionne
        date_conversion = datetime.strptime(date_str, '%d-%m-%Y')#conversion str -> datetime
        date = date_conversion.strftime('%Y-%m-%d')#conversion datetime -> str formatée

        sport = input("Quel sport as-tu pratiqué : ").strip()
        durée = int(input("Quelle était la durée de ton activité (en min) : "))
        rpe = int(input("Note cet effort sur une échelle de 1 à 10 : "))
        if not 1 <= rpe <= 10:
            print("❌ Vous devez saisir un nombre entre 1 et 10")
            time.sleep(2)
            créer_activité(account_id, username, password)
        else:
            fatigue = int(input("Quel est ton niveau de fatigue sur une échelle de 1 à 10 après cette entraînement : "))
            if not 1 <= fatigue <= 10:
                print("❌ Vous devez saisir un nombre entre 1 et 10")
                time.sleep(2)
                créer_activité(account_id, username, password)
            else:
                douleur = int(input("As-tu des douleurs après cette séance (0= non, 1= un peu, 2= oui, 3= blessure) : "))
                if not 0 <= douleur <= 3:
                    print("❌ Vous devez saisir un chiffre entre 0 et 3")
                    time.sleep(2)
                    créer_activité(account_id, username, password)
                else:
                    climat = int(input("Climat (0= Normal, 1= Chaud, 2= Froid, 3= Difficile) : "))
                    if not 0 <= climat <= 3:
                        print("❌ Vous devez saisir un chiffre entre 0 et 3")
                        time.sleep(2)
                        créer_activité(account_id, username, password)
                    else:
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

                        curseur.execute("INSERT INTO Activité (date_activité, sport, durée, rpe, fatigue, douleur, climat, account_id, charge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(date, sport, durée, rpe, fatigue, douleur, climat, account_id, charge_activité))          
                        con.commit()
                        print("")
                        print("✅ Votre activité a été enregistré.")
                        time.sleep(2)
                        accueil(account_id, username, password)

    except sqlite3.Error as e: #Erreur SQLite
        print("")
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        accueil(account_id, username, password)
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        accueil(account_id, username, password)

def charge_entraînement(account_id, username, password):
    print("")
    print("-- Charge d'entraînement --")
    print("⏳ Chargement ⏳")
    try:
        #date
        date_actuelle = date.today()

        ca = date_actuelle - timedelta(days=7)  #ca = charge aïgue
        ca_str = ca.strftime('%Y-%m-%d')
        curseur.execute("SELECT charge FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, ca_str))
        charges_aigue = [row[0] for row in curseur.fetchall()]

        cc = date_actuelle - timedelta(days=28)  #cc = charge chronique
        cc_str = cc.strftime('%Y-%m-%d')
        curseur.execute("SELECT charge FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, cc_str))
        charges_chronique = [row[0] for row in curseur.fetchall()] #Extrait les valeurs de 'charge' dans une liste

        #Calcul des moyennes
        charge_aigue = sum(charges_aigue) / len(charges_aigue) if charges_aigue else 0
        charge_chronique = sum(charges_chronique) / len(charges_chronique) if charges_chronique else 0

        #Ratio de charge
        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None

        print("")
        print(f"📈 Charge aiguë (7 jours) : {charge_aigue:.1f}")
        print(f"📈 Charge chronique (28 jours) : {charge_chronique:.1f}")
        if ratio is not None:
            print(f"📊 Ratio : {ratio:.2f}")
            print("")
            if ratio < 0.8:
                print("😴 Sous-entraînement")
            elif 0.8 <= ratio <= 1.3:
                print("🟢 Zone optimale, parfait")
            elif 1.3 < ratio <= 1.5:
                print("💪 Charge élevée, prudence !")
            else:
                print("⚠️ 🤕  Surentraînement ! Risque de blessure !")
        else:
            print("🚫 Données insuffisantes pour calculer le ratio.")
            
        time.sleep(2)
        accueil(account_id, username, password)

    except sqlite3.Error as e: #Erreur SQLite
        print("")
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        accueil(account_id, username, password)
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        time.sleep(2)
        accueil(account_id, username, password)

def password_valide(password):
    SpecialSymbol =['$', '@', '#', '%', '?', '!']
    val = True

    if len(password) < 6:
        print('❌ La longueur doit être d\'au moins 6 caractères')
        val = False

    if len(password) > 20:
        print('❌ La longueur ne doit pas dépasser 20 caractères')
        val = False

    if not any(char.isdigit() for char in password):
        print('❌ Le mot de passe doit contenir au moins un chiffre')
        val = False

    if not any(char.isupper() for char in password):
        print('❌ Le mot de passe doit contenir au moins une lettre majuscule')
        val = False

    if not any(char.islower() for char in password):
        print('❌ Le mot de passe doit contenir au moins une lettre minuscule')
        val = False

    if not any(char in SpecialSymbol for char in password):
        print('❌ Le mot de passe doit contenir au moins un des symboles spéciaux : $@#%?!')
        val = False
    if val:
        return val
    
    time.sleep(1)

def accueil(account_id, username, password):
        print("")
        print("-- 🏠 Accueil 🏠 --")
        print("")
        print("Choisissez une option ⬇️")
        print("")
        print("1. ✍🏻 Créer une activité ✍🏻")
        print("2. 🔁 Historique d'entraînement 🔁")
        print("3. 📈 Charge d'entraînement 📈")
        print("4. 💡 Conseils 💡")
        print("5. 👤 Mon Compte 👤")
        print("6. 🛑 Quitter 🛑")

        choix_accueil = input("Votre choix : ")

        if choix_accueil == "1":
            créer_activité(account_id, username, password)

        elif choix_accueil == "2":
            historique_entraînement(account_id, username, password)

        elif choix_accueil == "3":
            charge_entraînement(account_id, username, password)

        elif choix_accueil == "4":
            conseils(account_id, username, password)

        elif choix_accueil == "5":
            mon_compte(account_id, username, password)

        elif choix_accueil == "6":
            print("")
            print("👋 Au revoir et à bientôt sur Sprintia !")
            time.sleep(1)
            con.close()

        else:
            print("❌ Sélection incorrecte, veuillez réessayer")
            time.sleep(2)
            accueil(account_id, username, password)

def menu_de_connection():
    print("")
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
    print("1. 🌐 Connection 🌐")
    print("2. 🖋️  Inscription 🖋️")
    print("3. ℹ️  À propos ℹ️")
    print("4. 🛑  Quitter 🛑")

    choix = input("Votre choix : ")

    if choix == "1":
        connection()

    elif choix == "2":
        inscription()

    elif choix == "3":
        a_propos()      
           
    elif choix == "4":
        print("")
        print("👋 Au revoir et à bientôt sur Sprintia !")

    else:
        print("❌ Sélection incorrecte, veuillez réessayer")
        time.sleep(2)
        menu_de_connection()
                
    time.sleep(1)

def main():
    print("")
    print("🫡  Bonjour !")
    time.sleep(0.5)
    if date_début_bienvenue  <= date_actuelle <= date_fin_bienvenue:
        print("")
        print("Bienvenue sur la nouvelle version de Sprintia !")
        print("Nous espérons que les nouvelles fonctionnalités vous plairont.")
        print("Merci beaucoup pour votre soutien !")
        time.sleep(3)
    menu_de_connection()

if __name__ == "__main__":
    try:
        con = sqlite3.connect("sport_data1.0.db")
        curseur = con.cursor()

        curseur.execute('''
            CREATE TABLE IF NOT EXISTS Account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        curseur.execute('''
            CREATE TABLE IF NOT EXISTS Activité (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_activité TEXT,
                sport TEXT,
                durée INTEGER,
                rpe INTEGER,
                fatigue INTEGER,
                douleur INTEGER,
                climat INTEGER,
                charge INTEGER,
                account_id INTEGER,
                FOREIGN KEY (account_id) REFERENCES Account(id)
            )
        ''')
        con.commit()

    except sqlite3.Error as e:
        print("")
        print(f"❌ Erreur lors de la connexion à la base de données : {e}")
        print("Si le problème persiste, veuillez contacter le développeur.")
        con.close()
        exit() #Quitte le programme
    except Exception as e:
        print(f"❌ Une erreur inattendue est survenue : {e}")
        print("Si le problème persiste veuillez contacter le développeur.")
        con.close()
        exit()

    main()