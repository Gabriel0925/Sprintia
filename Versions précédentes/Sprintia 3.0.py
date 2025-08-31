import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import sqlite3
import hashlib
from datetime import datetime, timedelta
from datetime import date
from datetime import time as Time
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser
from urllib.parse import quote #pour remplir les champs (destinataire,...) dans une app mail

# Couleur
mode_actuel = ctk.get_appearance_mode()
if mode_actuel == "Dark":
    couleur1 = "#3d71a5"
    couleur1_hover = "#4a8bcb"
    couleur2 = "#8CB1C1"
    couleur2_hover = "#ABD1E1"
    couleur_fond = "#131d34"
    couleur_text = "#fbfcfb"
    mode_image = "Logo Sprintia Sombre.png"
else:
    couleur1 = "#4989bc"
    couleur1_hover = "#56a8ea"
    couleur2 = "#B6D8F2"
    couleur2_hover = "#D1EAFD"
    couleur_fond = "#fdfcfa"
    couleur_text = "#3a3a3a"
    mode_image = "Logo Sprintia Clair.png"

# Police d'écriture
taille1 = 28
taille2 = 20
taille3 = 16
font_principale = "DejaVu Sans"
font_secondaire = "DejaVu Sans Bold"
# Corner Radius
corner1 = 35
corner2 = 5
corner3 = 0
# Bordure
border1 = 2
border2 = 1
# Taille CTkEntry
entry_height = 45
# Taille CTkButton
button_height = 50
button_width = 180

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
    con.close()
    app.quit()

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

def reglage_par_default():
    ctk.set_appearance_mode("System")
    connection()

def a_propos(account_id, username, password):
    cadre_maj = ctk.CTkFrame(master=app, fg_color=couleur_fond)      
    cadre_maj.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_maj, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame_maj = ctk.CTkFrame(master=cadre_maj, fg_color="transparent")
    frame_maj.pack(pady=10)
    titre_frame = ctk.CTkFrame(master=frame_maj, fg_color="transparent")
    titre_frame.pack(side="left" , pady=10)
    bouton = ctk.CTkFrame(master=frame_maj, fg_color="transparent")
    bouton.pack(side="right", pady=10, padx=(50, 0))

    Titre = ctk.CTkLabel(master=titre_frame ,text="À propos", font=(font_secondaire, taille1))
    Titre.pack(pady=20)
    button_back = ctk.CTkButton(master=bouton, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_back.pack(side="left", padx=5, pady=10)

    frame_slogan = ctk.CTkFrame(master=cadre_maj, fg_color="transparent")
    frame_slogan.pack(padx=10, pady=(20, 10))
    slogan = ctk.CTkLabel(master=frame_slogan, text="Sprintia est conçue pour vous aidés avant et après un entraînement",
                          font=(font_principale, taille2))
    slogan.pack()

    frame_tout = ctk.CTkFrame(master=cadre_maj, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack(pady=(20, 10))
    frame_version = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame_version.pack(padx=10, pady=(10, 5))
    frame_dev = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame_dev.pack(padx=10, pady=(5, 10))

    version = ctk.CTkLabel(master=frame_version, text="Version Sprintia : ",
                          font=(font_principale, taille2), text_color=couleur1)
    version.pack(side="left", padx=10, pady=5)
    num_version = ctk.CTkLabel(master=frame_version, text="3.0.1",
                          font=(font_principale, taille2), text_color=couleur1)
    num_version.pack(side="left", padx=10, pady=5)
    nom_dev = ctk.CTkLabel(master=frame_dev, text="Sprintia est développé par Gabriel Chapet",
                          font=(font_principale, taille2), text_color=couleur1)
    nom_dev.pack(side="right", padx=10, pady=5)

    conteneur = ctk.CTkFrame(master=cadre_maj, fg_color=couleur_fond, corner_radius=corner1,
                             border_width=border1, border_color=couleur1)
    conteneur.pack(fill="x", expand=True, padx=25, pady=10)
    sous_titre= ctk.CTkLabel(master=conteneur, text="Pourquoi j'ai créé Sprintia ?", font=(font_secondaire, taille2))
    sous_titre.pack(pady=10)
    pourquoi = ctk.CTkLabel(master=conteneur, text="J'ai lancé Sprintia parce que pour moi, on n'a pas besoin de dépenser des fortunes pour avoir de la qualité. C'est un peu comme avec" \
                        "les montres connectées : on ne devrait pas être obligé d'acheter la toute dernière et la plus chère pour pouvoir profiter des dernières fonctionnalités." \
                        "De plus, certains constructeurs de montre connectées ce permettre de mettre un abonnement pour pouvoir bénificié de tout les fonctionnalités !" \
                        "Du coup, j'ai décidé de créer Sprintia pour faire les choses à ma manière !",
                        font=(font_principale, taille3), wraplength=950)
    pourquoi.pack(padx=10)
    sous_titre2= ctk.CTkLabel(master=conteneur, text="Qui suis-je ?", font=(font_secondaire, taille2))
    sous_titre2.pack(pady=10)
    quisuisje = ctk.CTkLabel(master=conteneur, 
                            text="J'adore le sport, la tech et l'imformatique. Ce que j'adore dans le sport," \
                            " c'est les algorithmes qui vont m'aider à m'entraîner et à progresser dans mon sport, sans avoir de coach." \
                            " Je développe Sprintia pour vous aider à vous entraîner gratuitement sans matériel. Le seul matériel requis" \
                            " pour faire fonctionner les algorithmes c'est une montre avec un chrono ou même un smartphone peut suffire pour utiliser Sprintia.",
                            font=(font_principale, taille3),  wraplength=950)
    quisuisje.pack(padx=10, pady=10)

def verifier_pause(account_id):
    #AND date_fin IS NULL = Cible uniquement les pause non terminés.
    curseur.execute("""SELECT type FROM Pauses WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    result = curseur.fetchone()
    return result[0] if result else None

def supprimer_activité(account_id, username, password, période_str):
    vider_fenetre(app)
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w", command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    carte_connexion = ctk.CTkFrame(master=cadre_activité, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 

    Titre = ctk.CTkLabel(master=frame, text="Supprimer une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    app.bind('<Return>', lambda event: supression(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="ID de l'activité à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT id_activité, date_activité, nom, sport, durée, distance, rpe FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str))
            activites = curseur.fetchall()

            headers = ["ID", "Date", "Nom", "Sport", "Durée (min)", "Distance", "RPE"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date_activité = datetime.strptime(data, '%Y-%m-%d')
                            data = date_activité.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
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
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: supression(account_id, username, password))
    button_check.pack(side="left", padx=2, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_retour.pack(side="left", padx=2, pady=20)

def ajouter_activité_intérieur(account_id, username, password):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}

    cadre_principal = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_principal.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_principal, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w", command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame1 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Intérieur")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=cadre_principal, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=(10, 20))
    frame_champs4 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    sport_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Sport", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_=1, to=10, number_of_steps=9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=10)
    nom_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Nom", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    nom_entry.pack(side="left", padx=(75, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")

    def enregistrer():
        nom = nom_entry.get().strip()
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
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erreur", 
                message="RPE invalide (1-10 requis)", 
                icon="cancel"
            )
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de fatigue invalide", 
                icon="cancel"
            )
            return
        if douleur is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de douleur invalide", 
                icon="cancel"
            )
            return
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_d
        try:
            curseur.execute("""INSERT INTO Activité_intérieur (date_activité, sport, durée, rpe, fatigue, douleur, charge, account_id, nom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, fatigue, douleur, charge, account_id, nom))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, fatigue, douleur, charge, account_id, nom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, fatigue, douleur, charge, account_id, nom))
            con.commit()
            CTkMessagebox(
                title="Succès",
                message="Votre activité a bien été enregistrée !",
                icon="check"
            )
            app.after(1500, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, username, password)])
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de l'ajout de votre activité.",
                icon="cancel"
            )
            return
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendue s'est produite, veuillez réessayer.",
                icon="cancel"
            )
            return
    bouton_valider = ctk.CTkButton(master=frame_champs4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_musculation(account_id, username, password):
    Options_matos = ["Poids de corps", "Avec équipement"]
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_lieu = {"Salle de sport": "salle de sport", "Domicile": "domicile", "Extérieur": "extérieur"}

    cadre_principal = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_principal.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_principal, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w", command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame1 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Musculation")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=cadre_principal, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)
    matos_entry = ctk.CTkComboBox(master=frame_champs1, values=Options_matos, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    matos_entry.pack(side="left", padx=10)
    matos_entry.set("Type d'entraînement")

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_=1, to=10, number_of_steps=9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=10)
    muscle_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Muscle travaillé", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    muscle_entry.pack(side="left", padx=(75, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    lieu_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_lieu.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    lieu_entry.pack(side="left", padx=10)
    lieu_entry.set("Lieu de la séance")

    rep_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre total de répétitions", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    rep_entry.pack(side="left", padx=10)
    serie_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre total de série", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    serie_entry.pack(side="left", padx=10)
    volume_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Volume total (ex : 5.5 kg)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    volume_entry.pack(side="left", padx=10)

    def enregistrer():
        muscle_travaillé = muscle_entry.get().strip()
        répétitions = rep_entry.get().strip()
        série = serie_entry.get().strip()
        volume = volume_entry.get().strip()
        if volume:
            try:
                volume_total = float(volume)
                if volume_total < 0:
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Erreur", 
                    message="Volume total invalide (entier positif requis)", 
                    icon="cancel"
                )
                return
        else:
            volume_total = None
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
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erreur", 
                message="RPE invalide (1-10 requis)", 
                icon="cancel"
            )
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        lieu = Options_lieu.get(lieu_entry.get().strip())
        équipement = matos_entry.get().strip()
        if fatigue is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de fatigue invalide", 
                icon="cancel"
            )
            return
        if douleur is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de douleur invalide", 
                icon="cancel"
            )
            return
        if lieu is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur du lieu invalide", 
                icon="cancel"
            )
            return
        if équipement is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur du type d'entraînement invalide", 
                icon="cancel"
            )
            return
        sport = "Musculation"
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        if équipement == "Avec équipement":
            facteur_matos = 1.1
        else:
            facteur_matos = 1.0
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * facteur_matos
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_c
        try:
            curseur.execute("""INSERT INTO Activité_musculation (date_activité, sport, durée, rpe, fatigue, douleur, charge, account_id, muscle_travaillé, répétitions, série, volume, équipement, lieu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, fatigue, douleur, charge, account_id, muscle_travaillé, répétitions, série, volume_total, équipement, lieu))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, fatigue, douleur, charge, account_id, muscle_travaillé, répétitions, série, volume, équipement, lieu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, fatigue, douleur, charge, account_id, muscle_travaillé, répétitions, série, volume_total, équipement, lieu))
            con.commit()
            CTkMessagebox(
                title="Succès",
                message="Votre activité a bien été enregistrée !",
                icon="check"
            )
            app.after(1500, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, username, password)])
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de l'ajout de votre activité.",
                icon="cancel"
            )
            return
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendue s'est produite, veuillez réessayer.",
                icon="cancel"
            )
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_fooball(account_id, username, password):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_type = ["Entraînement", "Match", "Tournoi", "City"]

    cadre_principal = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_principal.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_principal, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w", command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame1 = ctk.CTkFrame(master=cadre_principal, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Football")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=cadre_principal, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)
    type_entry = ctk.CTkComboBox(master=frame_champs1, values=Options_type, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    type_entry.pack(side="left", padx=10)
    type_entry.set("Type de séance de foot")

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_=1, to=10, number_of_steps=9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=10)
    humeur_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Humeur d'après match", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    humeur_entry.pack(side="left", padx=(75, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    climat_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_climat.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    climat_entry.pack(side="left", padx=10)
    climat_entry.set("Climat à l'entraînement")

    but_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre de but", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    but_entry.pack(side="left", padx=10)
    passe_d_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Nombre de passe décisive", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    passe_d_entry.pack(side="left", padx=10)

    def enregistrer():
        humeur = humeur_entry.get().strip()
        passe_décisive1 = passe_d_entry.get().strip()
        type_de_séances = type_entry.get().strip()
        if passe_décisive1:
            try:
                passe_décisive = int(passe_décisive1)
                if passe_décisive < 0:
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Erreur", 
                    message="Nombre de passe décisive invalide (entier positif requis)", 
                    icon="cancel"
                )
                return
        else:
            passe_décisive = None
        but1 = but_entry.get().strip()
        if but1:
            try:
                but = int(but1)
                if but < 0:
                    raise ValueError
            except ValueError:
                CTkMessagebox(
                    title="Erreur", 
                    message="Nombre de but invalide (entier positif requis)", 
                    icon="cancel"
                )
                return
        else:
            but = None
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
        
        sport = "Football"
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
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erreur", 
                message="RPE invalide (1-10 requis)", 
                icon="cancel"
            )
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de fatigue invalide", 
                icon="cancel"
            )
            return
        if douleur is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de douleur invalide", 
                icon="cancel"
            )
            return
        if climat is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de climat invalide", 
                icon="cancel"
            )
            return
        if type_de_séances is None:
            CTkMessagebox(
                title="Erreur", 
                message="Type de séance de foot invalide", 
                icon="cancel"
            )
            return

        if type_de_séances == "Entraînement":  
            coef_foot = 1        
        elif type_de_séances == "Match":
            coef_foot = 1.2
        elif type_de_séances == "City":
            coef_foot = 0.9
        else:  
            coef_foot = 1.4
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge_av = score_fatigue * charge_c
        charge =  charge_av*coef_foot
        try:
            curseur.execute("""INSERT INTO Activité_football (date_activité, sport, durée, rpe, fatigue, douleur, climat, charge, account_id, humeur, but, passe_décisive, type_de_séances) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, fatigue, douleur, climat, charge, account_id, humeur, but, passe_décisive, type_de_séances))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, fatigue, douleur, climat, charge, account_id, humeur, but, passe_décisive, type_de_séances) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, fatigue, douleur, climat, charge, account_id, humeur, but, passe_décisive, type_de_séances))
            con.commit()
            CTkMessagebox(
                title="Succès",
                message="Votre activité a bien été enregistrée !",
                icon="check"
            )
            app.after(1500, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, username, password)])
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de l'ajout de votre activité.",
                icon="cancel"
            )
            return
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendue s'est produite, veuillez réessayer.",
                icon="cancel"
            )
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_extérieur(account_id, username, password):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}

    cadre_principal = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_principal.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_principal, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w", command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame1 = ctk.CTkFrame(master=cadre_principal, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Extérieur")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=cadre_principal, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=cadre_principal, fg_color="transparent")
    frame_champs5.pack(padx=10, pady=(40, 10))

    app.bind('<Return>', lambda event: enregistrer())

    date_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=10)
    sport_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Sport", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="left", padx=10)
    duree_entry = ctk.CTkEntry(master=frame_champs1, placeholder_text="Durée (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    duree_entry.pack(side="left", padx=10)

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_=1, to=10, number_of_steps=9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=10)
    nom_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Nom", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    nom_entry.pack(side="left", padx=(75, 10))

    fatigue_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_fatigue.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    fatigue_entry.pack(side="left", padx=10)
    fatigue_entry.set("Fatigue post-entraînement")

    douleur_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_douleur.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    douleur_entry.pack(side="left", padx=10)
    douleur_entry.set("Douleur post-entraînement")
    climat_entry = ctk.CTkComboBox(master=frame_champs3, values=list(Options_climat.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    climat_entry.pack(side="left", padx=10)
    climat_entry.set("Climat à l'entraînement")

    distance_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(side="left", padx=10)
    denivele_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Dénivelé (m)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    denivele_entry.pack(side="left", padx=10)

    def enregistrer():
        nom = nom_entry.get().strip()
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
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erreur", 
                message="RPE invalide (1-10 requis)", 
                icon="cancel"
            )
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de fatigue invalide", 
                icon="cancel"
            )
            return
        if douleur is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de douleur invalide", 
                icon="cancel"
            )
            return
        if climat is None:
            CTkMessagebox(
                title="Erreur", 
                message="Valeur de climat invalide", 
                icon="cancel"
            )
            return
        distance = None
        denivele = None
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
                    return
        except ValueError:
            CTkMessagebox(
                title="Erreur", 
                message="Distance invalide (nombre positif requis)", 
                icon="cancel"
            )
            return
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
                    return       
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
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_c
        try:
            curseur.execute("""INSERT INTO Activité_extérieur (date_activité, sport, durée, distance, rpe, fatigue, douleur, climat, charge, account_id, nom, dénivelé) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, distance, rpe, fatigue, douleur, climat, charge, account_id, nom, denivele))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, distance, rpe, fatigue, douleur, climat, charge, account_id, nom, dénivelé) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, distance, rpe, fatigue, douleur, climat, charge, account_id, nom, denivele))
            con.commit()
            CTkMessagebox(
                title="Succès",
                message="Votre activité a bien été enregistrée !",
                icon="check"
            )
            app.after(1500, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
        except sqlite3.Error as e:
            CTkMessagebox(
                title="Erreur",
                message="Erreur de base de données lors de l'ajout de votre activité.",
                icon="cancel"
            )
            return
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendue s'est produite, veuillez réessayer.",
                icon="cancel"
            )
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def imc(account_id, username, password):
    cadre_imc = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_imc.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_imc, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_imc, fg_color="transparent")
    navbar.pack(pady=20)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Prédicteur de performance":
            app.after(0, lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
        elif choix == "Zones cardiaque":
            app.after(0, lambda: [vider_fenetre(app), zone_fc(account_id, username, password)])
        elif choix == "Calculateur IMC":
            app.after(0, lambda: [vider_fenetre(app), imc(account_id, username, password)])
        elif choix == "Estimation VMA":
            app.after(0, lambda: [vider_fenetre(app), VMA(account_id, username, password)])
        elif choix == "Estimation VO2max":
            app.after(0, lambda: [vider_fenetre(app), VO2MAX(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, 
                                            values=["Prédicteur de performance", "Zones cardiaque", "Calculateur IMC", "Estimation VMA", "Estimation VO2max"],
                                            height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                            corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                            fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                            text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Calculateur IMC")

    carte_connexion = ctk.CTkFrame(master=cadre_imc, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_imc(account_id, username, password))
    poids_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Poids (kg)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    poids_entry.pack(pady=(11, 5), padx=10)
    taille_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Taille (cm)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    taille_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_imc, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre temps de course\n directement sur votre appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
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
    button_check = ctk.CTkButton(master=cadre_imc, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: calcul_imc(account_id, username, password))
    button_check.pack(padx=10, pady=10)

def VO2MAX(account_id, username, password):
    cadre_vo2Max = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_vo2Max.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_vo2Max, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_vo2Max, fg_color="transparent")
    navbar.pack(pady=20)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Prédicteur de performance":
            app.after(0, lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
        elif choix == "Zones cardiaque":
            app.after(0, lambda: [vider_fenetre(app), zone_fc(account_id, username, password)])
        elif choix == "Calculateur IMC":
            app.after(0, lambda: [vider_fenetre(app), imc(account_id, username, password)])
        elif choix == "Estimation VMA":
            app.after(0, lambda: [vider_fenetre(app), VMA(account_id, username, password)])
        elif choix == "Estimation VO2max":
            app.after(0, lambda: [vider_fenetre(app), VO2MAX(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, 
                                            values=["Prédicteur de performance", "Zones cardiaque", "Calculateur IMC", "Estimation VMA", "Estimation VO2max"],
                                            height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                            corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                            fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                            text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Estimation VO2max")

    carte_connexion = ctk.CTkFrame(master=cadre_vo2Max, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_VO2MAX(account_id, username, password))
    vma_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="VMA", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vma_entry.pack(pady=(11, 5), padx=10)

    combo_genre = ctk.CTkComboBox(master=carte_connexion, values=["Homme", "Femme"], font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    combo_genre.pack(pady=5, padx=10)
    combo_genre.set("Sélectionnez votre genre")

    age_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Âge", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    age_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_vo2Max, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre temps de course\n directement sur votre appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

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

    button_check = ctk.CTkButton(master=cadre_vo2Max, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_VO2MAX(account_id, username, password))
    button_check.pack(padx=10, pady=20)

def VMA(account_id, username, password):
    cadre_vo2Max = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_vo2Max.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_vo2Max, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_vo2Max, fg_color="transparent")
    navbar.pack(pady=20)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Prédicteur de performance":
            app.after(0, lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
        elif choix == "Zones cardiaque":
            app.after(0, lambda: [vider_fenetre(app), zone_fc(account_id, username, password)])
        elif choix == "Calculateur IMC":
            app.after(0, lambda: [vider_fenetre(app), imc(account_id, username, password)])
        elif choix == "Estimation VMA":
            app.after(0, lambda: [vider_fenetre(app), VMA(account_id, username, password)])
        elif choix == "Estimation VO2max":
            app.after(0, lambda: [vider_fenetre(app), VO2MAX(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, 
                                            values=["Prédicteur de performance", "Zones cardiaque", "Calculateur IMC", "Estimation VMA", "Estimation VO2max"],
                                            height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                            corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                            fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                            text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Estimation VMA")

    Info = ctk.CTkLabel(master=cadre_vo2Max ,text="Pour une estimation plus précise, utilisez la distance parcourue à fond en 6 minutes.", font=(font_secondaire, taille2))
    Info.pack(padx=50, pady=10)

    carte_connexion = ctk.CTkFrame(master=cadre_vo2Max, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_VMA(account_id, username, password))
    distance_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(pady=(11, 5), padx=10)
    temps_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Temps (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    temps_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_vo2Max, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre temps de course\n directement sur votre appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

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
    button_check = ctk.CTkButton(master=cadre_vo2Max, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: calcul_VMA(account_id, username, password))
    button_check.pack(padx=10, pady=10)

def zone_fc(account_id, username, password):
    cadre_fc = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_fc.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_fc, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_fc, fg_color="transparent")
    navbar.pack(pady=20)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Prédicteur de performance":
            app.after(0, lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
        elif choix == "Zones cardiaque":
            app.after(0, lambda: [vider_fenetre(app), zone_fc(account_id, username, password)])
        elif choix == "Calculateur IMC":
            app.after(0, lambda: [vider_fenetre(app), imc(account_id, username, password)])
        elif choix == "Estimation VMA":
            app.after(0, lambda: [vider_fenetre(app), VMA(account_id, username, password)])
        elif choix == "Estimation VO2max":
            app.after(0, lambda: [vider_fenetre(app), VO2MAX(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, 
                                            values=["Prédicteur de performance", "Zones cardiaque", "Calculateur IMC", "Estimation VMA", "Estimation VO2max"],
                                            height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                            corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                            fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                            text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Zones cardiaque")

    carte_connexion = ctk.CTkFrame(master=cadre_fc, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_zone(account_id, username, password))
    age_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Âge", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    age_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_fc, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre temps de course\n directement sur votre appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

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
    button_check = ctk.CTkButton(master=cadre_fc, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_zone(account_id, username, password))
    button_check.pack(padx=10, pady=10)

def predicteur_temps(account_id, username, password):
    cadre_fc = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_fc.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_fc, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_fc, fg_color="transparent")
    navbar.pack(pady=20) 

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Prédicteur de performance":
            app.after(0, lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
        elif choix == "Zones cardiaque":
            app.after(0, lambda: [vider_fenetre(app), zone_fc(account_id, username, password)])
        elif choix == "Calculateur IMC":
            app.after(0, lambda: [vider_fenetre(app), imc(account_id, username, password)])
        elif choix == "Estimation VMA":
            app.after(0, lambda: [vider_fenetre(app), VMA(account_id, username, password)])
        elif choix == "Estimation VO2max":
            app.after(0, lambda: [vider_fenetre(app), VO2MAX(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, 
                                            values=["Prédicteur de performance", "Zones cardiaque", "Calculateur IMC", "Estimation VMA", "Estimation VO2max"],
                                            height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                            corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                            fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                            text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Prédicteur de performance")

    Info = ctk.CTkLabel(master=cadre_fc ,text="N'oubliez pas que cette prédiction est une estimation basée sur la\nthéorie"\
                         " et peut varier en fonction de nombreux facteurs\nle jour de la course !", font=(font_secondaire, taille2),
                         text_color=couleur_text)
    Info.pack(padx=50, pady=10)

    carte_connexion = ctk.CTkFrame(master=cadre_fc, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_temps(account_id, username, password))
    vma_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="VMA", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vma_entry.pack(pady=(11, 5), padx=10)
    distance_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=cadre_fc, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Votre confidentialité est notre priorité : nous calculons votre temps de course\n directement sur votre appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

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
    button_check = ctk.CTkButton(master=cadre_fc, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_temps(account_id, username, password))
    button_check.pack(padx=10, pady=10)

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
    app.after(0, lambda: [vider_fenetre(app), modifier_statut(account_id, username, password)])

def arreter_pause(account_id, username, password):
    curseur.execute("""UPDATE Pauses SET date_fin = date('now')WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    con.commit()
    CTkMessagebox(
        title="Enregistré",
        message="Reprise d'activité enregistrée !",
        icon="check"
    )
    app.after(0, lambda: [vider_fenetre(app), modifier_statut(account_id, username, password)])

def signaler_bug(account_id, username, password):
    cadre_avis = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_avis.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_avis, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_avis ,text="Signaler un bug", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(master=cadre_avis ,text="📣 Nous vous remercions pour votre contribution au développement de Sprintia." \
    "\nPour que le développeur puisse bien comprendre le bug, il faudrait détailler\nun maximum le bug que vous avez rencontré.", 
    font=(font_principale, taille2))
    info.pack(padx=50, pady=(20, 10))

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(master=cadre_avis, width=700, height=300, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille3),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(pady=10, padx=10)
    avis_entry.insert("0.0", "Description du bug :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if not avis:
            CTkMessagebox(
                title="Avis vide",
                message="Veuillez remplir le champs description de bug !",
                icon="cancel"
            )
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Rapport de bug"
        body = f"Nom d'utilisateur: {username}\n\nMessage de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            webbrowser.open(mailto_link)
            CTkMessagebox(
                title="Première étape terminée",
                message="Votre application mail par défaut s'est ouverte.\n" \
                "Veuillez simplement cliquer sur 'Envoyer' pour finaliser l'envoi de votre avis.",
                icon="info"
            )
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message=f"Impossible d'ouvrir votre application mail.\nVeuillez vérifier que vous avez une application pour gérer vos mails.",
                icon="cancel"
            )
    frame_boutons = ctk.CTkFrame(master=cadre_avis, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def proposer_fonction(account_id, username, password):
    cadre_avis = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_avis.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_avis, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_avis ,text="Proposer une fonction", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(master=cadre_avis ,text="📣 Nous vous remercions pour votre contribution au développement de Sprintia." \
                "\nPour que le développeur puisse bien comprendre ta demande, il faudrait détailler\nun maximum ton idée de fonctionnalité",
                font=(font_principale, taille2))
    info.pack(padx=50, pady=(20, 10))

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(master=cadre_avis, width=700, height=300, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille3),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(pady=10, padx=10)
    avis_entry.insert("0.0", "Description de votre fonctionnalité :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if not avis:
            CTkMessagebox(
                title="Avis vide",
                message="Veuillez remplir le champs fonctionnalité !",
                icon="cancel"
            )
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Proposition de nouvelle fonctionnalité"
        body = f"Nom d'utilisateur: {username}\n\nMessage de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            webbrowser.open(mailto_link)
            CTkMessagebox(
                title="Première étape terminée",
                message="Votre application mail par défaut s'est ouverte.\n" \
                "Veuillez simplement cliquer sur 'Envoyer' pour finaliser l'envoi de votre avis.",
                icon="info"
            )
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message=f"Impossible d'ouvrir votre application mail.\nVeuillez vérifier que vous avez une application pour gérer vos mails.",
                icon="cancel"
            )
    frame_boutons = ctk.CTkFrame(master=cadre_avis, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def avis (account_id, username, password):
    cadre_avis = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_avis.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_avis, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_avis ,text="Rédiger un avis", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(master=cadre_avis ,text="📣 Nous vous remercions pour votre contribution au développement de Sprintia.", 
                        font=(font_principale, taille2))
    info.pack(padx=50, pady=(20, 10))

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(master=cadre_avis, width=700, height=300, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille3),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(pady=10, padx=10)
    avis_entry.insert("0.0", "Votre avis :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if not avis:
            CTkMessagebox(
                title="Avis vide",
                message="Veuillez remplir le champs avis !",
                icon="cancel"
            )
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Avis sur Sprintia"
        body = f"Nom d'utilisateur: {username}\n\nMessage de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            webbrowser.open(mailto_link)
            CTkMessagebox(
                title="Première étape terminée",
                message="Votre application mail par défaut s'est ouverte.\n" \
                "Veuillez simplement cliquer sur 'Envoyer' pour finaliser l'envoi de votre avis.",
                icon="info"
            )
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message=f"Impossible d'ouvrir votre application mail.\nVeuillez vérifier que vous avez une application pour gérer vos mails.",
                icon="cancel"
            )

    frame_boutons = ctk.CTkFrame(master=cadre_avis, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def modifier_statut(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_statut.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_statut, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_statut ,text="Mettre en pause les analyses", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=50, pady=20)
    info = ctk.CTkLabel(master=cadre_statut ,text="Si vous avez besoin de souffler, ou que vous vous êtes blessé, vous pouvez\nmettre en pause les" \
    "analyses pour vous reposer.", font=(font_principale, taille2))
    info.pack(padx=50, pady=(25, 10))

    frame = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    curseur.execute("SELECT type FROM Pauses WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    result = curseur.fetchall()
    if result == []:
        info_statut = ctk.CTkLabel(master=frame, text="Votre statut d'entraînement actuel : Actif", font=(font_principale, taille2))
        info_statut.pack(padx=0, pady=10)
    elif result == [('vacances',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Votre statut d'entraînement actuel: Vacances", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == [('blessure',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Votre statut d'entraînement actuel : Blessure", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    else:
        CTkMessagebox(
            title="Erreur",
            message="Statut inconnu ou incohérent.",
            icon="cancel"
        )
    options = {"Vacances": "Vacances", "Blessure": "Blessure", "Reprendre les analyses": "Reprendre"}
    combo_statut = ctk.CTkComboBox(master=frame, values=list(options.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
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
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: enregistrer_activité(account_id, username, password))
    button_check.pack(side="left", padx=5, pady=10)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=10)

def modifier_password(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_statut.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_statut, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    navbar = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    navbar.pack(pady=20)
    frame2 = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")        
    frame2.pack(pady=(10, 20))
    carte = ctk.CTkFrame(master=cadre_statut, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)        
    carte.pack(pady=(10, 20))

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Mon compte":
            app.after(0, lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
        elif choix == "Modifier":
            app.after(0, lambda: [vider_fenetre(app), modifier_compte(account_id, username, password)])
        elif choix == "Supprimer mon compte":
            app.after(0, lambda: [vider_fenetre(app), supprimer_compte(account_id, username, password)])
        elif choix == "Mots de passe oublié":
            app.after(0, lambda: [vider_fenetre(app), modifier_password(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Mon compte", "Modifier", "Supprimer mon compte", "Mots de passe oublié"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Mots de passe oublié")
    button_back = ctk.CTkButton(master=navbar, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_back.pack(side="left", padx=10)

    info = ctk.CTkLabel(master=frame2 ,text="Mots de passe oublié ? Pas de panique, remplissez le formulaire ci-dessus et votre mots de passe sera modifié",
                         font=(font_secondaire, taille2), wraplength=800)
    info.pack(padx=50)

    app.bind('<Return>', lambda event: new_username(account_id, username, password))
    password_entry = ctk.CTkEntry(master=carte, placeholder_text="Nouveau mots de passe", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=370)
    password_entry.pack(pady=(12, 5), padx=11)
    password_entry2 = ctk.CTkEntry(master=carte, placeholder_text="Confirmez votre nouveau mots de passe", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=370)
    password_entry2.pack(pady=(5, 12), padx=11)
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
    button_check = ctk.CTkButton(master=cadre_statut, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: new_username(account_id, username, password))
    button_check.pack(padx=10, pady=15)

def modifier_compte(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_statut.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_statut, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    navbar = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    navbar.pack(pady=20)
    
    info_pack = ctk.CTkFrame(master=cadre_statut, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    info_pack.pack(pady=10)

    frame_username = ctk.CTkFrame(master=info_pack, fg_color="transparent")        
    frame_username.pack(padx=12, pady=(10, 5))
    frame_sport = ctk.CTkFrame(master=info_pack, fg_color="transparent")        
    frame_sport.pack(padx=12, pady=5)
    frame_bio = ctk.CTkFrame(master=info_pack, fg_color="transparent")        
    frame_bio.pack(padx=12, pady=(5, 10))

    enregistrer = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")        
    enregistrer.pack(pady=20)

    curseur.execute("SELECT sport FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchall()
    sport = result[0][0]
    curseur.execute("SELECT bio FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchall()
    bio = result[0][0]
    curseur.execute("SELECT username FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchall()
    username = result[0][0]

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Mon compte":
            app.after(0, lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
        elif choix == "Modifier":
            app.after(0, lambda: [vider_fenetre(app), modifier_compte(account_id, username, password)])
        elif choix == "Supprimer mon compte":
            app.after(0, lambda: [vider_fenetre(app), supprimer_compte(account_id, username, password)])
        elif choix == "Mots de passe oublié":
            app.after(0, lambda: [vider_fenetre(app), modifier_password(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Mon compte", "Modifier", "Supprimer mon compte", "Mots de passe oublié"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Modifier")
    button_back = ctk.CTkButton(master=navbar, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_back.pack(side="left", padx=10)

    app.bind('<Return>', lambda event: enregistré())
    LABEL_WIDTH = 250
    pseudo_label = ctk.CTkLabel(master=frame_username, text="Votre pseudo : ", font=(font_secondaire, taille2), text_color=couleur1,
                                width=LABEL_WIDTH)
    pseudo_label.pack(side="left")
    pseudo_entry = ctk.CTkEntry(master=frame_username, placeholder_text=f"{username}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    pseudo_entry.pack(side="left", padx=(0, 10), pady=(12,0))

    sport_label = ctk.CTkLabel(master=frame_sport, text="Votre sport favoris : ", font=(font_secondaire, taille2), text_color=couleur1,
                               width=LABEL_WIDTH)
    sport_label.pack(side="left")
    sport_favoris_entry = ctk.CTkEntry(master=frame_sport, placeholder_text=f"{sport}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_favoris_entry.pack(side="left", padx=(0, 12))

    bio_label = ctk.CTkLabel(master=frame_bio, text="Votre bio : ", font=(font_secondaire, taille2), text_color=couleur1,
                              width=LABEL_WIDTH)
    bio_label.pack(side="left")
    bio_entry = ctk.CTkEntry(master=frame_bio, placeholder_text=f"{bio}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    bio_entry.pack(side="left", padx=(0, 10), pady=(0,11))

    def enregistré():
        new_username = pseudo_entry.get().strip()
        new_sport = sport_favoris_entry.get().strip()
        new_bio = bio_entry.get().strip()
        if not new_username:
            new_username = username
        if not new_sport:
            new_sport = sport
        if not new_bio:
            new_bio = bio
        try:
            con.execute("UPDATE Account SET username = ?, sport = ?, bio = ? WHERE id = ?", (new_username, new_sport, new_bio, account_id))
            con.commit()
            CTkMessagebox(
                title="Opération réussi",
                message="Votre compte a été mis à jour avec succès.",
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
                message="Erreur de base de données lors de la mise à jour de votre compte.",
                icon="cancel"
            )
        except Exception as e:
            CTkMessagebox(
                title="Erreur",
                message="Une erreur inattendu s'est produite, veuillez réessayer.",
                icon="cancel"
            )
    button_enregistrer = ctk.CTkButton(master=enregistrer, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                         command=lambda: enregistré())
    button_enregistrer.pack(side="left", padx=10)

def supprimer_compte(account_id, username, password):
    cadre_statut = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_statut.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_statut, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    navbar = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    navbar.pack(pady=20)
    info = ctk.CTkFrame(master=cadre_statut, fg_color="transparent")
    info.pack()
    carte = ctk.CTkFrame(master=cadre_statut, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)        
    carte.pack(pady=(10, 20))

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Mon compte":
            app.after(0, lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
        elif choix == "Modifier":
            app.after(0, lambda: [vider_fenetre(app), modifier_compte(account_id, username, password)])
        elif choix == "Supprimer mon compte":
            app.after(0, lambda: [vider_fenetre(app), supprimer_compte(account_id, username, password)])
        elif choix == "Mots de passe oublié":
            app.after(0, lambda: [vider_fenetre(app), modifier_password(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Mon compte", "Modifier", "Supprimer mon compte", "Mots de passe oublié"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Supprimer mon compte")
    button_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_retour.pack(side="left", padx=10)

    info = ctk.CTkLabel(master=info ,text="Ton compte est sur le point d'être supprimé. Ça veut dire que toutes tes données" \
    "et ton accès à nos services seront perdus, et il n'y aura pas de retour en arrière possible.", font=(font_secondaire, taille2), wraplength=800)
    info.pack(padx=50, pady=10)
    info2 = ctk.CTkLabel(master=carte ,text="Êtes-vous vraiment certain de vouloir continuer ?", font=(font_principale, taille2),
                         text_color=couleur1)
    info2.pack(padx=50, pady=10) 

    options_suppr = {"Oui": "oui", "Non" : "non"}

    options = ctk.CTkComboBox(master=carte, values=list(options_suppr.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    options.pack(pady=10)
    options.set("Séléctionnez Oui ou Non")

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
    button_check = ctk.CTkButton(master=cadre_statut, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: valider(account_id, username, password))
    button_check.pack(padx=10, pady=15)

def ajouter_compétition(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame_tout = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack()
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(pady=(10, 5), padx=10)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(pady=(5, 5), padx=10)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(pady=(5, 10), padx=10)
    frame4 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame4.pack(pady=20)

    Titre = ctk.CTkLabel(master=frame ,text="Ajouter une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20, side="left")

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire"]
    app.bind('<Return>', lambda event: sql_ajouté(account_id, username, password))

    date_entry = ctk.CTkEntry(master=frame1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=(0, 5))    
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text="Sport", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="right", padx=(5, 0))

    nom_entry = ctk.CTkEntry(master=frame2, placeholder_text="Nom de la compétition", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    nom_entry.pack(side="left", padx=(0, 5))
    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text="Objectif", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    objectif_entry.pack(side="right", padx=(5, 0))

    lieu_entry = ctk.CTkEntry(master=frame3, placeholder_text="Lieu (optionnel)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    lieu_entry.pack(side="left", padx=(0, 5))
    priorite_entry = ctk.CTkComboBox(master=frame3, values=option, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    priorite_entry.pack(side="right", padx=(5, 0))
    priorite_entry.set("Priorité")

    def sql_ajouté(account_id, username, password):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip()
        date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
        date = date_conversion.strftime('%Y-%m-%d')
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu = lieu_entry.get().strip()
        priorité = priorite_entry.get().strip()

        if not nom or not date_str or not sport or not objectif or not priorité:
            CTkMessagebox(
                title="Erreur",
                message="Veuillez remplir tous les champs",
                icon="cancel"
            )
        else:
            try:
                curseur.execute("INSERT INTO Compétition (account_id, nom, date, sport, objectif, lieu, priorité) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, nom, date, sport, objectif, lieu, priorité))
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
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: sql_ajouté(account_id, username, password))
    button_enregistrer.pack(side="left", padx=5)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    button_back.pack(side="left", padx=5)

def supprimer_compétition(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_activité ,text="Supprimer une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)

    app.bind('<Return>', lambda event: supression(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de la compétition à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=350)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, nom, date, lieu FROM Compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Sport", "Nom", "Date", "Lieu"]
        for col_idx, header_text in enumerate(headers):
            label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
            label.grid(row=0, column=col_idx, padx=6, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 3:
                        date = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=("Arial", 14))
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
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id, username, password))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def toute_compétition(account_id, username, password):
    cadre_historique = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_historique.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_historique, text="Toutes les compétitions", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=(25, 10))

    boite3 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT nom, date, sport, objectif, lieu FROM Compétition WHERE account_id = ? ORDER BY date ASC", (account_id,))
            compétition_result = curseur.fetchall()

            headers = ["Nom", "Date", "Sport", "Objectif", "Lieu"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if compétition_result:
                for row_idx, activite in enumerate(compétition_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition n'a été enregistrée.", font=(font_principale, taille3))
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
    button_retour = ctk.CTkButton(master=cadre_historique, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    button_retour.pack(padx=10, pady=20)

def compétition(account_id, username, password):
    cadre_historique = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_historique.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_historique, fg_color="transparent")
    navbar.pack(pady=20)

    frame_boutons = ctk.CTkFrame(master=cadre_historique, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    boite3 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), performance(account_id, username, password)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Compétition")
    button_autre = ctk.CTkButton(master=navbar, text="🔚 Toutes les compétitions", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    width=260,
                                    command=lambda: [vider_fenetre(app), toute_compétition(account_id, username, password)])
    button_autre.pack(side="left", padx=10)

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), ajouter_compétition(account_id, username, password)])
    button_ajouter.pack(side="left", padx=2)
    button_delete = ctk.CTkButton(master=frame_boutons, text="🗑️  Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), supprimer_compétition(account_id, username, password)])
    button_delete.pack_forget()
    try:
            curseur.execute("SELECT nom, date, sport, objectif, lieu, priorité FROM Compétition WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
            compétition_result = curseur.fetchall()

            headers = ["Nom", "Date", "Sport", "Objectif", "Lieu", "Priorité"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if compétition_result:
                for row_idx, activite in enumerate(compétition_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
                button_delete.pack(side="left", padx=2)
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistrée.", font=(font_principale, taille1))
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
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    frame = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame_tout = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack()
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(pady=(10, 5), padx=10)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(pady=(5, 5), padx=10)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(pady=(5, 10), padx=10)
    frame4 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame4.pack(pady=20)

    options_statut = {"En cours": "en cours", "Atteint" : "atteint", "Non-atteint" : "non-atteint"}
    options_niveau = {"Débutant": "débutant", "Fondations": "fondations", "Intermédiaire" : "intermédiaire", "Avancé": "avancé", "Expert": "expert", "Maîtrise": "maîtrise"}
    Titre = ctk.CTkLabel(master=frame ,text="Ajouter un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    app.bind('<Return>', lambda event: sql_ajouté(account_id, username, password))
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text="Sport", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="left", padx=(0, 5))
    date_entry = ctk.CTkEntry(master=frame1, placeholder_text="Date (JJ-MM-AAAA)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="right", padx=(5, 0))

    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text="Objectif", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    objectif_entry.pack(side="left", padx=(0, 5))
    fréquence_entry = ctk.CTkEntry(master=frame2, placeholder_text="Fréquence (ex: 2 séances/semaine)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    fréquence_entry.pack(side="right", padx=(5, 0))

    niveau_entry = ctk.CTkComboBox(master=frame3, values=list(options_niveau.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    niveau_entry.pack(side="left", padx=(0, 5))
    niveau_entry.set("Niveau actuel")
    statut_entry = ctk.CTkComboBox(master=frame3, values=list(options_statut.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    statut_entry.pack(side="right", padx=(5, 0))
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
                message="Veuillez remplir tous les champs",
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
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                        command=lambda: sql_ajouté(account_id, username, password))
    button_enregistrer.pack(side="left", padx=5)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_back.pack(side="left", padx=5)

def modifier_niveau_final(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)       
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_activité ,text="Ajouter niveau final", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)
    app.bind('<Return>', lambda event: valider(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif à modifier", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=5)

    options = ["Débutant", "Fondations", "Intermédiaire", "Avancé", "Expert", "Maîtrise"]
    niveau_final = ctk.CTkComboBox(master=frame1, values=options, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    niveau_final.pack(pady=10, side="left", padx=5)
    niveau_final.set("Niveau final")

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, date, niveau_début, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Sport", "Date", "Niveau au début", "Statut"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=6, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
                for row_idx, activite in enumerate(result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 2:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def valider(account_id, username, password):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in result]

                if choix_id_saisi in ids_objectifs_disponibles:
                    fin_niveau = niveau_final.get().strip().lower()
                    if fin_niveau in ["débutant", "fondations", "intermédiaire", "avancé", "expert", "maîtrise"]:
                        objectif_id_db = choix_id_saisi
                        curseur.execute("UPDATE Objectif SET niveau_fin = ? WHERE id = ? AND account_id = ?", (fin_niveau, objectif_id_db, account_id))
                        con.commit()
                        CTkMessagebox(
                            title="Opération réussie",
                            message="Objectif mis à jour avec succès.",
                            icon="check"
                        )
                        app.after(1500, lambda: [vider_fenetre(app), modifier_niveau_final(account_id, username, password)])
                    else:
                        CTkMessagebox(
                            title="Erreur",
                            message="Niveau final invalide. Veuillez réessayer",
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
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: valider(account_id, username, password))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def supprimer_objectif(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_activité ,text="Supprimer un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)

    app.bind('<Return>', lambda event: supression(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Sport", "Date", "Objectif", "Statut"]
        for col_idx, header_text in enumerate(headers):
            label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
            label.grid(row=0, column=col_idx, padx=6, pady=15, sticky="ew")
            tableau_frame.grid_columnconfigure(col_idx, weight=1)
        if result:
            for row_idx, activite in enumerate(result):
                for col_idx, data in enumerate(activite):
                    if col_idx == 2:
                        date = datetime.strptime(str(data), '%Y-%m-%d')
                        data = date.strftime('%d-%m-%Y')
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
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
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id, username, password))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def tout_objectif(account_id, username, password):
    cadre_historique = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_historique.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_historique, text="Tous les objectifs", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=(25, 10))

    boite3 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT sport, date, objectif, niveau_début, niveau_fin FROM Objectif WHERE account_id = ? ORDER BY date ASC", (account_id,))
            compétition_result = curseur.fetchall()

            headers = ["Sport", "Date", "Objectifs", "Level début", "Level fin"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if compétition_result:
                for row_idx, activite in enumerate(compétition_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif n'a été enregistré.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
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
    button_retour = ctk.CTkButton(master=cadre_historique, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_retour.pack(padx=10, pady=20)

def modifier_objectif(account_id, username, password):
    cadre_activité = ctk.CTkFrame(master=app, fg_color=couleur_fond)       
    cadre_activité.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_activité ,text="Changer le statut", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame1.pack(pady=10)
    app.bind('<Return>', lambda event: modification(account_id, username, password))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif à modifier", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=5)

    options = ["En cours", "Atteint", "Non atteint"]
    new_entry = ctk.CTkComboBox(master=frame1, values=options, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    new_entry.pack(pady=10, side="left", padx=5)
    new_entry.set("Statut de l'objectif")

    frame_boutons = ctk.CTkFrame(master=cadre_activité, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=cadre_activité, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["id", "Sport", "Date", "Objectif", "Statut"]

        for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=6, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

        if result:
                for row_idx, activite in enumerate(result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 2:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré", font=(font_principale, taille1))
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
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: modification(account_id, username, password))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
    button_retour.pack(side="left", padx=5, pady=20)

def objectifs(account_id, username, password):
    cadre_historique = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    cadre_historique.pack(fill="both", expand=True)
    
    boite1 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_historique, fg_color="transparent")
    navbar.pack(pady=20)

    frame_boutons = ctk.CTkFrame(master=cadre_historique, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    boite3 = ctk.CTkFrame(master=cadre_historique, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), performance(account_id, username, password)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id, username, password)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Objectif")
    button_autre = ctk.CTkButton(master=navbar, text="🔚 Tous les objectifs", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    width=260,
                                    command=lambda: [vider_fenetre(app), tout_objectif(account_id, username, password)])
    button_autre.pack(side="left", padx=10)

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), ajouter_objectif(account_id, username, password)])
    button_ajouter.pack(side="left", padx=2)
    button_plus = ctk.CTkButton(master=frame_boutons, text="✏️  Changer le statut", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), modifier_objectif(account_id, username, password)])
    button_plus.pack_forget()
    button = ctk.CTkButton(master=frame_boutons, text="✏️  Changer niveau final", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), modifier_niveau_final(account_id, username, password)])
    button.pack_forget()
    button_delete = ctk.CTkButton(master=frame_boutons, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), supprimer_objectif(account_id, username, password)])
    button_delete.pack_forget()

    try:
            curseur.execute("SELECT sport, date, objectif, fréquence, niveau_début, niveau_fin, statut FROM Objectif WHERE account_id = ? AND date >= ? ORDER BY date ASC", (account_id, date_actuelle))
            objectif_result = curseur.fetchall()

            headers = ["Sport", "Date", "Objectif", "Fréquence", "Level début", "Level fin", "Statut"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=6, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)

            if objectif_result:
                for row_idx, activite in enumerate(objectif_result):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            date = datetime.strptime(data, '%Y-%m-%d')
                            data = date.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
                button_plus.pack(side="left", padx=2)
                button.pack(side="left", padx=2)
                button_delete.pack(side="left", padx=2)
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1))
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

def performance(account_id, username, password):
    cadre_performance = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_performance.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_performance, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    navbar = ctk.CTkFrame(master=cadre_performance, fg_color="transparent")
    navbar.pack(pady=20)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    fig = None
    canvas = None
    def fermer_graphique_pause(account_id, username, password):
        plt.close(fig)
        modifier_statut(account_id, username, password)
    def fermer_graphique(account_id, username, password):
        plt.close(fig)
        accueil(account_id, username, password)
    def fermer_graphique_mode():    
        nonlocal fig
        if fig:
            plt.close(fig)
            fig = None

    def mise_mode(choix):
        choix = mode_activité.get()
        if fig is None:
            if choix == "Charge d'entraînement":
                app.after(0, lambda: [vider_fenetre(app), performance(account_id, username, password)])
            elif choix == "Objectif":
                app.after(0, lambda: [vider_fenetre(app), objectifs(account_id, username, password)])
            elif choix == "Compétition":
                app.after(0, lambda: [vider_fenetre(app), compétition(account_id, username, password)])
        else:
            if choix == "Charge d'entraînement":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), performance(account_id, username, password)])
            elif choix == "Objectif":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), objectifs(account_id, username, password)])
            elif choix == "Compétition":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), compétition(account_id, username, password)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Charge d'entraînement")
    button_autre = ctk.CTkButton(master=navbar, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    command=lambda: [vider_fenetre(app), fermer_graphique_pause(account_id, username, password)])
    button_autre.pack(side="left", padx=10)

    charge_aigue = 0.0
    charge_chronique = 0.0
    try:
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
    parent_frame = ctk.CTkFrame(master=cadre_performance, fg_color="transparent")
    parent_frame.pack(fill="both", expand=True, pady=10)

    boite_charge_entraînement = ctk.CTkFrame(master=parent_frame, border_width=border2, border_color=couleur1, corner_radius=corner1,
                                             fg_color=couleur_fond)
    boite_charge_entraînement.pack(fill="both", expand=True, side="left", padx=10, pady=(0, 10))
    h1_boite_charge_entraînement = ctk.CTkFrame(master=boite_charge_entraînement, fg_color=couleur_fond)
    h1_boite_charge_entraînement.pack(pady=5)

    boite_analyse = ctk.CTkFrame(master=boite_charge_entraînement, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_analyse.pack(fill="both", expand=True, padx=15, pady=5)
    aigue = ctk.CTkFrame(master=boite_analyse, corner_radius=corner1, fg_color=couleur1)
    aigue.pack(fill="both", expand=True, padx=10, pady=(10, 5))
    chronique = ctk.CTkFrame(master=boite_analyse, corner_radius=corner1, fg_color=couleur1)
    chronique.pack(fill="both", expand=True, padx=10, pady=5)
    ratio_frame = ctk.CTkFrame(master=boite_analyse, corner_radius=corner1, fg_color=couleur1)
    ratio_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    boite_statut = ctk.CTkFrame(master=boite_charge_entraînement, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_statut.pack(fill="both", expand=True, padx=15, pady=(5, 15))
    h1_result_optimale = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    h1_result_optimale.pack(fill="both", expand=True, padx=10, pady=(10, 5))
    interprétation = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    interprétation.pack(fill="both", expand=True, padx=10, pady=5)
    conseil = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    conseil.pack(fill="both", expand=True, pady=(5, 10), padx=10)
    
    boite = ctk.CTkFrame(master=parent_frame, border_width=border2, border_color=couleur1, corner_radius=corner1,
                                             fg_color=couleur_fond)
    boite.pack(fill="both", expand=True, side="right", padx=10, pady=(0, 10))
    graphique = ctk.CTkFrame(master=boite, corner_radius=corner1, fg_color="white")
    graphique.pack(fill="both", expand=True, padx=15, pady=(15, 10))
    info = ctk.CTkFrame(master=boite, corner_radius=corner1, fg_color=couleur1)
    info.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    #rappel pour mettre le test a droite "anchor="w""
    h1 = ctk.CTkLabel(master=h1_boite_charge_entraînement, font=(font_secondaire, taille2), text="Analyse")
    h1.pack(padx=10, pady=(5, 0))
    result_analyse = ctk.CTkLabel(master=aigue, text=f"Charge aiguë (7 jours) : {charge_aigue:.1f}", font=(font_secondaire , taille3),
                                    width=300, wraplength=280)
    result_analyse.pack(fill="both", expand=True, padx=10, pady=10)
    result_analyse2 = ctk.CTkLabel(master=chronique, text=f"Charge chronique (28 jours) : {charge_chronique:.1f}", font=(font_principale, taille3),
                                    width=300, wraplength=280)
    result_analyse2.pack(fill="both", expand=True, padx=10, pady=10)
    pause = verifier_pause(account_id)
    if pause == "blessure":
        result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : actuellement en pause", font=(font_principale, taille3),
                        width=300, wraplength=280)
        result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="⛑️ Mode blessure : suivi désactivé", font=(font_principale, taille3),
                                        width=300, wraplength=280, text_color="#c60000")
        catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)           
        interpretation_statut = ctk.CTkLabel(master=interprétation, text="Vous êtes blessé pour le moment", font=(font_principale, taille3),
                                    width=300, wraplength=280)
        interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)              
        conseil_statut = ctk.CTkLabel(master=conseil, text="Prends le temps de laisser ton corps guérir afin de revenir plus fort.", font=(font_principale, taille3),
                                        width=300, wraplength=280)
        conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "vacances":
        result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : actuellement en pause", font=(font_principale, taille3),
                        width=300, wraplength=280)
        result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🏖️ Mode vacances : pas d'analyse !", font=(font_principale, taille3),
                                        width=300, wraplength=280, text_color="#6AC100")
        catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)          
        interpretation_statut = ctk.CTkLabel(master=interprétation, text="Vous êtes actuellement en vacances.", font=(font_principale, taille3),
                                    width=300, wraplength=280)
        interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)               
        conseil_statut = ctk.CTkLabel(master=conseil, text="Profite bien de cette pause pour te ressourcer et revenir plus motivé !", font=(font_principale, taille3),
                                        width=300, wraplength=280)
        conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
    else :
        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None
        if ratio is not None:
            result_analyse3 = ctk.CTkLabel(master=ratio_frame, text=f"Ratio : {ratio:.2f}", font=(font_principale, taille3),
                            width=300, wraplength=280)
            result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
            if ratio < 0.5: 
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🛌 Récupération active", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#75B7DD")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Charge très basse. Vous laissez votre corps vous reposer", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
                conseil_statut = ctk.CTkLabel(master=conseil, text="Fais une activité calme pour reprendre doucement en charge", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 0.5 <= ratio <= 0.8:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="😴 Sous-entraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#CBC500")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Vous êtes entrain de perdre en niveau", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                conseil_statut = ctk.CTkLabel(master=conseil, text="Vous pourriez augmenter légèrement l'intensité", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 0.8 <= ratio <= 0.9:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🔄 Maintien", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#00C073")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Charge adaptée pour conserver votre niveau", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                conseil_statut = ctk.CTkLabel(master=conseil, text="Allongez de 5 minutes vos séances pour progresser", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 0.9 <= ratio <= 1.1:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🟢 Progression optimale", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#00BA47")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Charge idéale pour améliorer vos performances", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                conseil_statut = ctk.CTkLabel(master=conseil, text="Continuez comme ça pour progresser !", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 1.1 < ratio <= 1.3:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="💪 Progression élévée", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#99c800")#3d71a5
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Vous progressez vite, attention aux blessures", 
                                                    font=(font_principale, taille3), width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
                conseil_statut = ctk.CTkLabel(master=conseil, text="Surveillez la fatigue de votre corps", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            else:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="⚠️ Surentraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#c60000")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Risque élevé de blessure", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
                conseil_statut = ctk.CTkLabel(master=conseil, text="Faites une pause de 2 à 3 jours pour éviter les blessures", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : 0.0", font=(font_principale, taille3),
                                                width=300, wraplength=280)
            result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
            catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🚫 Données insuffisantes", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#c60000")
            catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
            interpretation_statut = ctk.CTkLabel(master=interprétation, text="L'interprétation ne peut pas être déterminée.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
            interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
            conseil_statut = ctk.CTkLabel(master=conseil, text="Veuillez effectuer une séance de sport pour commencer les analyses.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
            conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)   
    try:   
        if data_pour_graphique:
            dates_graphique = [datetime.strptime(row[0], '%Y-%m-%d') for row in data_pour_graphique]
            charges_graphique = [row[1] for row in data_pour_graphique]

            fig, ax = plt.subplots(figsize=(12, 4))
            sns.lineplot(x=dates_graphique, y=charges_graphique, marker="o", color="black")

            ax.axhline(y=charge_chronique, color=couleur1, linestyle="-")
            ax.set_title("Évolution de la charge chronique")
            ax.set_xlabel("Date")
            ax.set_ylabel("Charge chronique")

            canvas = FigureCanvasTkAgg(fig, master=graphique)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True , pady=15, padx=15)
        else:
            not_data = ctk.CTkFrame(master=graphique, corner_radius=corner1, fg_color=couleur1)
            not_data.pack(expand=True, fill="both", padx=10, pady=10)
            pas_de_données = ctk.CTkLabel(master=not_data, text="Pas assez de données pour afficher un graphique.\nAjoutez quelques séances d'entraînement pour voir votre évolution !",
                                          font=(font_secondaire, taille2), wraplength=575)
            pas_de_données.pack(padx=15, pady=15)
            button_creer_activite = ctk.CTkButton(master=not_data, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                            command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
            button_creer_activite.pack(padx=(20, 2), pady=5)
    except Exception as e:
                CTkMessagebox(
                    title="Erreur",
                    message="Une erreur inattendu s'est produite, veuillez réessayer.",
                    icon="cancel"
                )
    titre_c_quoi = ctk.CTkLabel(master=info, text="C'est quoi la charge d'entraînement ?", font=(font_secondaire, taille2), wraplength=600)
    titre_c_quoi.pack(fill="both", expand=True, pady=(10, 10), padx=10)
    c_quoi = ctk.CTkLabel(master=info, 
                            text="La charge d'entraînement sert à optimiser ta progression sans te cramer, en trouvant le juste équilibre entre l'effort fourni et la récupération nécessaire. C'est ton meilleur ami pour éviter les blessures et planifier tes séances sportives intelligemment.",
                            font=(font_principale, taille3), wraplength=600)
    c_quoi.pack(fill="both", expand=True, padx=10, pady=(5, 10))

def mon_compte(account_id, username, password):
    cadre_compte = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_compte.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_compte, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    navbar = ctk.CTkFrame(master=cadre_compte, fg_color="transparent")
    navbar.pack(pady=20)
    info = ctk.CTkFrame(master=cadre_compte, corner_radius=corner1, fg_color=couleur1)
    info.pack(padx=15, pady=(0, 15))

    curseur.execute("SELECT sport FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchall()
    sport = result[0][0]
    curseur.execute("SELECT bio FROM Account WHERE id = ?", (account_id,))
    result = curseur.fetchall()
    bio = result[0][0]

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Mon compte":
            app.after(0, lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
        elif choix == "Modifier":
            app.after(0, lambda: [vider_fenetre(app), modifier_compte(account_id, username, password)])
        elif choix == "Supprimer mon compte":
            app.after(0, lambda: [vider_fenetre(app), supprimer_compte(account_id, username, password)])
        elif choix == "Mots de passe oublié":
            app.after(0, lambda: [vider_fenetre(app), modifier_password(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Mon compte", "Modifier", "Supprimer mon compte", "Mots de passe oublié"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Mon compte")
    button_back = ctk.CTkButton(master=navbar, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_back.pack(side="left", padx=10)

    info = ctk.CTkLabel(master=info ,text=
                        f"Votre ID : {account_id}\n\nVotre pseudo : {username}\n\nVotre sport favoris : {sport}\n\nVotre bio : {bio}", 
                        font=(font_principale, taille2), justify="left")
    info.pack(padx=20, pady=20)

def parametre(account_id, username, password):
    cadre_outils = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_outils.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_outils, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    Titre = ctk.CTkLabel(master=cadre_outils ,text="Paramètres", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=50, pady=20)

    frame_bouton = ctk.CTkFrame(master=cadre_outils, fg_color="transparent")
    frame_bouton.pack(pady=(20,0), padx=10)
    frame_bouton1 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton1.pack(pady=(20,0), padx=10)
    frame_bouton2 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton2.pack(pady=(10,0), padx=10)
    frame_bouton3 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton3.pack(pady=(10,20), padx=10)

    button_autre = ctk.CTkButton(master=frame_bouton1, text="👤 Mon Compte",
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3), fg_color=couleur2, 
                           hover_color=couleur2_hover, text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), mon_compte(account_id, username, password)])
    button_autre.pack(side="left" ,padx=10, pady=0)
    button_info = ctk.CTkButton(master=frame_bouton1, text="📢 À propos", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), a_propos(account_id, username, password)])
    button_info.pack(side="left", pady=0, padx=10)
    button_avis = ctk.CTkButton(master=frame_bouton2, text="🆕 Proposer une fonction", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), proposer_fonction(account_id, username, password)])
    button_avis.pack(side="left", pady=0, padx=10) 
    button_avis = ctk.CTkButton(master=frame_bouton2, text="🕷️  Signaler un bug", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), signaler_bug(account_id, username, password)])
    button_avis.pack(side="left", pady=0, padx=10) 
    button_avis = ctk.CTkButton(master=frame_bouton3, text="💬 Rédiger un avis", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), avis(account_id, username, password)])
    button_avis.pack(side="left", pady=0, padx=10)    
    button_deco = ctk.CTkButton(master=frame_bouton3, text="🚪Déconnexion", 
                            corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                            fg_color="#AC1724", hover_color="#8D1822",
                            command=lambda: [vider_fenetre(app), reglage_par_default()])
    button_deco.pack(side="left" ,padx=10, pady=0)

def accueil_intérieur(account_id, username, password):
    cadre_accueil = ctk.CTkFrame(master=app, fg_color=couleur_fond) 
    cadre_accueil.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    boite2 = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent", corner_radius=corner3)
    boite2.pack(side="top", fill="x", pady=20)
    topbar = ctk.CTkFrame(master=boite2, fg_color="transparent", corner_radius=corner3)
    topbar.pack(anchor="center")
    element_topbar = ctk.CTkFrame(master=topbar, fg_color="transparent")
    element_topbar.pack()

    boite_semi_header = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent")
    boite_semi_header.pack(side="top", pady=10)

    boite3 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color=couleur1, hover_color=couleur1_hover, width=button_width, anchor="w",
                                    command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    button_supprimer = ctk.CTkButton(master=element_topbar, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_activité(account_id, username, password, avoir_periode(combo_periode.get(), options_periode)))
    button_supprimer.pack(side="right", padx=2, pady=5)
    button_creer_activite = ctk.CTkButton(master=element_topbar, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
    button_creer_activite.pack(side="right", padx=(20, 2), pady=5)
    info = ctk.CTkLabel(master=element_topbar, text="Historique d'entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    info.pack(side="right", padx=20)
    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir": 9999}
    combo_periode = ctk.CTkComboBox(master=element_topbar, values=list(options_periode.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur2, button_color=couleur2, fg_color=couleur2,
                                    corner_radius=corner2, width=220, dropdown_fg_color=couleur2, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_periode.pack(side="right", padx=(10, 20), pady=5)
    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')
    
    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), accueil_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), accueil_football(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Intérieur")

    def mettre_a_jour_historique(selection):
        for widget in tableau_frame.winfo_children():
            widget.destroy()        
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute("SELECT sport, date_activité, durée, rpe, nom FROM Activité_intérieur WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            headers = ["Sport", "Date", "Durée", "RPE", "Nom"]
            for col_idx, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
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

def accueil_football(account_id, username, password):
    cadre_accueil = ctk.CTkFrame(master=app, fg_color=couleur_fond) 
    cadre_accueil.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    boite2 = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent", corner_radius=corner3)
    boite2.pack(side="top", fill="x", pady=20)
    topbar = ctk.CTkFrame(master=boite2, fg_color="transparent", corner_radius=corner3)
    topbar.pack(anchor="center")
    element_topbar = ctk.CTkFrame(master=topbar, fg_color="transparent")
    element_topbar.pack()

    boite_semi_header = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent")
    boite_semi_header.pack(side="top", pady=10)

    boite3 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color=couleur1, hover_color=couleur1_hover, width=button_width, anchor="w",
                                    command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    button_supprimer = ctk.CTkButton(master=element_topbar, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_activité(account_id, username, password, avoir_periode(combo_periode.get(), options_periode)))
    button_supprimer.pack(side="right", padx=2, pady=5)
    button_creer_activite = ctk.CTkButton(master=element_topbar, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
    button_creer_activite.pack(side="right", padx=(20, 2), pady=5)
    info = ctk.CTkLabel(master=element_topbar, text="Historique d'entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    info.pack(side="right", padx=20)
    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir": 9999}
    combo_periode = ctk.CTkComboBox(master=element_topbar, values=list(options_periode.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur2, button_color=couleur2, fg_color=couleur2,
                                    corner_radius=corner2, width=220, dropdown_fg_color=couleur2, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_periode.pack(side="right", padx=(10, 20), pady=5)
    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')
        
    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), accueil_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), accueil_football(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Football")

    def mettre_a_jour_historique(selection):
        for widget in tableau_frame.winfo_children():
            widget.destroy()        
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute("SELECT date_activité, durée, rpe, type_de_séances, humeur, but, passe_décisive FROM Activité_football WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            headers = ["Date", "Durée", "RPE", "Type", "Humeur", "But", "Passe D"]
            for col_idx, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 0:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
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

def accueil_musculation(account_id, username, password):
    cadre_accueil = ctk.CTkFrame(master=app, fg_color=couleur_fond) 
    cadre_accueil.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    boite2 = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent", corner_radius=corner3)
    boite2.pack(side="top", fill="x", pady=20)
    topbar = ctk.CTkFrame(master=boite2, fg_color="transparent", corner_radius=corner3)
    topbar.pack(anchor="center")
    element_topbar = ctk.CTkFrame(master=topbar, fg_color="transparent")
    element_topbar.pack()

    boite_semi_header = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent")
    boite_semi_header.pack(side="top", pady=10)

    boite3 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color=couleur1, hover_color=couleur1_hover, width=button_width, anchor="w",
                                    command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    button_supprimer = ctk.CTkButton(master=element_topbar, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_activité(account_id, username, password, avoir_periode(combo_periode.get(), options_periode)))
    button_supprimer.pack(side="right", padx=2, pady=5)
    button_creer_activite = ctk.CTkButton(master=element_topbar, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
    button_creer_activite.pack(side="right", padx=(20, 2), pady=5)
    info = ctk.CTkLabel(master=element_topbar, text="Historique d'entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    info.pack(side="right", padx=20)
    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir": 9999}
    combo_periode = ctk.CTkComboBox(master=element_topbar, values=list(options_periode.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur2, button_color=couleur2, fg_color=couleur2,
                                    corner_radius=corner2, width=220, dropdown_fg_color=couleur2, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_periode.pack(side="right", padx=(10, 20), pady=5)
    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')
    
    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), accueil_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), accueil_football(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Musculation")

    def mettre_a_jour_historique(selection):
        for widget in tableau_frame.winfo_children():
            widget.destroy()        
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute("SELECT date_activité, lieu, durée, rpe, équipement, muscle_travaillé, répétitions, série, volume FROM Activité_musculation WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            headers = ["Date", "Lieu", "Durée", "RPE", "Type", "Muscle", "Rép", "Série", "Volume"]
            for col_idx, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=110)
                label.grid(row=0, column=col_idx, padx=5, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 0:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=100)
                        label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
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

def accueil(account_id, username, password):
    cadre_accueil = ctk.CTkFrame(master=app, fg_color=couleur_fond) 
    cadre_accueil.pack(fill="both", expand=True)

    boite1 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur2, corner_radius=corner3)
    boite1.pack(side="left", fill="y")
    sidebar = ctk.CTkFrame(master=boite1, fg_color=couleur2, corner_radius=corner3)
    sidebar.pack(fill="both", expand=True)
    titre_sidebar = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    titre_sidebar.pack(pady=20)
    element_nav = ctk.CTkFrame(master=sidebar, fg_color=couleur2)
    element_nav.pack(pady=(50, 10), fill="y", expand=True)

    boite2 = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent", corner_radius=corner3)
    boite2.pack(side="top", fill="x", pady=20)
    topbar = ctk.CTkFrame(master=boite2, fg_color="transparent", corner_radius=corner3)
    topbar.pack(anchor="center")
    element_topbar = ctk.CTkFrame(master=topbar, fg_color="transparent")
    element_topbar.pack()

    boite_semi_header = ctk.CTkFrame(master=cadre_accueil, fg_color="transparent")
    boite_semi_header.pack(side="top", pady=10)

    boite3 = ctk.CTkFrame(master=cadre_accueil, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    titre_dans_sidebar = ctk.CTkLabel(master=titre_sidebar, text="Sprintia", font=(font_secondaire, taille1), text_color=couleur1)
    titre_dans_sidebar.pack()
    button_exercice = ctk.CTkButton(master=element_nav, text="💪 Exercice", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color=couleur1, hover_color=couleur1_hover, width=button_width, anchor="w",
                                    command=lambda: [vider_fenetre(app), accueil(account_id, username, password)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), performance(account_id, username, password)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id, username, password)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id, username, password)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)

    button_supprimer = ctk.CTkButton(master=element_topbar, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_activité(account_id, username, password, avoir_periode(combo_periode.get(), options_periode)))
    button_supprimer.pack(side="right", padx=2, pady=5)
    button_creer_activite = ctk.CTkButton(master=element_topbar, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id, username, password)])
    button_creer_activite.pack(side="right", padx=(20, 2), pady=5)
    info = ctk.CTkLabel(master=element_topbar, text="Historique d'entraînement", font=(font_secondaire, taille1), text_color=couleur_text)
    info.pack(side="right", padx=20)
    options_periode = {"1 semaine": 7, "1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "Tout voir": 9999}
    combo_periode = ctk.CTkComboBox(master=element_topbar, values=list(options_periode.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur2, button_color=couleur2, fg_color=couleur2,
                                    corner_radius=corner2, width=220, dropdown_fg_color=couleur2, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur2_hover, text_color=couleur1, dropdown_text_color=couleur1)
    combo_periode.pack(side="right", padx=(10, 20), pady=5)
    def avoir_periode(selection_text, options_dict):
        jours_a_soustraire = options_dict[selection_text]
        date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
        return date_debut.strftime('%Y-%m-%d')
    
    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil(account_id, username, password)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), accueil_intérieur(account_id, username, password)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), accueil_musculation(account_id, username, password)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), accueil_football(account_id, username, password)])

    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Extérieur", "Intérieur", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Extérieur")

    def mettre_a_jour_historique(selection):
        for widget in tableau_frame.winfo_children():
            widget.destroy()        
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute("SELECT sport, date_activité, durée, rpe, nom, distance, dénivelé FROM Activité_extérieur WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            headers = ["Sport", "Date", "Durée", "RPE", "Nom", "Distance", "Dénivelé"]
            for col_idx, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 1:
                            data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
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

def connection():
    cadre_connection = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_connection.pack(fill="both", expand=True)

    boite_géante = ctk.CTkFrame(master=cadre_connection, fg_color="transparent")        
    boite_géante.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    boite1 = ctk.CTkFrame(master=boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite1.pack(side="left", pady=10, padx=20, fill="both", expand=True)
    titre = ctk.CTkFrame(master=boite1, fg_color="transparent")        
    titre.pack(pady=(20, 10), padx=20)
    message = ctk.CTkFrame(master=boite1, fg_color="transparent")        
    message.pack(pady=(0, 10), padx=10)
    frame_bouton = ctk.CTkFrame(master=boite1, fg_color="transparent")
    frame_bouton.pack(fill="x", pady=(20, 10), padx=20)
    carte_connexion = ctk.CTkFrame(master=boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(fill="x", pady=(20, 5), padx=20)  
    bouton_action = ctk.CTkFrame(master=boite1, fg_color="transparent")        
    bouton_action.pack(fill="x", pady=5, padx=20)
    boite2 = ctk.CTkFrame(master=boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite2.pack(side="right", pady=10, padx=20, fill="both", expand=True)
    img = ctk.CTkFrame(master=boite2, fg_color="transparent")        
    img.pack(pady=20, padx=20)

    Titre = ctk.CTkLabel(master=titre ,text="Bienvenue sur Sprintia\n", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()
    messages = ctk.CTkLabel(master=message ,text="Content de te revoir !", font=(font_principale, taille2), text_color=couleur_text)
    messages.pack()

    button_connection = ctk.CTkButton(master=frame_bouton, text="✔️ Connection", fg_color=couleur1, hover_color=couleur1_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), connection()])
    button_connection.pack(expand=True, fill="x", side="left", padx=1)
    button_inscription = ctk.CTkButton(master=frame_bouton, text="Inscription", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), inscription()])
    button_inscription.pack(expand=True, fill="x", side="right", padx=1)

    app.bind('<Return>', lambda event: verifier_identifiants())
    username_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Pseudo", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white")
    username_entry.pack(fill="x", pady=(10, 5), padx=10)
    password_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Mot de passe", show="*", border_color=couleur1,fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white")
    password_entry.pack(fill="x", pady=(0, 10), padx=10)

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
    button_valider = ctk.CTkButton(master=bouton_action, text="Se connecter", fg_color=couleur1, hover_color=couleur1_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille2), command=verifier_identifiants)
    button_valider.pack(fill="x", pady=(0, 10))

    mon_image_pil = Image.open(mode_image)
    largeur_img = 300
    hauteur_img = 400
    image_redimensionner = mon_image_pil.resize((largeur_img, hauteur_img), Image.Resampling.LANCZOS)
    CTk_image = ctk.CTkImage(light_image=image_redimensionner, dark_image=image_redimensionner, size=(largeur_img, hauteur_img))
    label_image = ctk.CTkLabel(master=img, image=CTk_image, text="")
    label_image.pack()

def inscription():
    cadre_inscription = ctk.CTkFrame(master=app, fg_color=couleur_fond)        
    cadre_inscription.pack(fill="both", expand=True)

    boite_géante = ctk.CTkFrame(master=cadre_inscription, fg_color="transparent")        
    boite_géante.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    boite1 = ctk.CTkFrame(master=boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite1.pack(side="left", pady=10, padx=20, fill="both", expand=True)
    titre = ctk.CTkFrame(master=boite1, fg_color="transparent")        
    titre.pack(pady=(20, 10), padx=20)
    message = ctk.CTkFrame(master=boite1, fg_color="transparent")        
    message.pack(pady=(0, 10), padx=10)
    frame_bouton = ctk.CTkFrame(master=boite1, fg_color="transparent")
    frame_bouton.pack(fill="x", pady=(20, 10), padx=20)
    carte_inscription = ctk.CTkFrame(master=boite1, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_inscription.pack(fill="x", pady=(20, 5), padx=20)  
    bouton_action = ctk.CTkFrame(master=boite1, fg_color="transparent")        
    bouton_action.pack(fill="x", pady=5, padx=20)
    boite2 = ctk.CTkFrame(master=boite_géante, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color="transparent")        
    boite2.pack(side="right", pady=10, padx=20, fill="both", expand=True)
    img = ctk.CTkFrame(master=boite2, fg_color="transparent")        
    img.pack(fill="both", expand=True, padx=20, pady=50)

    Titre = ctk.CTkLabel(master=titre ,text="Bienvenue sur Sprintia\n", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack()
    message = ctk.CTkLabel(master=message ,text="Prêt à atteindre tes objectifs sportifs ? Tu es au bon endroit !", font=(font_principale, taille2), 
                           text_color=couleur_text, wraplength=400)
    message.pack()

    button_connection = ctk.CTkButton(master=frame_bouton, text="Connection", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), connection()])
    button_connection.pack(expand=True, fill="x", side="left", padx=1)
    button_inscription = ctk.CTkButton(master=frame_bouton, text="✔️  Inscription", fg_color=couleur1, hover_color=couleur1_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), inscription()])
    button_inscription.pack(expand=True, fill="x", side="right", padx=1)

    app.bind('<Return>', lambda event: verifier_identifiants_connexion())
    username_entry = ctk.CTkEntry(master=carte_inscription, placeholder_text="Pseudo", border_color=couleur1,fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white")
    username_entry.pack(fill="x", pady=(10, 5), padx=10)
    password_entry = ctk.CTkEntry(master=carte_inscription, placeholder_text="Mot de passe", show="*", border_color=couleur1,fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white")
    password_entry.pack(fill="x", pady=(0, 5), padx=10)
    password_confirm= ctk.CTkEntry(master=carte_inscription, placeholder_text="Confirmer mot de passe", show="*", border_color=couleur1,
                                   fg_color=couleur1, height=entry_height, font=(font_principale, taille3), corner_radius=corner1, 
                                   placeholder_text_color ="white", text_color="white")
    password_confirm.pack(fill="x", pady=(0, 10), padx=10)
    
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
    button_valider = ctk.CTkButton(master=bouton_action, text="S'incrire", fg_color=couleur1, hover_color=couleur1_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille2), command=verifier_identifiants_connexion)
    button_valider.pack(fill="x", pady=(0, 10))

    mon_image_pil = Image.open(mode_image)
    largeur_img = 300
    hauteur_img = 400
    image_redimensionner = mon_image_pil.resize((largeur_img, hauteur_img), Image.Resampling.LANCZOS)
    CTk_image = ctk.CTkImage(light_image=image_redimensionner, dark_image=image_redimensionner, size=(largeur_img, hauteur_img))
    label_image = ctk.CTkLabel(master=img, image=CTk_image, text="")
    label_image.pack()

def mettre_à_jour_bdd():
    try:
        curseur.execute("ALTER TABLE Compétition ADD COLUMN lieu TEXT")
    except sqlite3.OperationalError:
        pass  
    try:
        curseur.execute("ALTER TABLE Objectif ADD COLUMN niveau_fin TEXT")
    except sqlite3.OperationalError:
        pass  
    try:
        curseur.execute("ALTER TABLE Compétition ADD COLUMN priorité TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Account ADD COLUMN sport TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Account ADD COLUMN bio TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN muscle_travaillé TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN répétitions TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN série TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN volume TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN équipement TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN lieu TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN humeur TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN but TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN passe_décisive TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité ADD COLUMN type_de_séances TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité DROP COLUMN allure")
    except sqlite3.Error as e:
        pass
    try:
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_extérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_intérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_musculation (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_football (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
    except sqlite3.Error as e:
        pass
    connection()

if __name__ == "__main__":
    try:
        con = sqlite3.connect("data_base.db")
        curseur = con.cursor()

        curseur.execute('''CREATE TABLE IF NOT EXISTS Account (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL, sport TEXT, bio TEXT)''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_extérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_intérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_musculation (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_football (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,dénivelé INTEGER,rpe INTEGER,fatigue INTEGER,douleur INTEGER,climat INTEGER,charge INTEGER,nom TEXT,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Compétition (id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT NOT NULL,date TEXT NOT NULL,sport TEXT NOT NULL,objectif TEXT NOT NULL, lieu TEXT,priorité TEXT,account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Objectif (id INTEGER PRIMARY KEY AUTOINCREMENT,sport TEXT NOT NULL,date TEXT NOT NULL,objectif TEXT NOT NULL,fréquence TEXT NOT NULL,niveau_début TEXT NOT NULL,niveau_fin TEXT,statut TEXT, account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Pauses (id INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER NOT NULL,type TEXT CHECK(type IN ('vacances', 'blessure')),date_debut TEXT DEFAULT CURRENT_DATE,date_fin TEXT,FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        con.commit()
        ctk.set_appearance_mode("System")
        app = ctk.CTk()
        app.geometry("1050x600")
        app.title("Sprintia")
        mettre_à_jour_bdd()
        app.protocol("WM_DELETE_WINDOW", fermer_app)
        app.bind("<Control-w>", lambda event: fermer_app())
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
