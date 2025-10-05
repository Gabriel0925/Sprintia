import customtkinter as ctk
from PIL.ImageOps import expand
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import tkcalendar
import sqlite3
import hashlib
import math
from datetime import datetime, timedelta
from datetime import date
from datetime import time as Time
import matplotlib.pyplot as plt
import seaborn as sns
import random
import webbrowser
from urllib.parse import quote #pour remplir les champs (destinataire,...) dans une app mail
from tkinter import messagebox

# Version Sprintia
version_numéro = "3.2"
version_entière = "3.2 BÊTA 3 | Version Novembre 2025"
date_de_sortie = "05 Octobre 2025"
type_de_maj = "Mise à jour mineur"

# Couleur
couleur1 = "#3d71a5"
couleur1_hover = "#4a8bcb"
couleur2 = "#8CB1C1"
couleur2_hover = "#ABD1E1"
couleur_fond = "#131d34"
couleur_text = "#fbfcfb"
mode_image = "Logo Sprintia Sombre.png"

# Police d'écriture
taille1 = 30
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
border2 = border1
# Taille CTkEntry
entry_height = 45
# Taille CTkButton
button_height = 50
height_expressive = 60
widht_expressive = 450
button_width = 180 # c'est pour les boutons de la sidebar

# variables
date_actuelle = date.today()
date_actuelle_format = date_actuelle.strftime("%d-%m-%Y")

# heure
maintenant = datetime.now()
heure_actuelle_objet = maintenant.time()

# variable globale
periode_séléctionner = "1 semaine"

def vider_fenetre(app):
    for widget in app.winfo_children():
        widget.destroy()

def fermer_app(app, con):
    if con:
        con.close()
    app.quit()

def password_valide(password):
    SpecialSymbol =["!",  "@",  "#",  "$",  "%",  "^",  "&", "*", "(", ")", "-", "_", "=", "+", "[", "]",  "{", "}", ";", ":", ",", "<", ">", ".", "?"]
    val = True

    if len(password) < 6:
        messagebox.showerror("Mot de passe invalide", "La longueur doit être d'au moins 6 caractères !")
        val = False
        return val

    if len(password) > 20:
        messagebox.showerror("Mot de passe invalide", "La longueur ne doit pas dépasser 20 caractères !")
        val = False
        return val

    if not any(char.isdigit() for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins un chiffre !")
        val = False
        return val

    if not any(char.isupper() for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins une lettre majuscule !")
        val = False
        return val

    if not any(char.islower() for char in password):
        messagebox.showerror("Mot de passe invalide", "Le mot de passe doit contenir au moins une lettre minuscule !")
        val = False
        return val

    if not any(char in SpecialSymbol for char in password):
        messagebox.showerror("""Mot de passe invalide", "Le mot de passe doit contenir au moins un des symboles spéciaux :\n" \
        "!",  "@",  "#",  "$",  "%",  "^",  "&", "*", "(", ")", "-", "_", "=", "+", "[", "]",  "{", "}", ";", ":", ",", "<", ">", ".", "?""")
        val = False
        return val
    if val:
        return val
