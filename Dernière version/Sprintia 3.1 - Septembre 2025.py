import customtkinter as ctk
from PIL.ImageOps import expand
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
from tkinter import messagebox

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

# variables
date_actuelle = date.today()

# heure
maintenant = datetime.now()
heure_actuelle_objet = maintenant.time()

# variable globale
periode_séléctionner = "1 semaine"

def sidebar_exercice(account_id):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
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
                                    anchor="w", command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
def sidebar_performance(account_id):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
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
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
def sidebar_outil(account_id):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
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
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil",  font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1, width=button_width,
                                    fg_color="transparent", hover_color=couleur2_hover, text_color=couleur1, height=button_height,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)
def sidebar_paramètre(account_id):
    boite1 = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner3)
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
                                    text_color=couleur1, command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_exercice.pack(side="top", padx=(10, 40), pady=2)
    button_performance = ctk.CTkButton(master=element_nav, text="🚀 Performance", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_performance.pack(side="top", padx=(10, 40), pady=2)
    button_outils = ctk.CTkButton(master=element_nav, text="🔧 Outil", font=(font_principale, taille3), corner_radius=corner1,
                                    height=button_height, fg_color="transparent", hover_color=couleur2_hover, width=button_width, anchor="w",
                                    text_color=couleur1,
                                    command=lambda: [vider_fenetre(app), predicteur_temps(account_id)])
    button_outils.pack(side="top", padx=(10, 40), pady=2)
    button_autre = ctk.CTkButton(master=element_nav, text="⚙️ Paramètres", font=(font_principale, taille3), corner_radius=corner1,
                                    fg_color=couleur1, hover_color=couleur1_hover, height=button_height, width=button_width,
                                    anchor="w",
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_autre.pack(side="top", padx=(10, 40), pady=2)


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
        messagebox.showerror("Mot de passe invalide", "La longueur doit être d'au moins 6 caractères !")
        val = False

    if len(password) > 20:
        messagebox.showerror("Mot de passe invalide", "La longueur ne doit pas dépasser 20 caractères !")
        val = False

    if not any(char.isdigit() for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins un chiffre !")
        val = False

    if not any(char.isupper() for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins une lettre majuscule !")
        val = False

    if not any(char.islower() for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins une lettre minuscule !")
        val = False

    if not any(char in SpecialSymbol for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins un des symboles spéciaux : $@#%?!")
        val = False
    if val:
        return val

def navbar_mon_compte(account_id, mode_actuel):
    sidebar_paramètre(account_id)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Mon compte":
            app.after(0, lambda: [vider_fenetre(app), mon_compte(account_id)])
        elif choix == "Modifier":
            app.after(0, lambda: [vider_fenetre(app), modifier_compte(account_id)])
        elif choix == "Supprimer mon compte":
            app.after(0, lambda: [vider_fenetre(app), supprimer_compte(account_id)])
        elif choix == "Mot de passe oublié":
            app.after(0, lambda: [vider_fenetre(app), modifier_password(account_id)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Mon compte", "Modifier", "Supprimer mon compte", "Mot de passe oublié"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set(mode_actuel)
    button_back = ctk.CTkButton(master=navbar, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_back.pack(side="left", padx=10)

def aide_objectif(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_objectif (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("Info sur le menu déroulant", "Lorsque tu modifies ton objectif, les menus déroulants se réinitialisent. Pense donc à sélectionner à nouveau une option pour 'Level Final' et 'Statut de l'objectif', même si tu les avais déjà définis lors de la création de l'objectif.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def aide_compétition(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_compétition (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("Info sur le menu déroulant", "Lorsque tu modifies ta compétition, les menus déroulants se réinitialisent. Pense donc à sélectionner à nouveau une option pour 'Priorité', même si tu l'avais déjà défini lors de la création de la compétition.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def aide_podcast(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_podcast WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_podcast (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("Pas envie de lire le patch note ? Pas de problème ! On a une solution pour vous.", "Découvrez toutes les nouveautés de la mise à jour Sprintia 3.1 en écoutant notre Podcast.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def aide_bienvenue(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_bienvenue WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_bienvenue (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("Bienvenue dans Sprintia 3.1", "Découvre une nouvelle manière de t’entraîner en course à pied grâce à l’indulgence de course.")
            messagebox.showinfo("Bienvenue dans Sprintia 3.1", "Découvre un nouveau mode Course pour l'enregistrement des données spécifique à ce sport.")
            messagebox.showinfo("Bienvenue dans Sprintia 3.1", "Découvre toutes les nouveautés de Sprintia 3.1 dans le Patch Note dans les paramètres.")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def aide_rpe(account_id):
    try:
        curseur.execute("SELECT aide FROM Aide_rpe WHERE account_id = ?", (account_id,))
        result = curseur.fetchone()
        if result and result[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
            pass
        else:
            appris = "fait"
            curseur.execute("INSERT INTO Aide_rpe (account_id, aide)VALUES (?, ?)", (account_id, appris))
            con.commit()
            messagebox.showinfo("C'est quoi le RPE ?", "Le RPE, c'est une manière subjective de mesurer l'intensité de ton entraînement. En gros, tu notes l'effort que tu ressens sur une échelle de 1 à 10.")
            messagebox.showinfo("Information importante", "Pour la distance, utilise un point au lieu d’une virgule. Par exemple, écris 9.62 pour indiquer 9,62 km.")
            messagebox.showinfo("Information importante", "Lorsque tu indiques la durée, il faut arrondir les minutes. Par exemple, si ta séance a duré 20 minutes et 44 secondes, tu devras noter 21 !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def a_propos(account_id):
    sidebar_paramètre(account_id)

    frame_maj = ctk.CTkFrame(master=app, fg_color="transparent")
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
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_back.pack(side="left", padx=5, pady=10)

    frame_slogan = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_slogan.pack(padx=10, pady=(20, 10))
    slogan = ctk.CTkLabel(master=frame_slogan, text="Sprintia est conçue pour t'aider avant et après un entraînement",
                          font=(font_principale, taille2))
    slogan.pack()

    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack(pady=(20, 10))
    frame_version = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame_version.pack(padx=10, pady=(10, 5))
    frame_dev = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame_dev.pack(padx=10, pady=(5, 10))

    version = ctk.CTkLabel(master=frame_version, text="Version Sprintia : ",
                          font=(font_principale, taille2), text_color=couleur1)
    version.pack(side="left", padx=10, pady=5)
    num_version = ctk.CTkLabel(master=frame_version, text="3.1 | Version Septembre 2025",
                          font=(font_principale, taille2), text_color=couleur1)
    num_version.pack(side="left", padx=10, pady=5)
    nom_dev = ctk.CTkLabel(master=frame_dev, text="Sprintia est développé par Gabriel Chapet",
                          font=(font_principale, taille2), text_color=couleur1)
    nom_dev.pack(side="right", padx=10, pady=5)

    conteneur = ctk.CTkFrame(master=app, fg_color=couleur_fond, corner_radius=corner1,
                             border_width=border1, border_color=couleur1)
    conteneur.pack(fill="x", expand=True, padx=25, pady=10)
    sous_titre= ctk.CTkLabel(master=conteneur, text="Pourquoi j'ai créé Sprintia ?", font=(font_secondaire, taille2))
    sous_titre.pack(pady=10)
    pourquoi = ctk.CTkLabel(master=conteneur, text="J'ai lancé Sprintia parce que pour moi, on n'a pas besoin de dépenser des fortunes pour avoir de la qualité. C'est un peu comme avec" \
                        " les montres connectées : on ne devrait pas être obligé d'acheter la toute dernière et la plus chère pour pouvoir profiter des dernières fonctionnalités." \
                        " De plus, certains constructeurs de montre connectées ce permettre de mettre un abonnement pour pouvoir bénificié de tout les fonctionnalités !" \
                        " Du coup, j'ai décidé de créer Sprintia pour faire les choses à ma manière !",
                        font=(font_principale, taille3), wraplength=950)
    pourquoi.pack(padx=10)
    sous_titre2= ctk.CTkLabel(master=conteneur, text="Qui suis-je ?", font=(font_secondaire, taille2))
    sous_titre2.pack(pady=10)
    quisuisje = ctk.CTkLabel(master=conteneur, 
                            text="J'adore le sport, la tech et l'imformatique. Ce que j'adore dans le sport," \
                            " c'est les algorithmes qui vont m'aider à m'entraîner et à progresser dans mon sport, sans avoir de coach." \
                            " Je développe Sprintia pour vous aider à vous entraîner gratuitement sans matériel. Le seul matériel requis" \
                            " pour faire fonctionner les algorithmes c'est une montre avec un chrono ou même un smartphone peut suffire pour utiliser Sprintia." \
                            " Mais pour avoir un suivi plus complet, tu peux utiliser ton téléphone pour le GPS en course, vélo au moins tu pourras intégrer plus de données" \
                            " dans Sprintia !",
                            font=(font_principale, taille3),  wraplength=950)
    quisuisje.pack(padx=10, pady=10)

def verifier_pause(account_id):
    #AND date_fin IS NULL = Cible uniquement les pause non terminés.
    curseur.execute("""SELECT type FROM Pauses_v2 WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
    result = curseur.fetchone()
    return result[0] if result else None

def supprimer_activité(account_id, période_str):
    vider_fenetre(app)
    sidebar_exercice(account_id)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=(20, 10))
    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 

    Titre = ctk.CTkLabel(master=frame, text="Supprimer une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="ID de l'activité à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack()
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=5)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT id_activité, sport, date_activité, durée, rpe FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC", (account_id, période_str))
            activites = curseur.fetchall()

            headers = ["ID", "Sport", "Date", "Durée", "RPE"]

            for col_idx, header_text in enumerate(headers): #_idx= index de colonne
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=130)
                label.grid(row=0, column=col_idx, padx=15, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(col_idx, weight=1)
            if activites:
                for row_idx, activite in enumerate(activites):
                    for col_idx, data in enumerate(activite):
                        if col_idx == 2:
                            date_activité = datetime.strptime(data, '%Y-%m-%d')
                            data = date_activité.strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de l'historique !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
    def supression(account_id):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in activites]

                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Activité WHERE id_activité = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Activité supprimée avec succès.")
                    vider_fenetre(app)
                    exercice(account_id)
                else:
                    messagebox.showerror("Erreur", "L'ID de l'activité saisie n'existe pas ou n'appartient pas à votre compte.")
                    return
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de l'activité.")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer.")
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: supression(account_id))
    button_check.pack(side="left", padx=2, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), exercice(account_id)])
    button_retour.pack(side="left", padx=2, pady=20)

def ajouter_activité_course(account_id):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_type = ["Normal", "Endurance", "Fractionné", "Spécifique", "Trail", "Ultrafond", "Compétition"]

    sidebar_exercice(account_id)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité",
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Course")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover,
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=(10, 20))
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
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
    type_entry.set("Type de séance")

    rpe_label = ctk.CTkLabel(master=frame_champs2, text="RPE", font=(font_principale, taille3), text_color=couleur_text)
    rpe_label.pack(side="left", padx=(75, 0))
    def valeur_rpe(valeur):
        rpe_label.configure(text=f"RPE : {valeur:.0f}")
    rpe_entry = ctk.CTkSlider(master=frame_champs2, width=400, height=20, from_=1, to=10, number_of_steps=9, command=valeur_rpe,
                              progress_color=couleur1, button_color=couleur1, button_hover_color=couleur1_hover,
                              corner_radius=10, button_length=15, fg_color=couleur_text)
    rpe_entry.pack(side="left", padx=10)
    distance_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(side="left", padx=(75, 10))

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

    allure_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Allure (ex : 6:00 /km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    allure_entry.pack(side="left", padx=10)
    denivele_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Dénivelé (m)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    denivele_entry.pack(side="left", padx=10)
    vmax_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Vitesse max (ex : 15.8)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vmax_entry.pack(side="left", padx=10)

    def enregistrer():
        type = type_entry.get().strip()
        if type == "Type de séance":
            messagebox.showerror("Type manquant", "Séléctionne un type d'entraînement")
            return
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide ! Utilisez JJ-MM-AAAA ! Avec des tirets !")

        sport = "Course"
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
        distance = None
        denivele = None
        allure = allure_entry.get().strip()
        if not allure:
            allure = None
        vmax_str = vmax_entry.get().strip()
        if not vmax_str:
            vmax = None
        else:
            try:
                vmax = float(vmax_str)
                if vmax <= 0:
                    messagebox.showerror("Erreur", "La vitesse max doit être supérieure à 0 !")
                    return
            except ValueError:
                messagebox.showerror("Erreur", "La vitesse max est invalide (nombre positif requis) !")
                return
        try:
            dist_str = distance_entry.get().strip()
            if dist_str:
                distance = float(dist_str)
                if distance <= 0:
                    messagebox.showerror("Erreur", "La distance doit être supérieur à 0 !")
                    return
        except ValueError:
            messagebox.showerror("Erreur", "Distance invalide (nombre positif requis) !")
            return
        try:
            deniv_str = denivele_entry.get().strip()
            if deniv_str:
                denivele = int(deniv_str)
                if denivele <= 0:
                    messagebox.showerror("Erreur", "Le dénivelé doit être supérieur à 0. !")
                    return
        except ValueError:
            messagebox.showerror("Erreur", "Dénivelé invalide (entier positif requis) !")
            return

        charge_de_base = duree * rpe

        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        if type == "Normal":
            coef = 1.0
        elif type == "Endurance":
            coef = 1.05
        elif type == "Fractionné" or "Spécifique":
            coef = 1.1
        elif type == "Trail" or "Compétition":
            coef = 1.25
        elif type == "Ultrafond":
            coef = 1.30

        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = (score_fatigue * charge_c)*coef
        try:
            curseur.execute("""INSERT INTO Activité_running (date_activité, sport, durée, distance, rpe, charge, account_id, nom, dénivelé, allure, vitesse_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, distance, rpe, charge, account_id, type, denivele, allure, vmax))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_intérieur(account_id):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}

    sidebar_exercice(account_id)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Intérieur")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=(10, 20))
    frame_champs4 = ctk.CTkFrame(master=app, fg_color="transparent")
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
    nom_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Type", border_color=couleur1, fg_color=couleur1,
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
        if len(nom) > 20:
            messagebox.showerror("Type trop long", "Le type de ton entraînement fait plus de 20 caractères")
            return
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        
        sport = sport_entry.get().strip()
        if not sport:
            messagebox.showerror("Erreur", "Le sport est obligatoire !")
            return 
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_d
        try:
            curseur.execute("""INSERT INTO Activité_intérieur (date_activité, sport, durée, rpe, charge, account_id, nom) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id, nom))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_musculation(account_id):
    Options_matos = ["Poids de corps", "Avec équipement"]
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_lieu = {"Salle de sport": "salle de sport", "Domicile": "domicile", "Extérieur": "extérieur"}

    sidebar_exercice(account_id)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Musculation")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
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
                messagebox.showerror("Erreur", "Volume total invalide (entier positif requis) !")
                return
        else:
            volume_total = None
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        lieu = Options_lieu.get(lieu_entry.get().strip())
        équipement = matos_entry.get().strip()
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if lieu is None:
            messagebox.showerror("Lieu est vide", "Le lieu est obligatoire !")
            return
        if équipement is None:
            messagebox.showerror("Le type est vide", "Le type est obligatoire !")
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
            curseur.execute("""INSERT INTO Activité_musculation (date_activité, sport, durée, rpe, charge, account_id, muscle_travaillé, répétitions, série, volume, équipement, lieu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id, muscle_travaillé, répétitions, série, volume_total, équipement, lieu))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_fooball(account_id):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}
    Options_type = ["Entraînement", "Match", "Tournoi", "City"]

    sidebar_exercice(account_id)

    frame1 = ctk.CTkFrame(master=app, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Football")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
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
    score_entry = ctk.CTkEntry(master=frame_champs4, placeholder_text="Score (ex : 3-2)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    score_entry.pack(side="left", padx=10)

    def enregistrer():
        humeur = humeur_entry.get().strip()
        passe_décisive1 = passe_d_entry.get().strip()
        type_de_séances = type_entry.get().strip()
        score = score_entry.get().strip()
        if humeur:
            pass
        else:
            humeur = None
        if score:
            pass
        else:
            score = None
        if passe_décisive1:
            try:
                passe_décisive = int(passe_décisive1)
                if passe_décisive < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Nombre de passe décisive invalide (entier positif requis) !")
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
                messagebox.showerror("Erreur", "Nombre de but invalide (entier positif requis) !")
                return
        else:
            but = None
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
        
        sport = "Football"
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
        if type_de_séances is None:
            messagebox.showerror("Type de séances de foot est vide", "Le type de séance de foot est obligatoire !")
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
            curseur.execute("""INSERT INTO Activité_football (date_activité, sport, durée, rpe, charge, account_id, humeur, but, passe_décisive, type_de_séances, score) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id, humeur, but, passe_décisive, type_de_séances, score))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)

def ajouter_activité_extérieur(account_id):
    Options_douleur = {"Non": 0, "Un peu": 1, "Oui": 2, "Blessure": 3}
    Options_climat = {"Normal": 0, "Chaud": 1, "Froid": 2, "Difficile": 3}
    Options_fatigue = {"Non": 0, "Un peu": 2.5, "Oui": 5}

    sidebar_exercice(account_id)

    frame1 = ctk.CTkFrame(master=app, corner_radius=20, fg_color="transparent")        
    frame1.pack(pady=20)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=(0, 10))

    Titre = ctk.CTkLabel(master=frame1, text="Ajouter une activité", 
                font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Extérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
        elif choix == "Intérieur":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_intérieur(account_id)])
        elif choix == "Musculation":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_musculation(account_id)])
        elif choix == "Football":
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_fooball(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), ajouter_activité_course(account_id)])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Extérieur")
    bouton_retour = ctk.CTkButton(master=navbar, text="🔙 Retour", corner_radius=corner2, fg_color=couleur2, hover_color=couleur2_hover, 
                                height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                command=lambda: [vider_fenetre(app), exercice(account_id)])
    bouton_retour.pack(side="left", padx=10)

    frame_activité = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)
    frame_activité.pack(padx=10, pady=(10, 0))
    frame_champs1 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs1.pack(padx=10, pady=(20, 10))
    frame_champs2 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs2.pack(padx=10, pady=10)
    frame_champs3 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs3.pack(padx=10, pady=10)
    frame_champs4 = ctk.CTkFrame(master=frame_activité, fg_color="transparent")
    frame_champs4.pack(padx=10, pady=(10, 20))
    frame_champs5 = ctk.CTkFrame(master=app, fg_color="transparent")
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
    nom_entry = ctk.CTkEntry(master=frame_champs2, placeholder_text="Type", border_color=couleur1, fg_color=couleur1,
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
        if len(nom) > 20:
            messagebox.showerror("Type trop long", "Le type de votre entraînement fait plus de 20 caractères")
            return
        try:
            date_str = date_entry.get().strip()
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            if date_obj > datetime.now():
                messagebox.showerror("Erreur", "La date ne peut pas être dans le futur !")
                return
            date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide. Utilisez JJ-MM-AAAA.")
            return
        
        sport = sport_entry.get().strip()
        if not sport:
            messagebox.showerror("Erreur", "Le sport est obligatoire !")
            return 
        try:
            duree = int(duree_entry.get().strip())
            if duree <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Durée invalide (entier positif requis) !")
            return 
        try:
            rpe = int(rpe_entry.get())
            if not 1 <= rpe <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "RPE invalide (1-10 requis) !")
            return
        douleur = Options_douleur.get(douleur_entry.get().strip())
        climat = Options_climat.get(climat_entry.get().strip())
        fatigue = Options_fatigue.get(fatigue_entry.get().strip())
        if fatigue is None:
            messagebox.showerror("Fatigue est vide", "La fatigue est obligatoire !")
            return
        if douleur is None:
            messagebox.showerror("Douleur est vide", "La douleur est obligatoire !")
            return
        if climat is None:
            messagebox.showerror("Climat est vide", "Le climat est obligatoire !")
            return
        distance = None
        denivele = None
        try:
            dist_str = distance_entry.get().strip()
            if dist_str:
                distance = float(dist_str)
                if distance <= 0:
                    messagebox.showerror("Erreur", "La distance doit être supérieur à 0 !")
                    return
        except ValueError:
            messagebox.showerror("Erreur", "Distance invalide (nombre positif requis) !")
            return
        try:
            deniv_str = denivele_entry.get().strip()
            if deniv_str:
                denivele = int(deniv_str)
                if denivele <= 0:
                    messagebox.showerror("Erreur", "Le dénivelé doit être supérieur à 0. !")
                    return       
        except ValueError:
            messagebox.showerror("Erreur", "Dénivelé invalide (entier positif requis) !")
            return
                                            
        charge_de_base = duree * rpe
        
        modificateurs_douleur = [0.9, 1.05, 1.2, 1.4]
        modificateurs_climat = [0.95, 1.1, 1.05, 1.2]
        
        charge_d = charge_de_base * modificateurs_douleur[douleur]
        charge_c = charge_d * modificateurs_climat[climat]
        score_fatigue = 1 + (fatigue - 2.5) * 0.05
        charge = score_fatigue * charge_c
        try:
            curseur.execute("""INSERT INTO Activité_extérieur (date_activité, sport, durée, distance, rpe, charge, account_id, nom, dénivelé) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, distance, rpe, charge, account_id, nom, denivele))
            con.commit()
            curseur.execute("""INSERT INTO Activité (date_activité, sport, durée, rpe, charge, account_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (date, sport, duree, rpe, charge, account_id))
            con.commit()
            messagebox.showinfo("Succès", "Ton activité a bien été enregistrée !")
            vider_fenetre(app)
            exercice(account_id)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton activité.")
            return
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye.")
            return
    bouton_valider = ctk.CTkButton(master=frame_champs5, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3), command=lambda : enregistrer())
    bouton_valider.pack(side="left", padx=10)
    aide_rpe(account_id)

def navbar_outil(account_id, mode_actuel):
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=20)

    def mise_mode(choix):
        choix = mode_activité.get()
        navigation = {
            "Prédicteur de performance": lambda: [vider_fenetre(app), predicteur_temps(account_id)],
            "Zones cardiaque": lambda: [vider_fenetre(app), zone_fc(account_id)],
            "Calculateur IMC": lambda: [vider_fenetre(app), imc(account_id)],
            "Estimation VMA": lambda: [vider_fenetre(app), VMA(account_id)],
            "Estimation VO2max": lambda: [vider_fenetre(app), VO2MAX(account_id)]
        }
        app.after(0, navigation[choix])

    mode_activité = ctk.CTkSegmentedButton(master=navbar, 
                                            values=["Prédicteur de performance", "Zones cardiaque", "Calculateur IMC", "Estimation VMA", "Estimation VO2max"],
                                            height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                            corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                            fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                            text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set(mode_actuel)

def imc(account_id):
    sidebar_outil(account_id)
    navbar_outil(account_id, "Calculateur IMC")

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_imc())
    poids_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Poids (kg)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    poids_entry.pack(pady=(11, 5), padx=10)
    taille_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Taille (cm)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    taille_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1, wraplength=800)
    result.pack(padx=50, pady=10)

    def calcul_imc():
        try:
            poids = float(poids_entry.get().strip())
            taille_conversion = float(taille_entry.get().strip())
            taille = taille_conversion/100

            if poids <= 0 or taille <= 0:
                messagebox.showerror("Erreur", "La taille et le poids doivent être supérieur à 0 !")
                return
            if not poids or not taille:
                messagebox.showerror("Erreur", "La taille et le poids ne peuvent pas être vides !")
                return
            else:
                imc = poids / (taille ** 2)

                if imc <= 18.5:
                    interprétation = "Ton IMC se situe dans la zone de maigreur. Cela peut correspondre à ta morphologie naturelle, mais si tu ressens de la fatigue ou des inquiétudes, un avis médical peut être utile pour vérifier ton état de santé global."
                elif 18.5 <= imc <= 24.999:
                    interprétation = "Super, ton IMC est dans la zone de corpulence normale ! C’est un bon indicateur, mais n’oublie pas que la santé dépend aussi d’autres facteurs comme l’équilibre alimentaire, l’activité physique et le bien-être général."
                elif 25 <= imc <= 29.999:
                    interprétation = "Ton IMC est dans la zone de surpoids. Cela peut être lié à différents facteurs (morphologie, mode de vie, génétique, etc.). Si tu le souhaites, un professionnel peut t’aider à faire le point sur tes habitudes."
                elif 30 <= imc <= 34.999:
                    interprétation = "Ton IMC indique une obésité modérée. Cela ne définit pas ta santé à lui seul, mais un accompagnement personnalisé (médecin, nutritionniste) peut t’aider à trouver un équilibre adapté à tes besoins."
                elif 35 <= imc <= 39.999:
                    interprétation = "Ton IMC est dans la zone d’obésité sévère. Pour aborder cela de manière globale, un suivi médical ou nutritionnel peut te soutenir dans une démarche adaptée et bienveillante."
                elif imc >= 40:
                    interprétation = "Ton IMC se situe dans la zone d’obésité de grade 3. C’est une situation où un suivi médical régulier est important pour ta santé. N’hésite pas à en parler à un professionnel."
                else:
                    interprétation = "Une erreur est survenue, réesaye plus tard."
                    
                result.configure(text=f"Ton IMC est : {imc:.2f}\n\n{interprétation}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye.")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: calcul_imc())
    button_check.pack(padx=10, pady=10)

def VO2MAX(account_id):
    sidebar_outil(account_id)
    navbar_outil(account_id, "Estimation VO2max")

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_VO2MAX(account_id))
    vma_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="VMA", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vma_entry.pack(pady=(11, 5), padx=10)

    combo_genre = ctk.CTkComboBox(master=carte_connexion, values=["Homme", "Femme"], font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    combo_genre.pack(pady=5, padx=10)
    combo_genre.set("Sélectionne ton genre")

    age_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Âge", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    age_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_VO2MAX(account_id):
        try:
            vma = float(vma_entry.get().strip())
            age = float(age_entry.get().strip())
            genre = combo_genre.get().strip()

            if vma <= 0:
                messagebox.showerror("Erreur", "La VMA doit être supérieur à 0 !")
                return
            if age < 14:
                messagebox.showerror("Erreur", "L'âge minimum pour cette fonction est de 14 ans !")
                return
            if not vma or not age:
                messagebox.showerror("Erreur", "La VMA et l'âge ne peuvent pas être vides !")
                return
            else:
                vo2max = vma*3.5
                if genre == "Homme":
                    if 14 <= age <= 17 :
                        if vo2max >= 58:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 54 <= vo2max <= 58:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 50 <= vo2max <= 53:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 46 <= vo2max <= 49:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 18 <= age <= 25 :
                        if vo2max >= 56:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 52 <= vo2max <= 56:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 48 <= vo2max <= 51:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 44 <= vo2max <= 47:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 26 <= age <= 35 :
                        if vo2max >= 51:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 47 <= vo2max <= 51:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 43 <= vo2max <= 46:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 39 <= vo2max <= 42:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 36 <= age <= 45 :
                        if vo2max >= 45:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 41 <= vo2max <= 45:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 37 <= vo2max <= 40:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 33 <= vo2max <= 36:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 46 <= age <= 55 :
                        if vo2max >= 41:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 37 <= vo2max <= 41:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 33 <= vo2max <= 36:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 29 <= vo2max <= 32:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 56 <= age <= 65 :
                        if vo2max >= 37:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 33 <= vo2max <= 37:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 29 <= vo2max <= 32:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 25 <= vo2max <= 28:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if age >= 65 :
                        if vo2max >= 33:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 29 <= vo2max <= 33:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 25 <= vo2max <= 28:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 21 <= vo2max <= 24:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                elif genre == "Femme":
                    if 14 <= age <= 17 :
                        if vo2max >= 52:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 48 <= vo2max <= 52:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 44 <= vo2max <= 47:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 40 <= vo2max <= 43:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 18 <= age <= 25 :
                        if vo2max >= 48:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 44 <= vo2max <= 48:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 40 <= vo2max <= 43:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 36 <= vo2max <= 39:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 26 <= age <= 35 :
                        if vo2max >= 42:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 38 <= vo2max <= 42:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 34 <= vo2max <= 37:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 30 <= vo2max <= 33:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 36 <= age <= 45 :
                        if vo2max >= 37:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 33 <= vo2max <= 37:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 29 <= vo2max <= 32:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 25 <= vo2max <= 28:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 46 <= age <= 55 :
                        if vo2max >= 34:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 30 <= vo2max <= 34:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 26 <= vo2max <= 29:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 22 <= vo2max <= 25:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if 56 <= age <= 65 :
                        if vo2max >= 30:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 26 <= vo2max <= 30:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 22 <= vo2max <= 25:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 18 <= vo2max <= 21:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                    if age >= 65 :
                        if vo2max >= 27:
                            interprétation = "Supérieur\nTon VO2max est supérieur à la moyenne pour ta tranche d'âge, ce qui indique une excellente capacité cardiovasculaire"
                        elif 23 <= vo2max <= 27:
                            interprétation = "Excellent\nTu as une VO2max excellente pour ton âge, signe d'un très bon niveau de forme physique."
                        elif 19 <= vo2max <= 22:
                            interprétation = "Bon\nTon VO2max est bonne pour ton âge, témoignant d'une condition physique solide"
                        elif 15 <= vo2max <= 18:
                            interprétation = "Moyen\nTon VO2max se situe dans la moyenne pour ta tranche d'âge. Il y a de la marge pour progresser."
                        else:
                            interprétation = "Faible\nTon VO2max est faible pour ton âge. Essaye d'être moins sédentaire au quotidien."
                else:
                    interprétation = "Sexe non valide. Séléctionne 'Homme' ou 'Femme'."
                result.configure(text=f"Ton VO2max est de {vo2max:.2f} mL/min/kg.\n\n{interprétation}", wraplength=800,
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_VO2MAX(account_id))
    button_check.pack(padx=10, pady=20)

def VMA(account_id):
    sidebar_outil(account_id)
    navbar_outil(account_id, "Estimation VMA")

    Info = ctk.CTkLabel(master=app ,text="Pour une estimation plus précise, utilise la distance parcourue à fond en 6 minutes.", font=(font_secondaire, taille2))
    Info.pack(padx=50, pady=10)

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_VMA())
    distance_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(pady=(11, 5), padx=10)
    temps_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Temps (min)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    temps_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_VMA():
        try:
            distance = float(distance_entry.get().strip())
            try:
                temps_autre = int(temps_entry.get().strip())
                temps = temps_autre/60
                if distance <= 0 or temps <=0:
                    messagebox.showerror("Erreur", "La distance et le temps doivent être supérieur à 0 !")
                    return
                if distance <= 0 or temps <=0:
                    messagebox.showerror("Erreur", "La distance et le temps doivent être supérieur à 0 !")
                    return
            except ValueError:
                messagebox.showerror("Erreur", "Les minutes doivent être un nombre entier !")
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

                debut_zone1 = vma_estimée * 0.50
                fin_zone1 = vma_estimée * 0.60
                Zone1 = f"Zone 1 : Récupération active | {debut_zone1:.1f}km/h à {fin_zone1:.1f}km/h"
                debut_zone2 = vma_estimée * 0.60
                fin_zone2 = vma_estimée * 0.75
                Zone2 = f"Zone 2 : Fondamentale, base aérobie | {debut_zone2:.1f}km/h à {fin_zone2:.1f}km/h"
                debut_zone3 = vma_estimée * 0.75
                fin_zone3 = vma_estimée * 0.85
                Zone3 = f"Zone 3 : Seuil aérobie, amélioration de l’endurance| {debut_zone3:.1f}km/h à {fin_zone3:.1f}km/h"
                debut_zone4 = vma_estimée * 0.85
                fin_zone4 = vma_estimée * 0.95
                Zone4 = f"Zone 4 :  Seuil anaérobie, tolérance à l’effort intense | {debut_zone4:.1f}km/h à {fin_zone4:.1f}km/h"
                debut_zone5 = vma_estimée * 0.95
                Zone5 = f"Zone 5 : Vitesse maximale aérobie, puissance maximale | {debut_zone5:.1f}km/h à {vma_estimée:.1f}km/h"

                result.configure(text=f"Ta VMA est de {vma_estimée:.2f} km/h.\n\nTes Zones d’entraînement\n\n{Zone1}\n{Zone2}\n{Zone3}\n{Zone4}\n{Zone5}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: calcul_VMA())
    button_check.pack(padx=10, pady=10)

def zone_fc(account_id):
    sidebar_outil(account_id)
    navbar_outil(account_id, "Zones cardiaque")

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_zone(account_id))
    age_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Âge", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    age_entry.pack(pady=10, padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_zone(account_id):
        try:
            age = int(age_entry.get().strip())
            fc_max = 220 - age

            if age <= 0:
                messagebox.showerror("Erreur", "L'âge doit être supérieur à 0 !")
            if not age:
                messagebox.showerror("Erreur", "L'âge ne peut pas être vide !")
            debut_zone1 = fc_max*0.50
            fin_zone1 = fc_max*0.60
            Zone1 = f"Zone 1 : Récupération active - {debut_zone1:.0f}bpm à {fin_zone1:.0f}bpm"
            debut_zone2 = fc_max*0.60
            fin_zone2 = fc_max*0.70
            Zone2 = f"Zone 2 : Fondamentale, endurance de base | {debut_zone2:.0f}bpm à {fin_zone2:.0f}bpm"
            debut_zone3 = fc_max*0.70
            fin_zone3 = fc_max*0.80
            Zone3 = f"Zone 3 : Seuil aérobie, endurance active | {debut_zone3:.0f}bpm à {fin_zone3:.0f}bpm"
            debut_zone4 = fc_max*0.80
            fin_zone4 = fc_max*0.90
            Zone4 = f"Zone 4 :  Seuil anaérobie, résistance dure | {debut_zone4:.0f}bpm à {fin_zone4:.0f}bpm"
            debut_zone5 = fc_max*0.90
            Zone5 = f"Zone 5 : Vitesse maximale aérobie, puissance maximale | {debut_zone5:.0f}bpm à {fc_max:.0f}bpm"
            FC_max = f"Fréquence cardiaque maximum : {fc_max:.0f}bpm"

            result.configure(text=f"Tes Zones de Fréquence Cardiaque\n\n{Zone1}\n{Zone2}\n{Zone3}\n{Zone4}\n{Zone5}\n{FC_max}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_zone(account_id))
    button_check.pack(padx=10, pady=10)

def predicteur_temps(account_id):
    sidebar_outil(account_id)
    navbar_outil(account_id, "Prédicteur de performance")

    Info = ctk.CTkLabel(master=app ,text="N'oublie pas que cette prédiction est une estimation basée sur la\nthéorie"\
                         " et peut varier en fonction de nombreux facteurs\nle jour de la course !", font=(font_secondaire, taille2),
                         text_color=couleur_text)
    Info.pack(padx=50, pady=10)

    carte_connexion = ctk.CTkFrame(master=app, corner_radius=corner1, border_width=border2, border_color=couleur1, fg_color=couleur2)        
    carte_connexion.pack(pady=(20, 5), padx=20) 
    app.bind('<Return>', lambda event: calcul_temps(account_id))
    vma_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="VMA", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    vma_entry.pack(pady=(11, 5), padx=10)
    distance_entry = ctk.CTkEntry(master=carte_connexion, placeholder_text="Distance (km)", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    distance_entry.pack(pady=(5, 11), padx=10)

    cadre_result = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2)
    cadre_result.pack(pady=10)

    result = ctk.CTkLabel(master=cadre_result, text="🔒 Ta confidentialité est notre priorité : nous calculons ton temps de course\n directement sur ton appareil et ne stockons pas cette donnée.",
                           font=(font_secondaire, taille2), text_color=couleur1)
    result.pack(padx=50, pady=10)

    def calcul_temps(account_id):
        try:
            distance = float(distance_entry.get().strip())
            vma = float(vma_entry.get().strip())

            if distance <= 0 or vma <=0:
                messagebox.showerror("Erreur", "La distance et le temps doivent être supérieur à 0 !")
                return
            if not distance or not vma:
                messagebox.showerror("Erreur", "La distance et la vma ne peuvent pas être vides !")
                return
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

            result.configure(text=f"{interpretation}",
                                 anchor="w", justify="left")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: calcul_temps(account_id))
    button_check.pack(padx=10, pady=10)

def activer_pause(account_id, type_pause):
    curseur.execute("SELECT id FROM Pauses_v2 WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    try:
        #date('now') pour prendre direct la date aujourd'hui (c'est une fonction SQLite)
        curseur.execute("""INSERT INTO Pauses_v2 (account_id, type, date_debut)VALUES (?, ?, date('now'))""", (account_id, type_pause))
        con.commit()
        messagebox.showinfo("Enregistré", f"Pause {type_pause} activée !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", f"Erreur de base de données lors de l'activation de la pause {type_pause}.")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def arreter_pause(account_id):
    try:
        curseur.execute("""UPDATE Pauses_v2 SET date_fin = date('now')WHERE account_id = ? AND date_fin IS NULL""", (account_id,))
        con.commit()
        messagebox.showinfo("Enregistré", "Reprise d'activité enregistrée !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de l'activation de la reprise d'activité.")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def signaler_bug(account_id):
    sidebar_paramètre(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Signaler un bug", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(master=app ,text="📣 Nous te remercions pour ta contribution au développement de Sprintia." \
    "\nPour que le développeur puisse bien comprendre le bug, il faudrait détailler\nun maximum le bug que tu as rencontré.", 
    font=(font_principale, taille2))
    info.pack(padx=50, pady=(20, 10))

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(master=app, width=700, height=300, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille3),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(pady=10, padx=10)
    avis_entry.insert("0.0", "Description du bug :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if not avis:
            messagebox.showerror("Description du bug vide", "Veuillez remplir le champs description de bug !")
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Rapport de bug"
        body = f"Message de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            messagebox.showinfo("Première étape terminée", "Ton application de mail par défaut va s'ouvrir ! Il ne te resteras plus qu'à cliquer sur envoyer.")
            webbrowser.open(mailto_link)
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible d'ouvrir ton application mail. Vérifie que tu as une application pour gérer tes mails !")
    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def proposer_fonction(account_id):
    sidebar_paramètre(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Proposer une fonction", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(master=app ,text="📣 Nous te remercions pour ta contribution au développement de Sprintia." \
                "\nPour que le développeur puisse bien comprendre ta demande, il faudrait détailler\nun maximum ton idée de fonctionnalité",
                font=(font_principale, taille2))
    info.pack(padx=50, pady=(20, 10))

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(master=app, width=700, height=300, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille3),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(pady=10, padx=10)
    avis_entry.insert("0.0", "Description de votre fonctionnalité :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if not avis:
            messagebox.showerror("Proposition de fonctionnalité vide", "Veuille à remplir le champs fonctionnalité !")
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Proposition de nouvelle fonctionnalité"
        body = f"Message de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            messagebox.showinfo("Première étape terminée", "Ton application de mail par défaut va s'ouvrir ! Il ne te resteras plus qu'à cliquer sur envoyer.")
            webbrowser.open(mailto_link)
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible d'ouvrir ton application mail. Vérifie que tu as une application pour gérer tes mails. !")
    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def quoi_de_neuf(account_id):
    sidebar_paramètre(account_id)

    def podcast_open():
        messagebox.showinfo("Information", "Ton navigateur par défaut va s'ouvrir pour que tu puisses écouter le podcast.")
        webbrowser.open("https://drive.google.com/file/d/1wC3-FAmNuZtU5cx16RAwxUJ633HTNqIC/view?usp=drive_link")

    boite2 = ctk.CTkFrame(app, fg_color=couleur_fond)
    boite2.pack(side="right", expand=True, fill="both")
    header = ctk.CTkFrame(boite2, fg_color="transparent")
    header.pack(pady=10, padx=10)
    conteneur_patch_note = ctk.CTkFrame(boite2, fg_color=couleur2, corner_radius=corner1)
    conteneur_patch_note.pack(expand=True, fill="both", pady=(10, 15), padx=15)
    patch_note = ctk.CTkScrollableFrame(conteneur_patch_note, fg_color="transparent", scrollbar_button_color=couleur1,
                                           scrollbar_button_hover_color=couleur1_hover)
    patch_note.pack(expand=True, fill="both", pady=10, padx=10)

    Titre = ctk.CTkLabel(header, text="Quoi de neuf dans Sprintia 3.1", text_color=couleur_text, font=(font_secondaire, taille1))
    Titre.pack(side="left", padx=5)
    button_back = ctk.CTkButton(header, text="🎙️  Podcast", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=podcast_open)
    button_back.pack(side="left", padx=(20, 3))
    button_back = ctk.CTkButton(header, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_back.pack(side="left", padx=(3, 10))

    PatchNote = ctk.CTkLabel(patch_note, font=(font_principale, taille3), text_color=couleur1, wraplength=950, anchor="w", corner_radius=corner1,
        text="""Type : Mise à jour mineure\nDate de sortie : 31 Août 2025\n
    🆕 Nouvelles fonctionnalités
    • Option “Tous” : affiche désormais l’historique complet des entraînements.
    • "Quoi de neuf dans Sprintia 3.1" : nouvelle section dans les paramètres (accessible directement dans l’app).
    • Interprétation de l’IMC : ajout d’une phrase explicative au calculateur.
    • Zones de VMA : calcul et affichage par pourcentage, sur le modèle des zones de FC.
    • Nouveau statut “Pas commencé” pour les objectifs.
    • Nouvelle raison “Suspendre” pour la mise en pause des analyses.
    • Nouvelle donnée “Score” pour le football.
    • Nouveau mode Course pour l'enregistrement de données spécifique à la course.
    • Indulgence de course : cet algorithme va t'aider à ajuster ton kilométrage des 7 derniers jours pour rester dans une progression optimale.
    • Modification complète d’un objectif ou d’une compétition via un seul bouton (date, lieu, statut…).\n
    📊 Améliorations
    • Filtres persistants : mémorisation des choix (ex. conserver “1 mois” lors du passage d’Extérieur à Musculation).
    • Conseils et interprétations enrichis dans Charge d’entraînement.
    • Zones de FC : affichage de la FC Max.
    • Estimation VO₂max : ajout d’une interprétation des zones.
    • Aide intégrée : explications sur le diverses choses lors de la première utilisation de Sprintia.
    • Tableaux réorganisés pour plus de cohérence.
    • Affichage clair en cas d’absence de données dans Objectifs et Compétitions (remplace “None” ou cellules vides).
    • Nettoyage de la base de données pour plus de rapidité.
    • Mettre un autre type de pause même si une pause est déjà active (ex : passer de 'blessure' à 'vacances').
    • Programme bêta disponible depuis les paramètres.
    • Accès à un podcast qui présente les nouveautés de Sprintia.
    • Accès aux actu sur Sprintia.
    • Sprintia est disponible sur GitHub.
    • Après l’enregistrement d’une activité, d'un objectif ou d'une compétition, tu reviens automatiquement à la page précédente — pour gagner du temps.\n
    🐛 Corrections de bugs
    • Bio trop longue : problème résolu dans le profil et la modification de profil.
    • Coupure visuelle corrigée dans les en-têtes et le nom d’historique d’activité (Extérieur).
    • Longueur excessive des noms d’activité corrigée lors de la suppression.
    • Diverses corrections d’orthographe et fautes dans l’app.
    • Sprintia va désormais te tutoyer pour être plus proche de son utilisateur.
    • Gestion des erreurs du format de la date à l'ajout d'un objectif et d'une compétition.
    • Correction de bug lors de la suppression d'une activité.
    • Sécurité des données amélioré.
    • Amélioration légère de l'interface du graphique de Charge d'entraînement.
    • Optimisations du code pour la Side-Bar."""
    , justify="left")
    PatchNote.pack(expand=True, fill="both", padx=5, pady=5)
    aide_podcast(account_id)

def avis (account_id):
    sidebar_paramètre(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Rédiger un avis", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    info = ctk.CTkLabel(master=app ,text="📣 Nous te remercions pour ta contribution au développement de Sprintia.", 
                        font=(font_principale, taille2))
    info.pack(padx=50, pady=(20, 10))

    app.bind('<Return>', lambda event: envoyer())
    avis_entry = ctk.CTkTextbox(master=app, width=700, height=300, corner_radius=corner1, fg_color=couleur2, font=(font_principale, taille3),
                                scrollbar_button_color=couleur1, scrollbar_button_hover_color=couleur1_hover, text_color=couleur1,
                                border_color=couleur1, border_width=border1)
    avis_entry.pack(pady=10, padx=10)
    avis_entry.insert("0.0", "Votre avis :\n")

    def envoyer():
        avis = avis_entry.get("1.0", "end").strip()
        if not avis:
            messagebox.showerror("Avis vide", "Veuille à remplir le champs avis !")
            return
        #destinataire
        email_receiver = 'gabchap486@gmail.com'
        #objet
        subject = "Avis sur Sprintia"
        body = f"Message de l'utilisateur:\n{avis}"
        mailto_link = f"mailto:{email_receiver}?subject={quote(subject)}&body={quote(body)}"
        try:
            messagebox.showinfo("Première étape terminée", "Ton application de mail par défaut va s'ouvrir ! Il ne te resteras plus qu'à cliquer sur envoyer.")
            webbrowser.open(mailto_link)
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible d'ouvrir ton application mail. Vérifie que tu as une application pour gérer tes mails. !")
    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: envoyer())
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), parametre(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def mettre_en_pause_les_analyses_depuis_indulgence(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Mettre en pause les analyses", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=50, pady=20)
    info = ctk.CTkLabel(master=app ,text="Si tu as besoin de souffler, ou que tu t'es blessé, tu peux\nmettre en pause les " \
    "analyses pour te reposer et récupérer.", font=(font_principale, taille2))
    info.pack(padx=50, pady=(25, 10))

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    curseur.execute("SELECT type FROM Pauses_v2 WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    result = curseur.fetchall()
    if result == []:
        info_statut = ctk.CTkLabel(master=frame, text="Ton statut d'entraînement actuel : Actif", font=(font_principale, taille2))
        info_statut.pack(padx=0, pady=10)
    elif result == [('vacances',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel: Vacances", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == [('blessure',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel : Blessure", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == [('suspendre',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel : Suspendre", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    else:
        messagebox.showerror("Erreur", "Statut inconnu !")
    app.bind('<Return>', lambda event: enregistrer_activité(account_id))
    options = {"Vacances": "Vacances", "Blessure": "Blessure", "Suspendre": "Suspendre", "Reprendre les analyses": "Reprendre"}
    combo_statut = ctk.CTkComboBox(master=frame, values=list(options.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    combo_statut.pack(pady=10)
    combo_statut.set("Séléctionne la raison")

    def enregistrer_activité(account_id):
        statut_choisi = combo_statut.get()
        statut = options[statut_choisi]
        try:
            if statut == "Vacances":
                activer_pause(account_id, "vacances")
            elif statut == "Blessure":
                activer_pause(account_id, "blessure")
            elif statut == "Suspendre":
                activer_pause(account_id, "suspendre")
            elif statut == "Reprendre":
                arreter_pause(account_id)
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: enregistrer_activité(account_id))
    button_check.pack(side="left", padx=5, pady=10)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), indulgence_de_course(account_id)])
    button_retour.pack(side="left", padx=5, pady=10)

def mettre_en_pause_les_analyses(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Mettre en pause les analyses", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=50, pady=20)
    info = ctk.CTkLabel(master=app ,text="Si tu as besoin de souffler, ou que tu t'es blessé, tu peux\nmettre en pause les " \
    "analyses pour te reposer et récupérer.", font=(font_principale, taille2))
    info.pack(padx=50, pady=(25, 10))

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=10)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))

    curseur.execute("SELECT type FROM Pauses_v2 WHERE account_id = ? AND date_fin IS NULL", (account_id,))
    result = curseur.fetchall()
    if result == []:
        info_statut = ctk.CTkLabel(master=frame, text="Ton statut d'entraînement actuel : Actif", font=(font_principale, taille2))
        info_statut.pack(padx=0, pady=10)
    elif result == [('vacances',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel: Vacances", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == [('blessure',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel : Blessure", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    elif result == [('suspendre',)]:
        info_statut_actif = ctk.CTkLabel(master=frame, text=f"Ton statut d'entraînement actuel : Suspendre", font=(font_principale, taille2))
        info_statut_actif.pack(padx=0, pady=10)
    else:
        messagebox.showerror("Erreur", "Statut inconnu !")
    app.bind('<Return>', lambda event: enregistrer_activité(account_id))
    options = {"Vacances": "Vacances", "Blessure": "Blessure", "Suspendre": "Suspendre", "Reprendre les analyses": "Reprendre"}
    combo_statut = ctk.CTkComboBox(master=frame, values=list(options.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    combo_statut.pack(pady=10)
    combo_statut.set("Séléctionne la raison")

    def enregistrer_activité(account_id):
        statut_choisi = combo_statut.get()
        statut = options[statut_choisi]
        try:
            if statut == "Vacances":
                activer_pause(account_id, "vacances")
            elif statut == "Blessure":
                activer_pause(account_id, "blessure")
            elif statut == "Suspendre":
                activer_pause(account_id, "suspendre")
            elif statut == "Reprendre":
                arreter_pause(account_id)
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: enregistrer_activité(account_id))
    button_check.pack(side="left", padx=5, pady=10)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), charge_entraînement(account_id)])
    button_retour.pack(side="left", padx=5, pady=10)

def modifier_password(account_id):
    navbar_mon_compte(account_id, "Mot de passe oublié")
    frame2 = ctk.CTkFrame(master=app, fg_color="transparent")        
    frame2.pack(pady=(10, 20))
    carte = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)        
    carte.pack(pady=(10, 20))

    info = ctk.CTkLabel(master=frame2 ,text="Mot de passe oublié ? Pas de panique, remplis le formulaire ci-dessus et ton mot de passe sera modifié",
                         font=(font_secondaire, taille2), wraplength=800)
    info.pack(padx=50)

    app.bind('<Return>', lambda event: new_username(account_id))
    password_entry = ctk.CTkEntry(master=carte, placeholder_text="Nouveau mot de passe", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=370, show="*")
    password_entry.pack(pady=(12, 5), padx=11)
    password_entry2 = ctk.CTkEntry(master=carte, placeholder_text="Confirme ton nouveau mot de passe", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=370, show="*")
    password_entry2.pack(pady=(5, 12), padx=11)
    def new_username(account_id):
        new_password = password_entry.get()
        new_password2 = password_entry2.get()
        password_encode = new_password.encode("UTF-8")
        if new_password == new_password2:
            try:
                if not password_entry or not password_entry2:
                    messagebox.showerror("Erreur", "Le mots de passe ne peut pas être vide. Veuille à remplir tous les champs !")
                    return
                else:
                    if (password_valide(new_password)):
                        sha256 = hashlib.sha256()
                        sha256.update(password_encode)
                        hashed_password = sha256.hexdigest()
                        con.execute("UPDATE Account SET password = ? WHERE id = ?", (hashed_password, account_id))
                        con.commit()
                        messagebox.showinfo("Enregistré", "Ton mots de passe à bien été modifié !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur base de données", "Erreur de base de données lors du changement de ton mot de passe !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        else:
            messagebox.showerror("Erreur", "Les mots de passe saisis ne correspondent pas !")
    button_check = ctk.CTkButton(master=app, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: new_username(account_id))
    button_check.pack(padx=10, pady=15)

def modifier_compte(account_id):
    navbar_mon_compte(account_id, "Modifier")
    info_pack = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)
    info_pack.pack(pady=10)

    frame_username = ctk.CTkFrame(master=info_pack, fg_color="transparent")        
    frame_username.pack(padx=12, pady=(10, 5))
    frame_sport = ctk.CTkFrame(master=info_pack, fg_color="transparent")        
    frame_sport.pack(padx=12, pady=5)
    frame_bio = ctk.CTkFrame(master=info_pack, fg_color="transparent")        
    frame_bio.pack(padx=12, pady=(5, 10))

    enregistrer = ctk.CTkFrame(master=app, fg_color="transparent")        
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

    app.bind('<Return>', lambda event: enregistré())
    if bio is None:
        width_entry = 275
    else:
        if len(bio) < 30:
            width_entry = 275
        else:
            width_entry = 375
    LABEL_WIDTH = 250
    pseudo_label = ctk.CTkLabel(master=frame_username, text="Ton pseudo : ", font=(font_secondaire, taille2), text_color=couleur1,
                                width=LABEL_WIDTH)
    pseudo_label.pack(side="left")
    pseudo_entry = ctk.CTkEntry(master=frame_username, placeholder_text=f"{username}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=width_entry)
    pseudo_entry.pack(side="left", padx=(0, 10), pady=(12,0))

    sport_label = ctk.CTkLabel(master=frame_sport, text="Ton sport favoris : ", font=(font_secondaire, taille2), text_color=couleur1,
                               width=LABEL_WIDTH)
    sport_label.pack(side="left")
    sport_favoris_entry = ctk.CTkEntry(master=frame_sport, placeholder_text=f"{sport if sport is not None else "Ajoute un sport favoris."}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=width_entry)
    sport_favoris_entry.pack(side="left", padx=(0, 12))

    bio_label = ctk.CTkLabel(master=frame_bio, text="Ta bio : ", font=(font_secondaire, taille2), text_color=couleur1,
                              width=LABEL_WIDTH)
    bio_label.pack(side="left", anchor="n")
    if bio is None:
        bio_entry = ctk.CTkEntry(master=frame_bio, placeholder_text=f"{bio if bio is not None else "Ajoute une bio."}", border_color=couleur1, fg_color=couleur1,
                                      height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                      text_color="white", width=width_entry)
        bio_entry.pack(side="left", padx=(0, 10), pady=(0,11))
    else:
        if len(bio) < 30:
            bio_entry = ctk.CTkEntry(master=frame_bio, placeholder_text=f"{bio}", border_color=couleur1, fg_color=couleur1,
                                          height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                          text_color="white", width=width_entry)
            bio_entry.pack(side="left", padx=(0, 10), pady=(0,11))
        else:
            bio_entry = ctk.CTkTextbox(master=frame_bio, width=width_entry, corner_radius=corner1, fg_color=couleur1,
                                        font=(font_principale, taille3),
                                        scrollbar_button_color=couleur2, scrollbar_button_hover_color=couleur2_hover,
                                        text_color=couleur_text,
                                        border_color=couleur1, border_width=border1)
            bio_entry.pack(pady=(0, 10), padx=(0, 10), fill="both", expand=True)
            bio_entry.insert("0.0", bio)

    def enregistré():
        new_username = pseudo_entry.get().strip()
        new_sport = sport_favoris_entry.get().strip()
        try:
            new_bio = bio_entry.get("1.0", "end").strip()
        except: 
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
            messagebox.showinfo("Opération réussi", "Ton compte a été mis à jour avec succès !")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur base de données", "Ce pseudo est déjà utilisé, réessaye avec un autre pseudo !")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la mise à jour de ton compte !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=enregistrer, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                         command=lambda: enregistré())
    button_enregistrer.pack(side="left", padx=10)

def supprimer_compte(account_id):
    navbar_mon_compte(account_id, "Supprimer mon compte")
    info = ctk.CTkFrame(master=app, fg_color="transparent")
    info.pack()
    carte = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur2, border_width=border1, border_color=couleur1)        
    carte.pack(pady=(10, 20))

    info = ctk.CTkLabel(master=info ,text="Ton compte est sur le point d'être supprimé. Ça veut dire que toutes tes données " \
    "et ton accès à à Sprintia sera perdu, et il n'y aura pas de retour en arrière possible.", font=(font_secondaire, taille2), wraplength=800)
    info.pack(padx=50, pady=10)
    info2 = ctk.CTkLabel(master=carte ,text="Es-tu vraiment certain de vouloir continuer ?", font=(font_principale, taille2),
                         text_color=couleur1)
    info2.pack(padx=50, pady=10) 

    options_suppr = {"Oui": "oui", "Non" : "non"}

    options = ctk.CTkComboBox(master=carte, values=list(options_suppr.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    options.pack(pady=10)
    options.set("Séléctionnez Oui ou Non")

    def valider(account_id):
        options_choisi = options.get()
        option = options_suppr[options_choisi]
        if option == "oui":
            try:
                curseur.execute("DELETE FROM Pauses_v2 WHERE account_id = ?", (account_id,))

                curseur.execute("DELETE FROM Objectif WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Compétition WHERE account_id = ?", (account_id,))

                curseur.execute("DELETE FROM Activité WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Activité_extérieur WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Activité_running WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Activité_intérieur WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Activité_musculation WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Activité_football WHERE account_id = ?", (account_id,))

                curseur.execute("DELETE FROM Account WHERE id = ?", (account_id,))

                curseur.execute("DELETE FROM Aide_rpe WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Aide_bienvenue WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Aide_objectif WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Aide_compétition WHERE account_id = ?", (account_id,))
                curseur.execute("DELETE FROM Aide_podcast WHERE account_id = ?", (account_id,))
                con.commit()
                messagebox.showinfo("Opération réussi", "Compte supprimé avec succès ! Au revoir !")
                vider_fenetre(app)
                inscription()
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression du compte !")
            except Exception as e:            
                messagebox.showerror("Erreur", "Une erreur inattendue s'est produite, réessaye !")
        else:
            messagebox.showinfo("Suppression de compte annulé", "Ton compte n'a pas été supprimé !")
            return
    button_check = ctk.CTkButton(master=app, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: valider(account_id))
    button_check.pack(padx=10, pady=15)

def ajouter_compétition(account_id):
    sidebar_performance(account_id)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack()
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(pady=(10, 5), padx=10)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(pady=(5, 5), padx=10)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(pady=(5, 10), padx=10)
    frame4 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame4.pack(pady=20)

    Titre = ctk.CTkLabel(master=frame ,text="Ajouter une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20, side="left")

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire"]
    app.bind('<Return>', lambda event: sql_ajouté(account_id))

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

    def sql_ajouté(account_id):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip()
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu_avant = lieu_entry.get().strip()
        priorité_avant = priorite_entry.get().strip()
        if priorité_avant == "Priorité":
            priorité = None
        else:
            priorité = priorité_avant
        if not lieu_avant :
            lieu = None
        else:
            lieu = lieu_avant

        if not nom or not date_str or not sport or not objectif:
            messagebox.showerror("Erreur", "Veuille à remplir tous les champs !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur de format de date", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("INSERT INTO Compétition (account_id, nom, date, sport, objectif, lieu, priorité) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, nom, date, sport, objectif, lieu, priorité))
                con.commit()
                messagebox.showinfo("Enregistré", "Ta compétition a été enregistré, bonne chance !")
                vider_fenetre(app)
                compétition(account_id)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(side="left", padx=5)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), compétition(account_id)])
    button_back.pack(side="left", padx=5)

def supprimer_compétition(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Supprimer une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(pady=10)

    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de la compétition à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=350)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, nom, date, lieu FROM Compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Nom", "Date", "Lieu"]
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
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille2))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_competitions_disponibles = [comp[0] for comp in result]

                if choix_id_saisi in ids_competitions_disponibles:
                    competition_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Compétition WHERE id = ? AND account_id = ?", (competition_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Compétition supprimée avec succès.")
                    vider_fenetre(app)
                    compétition(account_id)
                else:
                    messagebox.showerror("Erreur", "L'ID de la compétition saisie n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), compétition(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def modifier_compétition_étape2(account_id, result_id):    
    id_modifier = result_id[0][0]
    sidebar_performance(account_id)
    try:
        curseur.execute("SELECT date, sport, nom, objectif, lieu, priorité FROM Compétition WHERE id = ? AND account_id = ?",(id_modifier, account_id))
        data_compétition = curseur.fetchall()
        premiere_ligne = data_compétition[0]
        date1 = premiere_ligne[0]
        date_conversion = datetime.strptime(date1, "%Y-%m-%d")
        date_value = date_conversion.strftime("%d-%m-%Y")
        sport_value = premiere_ligne[1]
        nom_value = premiere_ligne[2]
        objectif_value = premiere_ligne[3]
        lieu_value = premiere_ligne[4]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ta compétition !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack()
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(pady=(10, 5), padx=10)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(pady=(5, 5), padx=10)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(pady=(5, 10), padx=10)
    frame4 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame4.pack(pady=20)

    Titre = ctk.CTkLabel(master=frame ,text="Modifier une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20, side="left")

    option = ["Événement Principal", "Événement Secondaire", "Événement tertiaire"]
    app.bind('<Return>', lambda event: sql_ajouté(account_id))

    date_entry = ctk.CTkEntry(master=frame1, placeholder_text=f"{date_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="left", padx=(0, 5))    
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text=f"{sport_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="right", padx=(5, 0))

    nom_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{nom_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    nom_entry.pack(side="left", padx=(0, 5))
    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{objectif_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    objectif_entry.pack(side="right", padx=(5, 0))

    lieu_entry = ctk.CTkEntry(master=frame3, placeholder_text=f"{lieu_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    lieu_entry.pack(side="left", padx=(0, 5))
    priorite_entry = ctk.CTkComboBox(master=frame3, values=option, font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    priorite_entry.pack(side="right", padx=(5, 0))
    priorite_entry.set("Priorité")

    def sql_ajouté(account_id):
        nom = nom_entry.get().strip()
        date_str = date_entry.get().strip()
        sport = sport_entry.get().strip()
        objectif = objectif_entry.get().strip()
        lieu = lieu_entry.get().strip()
        priorité = priorite_entry.get().strip()

        if not sport:
            sport = sport_value
        if not date_str:
            date_str = date_value
        if not objectif:
            objectif = objectif_value
        if not nom:
            nom = nom_value
        if not lieu:
            lieu = lieu_value

        if priorité == "Priorité":
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Priorité' !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur de format de date", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("UPDATE Compétition SET nom = ?, date = ?, sport = ?, objectif = ?, lieu = ?, priorité = ? WHERE id = ? AND account_id = ?", 
                                (nom, date, sport, objectif, lieu, priorité, id_modifier, account_id))
                con.commit()
                messagebox.showinfo("Enregistré", "Ta compétition a été modifiée avec succès !")
                vider_fenetre(app)
                compétition(account_id)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(side="left", padx=5)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), modifier_compétition_étape1(account_id)])
    button_back.pack(side="left", padx=5)
    aide_compétition(account_id)

def modifier_compétition_étape1(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Modifier une compétition", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(padx=50, pady=(20, 0))

    app.bind('<Return>', lambda event: valider(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de la compétition à modifier", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=300)
    choix_entry.pack(pady=10, side="left", padx=5)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, nom, date, sport, lieu, priorité FROM Compétition WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["ID", "Nom", "Date", "Sport", "Lieu", "Priorité"]

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
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                         text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistré", font=(font_principale, taille1))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def valider(account_id):
            choix = choix_entry.get().strip()
            try:
                if not choix:
                    messagebox.showerror("Erreur", "ID ne peut pas être vide ! Merci de saisir un identifiant !")
                try:
                    id = int(choix)
                    if id < 0:
                        messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                        return
                except:
                    messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                    return

                curseur.execute("SELECT id FROM Compétition WHERE id = ? AND account_id = ?", (id, account_id))
                result_id = curseur.fetchall()
                if result_id:
                    vider_fenetre(app)
                    modifier_compétition_étape2(account_id, result_id)
                else:
                    messagebox.showerror("Erreur", "ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de la compétition !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
    button_check = ctk.CTkButton(master=frame_boutons, text="Suivant", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: valider(account_id))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), compétition(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def toute_compétition(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app, text="Toutes les compétitions", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=(25, 10))

    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT nom, date, sport, objectif, lieu, priorité FROM Compétition WHERE account_id = ? ORDER BY date ASC", (account_id,))
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
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition n'a été enregistrée.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_retour = ctk.CTkButton(master=app, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), compétition(account_id)])
    button_retour.pack(padx=10, pady=20)

def compétition(account_id):
    sidebar_performance(account_id)

    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=20)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Compétition")
    button_autre = ctk.CTkButton(master=navbar, text="🔚 Toutes les compétitions", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    width=260,
                                    command=lambda: [vider_fenetre(app), toute_compétition(account_id)])
    button_autre.pack(side="left", padx=10)

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), ajouter_compétition(account_id)])
    button_ajouter.pack(side="left", padx=2)
    button_modifier = ctk.CTkButton(master=frame_boutons, text="✏️  Modifier", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), modifier_compétition_étape1(account_id)])
    button_modifier.pack_forget()
    button_delete = ctk.CTkButton(master=frame_boutons, text="🗑️  Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), supprimer_compétition(account_id)])
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
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=15, pady=15, sticky="ew")
                button_modifier.pack(side="left", padx=2)
                button_delete.pack(side="left", padx=2)
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucune compétition futur n'a été enregistrée.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes compétitions !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def ajouter_objectif(account_id):
    sidebar_performance(account_id)

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack()
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(pady=(10, 5), padx=10)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(pady=(5, 5), padx=10)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(pady=(5, 10), padx=10)
    frame4 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame4.pack(pady=20)

    options_statut = {"Pas encore démarré":"Pas encore démarré", "En cours": "En cours", "Atteint" : "Atteint", "Non-atteint" : "Non-atteint"}
    options_niveau = {"Débutant": "Débutant", "Fondations": "Fondations", "Intermédiaire" : "Intermédiaire", "Avancé": "Avancé", "Expert": "Expert", "Maîtrise": "Maîtrise"}
    Titre = ctk.CTkLabel(master=frame ,text="Ajouter un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    app.bind('<Return>', lambda event: sql_ajouté(account_id))
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
    fréquence_entry = ctk.CTkEntry(master=frame2, placeholder_text="Fréquence (ex: 2x/semaine)", border_color=couleur1, fg_color=couleur1,
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

    def sql_ajouté(account_id):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip()
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau_choisi = niveau_entry.get()
        niveau = options_niveau[niveau_choisi]
        statut_choisi = statut_entry.get()
        statut = options_statut[statut_choisi]

        if not sport or not date_str or not objectif or not fréquence or not niveau or not statut:
            messagebox.showerror("Erreur", "Merci de remplir tous les champs !")
            return
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("INSERT INTO Objectif (account_id, sport, date, objectif, fréquence, niveau_début, statut) VALUES (?, ?, ?, ?, ?, ?, ?)", (account_id, sport, date, objectif, fréquence, niveau, statut))
                con.commit()
                messagebox.showinfo("Enregistré", "Ton objectif a été enregistré, bonne chance !")
                vider_fenetre(app)
                objectifs(account_id)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de l'ajout de ton objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                        command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(side="left", padx=5)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), objectifs(account_id)])
    button_back.pack(side="left", padx=5)

def modifier_objectif_étape2(account_id, result_id):    
    id_modifier = result_id[0][0]
    sidebar_performance(account_id)
    try:
        curseur.execute("SELECT date, objectif, fréquence, sport FROM Objectif WHERE id = ? AND account_id = ?",(id_modifier, account_id))
        data_objectif = curseur.fetchall()
        premiere_ligne = data_objectif[0]
        date1 = premiere_ligne[0]
        date_conversion = datetime.strptime(date1, "%Y-%m-%d")
        date_value = date_conversion.strftime("%d-%m-%Y")
        objectif_value = premiere_ligne[1]
        frequence_value = premiere_ligne[2]
        sport_value = premiere_ligne[3]
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ton objectif !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=(20, 10))
    frame_tout = ctk.CTkFrame(master=app, fg_color=couleur2, corner_radius=corner1)
    frame_tout.pack()
    frame1 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame1.pack(pady=(10, 5), padx=10)
    frame2 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame2.pack(pady=(5, 5), padx=10)
    frame3 = ctk.CTkFrame(master=frame_tout, fg_color=couleur2, corner_radius=corner1)
    frame3.pack(pady=(5, 10), padx=10)
    frame4 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame4.pack(pady=20)

    options_statut = {"Pas encore démarré":"Pas encore démarré", "En cours": "En cours", "Atteint" : "Atteint", "Non-atteint" : "Non-atteint"}
    options_niveau = {"Débutant": "Débutant", "Fondations": "Fondations", "Intermédiaire" : "Intermédiaire", "Avancé": "Avancé", "Expert": "Expert", "Maîtrise": "Maîtrise"}
    
    Titre = ctk.CTkLabel(master=frame ,text="Modifier un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    app.bind('<Return>', lambda event: sql_ajouté(account_id))
    sport_entry = ctk.CTkEntry(master=frame1, placeholder_text=f"{sport_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    sport_entry.pack(side="left", padx=(0, 5))
    date_entry = ctk.CTkEntry(master=frame1, placeholder_text=f"{date_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    date_entry.pack(side="right", padx=(5, 0))

    objectif_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{objectif_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    objectif_entry.pack(side="left", padx=(0, 5))
    fréquence_entry = ctk.CTkEntry(master=frame2, placeholder_text=f"{frequence_value}", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    fréquence_entry.pack(side="right", padx=(5, 0))

    niveau_entry = ctk.CTkComboBox(master=frame3, values=list(options_niveau.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    niveau_entry.pack(side="left", padx=(0, 5))
    niveau_entry.set("Level final")
    statut_entry = ctk.CTkComboBox(master=frame3, values=list(options_statut.keys()), font=(font_principale, taille3), height=button_height, 
                                    state="readonly", border_width=border1, border_color=couleur1, button_color=couleur1, fg_color=couleur1,
                                    corner_radius=corner2, width=275, dropdown_fg_color=couleur1, dropdown_font=(font_principale, taille3),
                                    dropdown_hover_color = couleur1_hover, text_color="white", dropdown_text_color="white")
    statut_entry.pack(side="right", padx=(5, 0))
    statut_entry.set("Statut de l'objectif")

    def sql_ajouté(account_id):
        sport = sport_entry.get().strip()
        date_str = date_entry.get().strip()
        objectif = objectif_entry.get().strip()
        fréquence = fréquence_entry.get().strip()
        niveau_choisi = niveau_entry.get()
        try:
            niveau = options_niveau[niveau_choisi]
        except Exception: 
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Niveau final' !")
            return
        statut_choisi = statut_entry.get()
        try:
            statut = options_statut[statut_choisi]
        except Exception:
            messagebox.showerror("Erreur", "Merci de remplir le champs 'Statut de l'objectif' !")
            return
        if not sport:
            sport = sport_value
        if not date_str:
            date_str = date_value
        if not objectif:
            objectif = objectif_value
        if not fréquence:
            fréquence = frequence_value
        try:
            date_conversion = datetime.strptime(date_str, '%d-%m-%Y')
            date = date_conversion.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Erreur", "La date doit être au format JJ-MM-AAAA !")
            return
        else:
            try:
                curseur.execute("UPDATE Objectif SET sport = ?, date = ?, objectif = ?, fréquence = ?, niveau_fin = ?, statut = ? WHERE id = ? AND account_id = ?",
                    (sport, date, objectif, fréquence, niveau, statut, id_modifier, account_id))
                con.commit()
                messagebox.showinfo("Enregistré", "Ton objectif a été modifié avec succès!")
                vider_fenetre(app)
                objectifs(account_id)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de ton objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_enregistrer = ctk.CTkButton(master=frame4, text="Enregistrer", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                        command=lambda: sql_ajouté(account_id))
    button_enregistrer.pack(side="left", padx=5)
    button_back = ctk.CTkButton(master=frame4, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), modifier_objectif_étape1(account_id)])
    button_back.pack(side="left", padx=5)
    aide_objectif(account_id)

def modifier_objectif_étape1(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Modifier un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(padx=50, pady=(20, 0))

    app.bind('<Return>', lambda event: valider(account_id))
    choix_entry = ctk.CTkEntry(frame1, placeholder_text="ID de l'objectif à modifier", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=5)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, date, niveau_début, niveau_fin, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Date", "Level début", "Level fin", "Statut"]

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
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré", font=(font_principale, taille1))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def valider(account_id):
            choix = choix_entry.get().strip()
            try:
                if not choix:
                    messagebox.showerror("Erreur", "ID ne peut pas être vide ! Merci de saisir un identifiant !")
                try:
                    id = int(choix)
                    if id < 0:
                        messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                        return
                except:
                    messagebox.showerror("Erreur", "ID doit être un nombre entier positif !")
                    return

                curseur.execute("SELECT id FROM Objectif WHERE id = ? AND account_id = ?", (id, account_id))
                result_id = curseur.fetchall()
                if result_id:
                    vider_fenetre(app)
                    modifier_objectif_étape2(account_id, result_id)
                else:
                    messagebox.showerror("Erreur", "ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la modification de l'objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, veuillez réessayer !")
    button_check = ctk.CTkButton(master=frame_boutons, text="Suivant", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: valider(account_id))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), objectifs(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def supprimer_objectif(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app ,text="Supprimer un objectif", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=20)

    frame1 = ctk.CTkFrame(master=app, fg_color="transparent")
    frame1.pack(pady=10)

    app.bind('<Return>', lambda event: supression(account_id))
    choix_entry = ctk.CTkEntry(master=frame1, placeholder_text="ID de l'objectif à supprimer", border_color=couleur1, fg_color=couleur1,
                                  height=entry_height, font=(font_principale, taille3), corner_radius=corner1, placeholder_text_color ="white",
                                  text_color="white", width=275)
    choix_entry.pack(pady=10, side="left", padx=10)

    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(0, 10))
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
        curseur.execute("SELECT id, sport, date, objectif, statut FROM Objectif WHERE account_id = ?", (account_id,))
        result = curseur.fetchall()
        headers = ["ID", "Sport", "Date", "Objectif", "Statut"]
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
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille2))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)

        def supression(account_id):
            choix = choix_entry.get().strip()
            try:
                choix_id_saisi = int(choix)
                ids_objectifs_disponibles = [obj[0] for obj in result]

                if choix_id_saisi in ids_objectifs_disponibles:
                    objectif_id_db = choix_id_saisi
                    curseur.execute("DELETE FROM Objectif WHERE id = ? AND account_id = ?", (objectif_id_db, account_id))
                    con.commit()
                    messagebox.showinfo("Suppression réussie", "Objectif supprimé avec succès.")
                    vider_fenetre(app)
                    objectifs(account_id)
                else:
                    messagebox.showerror("Erreur", "L'ID de l'objectif saisi n'existe pas ou n'appartient pas à ton compte !")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", "Erreur de base de données lors de la suppression de l'objectif !")
            except Exception as e:
                messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_check = ctk.CTkButton(master=frame_boutons, text="Valider", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: supression(account_id))
    button_check.pack(side="left", padx=5, pady=20)
    button_retour = ctk.CTkButton(master=frame_boutons, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                 command=lambda: [vider_fenetre(app), objectifs(account_id)])
    button_retour.pack(side="left", padx=5, pady=20)

def tout_objectif(account_id):
    sidebar_performance(account_id)

    Titre = ctk.CTkLabel(master=app, text="Tous les objectifs", font=(font_secondaire, taille1))
    Titre.pack(padx=50, pady=(25, 10))

    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)
    try:
            curseur.execute("SELECT sport, date, objectif, fréquence, niveau_début, niveau_fin, statut FROM Objectif WHERE account_id = ? ORDER BY date ASC", (account_id,))
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
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
            else:
                pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1))
                pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    button_retour = ctk.CTkButton(master=app, text="🔙 Retour", fg_color=couleur2, hover_color=couleur2_hover,
                                    corner_radius=corner2, height=button_height, text_color=couleur1,
                                    font=(font_principale, taille3),
                                    command=lambda: [vider_fenetre(app), objectifs(account_id)])
    button_retour.pack(padx=10, pady=20)

def objectifs(account_id):
    sidebar_performance(account_id)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=20)
    frame_boutons = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_boutons.pack(pady=(20, 5))
    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Objectif")
    button_autre = ctk.CTkButton(master=navbar, text="🔚 Tous les objectifs", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    width=260,
                                    command=lambda: [vider_fenetre(app), tout_objectif(account_id)])
    button_autre.pack(side="left", padx=10)

    button_ajouter = ctk.CTkButton(master=frame_boutons, text="➕  Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), ajouter_objectif(account_id)])
    button_ajouter.pack(side="left", padx=2)
    button_modifier = ctk.CTkButton(master=frame_boutons, text="✏️  Modifier", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), modifier_objectif_étape1(account_id)])
    button_modifier.pack_forget()
    button_delete = ctk.CTkButton(master=frame_boutons, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), supprimer_objectif(account_id)])
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
                    label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                        text_color=couleur_text, wraplength=130)
                    label.grid(row=row_idx + 1, column=col_idx, padx=6, pady=15, sticky="ew")
            button_modifier.pack(side="left", padx=2)
            button_delete.pack(side="left", padx=2)
        else:
            pas_données = ctk.CTkLabel(master=tableau_frame, text="Aucun objectif futur n'a été enregistré.", font=(font_principale, taille1))
            pas_données.grid(row=1, column=0, columnspan=len(headers), pady=20)
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de tes objectifs!")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

def indulgence_de_course(account_id):
    sidebar_performance(account_id)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=20)

    D28J = date_actuelle - timedelta(days=28)
    D28J_str = D28J.strftime('%Y-%m-%d')
    curseur.execute("SELECT distance FROM activité_running WHERE account_id = ? AND date_activité >= ?", (account_id, D28J_str))
    distance28J = [row[0] for row in curseur.fetchall()]
    distance_moyenne_des_derniers_28_jours = sum(distance28J) / len(distance28J) if distance28J else 0
    if distance_moyenne_des_derniers_28_jours < 10:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.18
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.25
    elif 10 <= distance_moyenne_des_derniers_28_jours <= 20:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.15
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.20
    elif 20 <= distance_moyenne_des_derniers_28_jours <= 40:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.12
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.15
    elif 40 <= distance_moyenne_des_derniers_28_jours <= 60:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.09
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.12
    else:
        distance_maximumconseillé_début = distance_moyenne_des_derniers_28_jours*1.06
        distance_maximumconseillé_fin = distance_moyenne_des_derniers_28_jours*1.10

    D7J = date_actuelle - timedelta(days=7)
    D7J_str = D7J.strftime('%Y-%m-%d')
    curseur.execute("SELECT distance FROM activité_running WHERE account_id = ? AND date_activité >= ?", (account_id, D7J_str))
    distance7J = [row[0] for row in curseur.fetchall()]
    distance_des_derniers_7_jours = sum(distance7J) if distance7J else 0

    def mise_mode(choix):
        choix = mode_activité.get()
        if choix == "Charge d'entraînement":
            app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
        elif choix == "Objectif":
            app.after(0, lambda: [vider_fenetre(app), objectifs(account_id)])
        elif choix == "Compétition":
            app.after(0, lambda: [vider_fenetre(app), compétition(account_id)])
        else:
            app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover,
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Indulgence de course")
    button_autre = ctk.CTkButton(master=navbar, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    command=lambda: [vider_fenetre(app), mettre_en_pause_les_analyses_depuis_indulgence(account_id)])
    button_autre.pack(side="left", padx=10)

    boite_distance_course_gauche = ctk.CTkFrame(master=app, border_width=border2, border_color=couleur1, corner_radius=corner1,
                                             fg_color=couleur_fond)
    boite_distance_course_gauche.pack(fill="both", expand=True, side="left", padx=(40, 10), pady=(30, 40))
    h1_boite_distance_course = ctk.CTkFrame(master=boite_distance_course_gauche, fg_color=couleur_fond)
    h1_boite_distance_course.pack(pady=5)

    boite_analyse_kilométrage = ctk.CTkFrame(master=boite_distance_course_gauche, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_analyse_kilométrage.pack(fill="both", expand=True, padx=15, pady=5)
    distance_7_jours = ctk.CTkFrame(master=boite_analyse_kilométrage, corner_radius=corner1, fg_color=couleur1)
    distance_7_jours.pack(fill="both", expand=True, padx=10, pady=(10, 5))
    distance_maximum = ctk.CTkFrame(master=boite_analyse_kilométrage, corner_radius=corner1, fg_color=couleur1)
    distance_maximum.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    boite_statut = ctk.CTkFrame(master=boite_distance_course_gauche, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_statut.pack(fill="both", expand=True, padx=15, pady=(5, 15))
    h1_zone = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    h1_zone.pack(fill="both", expand=True, padx=10, pady=(10, 5))
    interprétation = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    interprétation.pack(fill="both", expand=True, pady=(5, 10), padx=10)

    boite_distance_course_droit = ctk.CTkFrame(master=app, border_width=border2, border_color=couleur1, corner_radius=corner1,
                                             fg_color=couleur_fond)
    boite_distance_course_droit.pack(fill="both", expand=True, side="right", padx=(10, 40), pady=(30, 40))

    boite_statut = ctk.CTkFrame(master=boite_distance_course_droit, border_width=border2, border_color=couleur1, corner_radius=corner1, fg_color=couleur2)
    boite_statut.pack(fill="both", expand=True, pady=15, padx=15)
    distance_moyenne_28J = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    distance_moyenne_28J.pack(fill="both", expand=True, padx=10, pady=(10, 5))
    conseil = ctk.CTkFrame(master=boite_statut, corner_radius=corner1, fg_color=couleur1)
    conseil.pack(fill="both", expand=True, pady=(5, 10), padx=10)
    
    info = ctk.CTkFrame(master=boite_distance_course_droit, corner_radius=corner1, fg_color=couleur1)
    info.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    h1 = ctk.CTkLabel(master=h1_boite_distance_course, font=(font_secondaire, taille2), text="7 derniers jours")
    h1.pack(padx=10, pady=(5, 0))
    distance_7J = ctk.CTkLabel(distance_7_jours, text=f"Distance (7 jours) : {distance_des_derniers_7_jours:.2f} km", font=(font_principale , taille2),
                                    width=300, wraplength=300)
    distance_7J.pack(fill="both", expand=True, padx=10, pady=10)

    distance_moyenne_du_mois = ctk.CTkLabel(distance_moyenne_28J, text=f"Distance moyenne (28 jours) : {distance_moyenne_des_derniers_28_jours:.2f} km", font=(font_principale, taille2),
                                width=300, wraplength=500)
    distance_moyenne_du_mois.pack(fill="both", expand=True, padx=10, pady=10)  
    pause = verifier_pause(account_id)
    if pause == "blessure":
        Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdomadaire conseillée : actuellement en pause", font=(font_secondaire, taille2),
                                        width=300, wraplength=300)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)
        zone = ctk.CTkLabel(master=h1_zone, text="⛑️ Mode blessure : suivi désactivé", font=(font_secondaire, taille2),
                                width=300, wraplength=300, text_color="#c60000")
        zone.pack(fill="both", expand=True, padx=10, pady=10)                 
        interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tu es blessé pour le moment.", font=(font_principale, taille3),
                                        width=300, wraplength=300)
        interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)      
        conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Prends vraiment le temps de laisser ton corps se régénérer en profondeur, afin de revenir encore plus fort et plus déterminé que jamais.", font=(font_principale, taille3),
                                    width=300, wraplength=500)
        conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "vacances":
        Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdomadaire conseillée : actuellement en pause", font=(font_secondaire, taille2),
                                        width=300, wraplength=300)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)
        zone = ctk.CTkLabel(master=h1_zone, text="🏖️ Mode vacances : pas d'analyse !", font=(font_secondaire, taille2),
                                width=300, wraplength=300, text_color="#6AC100")
        zone.pack(fill="both", expand=True, padx=10, pady=10)                 
        interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tu es actuellement en vacances.", font=(font_principale, taille3),
                                        width=300, wraplength=300)
        interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)      
        conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Profite de cette pause pour te ressourcer, apprécier les moments de détente et les repas, et reviens encore plus motivé !", font=(font_principale, taille3),
                                    width=300, wraplength=500)
        conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "suspendre":
        Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdomadaire conseillée : actuellement en pause", font=(font_secondaire , taille3),
                                        width=300, wraplength=300)
        Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)
        zone = ctk.CTkLabel(master=h1_zone, text="💤 Mode suspension activé : aucune analyse en cours", font=(font_secondaire, taille2),
                                width=300, wraplength=300, text_color="#6AC100")
        zone.pack(fill="both", expand=True, padx=10, pady=10)                 
        interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tes analyses sont temporairement en pause pendant ce mode suspension.", font=(font_principale, taille3),
                                        width=300, wraplength=300)
        interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)      
        conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Profite-en pour te reposer sans pression, on reprend les suivis dès ton retour à l’entraînement !", font=(font_principale, taille3),
                                    width=300, wraplength=500)
        conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
    else:
        if distance_moyenne_des_derniers_28_jours == 0:
            Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance maximale hebdomadaire conseillée :\nDonnées insuffisantes", font=(font_secondaire, taille2),
                                            width=300, wraplength=300)
            Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)

            zone = ctk.CTkLabel(master=h1_zone, text="🚫 Données insuffisantes", font=(font_secondaire, taille2),
                                        width=300, wraplength=300, text_color="#c60000")
            zone.pack(fill="both", expand=True, padx=10, pady=10)              
            interprétation_zone = ctk.CTkLabel(master=interprétation, text="L'interprétation de votre zone d'indulgence de course ne peut pas être déterminée.", font=(font_principale, taille3),
                                            width=300, wraplength=300)
            interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                    
            conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Pour pouvoir obtenir des interprétations et des conseils de course. Fais une séance de sport pour lancer les analyses et évaluer ton indulgence de course.", font=(font_principale, taille3),
                                            width=300, wraplength=500)
            conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            Distance_maximal_conseillé = ctk.CTkLabel(distance_maximum, text=f"Distance hebdomadaire conseillée entre :\n{distance_maximumconseillé_début:.1f} et {distance_maximumconseillé_fin:.1f} km", font=(font_secondaire, taille2),
                                            width=300, wraplength=300)
            Distance_maximal_conseillé.pack(fill="both", expand=True, padx=10, pady=10)

            if distance_moyenne_des_derniers_28_jours < distance_des_derniers_7_jours < distance_maximumconseillé_fin:
                zone = ctk.CTkLabel(master=h1_zone, text="🚀 Zone optimale pour progresser", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#00BA47")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Tu es en train de progresser en course, bravo ! Tu as fais le plus dur !", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                        
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Pour continuer à avancer et voir des résultats sur le long terme, fais en sorte de maintenir ce volume d’entraînement chaque semaine. C’est la régularité qui te permettra de progresser de manière stable, efficace et idéal pour éviter les blessures. Continue comme ça !", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

            elif distance_des_derniers_7_jours > distance_maximumconseillé_fin:
                zone = ctk.CTkLabel(master=h1_zone, text="🤕 Zone optimale pour se blesser", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#c60000")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Ton volume kilométrique hebdomadaire est actuellement très élevé par rapport à d'habitude.", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                        
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Prends quelques jours de pause sans courir pour permettre à ton corps de bien récupérer. La course à pied sollicite énormément tes muscles et articulations, et enchaîner sans repos augmente le risque de blessure. Ce temps de récupération est essentiel pour revenir plus fort et éviter la surcharge.", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

            elif distance_des_derniers_7_jours == distance_moyenne_des_derniers_28_jours:
                zone = ctk.CTkLabel(master=h1_zone, text="😴 Zone optimale pour stagner", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#00C073")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Ton volume est stable mais légèrement trop bas pour progresser. Tu maintiens ton niveau, mais tu risques de plafonner.", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Augmente progressivement ton volume hebdomadaire. De petites augmentations régulières te permettront de sortir de la stagnation sans te blesser, et de retrouver une dynamique de progression.", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

            else:
                zone = ctk.CTkLabel(master=h1_zone, text="⏬ Zone optimale pour perdre du niveau", font=(font_secondaire, taille2),
                                            width=300, wraplength=300, text_color="#C01802")
                zone.pack(fill="both", expand=True, padx=10, pady=10)              
                interprétation_zone = ctk.CTkLabel(master=interprétation, text="Ton volume kilométrique hebdomadaire est actuellement en dessous des niveaux optimaux pour progresser. Tu en fais moins que d'habitude !", font=(font_principale, taille3),
                                                width=300, wraplength=300)
                interprétation_zone.pack(fill="both", expand=True, padx=10, pady=10)
                        
                conseil_pour_progresser = ctk.CTkLabel(master=conseil, text="Si tu restes 3 à 4 jours sans courir alors que ton corps est habitué à un certain volume d’entraînement, tu risques de perdre en endurance et en progression. La course à pied demande une régularité pour maintenir tes capacités et continuer à avancer. Trop réduire ton entraînement peut te faire régresser.", font=(font_principale, taille3),
                                                width=300, wraplength=500)
                conseil_pour_progresser.pack(fill="both", expand=True, padx=10, pady=10)

    titre_c_quoi = ctk.CTkLabel(master=info, text="C'est quoi l'indulgence de course ?", font=(font_secondaire, taille2), wraplength=500)
    titre_c_quoi.pack(fill="both", expand=True, pady=(10, 10), padx=10)
    c_quoi = ctk.CTkLabel(master=info, 
                          text="L’indulgence de course t’aide à ajuster ton kilométrage des 7 derniers jours pour rester dans une progression optimale, sans dépasser ta limite. Tu peux ainsi continuer à t’améliorer tout en réduisant les risques de blessure. Cette analyse est un guide, mais n’oublie jamais d’écouter les signaux de ton corps. Une fonctionnalité adaptée à tous les niveaux !",
                            font=(font_principale, taille3), wraplength=500)
    c_quoi.pack(fill="both", expand=True, padx=10, pady=(5, 10))

def charge_entraînement(account_id):
    sidebar_performance(account_id)
    navbar = ctk.CTkFrame(master=app, fg_color="transparent")
    navbar.pack(pady=20)

    fig = None
    canvas = None
    def fermer_graphique_pause(account_id):
        plt.close(fig)
        mettre_en_pause_les_analyses(account_id)
    def fermer_graphique_mode():    
        nonlocal fig
        if fig:
            plt.close(fig)
            fig = None

    def mise_mode(choix):
        choix = mode_activité.get()
        if fig is None:
            if choix == "Charge d'entraînement":
                app.after(0, lambda: [vider_fenetre(app), charge_entraînement(account_id)])
            elif choix == "Indulgence de course":
                app.after(0, lambda: [vider_fenetre(app), indulgence_de_course(account_id)])
            elif choix == "Objectif":
                app.after(0, lambda: [vider_fenetre(app), objectifs(account_id)])
            elif choix == "Compétition":
                app.after(0, lambda: [vider_fenetre(app), compétition(account_id)])
        else:
            if choix == "Charge d'entraînement":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), charge_entraînement(account_id)])
            elif choix == "Indulgence de course":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), indulgence_de_course(account_id)])
            elif choix == "Objectif":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), objectifs(account_id)])
            elif choix == "Compétition":
                app.after(0, lambda: [fermer_graphique_mode(), vider_fenetre(app), compétition(account_id)])
    mode_activité = ctk.CTkSegmentedButton(master=navbar, values=["Charge d'entraînement", "Indulgence de course", "Objectif", "Compétition"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set("Charge d'entraînement")
    button_autre = ctk.CTkButton(master=navbar, text="⏸️ Mettre en pause les analyses", fg_color=couleur2, hover_color=couleur2_hover,
                                    font=(font_principale, taille3), text_color=couleur1, height=button_height, corner_radius=corner2,
                                    command=lambda: [vider_fenetre(app), fermer_graphique_pause(account_id)])
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
        messagebox.showerror("Erreur", "Erreur de base de données lors du calcul de charge d'entraînement !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    parent_frame = ctk.CTkFrame(master=app, fg_color="transparent")
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
    result_analyse = ctk.CTkLabel(master=aigue, text=f"Charge aiguë (7 jours) : {charge_aigue:.1f}", font=(font_principale , taille3),
                                    width=300, wraplength=280)
    result_analyse.pack(fill="both", expand=True, padx=10, pady=10)
    result_analyse2 = ctk.CTkLabel(master=chronique, text=f"Charge chronique (28 jours) : {charge_chronique:.1f}", font=(font_principale, taille3),
                                    width=300, wraplength=280)
    result_analyse2.pack(fill="both", expand=True, padx=10, pady=10)
    pause = verifier_pause(account_id)
    if pause == "blessure":
        result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : actuellement en pause", font=(font_secondaire, taille2),
                        width=300, wraplength=280)
        result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="⛑️ Mode blessure : suivi désactivé", font=(font_principale, taille3),
                                        width=300, wraplength=280, text_color="#c60000")
        catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)           
        interpretation_statut = ctk.CTkLabel(master=interprétation, text="Tu es blessé pour le moment", font=(font_principale, taille3),
                                    width=300, wraplength=280)
        interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)              
        conseil_statut = ctk.CTkLabel(master=conseil, text="Prends vraiment le temps de laisser ton corps se régénérer en profondeur, afin de revenir encore plus fort et plus déterminé que jamais.", font=(font_principale, taille3),
                                        width=300, wraplength=280)
        conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "vacances":
        result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : actuellement en pause", font=(font_secondaire, taille2),
                        width=300, wraplength=280)
        result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🏖️ Mode vacances : pas d'analyse !", font=(font_principale, taille3),
                                        width=300, wraplength=280, text_color="#6AC100")
        catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)          
        interpretation_statut = ctk.CTkLabel(master=interprétation, text="Tu es actuellement en vacances.", font=(font_principale, taille3),
                                    width=300, wraplength=280)
        interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)               
        conseil_statut = ctk.CTkLabel(master=conseil, text="Profite de cette pause pour te ressourcer, apprécier les moments de détente et les repas, et reviens encore plus motivé !", font=(font_principale, taille3),
                                        width=300, wraplength=280)
        conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
    elif pause == "suspendre":
        result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : actuellement en pause", font=(font_secondaire, taille2),
                        width=300, wraplength=280)
        result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
        catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="💤 Mode suspension activé : aucune analyse en cours.", font=(font_principale, taille3),
                                        width=300, wraplength=280, text_color="#6AC100")
        catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)
        interpretation_statut = ctk.CTkLabel(master=interprétation, text="Tes analyses sont temporairement en pause pendant ce mode suspension.", font=(font_principale, taille3),
                                    width=300, wraplength=280)
        interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)
        conseil_statut = ctk.CTkLabel(master=conseil, text="Profite-en pour te reposer sans pression, on reprend les suivis dès ton retour à l’entraînement !", font=(font_principale, taille3),
                                        width=300, wraplength=280)
        conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
    else :
        if charge_chronique > 0:
            ratio = charge_aigue / charge_chronique
        else:
            ratio = None
        if ratio is not None:
            result_analyse3 = ctk.CTkLabel(master=ratio_frame, text=f"Ratio : {ratio:.2f}", font=(font_secondaire, taille2),
                            width=300, wraplength=280)
            result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
            if ratio < 0.5: 
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🛌 Récupération active", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#75B7DD")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Charge très basse. Tu laisse ton corps se reposer mais jusqu'à quand !", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
                conseil_statut = ctk.CTkLabel(master=conseil, text="Fais une activité physique régulière pour reprendre en main ton entraînement et éviter de perdre ton niveau actuel.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 0.5 <= ratio <= 0.8:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="😴 Sous-entraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#CBC500")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Tu es entrain de perdre du niveau, attention !", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                conseil_statut = ctk.CTkLabel(master=conseil, text="Tu pourrais augmenter légèrement l'intensité de tes entraînements si tu veux basculer en mode maintien et stabiliser tes performances.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 0.8 <= ratio <= 0.9:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🔄 Maintien", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#00C073")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Charge adaptée pour conserver ton niveau", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                conseil_statut = ctk.CTkLabel(master=conseil, text="Allonge de 5 minutes tes séances pour basculer en mode progression optimale et améliorer tes performances.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 0.9 <= ratio <= 1.1:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🟢 Progression optimale", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#00BA47")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Charge idéale pour améliorer tes performances", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                conseil_statut = ctk.CTkLabel(master=conseil, text="Continue comme ça pour progresser ! Garde cette même régularité dans tes entraînements pour rester en mode progression optimale.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            elif 1.1 < ratio <= 1.3:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="💪 Progression élévée", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#99c800")#3d71a5
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Tu progresse vite mais fait attention aux blessures",
                                                    font=(font_principale, taille3), width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
                conseil_statut = ctk.CTkLabel(master=conseil, text="Surveille bien la fatigue de ton corps pour éviter les blessures : en gardant cette charge deux semaines, le risque reste limité.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
            else:
                catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="⚠️ Surentraînement", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#c60000")
                catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
                interpretation_statut = ctk.CTkLabel(master=interprétation, text="Risque élevé de blessure", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
                conseil_statut = ctk.CTkLabel(master=conseil, text="Prends 2 à 3 jours de pause pour laisser ton corps récupérer et réduire les risques de blessure.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
                conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)
        else:
            result_analyse3 = ctk.CTkLabel(master=ratio_frame, text="Ratio : 0.0", font=(font_secondaire, taille2),
                                                width=300, wraplength=280)
            result_analyse3.pack(fill="both", expand=True, padx=10, pady=10)
            catégorie_statut = ctk.CTkLabel(master=h1_result_optimale, text="🚫 Données insuffisantes", font=(font_secondaire, taille2),
                                                width=300, wraplength=280, text_color="#c60000")
            catégorie_statut.pack(fill="both", expand=True, padx=10, pady=10)             
            interpretation_statut = ctk.CTkLabel(master=interprétation, text="L'interprétation ne peut pas être déterminée.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
            interpretation_statut.pack(fill="both", expand=True, padx=10, pady=10)                
            conseil_statut = ctk.CTkLabel(master=conseil, text="Fais une séance de sport pour lancer les analyses et évaluer ta charge actuelle.", font=(font_principale, taille3),
                                                width=300, wraplength=280)
            conseil_statut.pack(fill="both", expand=True, padx=10, pady=10)   
    try:   
        if data_pour_graphique:
            dates_graphique = [datetime.strptime(row[0], '%Y-%m-%d') for row in data_pour_graphique]
            charges_graphique = [row[1] for row in data_pour_graphique]

            fig, ax = plt.subplots(figsize=(12, 4))
            sns.lineplot(x=dates_graphique, y=charges_graphique, marker="o", color="black")

            ax.axhline(y=charge_chronique, color=couleur1, linestyle="--", label="Charge chronique")
            ax.set_title("Évolution de la charge chronique")
            ax.set_xlabel("Date")
            ax.set_ylabel("Charge chronique")

            canvas = FigureCanvasTkAgg(fig, master=graphique)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True , pady=15, padx=15)
        else:
            not_data = ctk.CTkFrame(master=graphique, corner_radius=corner1, fg_color=couleur1)
            not_data.pack(expand=True, fill="both", padx=10, pady=10)
            pas_de_données = ctk.CTkLabel(master=not_data, text="Pas assez de données pour afficher un graphique.\nAjoute quelques séances d'entraînement pour voir votre évolution !",
                                          font=(font_secondaire, taille2), wraplength=575)
            pas_de_données.pack(padx=15, pady=15)
            button_creer_activite = ctk.CTkButton(master=not_data, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                                            corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                            command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
            button_creer_activite.pack(padx=(20, 2), pady=5)
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    titre_c_quoi = ctk.CTkLabel(master=info, text="C'est quoi la charge d'entraînement ?", font=(font_secondaire, taille2), wraplength=600)
    titre_c_quoi.pack(fill="both", expand=True, pady=(10, 10), padx=10)
    c_quoi = ctk.CTkLabel(master=info, 
                            text="La charge d'entraînement sert à optimiser ta progression sans te cramer, en trouvant le juste équilibre entre l'effort fourni et la récupération nécessaire. C'est ton meilleur ami pour éviter les blessures et planifier tes séances sportives intelligemment.",
                            font=(font_principale, taille3), wraplength=600)
    c_quoi.pack(fill="both", expand=True, padx=10, pady=(5, 10))

def mon_compte(account_id):
    navbar_mon_compte(account_id, "Mon compte")
    info = ctk.CTkFrame(master=app, corner_radius=corner1, fg_color=couleur1)
    info.pack(padx=15, pady=20)

    curseur.execute("SELECT sport FROM Account WHERE id = ?", (account_id,))
    result1 = curseur.fetchall()
    sport = result1[0][0]
    curseur.execute("SELECT bio FROM Account WHERE id = ?", (account_id,))
    result2 = curseur.fetchall()
    bio = result2[0][0]
    curseur.execute("SELECT username FROM Account WHERE id = ?", (account_id,))
    result3 = curseur.fetchall()
    username = result3[0][0]

    info = ctk.CTkLabel(master=info ,text=
                        f"Ton ID : {account_id}\n\nTon pseudo : {username}\n\nTon sport favoris : {sport if sport is not None else "Tu n'as pas de sport."}\n\nTa bio : {bio if bio is not None else "Tu n'as pas de bio."}", 
                        font=(font_principale, taille2), justify="left", wraplength=800)
    info.pack(padx=20, pady=20)

def parametre(account_id):
    sidebar_paramètre(account_id)

    def actu():
        messagebox.showinfo("Information", "Ton navigateur par défaut va s'ouvrir pour que tu puisses avoir accès aux actualités sur Sprintia.")
        webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Actu")
    def beta_testeur():
        messagebox.showwarning("Information", "Ton navigateur va s'ouvrir pour que tu puisses télécharger le programme bêta. Juste un rappel important : une version bêta n’est pas adaptée à tous les utilisateurs. Je t’invite à bien consulter la documentation avant de commencer.")
        webbrowser.open("https://github.com/Gabriel0925/Sprintia/tree/main/Programme%20B%C3%8ATA")

    Titre = ctk.CTkLabel(master=app ,text="Paramètres", font=(font_secondaire, taille1), text_color=couleur_text)
    Titre.pack(padx=50, pady=20)

    frame_bouton = ctk.CTkFrame(master=app, fg_color="transparent")
    frame_bouton.pack(pady=(20,0), padx=10)
    frame_bouton1 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton1.pack(pady=(20,0), padx=10)
    frame_bouton2 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton2.pack(pady=(10,0), padx=10)
    frame_bouton3 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton3.pack(pady=(10,0), padx=10)
    frame_bouton4 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton4.pack(pady=(10,0), padx=10)
    frame_bouton5 = ctk.CTkFrame(master=frame_bouton, fg_color="transparent")
    frame_bouton5.pack(pady=(10,20), padx=10)

    button_autre = ctk.CTkButton(master=frame_bouton1, text="👤 Mon Compte",
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3), fg_color=couleur2, 
                           hover_color=couleur2_hover, text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), mon_compte(account_id)])
    button_autre.pack(side="left" ,padx=10, pady=0)
    button_info = ctk.CTkButton(master=frame_bouton1, text="📢 À propos", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), a_propos(account_id)])
    button_info.pack(side="left", pady=0, padx=10)
    button_nouveauté = ctk.CTkButton(master=frame_bouton2, text="✨ Quoi de neuf dans Sprintia 3.1", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1,
                           command=lambda: [vider_fenetre(app), quoi_de_neuf(account_id)])
    button_nouveauté.pack(side="left", pady=0, padx=10)
    button_avis = ctk.CTkButton(master=frame_bouton2, text="🆕 Proposer une fonction", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), proposer_fonction(account_id)])
    button_avis.pack(side="left", pady=0, padx=10) 
    button_avis = ctk.CTkButton(master=frame_bouton3, text="🕷️  Signaler un bug", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), signaler_bug(account_id)])
    button_avis.pack(side="left", pady=0, padx=10) 
    button_avis = ctk.CTkButton(master=frame_bouton3, text="💬 Rédiger un avis", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=lambda: [vider_fenetre(app), avis(account_id)])
    button_avis.pack(side="left", pady=0, padx=10)
    button_avis = ctk.CTkButton(master=frame_bouton4, text="📰 Actu Sprintia", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=actu)
    button_avis.pack(side="left", pady=0, padx=10)   
    button_avis = ctk.CTkButton(master=frame_bouton4, text="🧪 Rejoindre la bêta", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                           text_color=couleur1, 
                           command=beta_testeur)
    button_avis.pack(side="left", pady=0, padx=10)      
    button_deco = ctk.CTkButton(master=frame_bouton5, text="🚪Déconnexion",
                            corner_radius=corner2, width=300, height=button_height, font=(font_principale, taille3),
                            fg_color="#AC1724", hover_color="#E32131",
                            command=lambda: [vider_fenetre(app), connexion()])
    button_deco.pack(side="left" ,padx=10, pady=0)

def interface_exercice(account_id, type_de_catégorie, headers, requête_sql):
    global periode_séléctionner #global = pour dire que la variable existe en dehors de la fonction et que je vais la modifier
    sidebar_exercice(account_id)

    boite2 = ctk.CTkFrame(master=app, fg_color="transparent", corner_radius=corner3)
    boite2.pack(side="top", fill="x", pady=20)
    topbar = ctk.CTkFrame(master=boite2, fg_color="transparent", corner_radius=corner3)
    topbar.pack(anchor="center")
    element_topbar = ctk.CTkFrame(master=topbar, fg_color="transparent")
    element_topbar.pack()

    boite_semi_header = ctk.CTkFrame(master=app, fg_color="transparent")
    boite_semi_header.pack(side="top", pady=10)

    boite3 = ctk.CTkFrame(master=app, fg_color=couleur_fond)
    boite3.pack(side="top", fill="both", expand=True, pady=10)
    frame = ctk.CTkFrame(master=boite3, fg_color=couleur_fond, corner_radius=corner1, border_width=border2, border_color=couleur1)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    tableau_frame = ctk.CTkScrollableFrame(master=frame, fg_color=couleur_fond, scrollbar_button_color=couleur2, 
                                           scrollbar_button_hover_color=couleur2_hover)
    tableau_frame.pack(fill="both", expand=True, padx=20, pady=5)

    button_supprimer = ctk.CTkButton(master=element_topbar, text="🗑️ Supprimer", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: supprimer_activité(account_id, avoir_periode(combo_periode.get(), options_periode)))
    button_supprimer.pack(side="right", padx=2, pady=5)
    button_creer_activite = ctk.CTkButton(master=element_topbar, text="➕ Ajouter", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                                        command=lambda: [vider_fenetre(app), ajouter_activité_extérieur(account_id)])
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
        navigation = {
            "Extérieur": lambda: [vider_fenetre(app), exercice_extérieur(account_id)],
            "Intérieur": lambda: [vider_fenetre(app), exercice_intérieur(account_id)],
            "Musculation": lambda: [vider_fenetre(app), exercice_musculation(account_id)],
            "Football": lambda: [vider_fenetre(app), exercice_football(account_id)],
            "Tous": lambda: [vider_fenetre(app), exercice(account_id)],
            "Course": lambda: [vider_fenetre(app), exercice_course(account_id)]
        }
        app.after(0, navigation[choix])

    mode_activité = ctk.CTkSegmentedButton(master=boite_semi_header, values=["Tous", "Extérieur", "Intérieur", "Course", "Musculation", "Football"],
                                           height=button_height, selected_color=couleur_fond, selected_hover_color=couleur2_hover, 
                                           corner_radius=corner1, command=mise_mode, font=(font_principale, taille3),
                                           fg_color=couleur2, unselected_color=couleur2, unselected_hover_color=couleur2_hover,
                                           text_color=couleur1)
    mode_activité.pack(side="left")
    mode_activité.set(type_de_catégorie)
    if type_de_catégorie == "Musculation":
        wraplength_tableau = 100
    elif type_de_catégorie == "Tous":
        wraplength_tableau = 180
    elif type_de_catégorie == "Course":
        wraplength_tableau = 100
    else:
        wraplength_tableau = 130

    if type_de_catégorie == "Musculation":
        padx_tableau = 2
    elif type_de_catégorie == "Tous":
        padx_tableau = 15
    elif type_de_catégorie == "Course":
        padx_tableau = 2
    elif type_de_catégorie == "Intérieur":
        padx_tableau = 15
    elif type_de_catégorie == "Football":
        padx_tableau = 8
    elif type_de_catégorie == "Extérieur":
        padx_tableau = 10

    def mettre_a_jour_historique(selection):
        global periode_séléctionner
        periode_séléctionner = selection
        for widget in tableau_frame.winfo_children():
            widget.grid_remove()
        try:
            jours_a_soustraire = options_periode[selection]
            date_debut = date_actuelle - timedelta(days=jours_a_soustraire)
            période_str_pour_requete = date_debut.strftime('%Y-%m-%d')
            curseur.execute(f"{requête_sql}", (account_id, période_str_pour_requete))
            activites = curseur.fetchall()
            for colonne, header_text in enumerate(headers):
                label = ctk.CTkLabel(master=tableau_frame, text=header_text, font=(font_secondaire, taille2),
                                     fg_color=couleur1, corner_radius=corner1, text_color=couleur_text,
                                     height=40, wraplength=wraplength_tableau)
                label.grid(row=0, column=colonne, padx=padx_tableau, pady=15, sticky="ew")
                tableau_frame.grid_columnconfigure(colonne, weight=1)
            if activites:
                for ligne, activite in enumerate(activites):
                    for colonne, data in enumerate(activite):
                        try:
                            if colonne == 1:
                                data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        except:
                            if colonne == 0:
                                data = datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')
                        label = ctk.CTkLabel(master=tableau_frame, text=str(data if data is not None else "-"), font=(font_principale, taille3),
                                             text_color=couleur_text, wraplength=130)
                        label.grid(row=ligne + 1, column=colonne, padx=10, pady=15, sticky="ew")
            else:
                pas_donnees = ctk.CTkLabel(master=tableau_frame, text="Aucune activité enregistrée pour cette période.", font=(font_principale, taille1))
                pas_donnees.grid(row=1, column=0, columnspan=len(headers), pady=20)
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de la récupération de ton historique !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    combo_periode.configure(command=mettre_a_jour_historique)
    combo_periode.set(periode_séléctionner)
    mettre_a_jour_historique(periode_séléctionner)
    aide_bienvenue(account_id)

def exercice_course(account_id):
    requête_sql = "SELECT date_activité, durée, rpe, nom, distance, allure, dénivelé, vitesse_max FROM Activité_running WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Distance", "Allure", "Dénivelé", "Vitesse max"]
    interface_exercice(account_id, "Course", headers, requête_sql)

def exercice_intérieur(account_id):
    requête_sql = "SELECT sport, date_activité, durée, rpe, nom FROM Activité_intérieur WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Type"]
    interface_exercice(account_id, "Intérieur", headers, requête_sql)

def exercice_football(account_id):
    requête_sql = "SELECT date_activité, durée, rpe, type_de_séances, humeur, but, passe_décisive, score FROM Activité_football WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Durée", "RPE", "Type", "Humeur", "But", "Passe D", "Score"]
    interface_exercice(account_id, "Football", headers, requête_sql)

def exercice_musculation(account_id):
    requête_sql = "SELECT date_activité, lieu, durée, rpe, équipement, muscle_travaillé, répétitions, série, volume FROM Activité_musculation WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Date", "Lieu", "Durée", "RPE", "Type", "Muscle", "Rép", "Série", "Volume"]
    interface_exercice(account_id, "Musculation", headers, requête_sql)

def exercice_extérieur(account_id):
    requête_sql = "SELECT sport, date_activité, durée, rpe, nom, distance, dénivelé FROM Activité_extérieur WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Type", "Distance", "Dénivelé"]
    interface_exercice(account_id, "Extérieur", headers, requête_sql)

def exercice(account_id):
    requête_sql = "SELECT sport, date_activité, durée, rpe, ROUND(charge, 1) FROM Activité WHERE account_id = ? AND date_activité >= ? ORDER BY date_activité DESC"
    headers = ["Sport", "Date", "Durée", "RPE", "Charge d'entraînement"]
    interface_exercice(account_id, "Tous", headers, requête_sql)

def connexion():
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

    button_connection = ctk.CTkButton(master=frame_bouton, text="✔️ Connexion", fg_color=couleur1, hover_color=couleur1_hover,
                           corner_radius=corner1, height=button_height, font=(font_principale, taille3),
                           command=lambda: [vider_fenetre(app), connexion()])
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
            messagebox.showerror("Champs manquants", "Le pseudo et le mot de passe ne peuvent pas être vides")
            return
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            curseur.execute("SELECT id FROM Account WHERE username = ? AND password = ?", (username, hashed_password))
            result = curseur.fetchone()

            if result:
                account_id = result[0]
                vider_fenetre(app)
                exercice(account_id)
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects, réessaye !")
        except sqlite3.Error as e:
            messagebox.showwarning("Erreur", "Erreur de base de données lors de la connexion à ton compte !")
        except Exception as e:
            messagebox.showwarning("Erreur", "Une erreur inattendu s'est produite, réessaye !")
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

    button_connection = ctk.CTkButton(master=frame_bouton, text="Connexion", fg_color=couleur2, hover_color=couleur2_hover,
                           corner_radius=corner2, height=button_height, font=(font_principale, taille3), text_color=couleur1,
                           command=lambda: [vider_fenetre(app), connexion()])
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
                messagebox.showerror("Champs manquants", "Le pseudo et le mot de passe ne peuvent pas être vides !")
                return
            if password != password_confirmation:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas !")
                return
            if (password_valide(password)):
                sha256 = hashlib.sha256()
                sha256.update(password_encode)
                hashed_password = sha256.hexdigest()
                curseur.execute("INSERT INTO Account (username, password) VALUES (?, ?)", (username, hashed_password))
                con.commit()
                account_id = curseur.lastrowid
                messagebox.showinfo("Inscription réussie", f"Bienvenue {username} !")
                vider_fenetre(app)
                exercice(account_id)
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur", "Ce pseudo est déjà utilisé. Essaye d'en utiliser un autre !")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données lors de l'inscription !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
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

def mettre_à_jour_base_de_donées():
    try:
        curseur.execute("DROP TABLE Pauses")
    except sqlite3.Error as e:
        pass
    try:
        curseur.execute("DROP TABLE Aide")
    except sqlite3.Error as e:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_football ADD COLUMN score TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Aide ADD COLUMN modifier_objectif TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Aide ADD COLUMN modifier_compétition TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Aide ADD COLUMN bienvenue TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN nom")
        curseur.execute("ALTER TABLE Activité_football DROP COLUMN muscle_travaillé")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN muscle_travaillé")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN but")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité_intérieur DROP COLUMN type_de_séances")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN type_de_séances")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN nom")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité_musculation DROP COLUMN but")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN muscle_travaillé")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN but")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité_extérieur DROP COLUMN type_de_séances")
    except sqlite3.OperationalError:
        pass
    try:
        curseur.execute("ALTER TABLE Activité DROP COLUMN muscle_travaillé")
        curseur.execute("ALTER TABLE Activité DROP COLUMN douleur")
        curseur.execute("ALTER TABLE Activité DROP COLUMN climat")
        curseur.execute("ALTER TABLE Activité DROP COLUMN distance")
        curseur.execute("ALTER TABLE Activité DROP COLUMN dénivelé")
        curseur.execute("ALTER TABLE Activité DROP COLUMN but")
        curseur.execute("ALTER TABLE Activité DROP COLUMN répétitions")
        curseur.execute("ALTER TABLE Activité DROP COLUMN série")
        curseur.execute("ALTER TABLE Activité DROP COLUMN volume")
        curseur.execute("ALTER TABLE Activité DROP COLUMN équipement")
        curseur.execute("ALTER TABLE Activité DROP COLUMN lieu")
        curseur.execute("ALTER TABLE Activité DROP COLUMN fatigue")
        curseur.execute("ALTER TABLE Activité DROP COLUMN nom")
        curseur.execute("ALTER TABLE Activité DROP COLUMN humeur")
        curseur.execute("ALTER TABLE Activité DROP COLUMN passe_décisive")
        curseur.execute("ALTER TABLE Activité DROP COLUMN type_de_séances")
    except sqlite3.OperationalError:
        pass
    connexion()

def maj_base_de_données():
    sport_première_étape = "course"
    sport_deuxième_étape = "pied"
    sport = "course"
    trail = "trail"
    ultrafond = "ultrafond"
    sport2_première_étape = "course"
    sport2_deuxième_étape = "piste"
    sport3_première_étape = "tapis"
    sport3_deuxième_étape = "course"
    appris = "fait"
    try:
        # Le %% ça créer une recherche et le LIKE ça va faire une recherche qui contient "course" et "pied" ça veut dire que peut importe ce qu'il y a au milieu ca le transferera quand meme
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) LIKE ? AND LOWER(sport) LIKE ?", (f"%{sport_première_étape}%", f"%{sport_deuxième_étape}%"))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) LIKE ? AND LOWER(sport) LIKE ?", (f"%{sport2_première_étape}%", f"%{sport2_deuxième_étape}%"))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) LIKE ? AND LOWER(sport) LIKE ?", (f"%{sport3_première_étape}%", f"%{sport3_deuxième_étape}%"))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) = ?", (sport,))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) = ?", (trail,))
        curseur.execute("INSERT INTO Activité_running (account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom) SELECT account_id, date_activité, sport, durée, distance, dénivelé, rpe, charge, nom FROM Activité WHERE LOWER(sport) = ?", (ultrafond,))
        curseur.execute("INSERT INTO Maj_base_de_donnée (action) VALUES (?)", (appris,))
        con.commit()
        con.commit()
        mettre_à_jour_base_de_donées()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de donnée lors de la mise à jour de ta base de données !")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")

if __name__ == "__main__":
    try:
        con = sqlite3.connect("data_base.db")
        curseur = con.cursor()

        curseur.execute('''CREATE TABLE IF NOT EXISTS Account (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL, sport TEXT, bio TEXT)''')
        
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,rpe INTEGER,charge INTEGER,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_extérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC,dénivelé INTEGER,rpe INTEGER,charge INTEGER,nom TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_running (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,distance NUMERIC, vitesse_max NUMERIC, dénivelé INTEGER,rpe INTEGER,charge INTEGER,nom TEXT, allure TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_intérieur (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,rpe INTEGER,charge INTEGER,nom TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_musculation (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER,muscle_travaillé TEXT, répétitions TEXT, série TEXT, volume NUMERIC, équipement TEXT, lieu  TEXT,rpe INTEGER,charge INTEGER,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Activité_football (id_activité INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER,date_activité TEXT,sport TEXT,durée INTEGER, score TEXT, rpe INTEGER,charge INTEGER,humeur TEXT, but TEXT, passe_décisive TEXT, type_de_séances TEXT,FOREIGN KEY (account_id)REFERENCES Account (id) );''')
        
        curseur.execute('''CREATE TABLE IF NOT EXISTS Compétition (id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT NOT NULL,date TEXT NOT NULL,sport TEXT NOT NULL,objectif TEXT NOT NULL, lieu TEXT,priorité TEXT,account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Objectif (id INTEGER PRIMARY KEY AUTOINCREMENT,sport TEXT NOT NULL,date TEXT NOT NULL,objectif TEXT NOT NULL,fréquence TEXT NOT NULL,niveau_début TEXT NOT NULL,niveau_fin TEXT,statut TEXT, account_id INTEGER,FOREIGN KEY (account_id) REFERENCES Account(id))''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Pauses_v2 (id INTEGER PRIMARY KEY AUTOINCREMENT,account_id INTEGER NOT NULL,type TEXT CHECK(type IN ('vacances', 'blessure', 'suspendre')),date_debut TEXT DEFAULT CURRENT_DATE,date_fin TEXT,FOREIGN KEY (account_id) REFERENCES Account(id)  )''')

        curseur.execute('''CREATE TABLE IF NOT EXISTS Aide_rpe (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Aide_bienvenue (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Aide_objectif (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Aide_compétition (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Aide_podcast (account_id INTEGER NOT NULL,aide TEXT, FOREIGN KEY (account_id) REFERENCES Account(id)  )''')
        curseur.execute('''CREATE TABLE IF NOT EXISTS Maj_base_de_donnée (action TEXT)''')
        con.commit()
        ctk.set_appearance_mode("System")
        app = ctk.CTk(fg_color=couleur_fond)
        app.geometry("1050x600")
        app.title("Sprintia")
        try:
            curseur.execute("SELECT username FROM Account")
            result_premiere = curseur.fetchone()
            if result_premiere:
                curseur.execute("SELECT action FROM Maj_base_de_donnée")
                result_maj = curseur.fetchone()
                if result_maj and result_maj[0] == "fait": # result[0] = parce que fetchone renvoie ('fait',)
                    mettre_à_jour_base_de_donées()
                else:
                    maj_base_de_données()
            else:
                curseur.execute("INSERT INTO Maj_base_de_donnée (action) VALUES ('fait')")
                mettre_à_jour_base_de_donées()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", "Erreur de base de données !")
        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
        app.protocol("WM_DELETE_WINDOW", fermer_app)
        app.bind("<Control-w>", lambda event: fermer_app())
        app.mainloop()
    except sqlite3.Error as e:
        messagebox.showerror("Erreur", "Erreur de base de données lors de la connexion à la base de données !")
        con.close()
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur inattendu s'est produite, réessaye !")
    con.close()
