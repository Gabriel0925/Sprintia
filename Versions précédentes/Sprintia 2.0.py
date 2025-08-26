import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import sqlite3
import hashlib
import random
import csv
from datetime import datetime, timedelta
from datetime import date
from datetime import time as Time
import matplotlib.pyplot as plt
import seaborn as sns

#variables
date_actuelle = date.today()

#heure
maintenant = datetime.now()
heure_actuelle_objet = maintenant.time()
heure_debut = Time(hour=18, minute=0)
heure_fin = Time(hour=23, minute=59)

def vider_fenetre(app):
    for widget in app.winfo_children():
        widget.destroy()

def fermer_app():
    app.destroy()
    con.close()

def password_valide(password):
    SpecialSymbol =['$', '@', '#', '%', '?', '!']
    val = True

    if len(password) < 6:
        CTkMessagebox(
            title="Mot de passe invalide",
            message="La longueur doit être d'au moins 6 caractères",
            icon="cancel"
        )
        val = False

    if len(password) > 20:
        CTkMessagebox(
            title="Mot de passe invalide",
            message="La longueur ne doit pas dépasser 20 caractères",
            icon="cancel"
        )
        val = False

    if not any(char.isdigit() for char in password):
        CTkMessagebox(
            title="Mot de passe invalide",
            message="Le mot de passe doit contenir au moins un chiffre",
            icon="cancel"
        )
        val = False

    if not any(char.isupper() for char in password):
        CTkMessagebox(
            title="Mot de passe invalide",
            message="Le mot de passe doit contenir au moins une lettre majuscule",
            icon="cancel"
        )
        val = False

    if not any(char.islower() for char in password):
        CTkMessagebox(
            title="Mot de passe invalide",
            message="Le mot de passe doit contenir au moins une lettre minuscule",
            icon="cancel"
        )
        val = False

    if not any(char in SpecialSymbol for char in password):
        CTkMessagebox(
            title="Mot de passe invalide",
            message="Le mot de passe doit contenir au moins un des symboles spéciaux : $@#%?!",
            icon="cancel"
        )
        val = False
    if val:
        return val

def a_propos(account_id, username, password):
    cadre_maj = ctk.CTkFrame(master=app)      
    cadre_maj.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_maj ,text="Mise à jour", font=("Arial", 20, "bold"))
    text1 = ctk.CTkLabel(master=cadre_maj, text="Sprintia est conçue pour vous aidés avant et après un entraînement\n\n" \
    "Version : 2.0.1 | Développé par Gabriel Chapet\nBug repéré ? Envoie un mail à : gabchap486@gmail.com", font=("Arial", 15))
    Titre2= ctk.CTkLabel(master=cadre_maj, text="Pourquoi j'ai créé Sprintia ?", font=("Arial", 15, "bold"))
    text2 = ctk.CTkLabel(master=cadre_maj, text="J'ai lancé Sprintia parce que je crois qu'on n'a pas besoin de dépenser\n des fortunes pour avoir de la qualité. C'est un peu comme avec \n " \
    "les montres connectées : on ne devrait pas être obligé d'acheter la toute dernière et la plus chère.\n Moi, j'adore les montres de sport, " \
    "mais je voyais bien que les fabricants augmentaient\n toujours les prix, ou alors il y avait toujours un petit truc qui n'allait pas. \n " \
    "Du coup, j'ai décidé de créer Sprintia pour faire les choses à ma manière !", font=("Arial", 15))

    Titre.pack(padx=50, pady=(25, 5))
    text1.pack(padx=50, pady=(5, 5))
    Titre2.pack(padx=50, pady=(25, 5))
    text2.pack(padx=50, pady=(5, 5))

    frame_maj = ctk.CTkFrame(master=cadre_maj, fg_color="transparent")
    frame_maj.pack(pady=10)

    button_back = ctk.CTkButton(master=frame_maj, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                        corner_radius=10, height=35, font=("Arial", 16), 
                        command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_back.pack(pady=10)

def verifier_pause(account_id):
    #AND date_fin IS NULL = Cible uniquement les pause non terminés.
    curseur.execute("""SELECT type FROM Pauses WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    result = curseur.fetchone()
    return result[0] if result else None

def exportation_fichiers(account_id, username, password, période_str):
    vider_fenetre(app)
    cadre_fichier = ctk.CTkFrame(master=app)        
    cadre_fichier.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_fichier ,text="Exportez votre historique", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))
    try:
        curseur.execute("SELECT date_activité, nom, sport, durée, distance, rpe, fatigue, charge FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, période_str))
        activites = curseur.fetchall()
    except sqlite3 as e:
        CTkMessagebox(
            title="Erreur",
            message=f"Erreur de base de données lors de l'exportation de votre historique.",
            icon="cancel"
        )
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    try:
        données_csv = []
        for row in activites:
            date_activité = datetime.strptime(row[0], '%Y-%m-%d')
            date_formatée = date_activité.strftime('%d-%m-%Y')

            données_csv.append({
                "Date": date_formatée,
                "Nom": row[1],
                "Sport": row[2],
                "Durée (min)": row[3],
                "Distance": row[4],
                "RPE": row[5],
                "Fatigue": row[6],
                "Charge": row[7],
            })

        noms_colonnes = ["Date", "Nom", "Sport", "Durée (min)", "Distance", "RPE", "Fatigue", "Charge"]
        option_extension = {"Format CSV (Recommandé)": ".csv", "Format JSON": ".json", "Format TEXT": ".txt"}       

        nom_du_fichier_entry = ctk.CTkEntry(master=cadre_fichier, placeholder_text="Nom du fichier", width=250,
                                height=35)
        nom_du_fichier_entry.pack(pady=10, padx=10)
        format_du_fichier_entry = ctk.CTkComboBox(master=cadre_fichier, values=list(option_extension.keys()), width=250,
                                height=35, state="readonly", border_width=2, border_color="#187D4B", button_color="#187D4B")
        format_du_fichier_entry.pack(pady=10, padx=10)
        format_du_fichier_entry.set("Sélectionnez l'extension de fichier")

        frame_boutons = ctk.CTkFrame(master=cadre_fichier, fg_color="transparent")
        frame_boutons.pack(pady=(0, 10))

        def exporter(account_id, username, password):
            nom_fichier = nom_du_fichier_entry.get().strip()
            format_choisi = format_du_fichier_entry.get()
            extension = option_extension[format_choisi]
            nom_complet = f"{nom_fichier}{extension}"
            if not nom_fichier:
                CTkMessagebox(
                    title="Erreur",
                    message="Veuillez mettre un nom de fichier",
                    icon="cancel"
                )
                return
            with open(nom_complet, 'w', newline='', encoding='utf-8') as fichier_csv:
                writer = csv.DictWriter(fichier_csv, fieldnames=noms_colonnes)
                writer.writeheader()
                writer.writerows(données_csv)
            CTkMessagebox(
                title="Enregistré",
                message=f"Le fichier CSV a été sauvegardé sous le nom : {nom_complet}",
                icon="check"
            )
            app.after(1500, lambda: [vider_fenetre(app), exportation_fichiers(account_id, username, password, période_str)])
            
    except IOError as e:
        CTkMessagebox(
            title="Erreur lors de l'exportation de vos données d'activité",
            message=f"Erreur : {e}",
            icon="cancel"
        )
    except Exception as e:
        CTkMessagebox(
            title="Erreur inattendu",
            message=f"Erreur : {e}",
            icon="cancel"
        )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: exporter(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), exercice(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

def supprimer_activité(account_id, username, password, période_str):
    vider_fenetre(app)
    cadre_activité = ctk.CTkFrame(master=app)
    cadre_activité.pack(pady=20, padx=60, fill="both", expand=True)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)

    Titre = ctk.CTkLabel(master=frame ,text="Supprimer une activité", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10), side="left")

    app.bind('<Return>', lambda event: supression(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'activité à supprimer", width=320,
                               height=35)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    try:
            tableau_frame = ctk.CTkScrollableFrame(master=cadre_activité, fg_color="transparent")
            tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
            curseur.execute("SELECT id_activité, date_activité, nom, sport, durée, distance, rpe FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str))
            activites = curseur.fetchall()

            headers = ["ID", "Date", "Nom", "Sport", "Durée (min)", "Distance", "RPE"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                    fg_color="white", corner_radius=5)
                label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date_activité = datetime.strptime(data, '%Y-%m-%d')
                            data = date_activité.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=("Arial", 12))
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée ces 7 derniers jours.", font=("Arial", 14))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de la récupération de l'historique.",
                icon="cancel"
            )
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )

    def supression(account_id, username, password):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in activites]

                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Activité WHERE id_activité = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    CTkMessagebox(
                        title="Suppression réussie",
                        message="Activité supprimée avec succès.",
                        icon="check"
                    )
                    app.after(1500, lambda: [vider_fenetre(app), supprimer_activité(account_id, username, password, période_str)])
                else:
                    CTkMessagebox(
                        title="Erreur",
                        message="L'ID de l'activité saisie n'existe pas ou n'appartient pas à votre compte.",
                        icon="cancel"
                    )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur base de données",
                    message="Erreur de base de données lors de la suppression de l'activité.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
            
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                                 corner_radius=10, height=35, font=("Arial", 16),
                                 command=lambda: supression(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                 corner_radius=10, height=35, font=("Arial", 16),
                                 command=lambda: [vider_fenetre(app), exercice(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

def ajouter_activité(account_id, username, password):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    
    sport_avec_distance = {
        "vélo", "velo", "cyclisme", "bike", "vélo élliptique", "velo elliptique",
        "vélo d'intérieur", "velo d'interieur", "vélo d'appartement", "velo d'appartement",
        "vtt", "course à pied", "course", "running", "run", "course a pied",
        "tapis de course", "athlétisme", "athletisme", "course sur piste", "marche", 
        "marche à pied", "marche a pied", "course d'orientation", "randonnée", "trail", "ultra-trail"
    }
    
    sport_avec_dénivelé = {
        "ultra-trail", "randonnée", "randonnee", "trail", 
        "ski de fond", "ski alpin", "ski", "snowboard", "vtt"
    }
    cadre_principal = ctk.CTkFrame(master=app)
    cadre_principal.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_principal, text="Ajouter une activité", 
                font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    frame_boutons = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_boutons.pack(padx=10, pady=5)
    frame_champs1 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=5)
    frame_champs2 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=5)
    frame_champs3 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=5)
    frame_champs4 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=5)
    frame_champs5 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=5)

    app.bind('<Return>', lambda event: enregistrer())
    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", width=250, height=35)
    date_entry.pack(side="left", padx=10)
    sport_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Sport", width=250, height=35)
    sport_entry.pack(side="left", padx=10)

    duree_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Durée (min)", width=250, height=35)
    duree_entry.pack(side="left", padx=10)
    rpe_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="RPE (1 à 10)", width=250, height=35)
    rpe_entry.pack(side="left", padx=10)

    fatigue_entry = ctk.CTkEntry(master=frame_champs3, placeholder_text="Fatigue (1 à 10)", width=250, height=35)
    fatigue_entry.pack(side="left", padx=10)
    nom_entry = ctk.CTkEntry(master=frame_champs3, placeholder_text="Nom (Optionnel)", width=250, height=35)
    nom_entry.pack(side="left", padx=10)

    douleur_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_douleur.keys()), width=250, height=35, state="readonly"
                                    , border_width=2, border_color="#187D4B", button_color="#187D4B")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Séléctionnez le niveau de douleur")
    climat_entry = ctk.CTkComboBox(master=frame_champs4, values=list(Options_climat.keys()), width=250, height=35, state="readonly", border_width=2, border_color="#187D4B", button_color="#187D4B")
    climat_entry.pack(side="left", padx=10)
    climat_entry.set("Sélectionnez le climat")

    distance_entry = ctk.CTkEntry(master=frame_champs5, placeholder_text="Distance (km) (ex : 5.67)", width=250, height=35)
    denivele_entry = ctk.CTkEntry(master=frame_champs5, placeholder_text="Dénivelé (m)", width=250, height=35)

    def afficher_champs_conditionnels(event=None):
        sport = sport_entry.get().strip().lower()
        distance_entry.pack_forget()
        denivele_entry.pack_forget()
        
        if sport in sport_avec_distance:
            distance_entry.pack(side="left", padx=10)
        if sport in sport_avec_dénivelé:
            denivele_entry.pack(side="left", padx=10)

    sport_entry.bind("<KeyRelease>", afficher_champs_conditionnels)
    afficher_champs_conditionnels()

    def valider_entrees(account_id, username, password):
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                CTkMessagebox(
                    title="Erreur", 
                    message="La date ne peut pas être dans le futur", 
                    icon="cancel"
                    )
                return 
            date = date_obj.strftime('%Y-%m-%d')
            
            sport = sport_entry.get().strip()
            if not sport:
                CTkMessagebox(
                    title="Erreur",
                      message="Le sport est obligatoire", 
                      icon="cancel")
                return 
            try:
                duree = int(duree_entry.get().strip())
                if duree <= 0:
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Erreur", 
                    message="Durée invalide (entier positif requis)", 
                    icon="cancel"
                    )
                return 
            try:
                rpe = int(rpe_entry.get().strip())
                if not 1 <= rpe <= 10:
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Erreur", 
                    message="RPE invalide (1-10 requis)", 
                    icon="cancel"
                    )
                return
                
            try:
                fatigue = int(fatigue_entry.get().strip())
                if not 1 <= fatigue <= 10:
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Erreur", 
                    message="Fatigue invalide (1-10 requis)", 
                    icon="cancel"
                    )
                return 
                
            douleur = Options_douleur.get(douleur_entry.get().strip())
            climat = Options_climat.get(climat_entry.get().strip())
            
            if douleur is None or climat is None:
                CTkMessagebox(
                    title="Erreur", 
                    message="Valeur de douleur ou climat invalide", 
                    icon="cancel"
                    )
                return
                
            distance = None
            denivele = None
            sport_lower = sport.lower()
            
            if sport_lower in sport_avec_distance:
                try:
                    dist_str = distance_entry.get().strip()
                    if dist_str:
                        distance = float(dist_str)
                        if distance <= 0:
                            CTkMessagebox(
                                title="Erreur", 
                                message="La distance doit être supérieur à 0.", 
                                icon="cancel"
                                ) 
                except ValueError:
                    CTkMessagebox(
                        title="Erreur", 
                        message="Distance invalide (nombre positif requis)", 
                        icon="cancel"
                        )
                    return
                    
            if sport_lower in sport_avec_dénivelé:
                try:
                    deniv_str = denivele_entry.get().strip()
                    if deniv_str:
                        denivele = int(deniv_str)
                        if denivele <= 0:
                            CTkMessagebox(
                                title="Erreur", 
                                message="Le dénivelé doit être supérieur à 0.", 
                                icon="cancel"
                                )                 
                except ValueError:
                    CTkMessagebox(
                        title="Erreur", 
                        message="Dénivelé invalide (entier positif requis)", 
                        icon="cancel"
                        )
                    return
                                
            charge_de_base = duree * rpe
            
            modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
            modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
            
            charge_d = charge_de_base * modificateurs_douleur[douleur]
            charge_c = charge_d * modificateurs_climat[climat]
            score_fatigue = 1 + (fatigue - 5) * 0.05
            charge = score_fatigue * charge_c
            
            return {
                'date': date,
                'sport': sport,
                'duree': duree,
                'distance': distance,
                'rpe': rpe,
                'fatigue': fatigue,
                'douleur': douleur,
                'climat': climat,
                'charge': charge,
                'nom': nom_entry.get().strip() or None,
                'denivele': denivele
            }
            
        except ValueError:
            CTkMessagebox(
                title="Erreur", 
                message="Format de données invalide.", 
                icon="cancel"
                )
            return
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
                return 

    def enregistrer():
        donnees = valider_entrees(account_id, username, password)
        if not donnees:
            return
        try:
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, distance, rpe, fatigue, douleur, climat, charge, account_id, nom, dénivelé) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                donnees['date'], donnees['sport'], donnees['duree'], 
                donnees['distance'], donnees['rpe'],
                donnees['fatigue'], donnees['douleur'], donnees['climat'],
                donnees['charge'], account_id, donnees['nom'],
                donnees['denivele']
            ))
            con.commit()
            CTkMessagebox(
                title="Succès",
                message="Votre activité a bien été enregistrée !",
                icon="check"
            )
            app.after(1500, lambda: [vider_fenetre(app), ajouter_activité(account_id, username, password)])
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur BD",
                message="Erreur base de données lors de l'ajout de votre activité.",
                icon="cancel"
            )
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    bouton_valider = ctk.CTkButton(master=frame_boutons, text="Enregistrer", fg_color="#187D4B", hover_color="#13623B",corner_radius=10, height=35,
                                    font=("Arial", 16), command=enregistrer)
    bouton_valider.pack(side="left", padx=10)
    bouton_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", corner_radius=10, fg_color="#00578E", hover_color="#004774", 
                                height=35, font=("Arial", 16),
                                command=lambda: [vider_fenetre(app), exercice(account_id, username, password)])
    bouton_retour.pack(side="left", padx=10, pady=20)

def imc(account_id, username, password):
    cadre_imc = ctk.CTkFrame(master=app)        
    cadre_imc.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_imc ,text="Calculateur d'IMC", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    app.bind('<Return>', lambda event: calcul_imc(account_id, username, password))
    poids_entry = ctk.CTkEntry(master=cadre_imc, placeholder_text="Poids (kg) (Exemple : 70.3)", width=250,
                              height=35)
    poids_entry.pack(pady=10, padx=10)

    taille_entry = ctk.CTkEntry(master=cadre_imc, placeholder_text="Taille (cm)", width=250,
                              height=35)
    taille_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_imc, fg_color="white", corner_radius=20,)
    cadre_result.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_imc, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre IMC directement \n sur votre appareil et ne stockons pas cette donnée.",
                           font=("Arial", 15), text_color="#000002")
    result.pack(padx=50, pady=10)

    def calcul_imc(account_id, username, password):
        try:
            poids = float(poids_entry.get().strip())
            taille_conversion = float(taille_entry.get().strip())
            taille = taille_conversion/100

            if poids <= 0 or taille <= 0:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La taille et le poids doivent être supérieur à 0",
                    icon="cancel"
                )
            if not poids or not taille:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La taille et le poids ne peuvent pas être vides",
                    icon="cancel"
                )
            else:
                imc = poids / (taille ** 2)

                if imc <= 18.5:
                    interprétation = "Insuffisance pondérale (maigreur)"
                elif 18.5 <= imc <= 24.9:
                    interprétation = "Corpulence normale"
                elif 25 <= imc <= 29.9:
                    interprétation = "Surpoids"
                elif 30 <= imc <= 34.9:
                    interprétation = "Obésité modérée (niveau 1)"
                elif 35 <= imc <= 39.9:
                    interprétation = "Obésité sévère (niveau 2)"
                elif imc >= 40:
                    interprétation = "Obésité morbide (niveau 3)"
                else:
                    interprétation = "Une erreur est survenue, veuillez réesayer plus tard"
                    
                result.configure(text=f"Votre IMC est : {imc:.2f}\n{interprétation}")
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: calcul_imc(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: outils(account_id, username, password))
    button_retour.pack(side="left", padx=10, pady=20)

def VO2MAX(account_id, username, password):
    cadre_vo2Max = ctk.CTkFrame(master=app)        
    cadre_vo2Max.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_vo2Max ,text="Estimation VO2max", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    app.bind('<Return>', lambda event: calcul_VO2MAX(account_id, username, password))
    vma_entry = ctk.CTkEntry(master=cadre_vo2Max, placeholder_text="VMA (Exemple : 16.3)", width=250,
                              height=35)
    vma_entry.pack(pady=10, padx=10)

    combo_genre = ctk.CTkComboBox(master=cadre_vo2Max, values=["Homme", "Femme"], width=250,
                              height=35, state="readonly", border_width=2, border_color="#187D4B", button_color="#187D4B")
    combo_genre.pack(pady=10, padx=10)
    combo_genre.set("Sélectionnez votre genre")

    age_entry = ctk.CTkEntry(master=cadre_vo2Max, placeholder_text="Âge", width=250,
                              height=35)
    age_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_vo2Max, fg_color="white", corner_radius=20,)
    cadre_result.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_vo2Max, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre VO2max directement \n sur votre appareil et ne stockons pas cette donnée.",
                           font=("Arial", 15), text_color="#000002")
    result.pack(padx=50, pady=(10, 10))

    def calcul_VO2MAX(account_id, username, password):
        try:
            vma = float(vma_entry.get().strip())
            age = float(age_entry.get().strip())
            genre = combo_genre.get().strip()

            if vma <= 0:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La VMA doit être supérieur à 0",
                    icon="cancel"
                )
                return
            if age < 14:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : L'âge minimum pour cette fonction est de 14 ans",
                    icon="info"
                )
                return
            if not vma or not age:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La VMA et l'âge ne peuvent pas être vides",
                    icon="cancel"
                )
                return
            else:
                vo2max = vma*3.5
                if genre == "Homme":
                    if 14 <= age <= 17 :
                        if vo2max >= 58:
                            interprétation = "Supérieur"
                        elif 54 <= vo2max <= 58:
                            interprétation = "Excellent"
                        elif 50 <= vo2max <= 53:
                            interprétation = "Bon"
                        elif 46 <= vo2max <= 49:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                    if 18 <= age <= 25 :
                        if vo2max >= 56:
                            interprétation = "Supérieur"
                        elif 52 <= vo2max <= 56:
                            interprétation = "Excellent"
                        elif 48 <= vo2max <= 51:
                            interprétation = "Bon"
                        elif 44 <= vo2max <= 47:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                    if 26 <= age <= 35 :
                        if vo2max >= 51:
                            interprétation = "Supérieur"
                        elif 47 <= vo2max <= 51:
                            interprétation = "Excellent"
                        elif 43 <= vo2max <= 46:
                            interprétation = "Bon"
                        elif 39 <= vo2max <= 42:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                    if 36 <= age <= 45 :
                        if vo2max >= 45:
                            interprétation = "Supérieur"
                        elif 41 <= vo2max <= 45:
                            interprétation = "Excellent"
                        elif 37 <= vo2max <= 40:
                            interprétation = "Bon"
                        elif 33 <= vo2max <= 36:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                    if 46 <= age <= 55 :
                        if vo2max >= 41:
                            interprétation = "Supérieur"
                        elif 37 <= vo2max <= 41:
                            interprétation = "Excellent"
                        elif 33 <= vo2max <= 36:
                            interprétation = "Bon"
                        elif 29 <= vo2max <= 32:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                    if 56 <= age <= 65 :
                        if vo2max >= 37:
                            interprétation = "Supérieur"
                        elif 33 <= vo2max <= 37:
                            interprétation = "Excellent"
                        elif 29 <= vo2max <= 32:
                            interprétation = "Bon"
                        elif 25 <= vo2max <= 28:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                    if age >= 65 :
                        if vo2max >= 33:
                            interprétation = "Supérieur"
                        elif 29 <= vo2max <= 33:
                            interprétation = "Excellent"
                        elif 25 <= vo2max <= 28:
                            interprétation = "Bon"
                        elif 21 <= vo2max <= 24:
                            interprétation = "Moyen"
                        else:
                            interprétation = "Faible"
                elif genre == "Femme":
                    if 14 <= age <= 17 :
                        if vo2max >= 52:
                            interprétation = "Supérieur"
                        if 48 <= vo2max <= 52:
                            interprétation = "Excellent"
                        if 44 <= vo2max <= 47:
                            interprétation = "Bon"
                        if 40 <= vo2max <= 43:
                            interprétation = "Moyen"
                        if vo2max <= 40:
                            interprétation = "Faible"
                    if 18 <= age <= 25 :
                        if vo2max >= 48:
                            interprétation = "Supérieur"
                        if 44 <= vo2max <= 48:
                            interprétation = "Excellent"
                        if 40 <= vo2max <= 43:
                            interprétation = "Bon"
                        if 36 <= vo2max <= 39:
                            interprétation = "Moyen"
                        if vo2max <= 36:
                            interprétation = "Faible"
                    if 26 <= age <= 35 :
                        if vo2max >= 42:
                            interprétation = "Supérieur"
                        if 38 <= vo2max <= 42:
                            interprétation = "Excellent"
                        if 34 <= vo2max <= 37:
                            interprétation = "Bon"
                        if 30 <= vo2max <= 33:
                            interprétation = "Moyen"
                        if vo2max <= 30:
                            interprétation = "Faible"
                    if 36 <= age <= 45 :
                        if vo2max >= 37:
                            interprétation = "Supérieur"
                        if 33 <= vo2max <= 37:
                            interprétation = "Excellent"
                        if 29 <= vo2max <= 32:
                            interprétation = "Bon"
                        if 25 <= vo2max <= 28:
                            interprétation = "Moyen"
                        if vo2max <= 25:
                            interprétation = "Faible"
                    if 46 <= age <= 55 :
                        if vo2max >= 34:
                            interprétation = "Supérieur"
                        if 30 <= vo2max <= 34:
                            interprétation = "Excellent"
                        if 26 <= vo2max <= 29:
                            interprétation = "Bon"
                        if 22 <= vo2max <= 25:
                            interprétation = "Moyen"
                        if vo2max <= 22:
                            interprétation = "Faible"
                    if 56 <= age <= 65 :
                        if vo2max >= 30:
                            interprétation = "Supérieur"
                        if 26 <= vo2max <= 30:
                            interprétation = "Excellent"
                        if 22 <= vo2max <= 25:
                            interprétation = "Bon"
                        if 18 <= vo2max <= 21:
                            interprétation = "Moyen"
                        if vo2max <= 18:
                            interprétation = "Faible"
                    if age >= 65 :
                        if vo2max >= 27:
                            interprétation = "Supérieur"
                        if 23 <= vo2max <= 27:
                            interprétation = "Excellent"
                        if 19 <= vo2max <= 22:
                            interprétation = "Bon"
                        if 15 <= vo2max <= 18:
                            interprétation = "Moyen"
                        if vo2max <= 15:
                            interprétation = "Faible"
                else:
                    interprétation = "Sexe non valide. Veuillez séléctionner Homme ou Femme."
                result.configure(text=f"Votre VO2max est de {vo2max:.2f} mL/min/kg. \n {interprétation}")
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )

    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: calcul_VO2MAX(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: outils(account_id, username, password))
    button_retour.pack(side="left", padx=10, pady=20)

def VMA(account_id, username, password):
    cadre_vo2Max = ctk.CTkFrame(master=app)        
    cadre_vo2Max.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_vo2Max ,text="Estimation VMA", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    Info = ctk.CTkLabel(master=cadre_vo2Max ,text="Pour une estimation plus précise, utilisez la distance parcourue à fond en 6 minutes.", font=("Arial", 15))
    Info.pack(padx=50, pady=10)

    app.bind('<Return>', lambda event: calcul_VMA(account_id, username, password))
    distance_entry = ctk.CTkEntry(master=cadre_vo2Max, placeholder_text="Distance (km) (Exemple : 8.3)", width=250,
                              height=35)
    distance_entry.pack(pady=10, padx=10)

    temps_entry = ctk.CTkEntry(master=cadre_vo2Max, placeholder_text="Temps (min)", width=250,
                              height=35)
    temps_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_vo2Max, fg_color="white", corner_radius=20,)
    cadre_result.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_vo2Max, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous estimons votre VMA directement \n sur votre appareil et ne stockons pas cette donnée.",
                           font=("Arial", 15), text_color="#000002")
    result.pack(padx=50, pady=(10, 10))

    def calcul_VMA(account_id, username, password):
        try:
            distance = float(distance_entry.get().strip())
            temps_autre = float(temps_entry.get().strip())
            temps = temps_autre/60

            if distance <= 0 or temps <=0:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La distance et le temps doivent être supérieur à 0",
                    icon="cancel"
                )
            if not distance or not temps:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La distance et le temps ne peuvent pas être vides",
                    icon="cancel"
                )
            else:
                vma = distance / temps

                if distance <= 2:
                    vma_estimée = vma*1
                elif 2 <= distance <= 3:
                    vma_estimée = vma*1.05
                elif 3 <= distance <= 6:
                    vma_estimée = vma*1.2
                elif 6 <= distance <= 12:
                    vma_estimée = vma*1.45
                elif 12 <= distance <= 25:
                    vma_estimée = vma*1.52
                elif 21.0975 <= distance <= 42.195:
                    vma_estimée = vma*1.6
                else:
                    vma_estimée = vma*1.8

                result.configure(text=f"Votre VMA est de {vma_estimée:.2f} km/h.")
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )

    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: calcul_VMA(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: outils(account_id, username, password))
    button_retour.pack(side="left", padx=10, pady=20)

def zone_fc(account_id, username, password):
    cadre_fc = ctk.CTkFrame(master=app)        
    cadre_fc.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_fc ,text="Zones Cardiaque", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    app.bind('<Return>', lambda event: calcul_zone(account_id, username, password))
    age_entry = ctk.CTkEntry(master=cadre_fc, placeholder_text="Âge", width=250,
                              height=35)
    age_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_fc, fg_color="white", corner_radius=20,)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons vos zones de fréquence cardiaque\n directement sur votre appareil et ne stockons pas ces données.",
                           font=("Arial", 15), text_color="#000002")
    result.pack(padx=50, pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_fc, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    def calcul_zone(account_id, username, password):
        try:
            age = int(age_entry.get().strip())
            fc_max = 220 - age

            if age <= 0:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : L'âge doit être supérieur à 0",
                    icon="cancel"
                )
            if not age:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : L'âge ne peut pas être vide",
                    icon="cancel"
                )
            debut_zone1 = fc_max*0.50
            fin_zone1 = fc_max*0.60
            Zone1 = f"Zone 1 : Récupération active - {debut_zone1:.0f}bpm à {fin_zone1:.0f}bpm"
            debut_zone2 = fc_max*0.60
            fin_zone2 = fc_max*0.70
            Zone2 = f"Zone 2 : Fondamentale / Endurance de base - {debut_zone2:.0f}bpm à {fin_zone2:.0f}bpm"
            debut_zone3 = fc_max*0.70
            fin_zone3 = fc_max*0.80
            Zone3 = f"Zone 3 : Seuil aérobie / Endurance active - {debut_zone3:.0f}bpm à {fin_zone3:.0f}bpm"
            debut_zone4 = fc_max*0.80
            fin_zone4 = fc_max*0.90
            Zone4 = f"Zone 4 :  Seuil anaérobie / Résistance dure - {debut_zone4:.0f}bpm à {fin_zone4:.0f}bpm"
            debut_zone5 = fc_max*0.90
            Zone5 = f"Zone 5 : Vitesse maximale aérobie / Puissance maximale - {debut_zone5:.0f}bpm à {fc_max:.0f}bpm"

            result.configure(text=f"Vos Zones de Fréquence Cardiaque\n\n{Zone1}\n{Zone2}\n{Zone3}\n{Zone4}\n{Zone5}")
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )   

    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: calcul_zone(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: outils(account_id, username, password))
    button_retour.pack(side="left", padx=10, pady=20)

def predicteur_temps(account_id, username, password):
    cadre_fc = ctk.CTkFrame(master=app)        
    cadre_fc.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_fc ,text="Prédicteur de course", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    Info = ctk.CTkLabel(master=cadre_fc ,text="N'oubliez pas que cette prédiction est une estimation basée sur la théorie et peut varier\nen fonction de nombreux facteurs le jour de la course !", font=("Arial", 15))
    Info.pack(padx=50, pady=10)

    app.bind('<Return>', lambda event: calcul_temps(account_id, username, password))
    vma_entry = ctk.CTkEntry(master=cadre_fc, placeholder_text="VMA", width=250,
                              height=35)
    vma_entry.pack(pady=10, padx=10)

    distance_entry = ctk.CTkEntry(master=cadre_fc, placeholder_text="Distance (km)", width=250,
                              height=35)
    distance_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_fc, fg_color="white", corner_radius=20,)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre temps de course\n directement sur votre appareil et ne stockons pas cette donnée.",
                           font=("Arial", 15), text_color="#000002")
    result.pack(padx=50, pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_fc, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    def calcul_temps(account_id, username, password):
        try:
            distance = float(distance_entry.get().strip())
            vma = float(vma_entry.get().strip())

            if distance <= 0 or vma <=0:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La distance et le temps doivent être supérieur à 0",
                    icon="cancel"
                )
            if not distance or not vma:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur : La distance et la vma ne peuvent pas être vides",
                    icon="cancel"
                )
            if distance <= 2:
                vitesse_moyenne = vma*0.98
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 2 <= distance <= 3:
                vitesse_moyenne = vma*0.94
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 3 <= distance <= 6:
                vitesse_moyenne = vma*0.82
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 6 <= distance <= 12:
                vitesse_moyenne = vma*0.77
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 12 <= distance <= 25:
                vitesse_moyenne = vma*0.72
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            elif 21.0975 <= distance <= 42.195:
                vitesse_moyenne = vma*0.62
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"
            else:
                vitesse_moyenne = vma*0.55
                temps_calculer = distance/vitesse_moyenne
                heure = int(temps_calculer)
                minute_calculer = (temps_calculer-heure)*60
                minutes = int(minute_calculer)
                seconde = (minute_calculer-minutes)*60
                interpretation = f"Temps estimé : {heure:.0f}h {minutes:.0f}min {seconde:.0f}s"

            result.configure(text=f"{interpretation}")
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: calcul_temps(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: outils(account_id, username, password))
    button_retour.pack(side="left", padx=10, pady=20)

def activer_pause(account_id, username, password, type_pause):
    curseur.execute("SELECT id FROM Pauses WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    if curseur.fetchone():
        CTkMessagebox(
            title="Erreur",
            message="Une pause est déjà active.",
            icon="cancel"
        )
        return
    #date('now') pour prendre direct la date aujourd'hui (c'est une fonction SQLite)
    curseur.execute("""INSERT INTO Pauses (account_id, type, date_debut)VALUES (?, ?, date('now'))""", (account_id, type_pause))
    con.commit()
    CTkMessagebox(
        title="Enregistré",
        message=f"Pause {type_pause} activée !",
        icon="check"
    )

def arreter_pause(account_id, username, password):
    curseur.execute("""UPDATE Pauses SET date_fin = date('now')WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    con.commit()
    CTkMessagebox(
        title="Enregistré",
        message="Reprise d'activité enregistrée !",
        icon="check"
    )

def modifier_statut(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app)        
    cadre_statut.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_statut ,text="Modifier mon statut d'entraînement", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))
    info = ctk.CTkLabel(master=cadre_statut ,text="Si vous avez besoin de souffler, vous pouvez désormais mettre en pause les\n" \
    "analyses pour vous reposer.", font=("Arial", 15))
    info.pack(padx=50, pady=(25, 10))

    frame = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    curseur.execute("SELECT type FROM Pauses WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    result = curseur.fetchall()
    if result == []:
        info_statut = ctk.CTkLabel(master=frame, text="Votre statut d'entraînement actuel : Actif", font=("Arial", 15))
        info_statut.pack(padx=0, pady=10)
    elif result == [('vacances',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Votre statut d'entraînement actuel: Vacances", font=("Arial", 15))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == [('blessure',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Votre statut d'entraînement actuel : Blessure", font=("Arial", 15))
        info_statut_actif.pack(padx=0, pady=10)
    else:
        CTkMessagebox(
            title="Erreur",
            message="Statut inconnu ou incohérent.",
            icon="cancel"
        )
    options = {"Vacances": "Vacances", "Blessure": "Blessure", "Reprendre les analyses": "Reprendre"}
    combo_statut = ctk.CTkComboBox(master=frame, width=320, height=35, values=list(options.keys()), state="readonly"
                                   , border_width=2, border_color="#187D4B", button_color="#187D4B")
    combo_statut.pack(pady=10)
    combo_statut.set("Séléctionnez la raison")

    def enregistrer_activité(account_id, username, password):
        statut_choisi = combo_statut.get()
        statut = options[statut_choisi]
        try:
            if statut == "Vacances":
                activer_pause(account_id, username, password, "vacances")
            elif statut == "Blessure":
                activer_pause(account_id, username, password, "blessure")
            elif statut == "Reprendre":
                arreter_pause(account_id, username, password)
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                            corner_radius=10, height=35, font=("Arial", 16),
                            command=lambda: enregistrer_activité(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=10)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=10)

def modifier_password(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app)        
    cadre_statut.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_statut ,text="Changer mon mots de passe", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    app.bind('<Return>', lambda event: new_username(account_id, username, password))
    password_entry = ctk.CTkEntry(master=cadre_statut, placeholder_text="Nouveau mots de passe", width=260, show="*",
                                  height=35)
    password_entry.pack(pady=10)
    password_entry2 = ctk.CTkEntry(master=cadre_statut, placeholder_text="Confirmez votre nouveau mots de passe", width=260, show="*",
                                  height=35)
    password_entry2.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10))
    def new_username(account_id, username, password):
        new_password = password_entry.get()
        new_password2 = password_entry2.get()
        password_encode = new_password.encode("UTF-8")
        if new_password == new_password2:
            try:
                if not password_entry or not password_entry2:
                    CTkMessagebox(
                        title="Erreur",
                        message="Le mots de passe ne peut pas être vide. Veuillez remplir tous les champs !",
                        icon="cancel"
                    )
                else:
                    if (password_valide(new_password)):
                        sha256 = hashlib.sha256()
                        sha256.update(password_encode)
                        hashed_password = sha256.hexdigest()
                        con.execute("UPDATE Account SET password = ? WHERE id = ?", (hashed_password, account_id))
                        con.commit()
                        CTkMessagebox(
                            title="Enregistré",
                            message="Votre mots de passe à bien été modifié !",
                            icon="check"
                        )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur base de données",
                    message="Erreur de base de données lors du changement de mots de passe.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
        else:
            CTkMessagebox(
                title="Erreur",
                message="Les mots de passe saisis ne correspondent pas.",
                icon="cancel"
            )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                            corner_radius=10, height=35, font=("Arial", 16),
                            command=lambda: new_username(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=10)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=10)

def modifier_nom_utilisateur(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app)        
    cadre_statut.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_statut ,text="Changer mon pseudo", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    app.bind('<Return>', lambda event: new_password(account_id, username, password))
    username_entry = ctk.CTkEntry(master=cadre_statut, placeholder_text="Nouveau Pseudo", width=250,
                                  height=35)
    username_entry.pack(pady=10)
    username_entry2 = ctk.CTkEntry(master=cadre_statut, placeholder_text="Confirmez votre nouveau Pseudo", width=250,
                                  height=35)
    username_entry2.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10))
    def new_password(account_id, username, password):
        new_username = username_entry.get()
        new_username2 = username_entry2.get()
        if new_username == new_username2:
            try:
                if not username_entry or not username_entry2:
                    CTkMessagebox(
                        title="Erreur",
                        message="Le nom d'utilisateur ne peut pas être vide. Veuillez remplir tout les champs.",
                        icon="cancel"
                    )
                else:
                    con.execute("UPDATE Account SET username = ? WHERE id = ?", (new_username, account_id))
                    con.commit()
                    CTkMessagebox(
                        title="Enregistré",
                        message="Votre pseudo à bien été modifié !",
                        icon="check"
                    )
            except sqlite3.IntegrityError as e:
                CTkMessagebox(
                    title="Erreur base de données",
                    message="Ce pseudo est déjà utilisé, veuillez réessayer avec un autre pseudo.",
                    icon="cancel"
                )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors du changement du pseudo.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
        else:
            CTkMessagebox(
                title="Erreur",
                message="Les nom d'utilisateurs saisis ne correspondent pas.",
                icon="cancel"
            )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                            corner_radius=10, height=35, font=("Arial", 16),
                            command=lambda: new_password(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=10)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=10)

def supprimer_compte(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app)        
    cadre_statut.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_statut ,text="Supprimer mon compte", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10)) 
    info = ctk.CTkLabel(master=cadre_statut ,text="Ton compte est sur le point d'être supprimé. Ça veut dire que toutes tes données\n" \
    "et ton accès à nos services seront perdus, et il n'y aura pas de retour en arrière possible.", font=("Arial", 15))
    info.pack(padx=50, pady=(25, 10))
    info2 = ctk.CTkLabel(master=cadre_statut ,text="Êtes-vous vraiment certain de vouloir continuer ?", font=("Arial", 18))
    info2.pack(padx=50, pady=(25, 10)) 

    options_suppr = {"Oui": "oui", "Non" : "non"}

    options = ctk.CTkComboBox(master=cadre_statut, values=list(options_suppr.keys()), width=250, height=35, state="readonly"
                              , border_width=2, border_color="#187D4B", button_color="#187D4B")
    options.pack(pady=10)
    options.set("Séléctionnez Oui ou Non")

    frame_boutons = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame_boutons.pack(pady=(20, 10))

    def valider(account_id, username, password):
        options_choisi = options.get()
        option = options_suppr[options_choisi]
        if option == "oui":
            try:
                curseur.execute("DELETE FROM Pauses WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Objectif WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Compétition WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Activité WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Account WHERE id = ?", (account_id,))
                con.commit()
                CTkMessagebox(
                    title="Opération réussi",
                    message="Compte supprimé avec succès ! Au revoir !",
                    icon="check"
                )
                app.after(1500, lambda: [vider_fenetre(app), inscription()])
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors de la suppression du compte",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur inattendu",
                    message="Une erreur inattendu s'est produite, veuillez réessayer",
                    icon="cancel"
                )
        else:
            CTkMessagebox(
                title="Suppression de compte annulé",
                message="Votre compte n'a pas été supprimé",
                icon="info"
            )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                            corner_radius=10, height=35, font=("Arial", 16),
                            command=lambda: valider(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=10)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=10)

def ajouter_compétition(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app)       
    cadre_activité.pack(pady=20, padx=60, fill="both", expand=True)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=(20, 10))
    frame2 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame2.pack(pady=(0, 20))
    frame4 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame4.pack(pady=10)

    Titre = ctk.CTkLabel(master=frame ,text="Ajouter une compétition", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10), side="left")

    app.bind('<Return>', lambda event: sql_ajouté(account_id, username, password))
    nom_entry = ctk.CTkEntry(master=frame2, placeholder_text="Nom de la compétition", width=320,
                  height=35)
    nom_entry.pack(pady=(10, 0), side="left", padx=10)
    date_entry = ctk.CTkEntry(master=frame1, placeholder_text="Date de la compétition (JJ-MM-AAAA)", width=320,
                              height=35)
    date_entry.pack(pady=(10, 0), side="left", padx=10)    
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text="Sport", width=320,
                        height=35)
    sport_entry.pack(pady=(10, 0), side="left", padx=10)
    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text="Objectif", width=320,
                        height=35)
    objectif_entry.pack(pady=(10, 0), side="left", padx=10)

    def sql_ajouté(account_id, username, password):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip()
        date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
        date = date_conversion.strftime('%Y-%m-%d')
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()

        if not nom or not date_str or not sport or not objectif:
            CTkMessagebox(
                title="Erreur",
                message="Veuillez remplir tout les champs",
                icon="cancel"
            )
        else:
            try:
                curseur.execute("INSERT INTO Compétition (account_id, nom, date, sport, objectif) VALUES (?, ?, ?, ?, ?)", (account_id, nom, date, sport, objectif))
                con.commit()
                CTkMessagebox(
                    title="Enregistré",
                    message="Votre compétition a été enregistré, bonne chance !",
                    icon="check"
                )
                app.after(1500, lambda: [vider_fenetre(app), ajouter_compétition(account_id, username, password)])
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors de l'ajout de la compétition.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", 
                                    fg_color="#187D4B", hover_color="#13623B", corner_radius=10, height=35, font=("Arial", 16),
                                    command=lambda: sql_ajouté(account_id, username, password))
    button_enregistrer.pack(side="left", padx=10)

    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    button_back.pack(side="left", padx=10)

def supprimer_compétition(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app)
    cadre_activité.pack(pady=20, padx=60, fill="both", expand=True)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)

    Titre = ctk.CTkLabel(master=frame ,text="Supprimer une compétition", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10), side="left")

    app.bind('<Return>', lambda event: supression(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de la compétition à supprimer", width=320,
                               height=35)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    try:
        tableau_frame = ctk.CTkScrollableFrame(master=cadre_activité, fg_color="transparent")
        tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
        curseur.execute("SELECT id, nom, date FROM Compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Nom", "Date"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
            label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                 fg_color="white", corner_radius=5)
            label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)

        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 2:
                        date_obj = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date_obj.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=("Arial", 12))
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistrée.", font=("Arial", 14))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id, username, password):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_competitions_disponibles = [comp[0] for comp in result]

                if choix_id_saisi in ids_competitions_disponibles:
                    competition_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Compétition WHERE id = ? AND account_id = ?", (competition_id_db, account_id))
                    con.commit()
                    CTkMessagebox(
                        title="Suppression réussie",
                        message="Compétition supprimée avec succès.",
                        icon="check"
                    )
                    app.after(1500, lambda: [vider_fenetre(app), supprimer_compétition(account_id, username, password)])
                else:
                    CTkMessagebox(
                        title="Erreur",
                        message="L'ID de la compétition saisie n'existe pas ou n'appartient pas à votre compte.",
                        icon="cancel"
                    )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors de la suppression de la compétition.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    except sqlite3.Error as e:
        CTkMessagebox(
            title="Erreur",
            message="Erreur de base de données lors de la récupération de vos compétition.",
            icon="cancel"
        )
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                                 corner_radius=10, height=35, font=("Arial", 16),
                                 command=lambda: supression(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                 corner_radius=10, height=35, font=("Arial", 16),
                                 command=lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

def compétition(account_id, username, password):
    cadre_historique = ctk.CTkFrame(master=app)
    cadre_historique.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_historique, text="Compétition", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    frame_boutons = ctk.CTkFrame(master=cadre_historique, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), ajouter_compétition(account_id, username, password)])
    button_ajouter.pack(side="left", padx=10, pady=20)
    button_delete = ctk.CTkButton(master=frame_boutons, text="❌ Supprimer une compétition", fg_color="#AC1724", hover_color="#8D1822",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), supprimer_compétition(account_id, username, password)])
    button_delete.pack_forget()
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

    tableau_frame = ctk.CTkScrollableFrame(master=cadre_historique, fg_color="transparent")
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
    try:
            curseur.execute("SELECT nom, date, sport, objectif FROM Compétition WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
            compétition_result = curseur.fetchall()

            headers = ["Nom", "Date", "Sport", "Objectif"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                    fg_color="white", corner_radius=5)
                label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if compétition_result:
                for row_idx, activite in enumerate(compétition_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=("Arial", 12))
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
                button_delete.pack(side="left", padx=10, pady=20)
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistrée.", font=("Arial", 14))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de la récupération de vos compétitions.",
                icon="cancel"
            )
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )

def ajouter_objectif(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app)
    cadre_activité.pack(pady=20, padx=60, fill="both", expand=True)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=(20, 10))
    frame2 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame2.pack(pady=(0, 10))
    frame3 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame3.pack(pady=(0, 10))
    frame4 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame4.pack(pady=(20, 10))

    options_statut = {"En cours": "en cours", "Atteint" : "atteint", "Non-atteint" : "non-atteint"}
    options_niveau = {"Débutant": "débutant", "Intermédiaire" : "intermédiaire", "Avancé" : "avancé"}
    Titre = ctk.CTkLabel(master=frame ,text="Ajouter un objectif", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10), side="left")

    app.bind('<Return>', lambda event: sql_ajouté(account_id, username, password))
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text="Sport", width=320,
                        height=35)
    sport_entry.pack(pady=(10, 0), side="left", padx=10)
    date_entry = ctk.CTkEntry(master=frame1, placeholder_text="Date de l'objectif (JJ-MM-AAAA)", width=320,
                              height=35)
    date_entry.pack(pady=(10, 0), side="left", padx=10)
    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text="Objectif", width=320,
                        height=35)
    objectif_entry.pack(pady=(10, 0), side="left", padx=10)

    fréquence_entry = ctk.CTkEntry(master=frame2, placeholder_text="Fréquence (ex: 1-2 fois par semaine)", width=320,
                  height=35)
    fréquence_entry.pack(pady=(10, 0), side="left", padx=10)

    niveau_entry = ctk.CTkComboBox(master=frame3, values=list(options_niveau.keys()), width=320, state="readonly",
            height=35, border_width=2, border_color="#187D4B", button_color="#187D4B")
    niveau_entry.pack(pady=(10, 0), side="left", padx=10)
    niveau_entry.set("Niveau actuel")

    statut_entry = ctk.CTkComboBox(master=frame3, values=list(options_statut.keys()), width=320, state="readonly",
        height=35, border_width=2, border_color="#187D4B", button_color="#187D4B")
    statut_entry.pack(pady=(10, 0), side="left", padx=10)
    statut_entry.set("Statut de l'objectif")

    def sql_ajouté(account_id, username, password):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip()
        date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
        date = date_conversion.strftime('%Y-%m-%d')
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau_choisi = niveau_entry.get()
        niveau = options_niveau[niveau_choisi]
        statut_choisi = statut_entry.get()
        statut = options_statut[statut_choisi]

        if not sport or not date_str or not objectif or not fréquence or not niveau:
            CTkMessagebox(
                title="Erreur",
                message="Veuillez remplir tout les champs",
                icon="cancel"
            )
        else:
            try:
                curseur.execute("INSERT INTO Objectif (account_id, sport, date, objectif, fréquence, niveau_début, statut) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, sport, date, objectif, fréquence, niveau, statut))
                con.commit()
                CTkMessagebox(
                    title="Enregistré",
                    message="Votre objectif a été enregistré, bonne chance !",
                    icon="check"
                )
                app.after(1500, lambda: [vider_fenetre(app), ajouter_objectif(account_id, username, password)])
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors de l'ajout de votre objectif.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )

    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color="#187D4B", hover_color="#13623B",
                                        corner_radius=10, height=35, font=("Arial", 16),
                                        command=lambda: sql_ajouté(account_id, username, password))
    button_enregistrer.pack(side="left", padx=10)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_back.pack(side="left", padx=10)

def modifier_objectif(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app)       
    cadre_activité.pack(pady=20, padx=60, fill="both", expand=True)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)

    Titre = ctk.CTkLabel(master=frame ,text="Changer le statut", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10), side="left")

    app.bind('<Return>', lambda event: modification(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif à modifier", width=320,
                        height=35)
    choix_entry.pack(pady=10, side="left", padx=10)

    options = ["En cours", "Atteint", "Non atteint"]
    new_entry = ctk.CTkComboBox(master=frame1, values=options, width=320, state="readonly",
                        height=35, border_width=2, border_color="#187D4B", button_color="#187D4B")
    new_entry.pack(pady=10, side="left", padx=10)
    new_entry.set("Statut de l'objectif")

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    try:
        tableau_frame = ctk.CTkScrollableFrame(master=cadre_activité, fg_color="transparent")
        tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Sport", "Date", "Objectif", "Statut"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                    fg_color="white", corner_radius=5)
                label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

        if result:
                for row_idx, activite in enumerate(result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 2:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=("Arial", 12))
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
        else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré", font=("Arial", 14))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def modification(account_id, username, password):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in result]

                if choix_id_saisi in ids_objectifs_disponibles:
                    nouveau_statut = new_entry.get().strip().lower()
                    if nouveau_statut in ["en cours", "atteint", "non atteint"]:
                        objectif_id_db = choix_id_saisi
                        curseur.execute("UPDATE Objectif SET statut = ? WHERE id = ? AND account_id = ?", (nouveau_statut, objectif_id_db, account_id))
                        con.commit()
                        CTkMessagebox(
                            title="Opération réussie",
                            message="Objectif mis à jour avec succès.",
                            icon="check"
                        )
                        app.after(1500, lambda: [vider_fenetre(app), modifier_objectif(account_id, username, password)])
                    else:
                        CTkMessagebox(
                            title="Erreur",
                            message="Statut invalide. Veuillez réessayer",
                            icon="cancel"
                        )
                else:
                    CTkMessagebox(
                        title="Erreur",
                        message="L'ID de l'objectif saisi n'existe pas ou n'appartient pas à votre compte.",
                        icon="cancel"
                    )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message=f"Erreur de base de données lors de la modification de l'objectif.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors de la récupération de vos objectifs.",
                    icon="cancel"
                )
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: modification(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

def supprimer_objectif(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app)
    cadre_activité.pack(pady=20, padx=60, fill="both", expand=True)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)

    Titre = ctk.CTkLabel(master=frame ,text="Supprimer un objectif", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10), side="left")

    app.bind('<Return>', lambda event: supression(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif à supprimer", width=320,
                               height=35)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    try:
        tableau_frame = ctk.CTkScrollableFrame(master=cadre_activité, fg_color="transparent")
        tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Sport", "Date", "Objectif", "Statut"]

        for col_idx, header_text in enumerate(headers):
            label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                 fg_color="white", corner_radius=5)
            label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)

        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 2:
                        date = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=("Arial", 12))
                    label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=("Arial", 14))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id, username, password):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in result]

                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Objectif WHERE id = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    CTkMessagebox(
                        title="Suppression réussie",
                        message="Objectif supprimé avec succès.",
                        icon="check"
                    )
                    app.after(1500, lambda: [vider_fenetre(app), supprimer_objectif(account_id, username, password)])
                else:
                    CTkMessagebox(
                        title="Erreur",
                        message="L'ID de l'objectif saisi n'existe pas ou n'appartient pas à votre compte.",
                        icon="cancel"
                    )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Erreur de base de données lors de la suppression de l'objectif.",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    except sqlite3.Error as e:
        CTkMessagebox(
            title="Erreur",
            message="Erreur de base de données lors de la récupération de vos objectifs.",
            icon="cancel"
        )
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color="#187D4B", hover_color="#13623B",
                                 corner_radius=10, height=35, font=("Arial", 16),
                                 command=lambda: supression(account_id, username, password))
    button_check.pack(side="left", padx=10, pady=20)

    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                 corner_radius=10, height=35, font=("Arial", 16),
                                 command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

def objectifs(account_id, username, password):
    cadre_historique = ctk.CTkFrame(master=app)
    cadre_historique.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_historique, text="Objectif", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 10))

    frame_boutons = ctk.CTkFrame(master=cadre_historique, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), ajouter_objectif(account_id, username, password)])
    button_ajouter.pack(side="left", padx=10, pady=20)
    button_delete = ctk.CTkButton(master=frame_boutons, text="❌ Supprimer un objectif", fg_color="#AC1724", hover_color="#8D1822",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), supprimer_objectif(account_id, username, password)])
    button_delete.pack_forget()
    button_modifier = ctk.CTkButton(master=frame_boutons, text="✏️  Changer le statut", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), modifier_objectif(account_id, username, password)])
    button_modifier.pack_forget()
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                           corner_radius=10, height=35, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_retour.pack(side="left", padx=10, pady=20)

    tableau_frame = ctk.CTkScrollableFrame(master=cadre_historique, fg_color="transparent")
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)
    try:
            curseur.execute("SELECT sport, date, objectif, fréquence, niveau_début, statut FROM Objectif WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
            objectif_result = curseur.fetchall()

            headers = ["Sport", "Date", "Objectifs", "Fréquence", "Niveau au début de l'objectif", "Statut"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                    fg_color="white", corner_radius=5)
                label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if objectif_result:
                for row_idx, activite in enumerate(objectif_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=("Arial", 12))
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
                button_delete.pack(side="left", padx=10, pady=20)
                button_modifier.pack(side="left", padx=10, pady=20)
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=("Arial", 14))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de la récupération de l'historique.",
                icon="cancel"
            )
    except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendu s'est produite, veuillez réessayer.",
                icon="cancel"
            )

def exercice(account_id, username, password):
    cadre_exercice = ctk.CTkFrame(master=app)
    cadre_exercice.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_exercice, text="Exercice", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 15))
    
    frame_bouton = ctk.CTkFrame(master=cadre_exercice, fg_color="transparent")
    frame_bouton.pack(pady=10, padx=20)    
    
    frame_boutons = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_boutons.pack(pady=5, padx=20)
    
    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir": 9999}
    
    combo_periode = ctk.CTkComboBox(master=frame_boutons, values=list(options_periode.keys()), font=("Arial", 15), height=35, state="readonly"
                                    , border_width=2, border_color="#187D4B", button_color="#187D4B")
    combo_periode.pack(side="left", padx=(0, 10))

    info = ctk.CTkLabel(master=cadre_exercice, text="Historique d'entraînement", font=("Arial", 16))
    info.pack(padx=50, pady=10)

    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')

    button_creer_activite = ctk.CTkButton(master=frame_boutons, text="➕ Ajouter",
                                         corner_radius=10, height=35, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                                         command=lambda: [vider_fenetre(app), ajouter_activité(account_id, username, password)])
    button_creer_activite.pack(side="left", padx=10)
    
    button_exportation = ctk.CTkButton(master=frame_boutons, text="🔗 Exporter", fg_color="#187D4B", hover_color="#13623B",
                                         corner_radius=10, height=35, font=("Arial", 16),
                                         command=lambda: exportation_fichiers(account_id, username, password, avoir_periode(combo_periode.get(), options_periode)))
    button_exportation.pack_forget()
    
    button_supprimer = ctk.CTkButton(master=frame_boutons, text="❌ Supprimer", fg_color="#AC1724", hover_color="#8D1822",
                                         corner_radius=10, height=35, font=("Arial", 16),
                                         command=lambda: supprimer_activité(account_id, username, password, avoir_periode(combo_periode.get(), options_periode)))
    button_supprimer.pack_forget()
    
    button_back = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                         corner_radius=10, height=35, font=("Arial", 16),
                                         command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_back.pack(side="left", padx=10)

    tableau_frame = ctk.CTkScrollableFrame(master=cadre_exercice, fg_color="transparent")
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def mettre_a_jour_historique(selection):
        for widget in tableau_frame.winfo_children():
            widget.destroy()        
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute("SELECT date_activité, nom, sport, durée, distance, rpe, fatigue, charge FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            headers = ["Date", "Nom", "Sport", "Durée (min)", "Distance (km)", "RPE", "Fatigue", "Charge"]
            for col_idx, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=("Arial", 15), text_color="#000002",
                                     fg_color="white", corner_radius=5)
                label.grid(row=0, column=col_idx, padx=5, pady=2, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 0:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        elif col_idx == 7 and data is not None:
                             data = f"{float(data):.1f}"
                        
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=("Arial", 12))
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=2, sticky="ew")
                button_exportation.pack(side="left", padx=10, pady=20)
                button_supprimer.pack(side="left", padx=10, pady=20) 
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=("Arial", 14))
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)

        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de la récupération de votre historique", 
                icon="cancel"
                )
        except Exception as e:
            CTkMessagebox(
                title="Erreur", 
                message="Une erreur inattendu s'est produite, veuillez réessayer.", 
                icon="cancel"
                )
    combo_periode.configure(command=mettre_a_jour_historique)
    combo_periode.set("1 semaine")
    mettre_a_jour_historique("1 semaine")

def performance(account_id, username, password):
    cadre_performance = ctk.CTkFrame(master=app)        
    cadre_performance.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_performance ,text="Performance", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 15))

    frame_bouton = ctk.CTkFrame(master=cadre_performance, fg_color="transparent")
    frame_bouton.pack(pady=10, padx=20)
    try:
        frame_p1 = ctk.CTkFrame(master=cadre_performance, fg_color="white", corner_radius=20)
        frame_p1.pack(pady=20)

        date_actuelle = date.today()

        ca = date_actuelle - timedelta(days=7)
        ca_str = ca.strftime('%Y-%m-%d')
        curseur.execute("SELECT charge FROM Activité WHERE account_id = ? AND date_activité >= ?", (account_id, ca_str))
        charges_aigue = [row[0] for row in curseur.fetchall()]

        cc = date_actuelle - timedelta(days=28)
        cc_str = cc.strftime('%Y-%m-%d')
        curseur.execute("SELECT date_activité, charge FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité ASC", (account_id, cc_str))
        data_pour_graphique = curseur.fetchall()

        charge_aigue = sum(charges_aigue) / len(charges_aigue) if charges_aigue else 0

        #On prend le 2ème élément des data pour graphique pour avoir les charges et ne pas prendre les dates
        charge_chronique = sum([row[1] for row in data_pour_graphique]) / len(data_pour_graphique) if data_pour_graphique else 0

        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None

        info = ctk.CTkLabel(master=frame_p1 ,text="Charge d'entraînement", 
                                   font=("Arial", 18, "bold"), text_color="#000002")
        info.pack(padx=50, pady=(10, 15))
        text_charge = ctk.CTkLabel(master=frame_p1 ,text=f"Charge aiguë (7 jours) : {charge_aigue:.1f}\nCharge chronique (28 jours) : {charge_chronique:.1f}", 
                                   font=("Arial", 15), text_color="#000002")
        text_charge.pack(padx=50, pady=(10, 0))

        pause = verifier_pause(account_id)
        if pause == "blessure":
            info_pause = ctk.CTkLabel(master=frame_p1, text="⛑️ Mode blessure : suivi désactivé ! \n" \
            "Accorde à ton corps le temps de guérir, c'est un investissement pour revenir plus fort.", font=("Arial", 15),
                                      text_color="#B42828")
            info_pause.pack(padx=50, pady=20)
        elif pause == "vacances":
            info_pause = ctk.CTkLabel(master=frame_p1, text="🏖️ Mode vacances : pas d'analyse ! \n" \
            "Profite à fond de ce break, c'est le moment idéal pour recharger les batteries et revenir encore plus motivé !", font=("Arial", 15),
                                      text_color="#4B7617")
            info_pause.pack(padx=50, pady=20)
        else :
            if ratio is not None:
                info_ratio = ctk.CTkLabel(master=frame_p1, text=f"📊 Ratio : {ratio:.2f}", 
                                            font=("Arial", 15), text_color="#000002")
                info_ratio.pack(padx=50, pady=(0, 10))
                if ratio < 0.5: 
                    info_charge = ctk.CTkLabel(master=frame_p1, text="🛌 Récupération active : Charge très basse. Priorité à la régénération", 
                                            font=("Arial", 15), text_color="#1D597F")
                    info_charge.pack(padx=50, pady=10)
                elif 0.5 <= ratio <= 0.8:
                    info_charge = ctk.CTkLabel(master=frame_p1, text="😴 Sous-entraînement : Vous pourriez augmenter légèrement l'intensité.",
                                            font=("Arial", 15), text_color="#857B22")
                    info_charge.pack(padx=50, pady=10)
                elif 0.8 <= ratio <= 0.9:
                    info_charge = ctk.CTkLabel(master=frame_p1, text="🔄 Maintien : Charge adaptée pour conserver votre niveau.",
                                            font=("Arial", 15), text_color="#3D7D1F")
                    info_charge.pack(padx=50, pady=10)
                elif 0.9 <= ratio <= 1.1:
                    info_charge = ctk.CTkLabel(master=frame_p1, text="🟢 Progression optimale : Charge idéale pour améliorer vos performances",
                                            font=("Arial", 15), text_color="#09822B")
                    info_charge.pack(padx=50, pady=10)
                elif 1.1 < ratio <= 1.3:
                    info_charge = ctk.CTkLabel(master=frame_p1, text="💪 Progression élévée : Restez vigilant à la fatigue accumulée.",
                                            font=("Arial", 15), text_color="#768B0C")
                    info_charge.pack(padx=50, pady=10)
                else:
                    info_charge = ctk.CTkLabel(master=frame_p1, text="⚠️ Surentraînement : Risque élevé de blessure. Repos nécessaire.",
                                            font=("Arial", 15), text_color="#A30808")
                    info_charge.pack(padx=50, pady=10)
            else:
                info_charge = ctk.CTkLabel(master=frame_p1, text="🚫 Données insuffisantes pour calculer le ratio.",
                                        font=("Arial", 15), text_color="#A30808")
                info_charge.pack(padx=50, pady=10)
    except sqlite3.Error as e:
        CTkMessagebox(
            title="Erreur",
            message="Erreur de base de données lors du calcul de charge d'entraînement.",
            icon="cancel"
        )
    except Exception as e:
        CTkMessagebox(
            title="Erreur",
            message="Une erreur inattendu s'est produite, veuillez réessayer",
            icon="cancel"
        )
    def graphique_charge(account_id, username, password):
        vider_fenetre(app)
        try:    
                if data_pour_graphique:
                    cadre_graphique = ctk.CTkFrame(master=app)
                    cadre_graphique.pack(pady=20, padx=60, fill="both", expand=True)
                    
                    titre_graphique = ctk.CTkLabel(master=cadre_graphique, text="Évolution de la charge chronique", 
                                                font=("Arial", 20, "bold"))
                    titre_graphique.pack(padx=50, pady=(25, 10))
                    
                    frame_graph = ctk.CTkFrame(master=cadre_graphique, fg_color="white")
                    frame_graph.pack(pady=20)
                    dates_graphique = [datetime.strptime(row[0], '%Y-%m-%d') for row in data_pour_graphique]
                    charges_graphique = [row[1] for row in data_pour_graphique]

                    fig, ax = plt.subplots(figsize=(12, 5))
                    sns.lineplot(x=dates_graphique, y=charges_graphique, marker='o', color='blue', ax=ax)

                    ax.axhline(y=charge_chronique, color='red', linestyle='--')
                    ax.set_title("Évolution de la charge chronique")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Charge chronique")

                    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
                    canvas.draw()
                    canvas.get_tk_widget().pack(pady=10)

                    def fermer_graphique(account_id, username, password):
                        plt.close(fig)
                        performance(account_id, username, password)

                    button_back_graph = ctk.CTkButton(master=cadre_graphique, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                                     corner_radius=10, height=35, font=("Arial", 16),
                                                    command=lambda: [vider_fenetre(app), fermer_graphique(account_id, username, password)])
                    button_back_graph.pack(pady=10)
                else:
                    performance(account_id, username, password)
                    CTkMessagebox(
                        title="Pas de données",
                        message="❌ Pas assez de données pour afficher un graphique.",
                        icon="warning"
                    )
                    return
        except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    button_graphique = ctk.CTkButton(master=frame_bouton, text="📈 Graphique", corner_radius=10, height=35,
                            font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), graphique_charge(account_id, username, password)])
    button_graphique.pack(side="left", padx=10, pady=10)
    button_statut = ctk.CTkButton(master=frame_bouton, text="📊 Modifier mon statut entraînement",
                            corner_radius=10, height=35, font=("Arial", 16),
                            fg_color="#187D4B", hover_color="#13623B",
                            command=lambda: [vider_fenetre(app), modifier_statut(account_id, username, password)])
    button_statut.pack(side="left", padx=10, pady=10)
    button_objectif = ctk.CTkButton(master=frame_bouton, text="🎯 Objectif", 
                           corner_radius=10, height=35, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_objectif.pack(side="left", padx=10, pady=0)
    button_competition = ctk.CTkButton(master=frame_bouton, text="🏆 Compétition", 
                           corner_radius=10, height=35, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    button_competition.pack(side="left", padx=10, pady=0)
    button_back = ctk.CTkButton(master=frame_bouton, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                         corner_radius=10, height=35, font=("Arial", 16),
                                         command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_back.pack(side="left", padx=10)

def outils(account_id, username, password):
    vider_fenetre(app)
    cadre_outils = ctk.CTkFrame(master=app)        
    cadre_outils.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_outils ,text="Outil", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 25))

    frame_bouton = ctk.CTkFrame(master=cadre_outils, fg_color="transparent", border_color="white", border_width=1)
    frame_bouton.pack(pady=(20,0), padx=20)
    frame_bouton1 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton1.pack(pady=(20,0), padx=20)
    frame_bouton2 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton2.pack(pady=(20,0), padx=20)
    frame_bouton3 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton3.pack(pady=(20, 20), padx=20)
    frame_bouton4 = ctk.CTkFrame(master=cadre_outils, fg_color="transparent")
    frame_bouton4.pack(pady=(40,0), padx=20)

    button_predicteur_temps = ctk.CTkButton(master=frame_bouton1, text="⏱️ Prédicteur de course",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_predicteur_temps.pack(side="left", padx=10, pady=0)

    button_zones = ctk.CTkButton(master=frame_bouton1, text="❤️ Zones Cardiaque",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), zone_fc(account_id, username, password)])
    button_zones.pack(side="left", padx=10, pady=0)

    button_imc = ctk.CTkButton(master=frame_bouton2, text="⚖️ Calculateur IMC",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), imc(account_id, username, password)])
    button_imc.pack(side="left", padx=10, pady=0)

    button_vma = ctk.CTkButton(master=frame_bouton2, text="🚀 Estimation VMA", 
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), VMA(account_id, username, password)])
    button_vma.pack(side="left", padx=10, pady=0)

    button_VO2MAX = ctk.CTkButton(master=frame_bouton3, text="🫁 Estimation VO2max", 
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), VO2MAX(account_id, username, password)])
    button_VO2MAX.pack(side="left", padx=10, pady=0)

    button_back = ctk.CTkButton(master=frame_bouton4, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                         corner_radius=10, height=35, font=("Arial", 16),
                                         command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_back.pack(side="left", padx=10)

def mon_compte(account_id, username, password):
    cadre_compte = ctk.CTkFrame(master=app)        
    cadre_compte.pack(pady=20, padx=60, fill="both", expand=True)

    frame1 = ctk.CTkFrame(master=cadre_compte, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    frame_boutons1 = ctk.CTkFrame(master=cadre_compte, fg_color="transparent")
    frame_boutons1.pack(pady=(20, 10))
    frame2 = ctk.CTkFrame(master=cadre_compte, corner_radius=20, fg_color="white")        
    frame2.pack(pady=20, padx=20)

    curseur.execute("SELECT type FROM Pauses WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    result = curseur.fetchall()

    Titre = ctk.CTkLabel(master=frame1 ,text="Mon compte", font=("Arial", 20, "bold"))
    Titre.pack(padx=50, pady=(25, 0))

    info = ctk.CTkLabel(master=frame2 ,text=f"Votre ID : {account_id} \n\n Votre pseudo : {username}\n", font=("Arial", 15), text_color="#000002")
    info.pack(padx=20, pady=(20, 0))

    if result == []:
        info_statut = ctk.CTkLabel(master=frame2, text="Votre statut d'entraînement actuel : Actif", font=("Arial", 15), text_color="#000002")
        info_statut.pack(padx=20, pady=(0, 20))
    elif result == [('vacances',)]:
        info_statut_actif = ctk.CTkLabel(master=frame2, text="Votre statut d'entraînement actuel : Vacances", font=("Arial", 15), text_color="#000002")
        info_statut_actif.pack(padx=20, pady=(0, 20))
    elif result == [('blessure',)]:
        info_statut_actif = ctk.CTkLabel(master=frame2, text="Votre statut d'entraînement actuel : Blessure", font=("Arial", 15), text_color="#000002")
        info_statut_actif.pack(padx=20, pady=(0, 20))
    else:
        CTkMessagebox(
            title="Erreur",
            message="Statut inconnu ou incohérent",
            icon="cancel"
        )
    button_password = ctk.CTkButton(master=frame_boutons1, text="🔒 Changer mon mot de passe",
                            corner_radius=10, height=35, font=("Arial", 16),
                            fg_color="#187D4B", hover_color="#13623B",
                            command=lambda: [vider_fenetre(app), modifier_password(account_id, username, password)])
    button_password.pack(side="left", padx=10)
    button_username = ctk.CTkButton(master=frame_boutons1, text="🧑 Changer mon pseudo", 
                            corner_radius=10, height=35, font=("Arial", 16),
                            fg_color="#187D4B", hover_color="#13623B",
                            command=lambda: [vider_fenetre(app), modifier_nom_utilisateur(account_id, username, password)])
    button_username.pack(side="left", padx=10)
    button_suppr = ctk.CTkButton(master=frame_boutons1, text="❌ Supprimer mon compte", 
                            corner_radius=10, height=35, font=("Arial", 16),
                            fg_color="#AC1724", hover_color="#8D1822",
                            command=lambda: [vider_fenetre(app), supprimer_compte(account_id, username, password)])
    button_suppr.pack(side="left", padx=10)
    button_back = ctk.CTkButton(master=frame_boutons1, text="🔙 Retour", fg_color="#00578E", hover_color="#004774",
                                         corner_radius=10, height=35, font=("Arial", 16),
                                         command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_back.pack(side="left", padx=10)

def accueil(account_id, username, password):
    cadre_accueil = ctk.CTkFrame(master=app)   
    cadre_accueil.pack(pady=20, padx=60, fill="both", expand=True)
    if heure_debut <= heure_actuelle_objet <= heure_fin:
        Titre2 = ctk.CTkLabel(master=cadre_accueil ,text=f"Bonsoir {username} !", font=("Arial", 24))
        Titre2.pack(padx=50, pady=(25, 5))
    else:
        Titre2 = ctk.CTkLabel(master=cadre_accueil ,text=f"Bonjour {username} !", font=("Arial", 24))
        Titre2.pack(padx=50, pady=(25, 5))

    conseils = [
            "💡 Astuce : Démarre doucement.",
            "💡 Astuce : Fixe-toi des petits objectifs pour garder la motivation.",
            "💡 Astuce : Fais le sport que tu aimes.",
            "💡 Astuce : Varie tes activités, tes entraînements.",
            "💡 Astuce : Pense à t'échauffer.",
            "💡 Astuce : Écoute ton corps.",
            "💡 Astuce : Bois de l'eau.",
            "💡 Astuce : Mange sainement.",
            "💡 Astuce : Sois régulier, discipliner.",
            "💡 Astuce : Dors assez.",
            "💡 Astuce : Prépare tes affaires à l'avance pour ne pas avoir d'excuses le lendemain",
            "💡 Astuce : Étire-toi le soir pour éviter les courbatures.",
            "💡 Astuce : Ne te compare pas aux autres, compare toi au toi d'hier.",
            "💡 Astuce : Utilise Sprintia pour optimiser ton entraînement.",
            "💡 Astuce : Privilégie la discipline plutôt que la motivation.",
            "💡 Astuce : Prends des jours de repos, ça fait partit aussi de l'entraînement.",
            "💡 Astuce : Amuse-toi !",
            "💡 Astuce : Prends du plaisir à chaque séances de sport !",
            "💡 Astuce : Sois patient, les résultats vont finir par arriver avec le temps.",
    ]
    défi = [
            "⚡️  Défi : Chaise : Tiens 60s assis contre un mur.",
            "⚡️  Défi : Fais 10 burpees le plus vite possible.",
            "⚡️  Défi : Fais du Gainage pendant 90 secondes.",
            "⚡️  Défi : 100 squats : 100 squats",
            "⚡️  Défi : 20 fentes : 10 fentes par jambe.",
            "⚡️  Défi : Max pompes 60s : Fais un max de pompes en 1 minute.",
            "⚡️  Défi : Sprint sur place 60s : Cours sur place à fond pendant une minute.",
            "⚡️  Défi : 30 crunchs : Fais 30 crunchs.",
            "⚡️  Défi : Équilibre yeux fermés : Tiens 30s en équilibre sur chaque jambe les yeux fermés.",
            "⚡️  Défi : Escalier : Monte/descends 10 fois un escalier.",
            "⚡️  Défi : Fais 20 Jumping Jack.",
            "⚡️  Défi : Fais une minutes de gainage latéral.",
            "⚡️  Défi : Fais une minutes de mountain climber.",
            "⚡️  Défi : Fais 5 de burpees."
    ]
    motivation = [
            "🛡️ Motivation : Chaque effort compte. Ne lâche rien !",
            "🛡️ Motivation : Tes limites ? Elles sont faites pour être dépassées.",
            "🛡️ Motivation : Aujourd'hui, c'est le jour pour devenir plus fort.",
            "🛡️ Motivation : L'échec n'existe pas, seulement les leçons.",
            "🛡️ Motivation : Ne rêve pas ta vie, vis tes rêves.",
            "🛡️ Motivation : La seule mauvaise séance, c'est celle que tu ne fais pas.",
            "🛡️ Motivation : Passe à l'action, le reste suivra.",
            "🛡️ Motivation : Commence petit, rêve grand.",
            "🛡️ Motivation : La régularité bat l'intensité. Sois constant."
    ]
    
    conseil_du_jour = random.choice(conseils)
    défi_du_jour = random.choice(défi)
    motivation_du_jour = random.choice(motivation)

    frame = ctk.CTkFrame(master=cadre_accueil, border_width=1, border_color="white")
    frame.pack(pady=(30, 20))
    frame_conseil = ctk.CTkFrame(master=frame)
    frame_conseil.pack(pady=10, padx=10)
    frame_defi = ctk.CTkFrame(master=frame)
    frame_defi.pack(pady=10, padx=10)
    frame_motivation = ctk.CTkFrame(master=frame)
    frame_motivation.pack(pady=10, padx=10)

    titre_conseil = ctk.CTkLabel(master=frame_conseil, text=f"{conseil_du_jour}", text_color="#497B0C",
                                 font=("Arial", 16, "bold"), corner_radius=20)
    titre_conseil.pack(pady=10, padx=10)
    titre_défi = ctk.CTkLabel(master=frame_defi, text=f"{défi_du_jour}",  text_color="#AC4402",
                                 font=("Arial", 16, "bold"), corner_radius=20)
    titre_défi.pack(pady=10, padx=10)
    titre_motivation = ctk.CTkLabel(master=frame_motivation, text=f"{motivation_du_jour}",  text_color="#03639A",
                                 font=("Arial", 16, "bold"), corner_radius=20)
    titre_motivation.pack(pady=10, padx=10)
    
    frame_b = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent", border_width=1, border_color="white")
    frame_b.pack(pady=(20,0), padx=20)    
    frame_bouton = ctk.CTkFrame(master=frame_b, fg_color="transparent")
    frame_bouton.pack(pady=(20,0), padx=20)
    frame_bouton2 = ctk.CTkFrame(master=frame_b, fg_color="transparent")
    frame_bouton2.pack(pady=(20,0), padx=20)
    frame_bouton3 = ctk.CTkFrame(master=frame_b, fg_color="transparent")
    frame_bouton3.pack(pady=20, padx=20)

    button_exercice = ctk.CTkButton(master=frame_bouton, text="💪 Exercice",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), exercice(account_id, username, password)])
    button_exercice.pack(side="left" , padx=10, pady=0)
    button_performance = ctk.CTkButton(master=frame_bouton, text="🚀 Performance", 
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="left" , padx=10, pady=0)
    button_outils = ctk.CTkButton(master=frame_bouton2, text="🔧 Outil", 
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), outils(account_id, username, password)])
    button_outils.pack(side="left" ,padx=10, pady=0)
    button_autre = ctk.CTkButton(master=frame_bouton2, text="👤 Mon Compte",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#187D4B", hover_color="#13623B",
                           command=lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
    button_autre.pack(side="left" ,padx=10, pady=0)
    button_info = ctk.CTkButton(master=frame_bouton3, text="📢 Infos sur le logiciel", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, width=220, height=40, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), a_propos(account_id, username, password)])
    button_info.pack(side="left", pady=0, padx=10)
    button_deco = ctk.CTkButton(master=frame_bouton3, text="🚪Déconnexion", 
                           corner_radius=10, width=220, height=40, font=("Arial", 16), fg_color="#AC1724", hover_color="#8D1822",
                           command=lambda: [vider_fenetre(app), connection()])
    button_deco.pack(side="left" ,padx=10, pady=0)

def connection():
    cadre_connection = ctk.CTkFrame(master=app)        
    cadre_connection.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_connection ,text="Bienvenue sur Sprintia !", font=("Arial", 20, "bold"))
    Slogan = ctk.CTkLabel(master=cadre_connection, text="Ton cerveau d'entraînement !", font=("Arial", 15))
    
    Titre.pack(padx=50, pady=(25, 5))
    Slogan.pack(padx=50, pady=5)

    frame_bouton = ctk.CTkFrame(master=cadre_connection, fg_color="transparent")        
    frame_bouton.pack(pady=(20, 10))
    button_connection = ctk.CTkButton(master=frame_bouton, text="🌐 Connection", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), border_color="white", border_width=1,
                           command=lambda: [vider_fenetre(app), connection()])
    button_connection.pack(side="left", padx=10)
    button_inscription = ctk.CTkButton(master=frame_bouton, text="📝 Inscription", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, width=220, height=40, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), inscription()])
    button_inscription.pack(side="left", padx=10)

    frame_invite = ctk.CTkFrame(master=cadre_connection, corner_radius=10, border_width=1, border_color="white")        
    frame_invite.pack(pady=(25, 10))
    Titre2 = ctk.CTkLabel(master=frame_invite ,text="Connexion", font=("Arial", 18, "bold"))
    Titre2.pack(padx=50, pady=(15, 5))

    app.bind('<Return>', lambda event: verifier_identifiants())
    username_entry = ctk.CTkEntry(master=frame_invite, placeholder_text="Pseudo", width=250,
                                  height=35)
    username_entry.pack(pady=(15, 10), padx=20)
    password_entry = ctk.CTkEntry(master=frame_invite, placeholder_text="Mot de passe", show="*", width=250,
                                  height=35)
    password_entry.pack(pady=10, padx=20)

    def verifier_identifiants():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            CTkMessagebox(
                title="Champs manquants",
                message="Le pseudo et le mot de passe ne peuvent pas être vides",
                icon="cancel"
            )
            return

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        try:
            curseur.execute("SELECT id, username, password FROM Account WHERE username = ? AND password = ?", (username, hashed_password))
            result = curseur.fetchone()

            if result:
                account_id = result[0]
                app.after(100, lambda: [vider_fenetre(app), accueil(account_id, username, password)])
            else:
                CTkMessagebox(
                    title="Erreur",
                    message="Identifiants incorrects. Veuillez réessayer.",
                    icon="cancel"
                )
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de la connexion à votre compte.",
                icon="cancel"
            )
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendu s'est produite, veuillez réessayer",
                icon="cancel"
            )
    button_valider = ctk.CTkButton(master=frame_invite, text="Se connecter", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16), command=verifier_identifiants)
    button_valider.pack(padx=10, pady=15)

def inscription():
    cadre_connection = ctk.CTkFrame(master=app)        
    cadre_connection.pack(pady=20, padx=60, fill="both", expand=True)

    Titre = ctk.CTkLabel(master=cadre_connection ,text="Bienvenue sur Sprintia !", font=("Arial", 20, "bold"))
    Slogan = ctk.CTkLabel(master=cadre_connection, text="Ton cerveau d'entraînement !", font=("Arial", 15))
    
    Titre.pack(padx=50, pady=(25, 5))
    Slogan.pack(padx=50, pady=5)

    frame_bouton = ctk.CTkFrame(master=cadre_connection, fg_color="transparent")        
    frame_bouton.pack(pady=(20, 10))
    button_connection = ctk.CTkButton(master=frame_bouton, text="🌐 Connection", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, width=220, height=40, font=("Arial", 16),
                           command=lambda: [vider_fenetre(app), connection()])
    button_connection.pack(side="left", padx=10)
    button_inscription = ctk.CTkButton(master=frame_bouton, text="📝 Inscription", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, width=220, height=40, font=("Arial", 16), border_color="white", border_width=1,
                           command=lambda: [vider_fenetre(app), inscription()])
    button_inscription.pack(side="left", padx=10)

    frame_invite = ctk.CTkFrame(master=cadre_connection, corner_radius=10, border_width=1, border_color="white")        
    frame_invite.pack(pady=(25, 10))
    Titre2 = ctk.CTkLabel(master=frame_invite ,text="Inscription", font=("Arial", 18, "bold"))
    Titre2.pack(padx=50, pady=(15, 5))

    app.bind('<Return>', lambda event: verifier_identifiants_connexion())
    username_entry = ctk.CTkEntry(master=frame_invite, placeholder_text="Pseudo", width=250,
                                  height=35)
    username_entry.pack(pady=(15, 10), padx=20)
    password_entry = ctk.CTkEntry(master=frame_invite, placeholder_text="Mot de passe", show="*", width=250,
                                  height=35)
    password_entry.pack(pady=10)
    password_confirm= ctk.CTkEntry(master=frame_invite, placeholder_text="Confirmer mot de passe", show="*", width=250,
                                  height=35)
    password_confirm.pack(pady=10, padx=20)
    
    def verifier_identifiants_connexion():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        password_confirmation = password_confirm.get().strip()
        password_encode = password.encode("UTF-8")

        try:
            if not username_entry or not password_entry:
                CTkMessagebox(
                    title="Champs manquants",
                    message="Le pseudo et le mot de passe ne peuvent pas être vides",
                    icon="cancel"
                )
                return
                    
            if password != password_confirmation:
                CTkMessagebox(
                    title="Erreur",
                    message="Les mots de passe ne correspondent pas",
                    icon="cancel"
                )
                return
            if (password_valide(password)):
                sha256 = hashlib.sha256()
                sha256.update(password_encode)
                hashed_password = sha256.hexdigest()
                curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                account_id = curseur.lastrowid
                CTkMessagebox(
                    title="Inscription réussie",
                    message=f"Bienvenue {username} !",
                    icon="check"
                )
                app.after(1500, lambda: [vider_fenetre(app), accueil(account_id, username, password)])

        except sqlite3.IntegrityError as e:
            CTkMessagebox(
                title="Erreur base de données",
                message="Ce pseudo est déjà utilisé. Veuillez en utiliser un autre.",
                icon="cancel"
            )
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreurs",
                message="Erreur de base de données lors de l'inscription.",
                icon="cancel"
            )
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendu s'est produite, veuillez réessayer",
                icon="cancel"
            )
    button_valider = ctk.CTkButton(master=frame_invite, text="S'incrire", fg_color="#187D4B", hover_color="#13623B",
                           corner_radius=10, height=35, font=("Arial", 16), command=verifier_identifiants_connexion)
    button_valider.pack(padx=10, pady=15)

if __name__ == "__main__":
    try:
        con = sqlite3.connect("data_base.db")
        curseur = con.cursor()

        curseur.execute('''CREATE TABLE IF NOT EXISTS Account (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL)''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,allure INTEGER,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Compétition (id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT NOT NULL,date TEXT NOT NULL,sport TEXT NOT NULL,objectif TEXT NOT NULL,account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Objectif (id INTEGER PRIMARY KEY AUTOINCREMENT,sport TEXT NOT NULL,date TEXT NOT NULL,objectif TEXT NOT NULL,fréquence TEXT NOT NULL,niveau_début TEXT NOT NULL,statut TEXT, account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Pauses (id INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER NOT NULL,type TEXT CHECK(type IN ('vacances', 'blessure')),date_debut TEXT DEFAULT CURRENT_DATE,date_fin TEXT,FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        con.commit()
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")
        app = ctk.CTk()
        app.geometry("1050x550")
        app.title("Sprintia")
        connection()
        app.protocol("WM_DELETE_WINDOW", lambda: [con.close(), app.destroy()])
        app.mainloop()
    except sqlite3.Error as e:
        CTkMessagebox(
            title="Erreur",
            message="Erreur de base de données lors de la connexion à la base de données",
            icon= "cancel"
        )
        con.close()
    except Exception as e:
        CTkMessagebox(
            title="Erreur inattendu",
            message="Une erreur inattendu s'est produite, veuillez réessayer",
            icon="cancel"
        )
    con.close()
