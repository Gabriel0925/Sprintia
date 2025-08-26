import sqlite3
import hashlib
import time
from datetime import date, datetime, timedelta

date_actuelle = date.today()
date_début_maj = date(2025, 7, 6) #pas de mise à jour actuellement
date_fin_maj = date(2027, 7, 6)

def maj():
    print("🆕 Une mise à jour est disponible 🆕")
    print("")
    print("➡️  Sprintia 1.2 est disponible")
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
        time.sleep(10)
        print("⬇️  Téléchargement : 50%")
        time.sleep(10)
        print("⬇️  Téléchargement : 75%")
        time.sleep(10)
        print("⬇️  Téléchargement : 100%")
        time.sleep(2)
        print("📦 Installation ⏳")
        time.sleep(10)
        print("")
        print("✅ Sprintia a été mis à jour")
        time.sleep(2)
        print("")
        print("🔄 Veuillez ouvrir le nouveau fichiers Sprintia 1.2")
        time.sleep(2)

    elif choix_jour_de_maj == "2":
        print("👋 Au revoir et à bientôt sur Sprintia !")

try:
    con = sqlite3.connect("sport_data1.0.db")
    curseur = con.cursor()
except sqlite3.Error as e: #e pour montrer l'erreur
    print("")
    print(f"❌ Erreur lors de la connexion à la base de données : {e}")
    print("Si le problème persiste, veuillez contacter le développeur.")
    con.close()
    exit() #Quitte le programme


def charge_entraînement(account_id):
    print("")
    print("-- Charge d'entraînement --")
    print("⏳ Chargement ⏳")
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
    charge_aigue = sum(charges_aigue) / len(charges_aigue) if charges_aigue else 0
    charge_chronique = sum(charges_chronique) / len(charges_chronique) if charges_chronique else 0

    #Ratio de charge
    if charge_chronique > 0:
        ratio = charge_aigue / charge_chronique
    else:
        ratio = None

    print("")
    print(f"- 📈 Charge aiguë (7 jours) : {charge_aigue:.1f}")
    print(f"- 📈 Charge chronique (28 jours) : {charge_chronique:.1f}")
    if ratio is not None:
        print(f"📊 Ratio : {ratio:.2f}")
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

#Exigences des Mots de Passe
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

#Menu d'accueil
def accueil(account_id):
    while True:
        print("")
        print("-- 🏠 Accueil 🏠 --")
        print("")
        print("Choisissez une option ⬇️")
        print("")
        print("1. ✍🏻 Créer une activité ✍🏻")
        print("2. 📈 Charge d'entraînement 📈")
        print("3. 🛑 Quitter 🛑")

        choix_accueil = input("Votre choix : ")

        if choix_accueil == "1":
            print("")
            print("-- ✍🏻 Créer une activité ✍🏻 --")
            print("")

            try:
                #convertir les dates
                date_str = input("Quelle était la date de ton activité (JJ-MM-AAAA) : ").strip() #enlève les espaces au début et à la fin
                #Je dois d’abord convertir la chaîne date_str en un objet datetime pour que ça fonctionne
                date_conversion = datetime.strptime(date_str, '%d-%m-%Y')#conversion str -> datetime
                date = date_conversion.strftime('%Y-%m-%d')#conversion datetime -> str formatée

                sport = input("Quel sport as-tu pratiqué : ").strip()
                durée = int(input("Quelle était la durée de ton activité (en min) : "))
                rpe = int(input("Note cet effort sur une échelle de 1 à 10 : "))
                if not 1 <= rpe <= 10:
                    print("❌ Vous devez saisir un nombre entre 1 et 10")
                else:
                    fatigue = int(input("Quel est ton niveau de fatigue sur une échelle de 1 à 10 après cette entraînement : "))
                    if not 1 <= fatigue <= 10:
                        print("❌ Vous devez saisir un nombre entre 1 et 10")
                    else:
                        douleur = int(input("As-tu des douleurs après cette séance (0= non, 1= un peu, 2= oui, 3= blessure) : "))
                        if not 0 <= douleur <= 3:
                            print("❌ Vous devez saisir un chiffre entre 0 et 3")
                        else:
                            climat = int(input("Climat (0= Normal, 1= Chaud, 2= Froid, 3= Difficile) : "))
                            if not 0 <= climat <= 3:
                                print("❌ Vous devez saisir un chiffr entre 0 et 3")
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

                                curseur.execute("INSERT INTO Activité (date, sport, durée, rpe, fatigue, douleur, climat, account_id, charge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (date, sport, durée, rpe, fatigue, douleur, climat, account_id, charge_activité))          
                                con.commit()
                                print("")
                                print("✅ Votre activité a été enregistré.")
            except sqlite3.IntegrityError as e: #Erreur de contrainte UNIQUE dans la ligne username dans la table Account
                print("")
                print(f"❌ Erreur d'intégrité à la base de données : {e}")
                print("Ce nom d'utilisateur est probablement déjà utilisé ou un problème de données est survenu.")
                print("Veuillez réessayer avec un autre nom d'utilisateur.")
            except sqlite3.Error as e: #Erreur SQLite
                print("")
                print(f"❌ Erreur lors de la connexion à la base de données : {e}")
                print("Veuillez réessayer")
                print("Si le problème persiste veuillez contacter le développeur.")
            except Exception as e: #Capture toutes les erreurs inattendue
                print(f"❌ Une erreur inattendue est survenue lors de l'inscription : {e}")
                print("Veuillez réessayer.")
                print("Si le problème persiste veuillez contacter le développeur.")

        elif choix_accueil == "2":
            charge_entraînement(account_id)

        elif choix_accueil == "3":
            print("👋 Au revoir et à bientôt sur Sprintia !")
            con.close()
            break

        else:
            print("❌ Sélection incorrecte, veuillez réessayer")

#menu de connection 
print("")
print("-- 🏅 Bienvenue sur Sprintia ! 🏅 --")
print("🏃 Votre compagnon d'entraînement !")
if date_début_maj <= date_actuelle <= date_fin_maj:
    maj()
else:
    print("")
    print("Choisissez une option ⬇️")
    print("")
    print("1. 🌐  Connection 🌐")
    print("2. 🖋️   Inscription 🖋️")
    print("3. ℹ️   À propos ℹ️")
    print("4. 🛑  Quitter 🛑")

    choix = input("Votre choix : ")

    if choix == "1":
        print("")
        print("-- 🌐 Connection 🌐 --")

        try:
            username = input("Nom d'utilisateur : ").strip() #enlève les espaces au début et à la fin
            password = input("Mots de passe : ").encode('UTF-8')

            sha256 = hashlib.sha256()
            sha256.update(password)
            hashed_password = sha256.hexdigest() # Hache le mot de passe qui a été entré
            curseur.execute("SELECT id, username, password FROM Account WHERE username = ? AND password = ?", (username, hashed_password))
            result = curseur.fetchone()

            if not username or not password:
                print("")
                print("❌ Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
            if result:
                account_id = result[0]
                print("")
                print(f"✅ Vous êtes connectés en tant que {username}") #Ne pas oublier le f !
                accueil(account_id)
            else:
                print("❌ Identifiants incorrects. Veuillez réessayer.")
                con.close()

        except sqlite3.Error as e: 
            print("")
            print(f"❌ Erreur lors de la connexion à la base de données : {e}")
            print("Veuillez réessayer")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e: 
            print(f"❌ Une erreur inattendue est survenue lors de l'inscription : {e}")
            print("Veuillez réessayer.")
            print("Si le problème persiste veuillez contacter le développeur.")


    elif choix == "2":
        print("")
        print("-- 🖋️  Inscription 🖋️  --")
        username = input("Nom d'utilisateur (requis) : ").strip() #enlève les espaces au début et à la fin
        password_input = input("Mots de passe (requis) : ")
        password_encode = password_input.encode("UTF-8")

        try:
            if not username or not password_input:
                print("")
                print("❌ Le nom d'utilisateur et le mot de passe ne peuvent pas être vides.")
            else:
                if (password_valide(password_input)):
                    print("✅ Le mot de passe est valide")
                    sha256 = hashlib.sha256()
                    sha256.update(password_encode)
                    hashed_password = sha256.hexdigest()
                    curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
                    con.commit()
                    print("")
                    print("✅ Votre compte a été enregistré")
                    print(f"Bienvenue {username} ! Vous pouvez désormais utiliser Sprintia.") #Ne pas oublier le f !
                    print("Vous pouvez maintenant vous connecter. ➡️")
                else:
                    print("❌ Le mot de passe est invalide")

        except sqlite3.IntegrityError as e: #Erreur de contrainte UNIQUE dans la ligne username dans la table Account
            print("")
            print(f"❌ Erreur d'intégrité à la base de données : {e}")
            print("Ce nom d'utilisateur est probablement déjà utilisé ou un problème de données est survenu.")
            print("Veuillez réessayer avec un autre nom d'utilisateur.")
        except sqlite3.Error as e: #Erreur SQLite
            print("")
            print(f"❌ Erreur lors de la connexion à la base de données : {e}")
            print("Veuillez réessayer")
            print("Si le problème persiste veuillez contacter le développeur.")
        except Exception as e: #Capture toutes les erreurs inattendue
            print(f"❌ Une erreur inattendue est survenue lors de l'inscription : {e}")
            print("Veuillez réessayer.")
            print("Si le problème persiste veuillez contacter le développeur.")

    elif choix == "3":
        print("")
        print("-- ℹ️  À propos ℹ️ --")
        print("")
        print("Sprintia est conçue pour vous aidés avant et après un entraînement")
        print("Version : 1.1.3 - Alpha")
        print("🎯 Objectif de la version : Stabiliser le code existant et améliorer la robustesse des interactions de base.")
        print("Dernière mise à jour : 04 Juillet 2025")
        print("➡️  Développé par Gabriel Chapet")
        print("📧 gabchap486@gmail.com")
        print("")
        print("1. 🆕 Nouveautés 🆕")
        print("2. 🛑 Quitter 🛑")

        choix_info = input("Votre choix : ")

        if choix_info == "1":
            print("")
            print("-- 🆕 Nouveautés 🆕 --")
            print("")
            print("1️⃣  Validation des Données Entrée")
            print("2️⃣  Gestion des Erreurs de Base de Données")
            print("3️⃣  Exigences de Complexité de Mots de Passe lors de l'inscription")
            print("4️⃣  Intégration de '✨ GlyphFlow 🚀', une interface repensée pour une utilisation plus fluide et plus joli")
        
        elif choix_info == "2":
            print("👋 Au revoir et à bientôt sur Sprintia !")
            con.close()

    elif choix == "4":
        print("👋 Au revoir et à bientôt sur Sprintia !")

    else:
        print("❌ Sélection incorrecte, veuillez réessayer")