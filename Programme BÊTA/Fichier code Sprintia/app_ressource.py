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
version_entière = "3.2 BÊTA 4 | Version Novembre 2025"
date_de_sortie = "12 Octobre 2025"
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

# Mots sensibles à filtrer pour pseudo utilisateur
mot_sensible = [
    # Insultes et discriminations
    "connard", "pute", "salope", "nique", "merde", "enculé", "bite", "chienne",
    "raciste", "nazi", "fasciste", "pd", "fiotte", "bougnoule", "handicapé", "con",
    "conne", "débile", "idiot", "imbécile", "taré", "boloss", "lâche", "salaud",

    # Violence et haine
    "tueur", "violeur", "suicide", "meurtre", "terroriste", "guerre", "haine", "bombardement",
    "assassinat", "massacre", "exécution", "crucifier", "lyncher", "tabasser", "drogue", "armes", "pistolet", "fusil", "grenade",
    "attaque", "agression", "violence", "harcèlement",

    # Sexualité explicite
    "sexe", "porn", "fuck", "baise", "nik", "penis", "vagin", "cul", "chatte", "sexy",
    "viol", "sodomie", "branlette", "masturbation", "orgasme", "doigter", "baiser",
    "prostituée", "striptease", "pornstar", 

    # Marques/noms protégés
    "nike", "adidas", "apple", "samsung", "microsoft", "sprintia", "google", "facebook",
    "amazon", "tesla", "coca-cola", "pepsi", "starbucks", "mcdonalds",
    "youtube", "instagram", "twitter", "tiktok", "snapchat", "whatsapp",
    "windows", "android", "ios", "playstation", "xbox", "nintendo", "uber", "airbnb",
    "paypal", "visa", "mastercard", "bitcoin", "ethereum", "dogecoin", "twitch",
    "netflix", "hulu", "disney", "spotify", "deezer", "pandora", "soundcloud",
    "wordpress", "wix", "shopify", "squarespace", "godaddy", "bluehost",
    "adobe", "photoshop", "illustrator", "premiere", "after effects", "lightroom",
    "autodesk", "maya", "3ds max", "blender", "unity", "unreal engine",
    "intel", "amd", "nvidia", "qualcomm", "broadcom", "arm", "mediatek",
    "ford", "chevrolet", "toyota", "honda", "bmw", "mercedes", "audi", "volkswagen",
    "ferrari", "lamborghini", "porsche", "tesla", "bugatti", "mclaren", "rolls-royce",
    "harley-davidson", "ducati", "yamaha", "kawasaki", "suzuki", "bmw motorrad",
    "gucci", "prada", "chanel", "louis vuitton", "hermes", "dior", "versace", "armani", "burberry",
    "rolex"

    # Sportifs célèbres
    "messi", "ronaldo", "neymar", "mbappé", "lebron", "serena", "federer", "djokovic", "phelps",
    "bolt", "ali", "jordan", "brady", "curry", "durant", "harden", "giannis", "kawhi", "lillard", "tatum",
    "russell", "westbrook", "davis", "bryant", "wade", "pierce", "garnett", "nowitzki", "nash", "stockton", "malone", "robinson",
    "sanchez", "aguero", "suarez", "ibrahimovic", "rooney", "beckham", "zidane", "ronaldo nazario", "ronaldo fenoméno",
    "pele", "maradona", "cruyff", "platini", "beckenbauer", "muller", "gerrard", "lampard", "terry", "vidic", "ferdinand",
    "pirlo", "totti", "del piero", "baggio", "kaka", "ronaldinho", "henry", "shearer", "owen", "fowler", "robbie", "carragher", "scholes", "giggs", "keane",
    "vettel", "hamilton", "alonso", "verstappen", "kilian jornet", "usain bolt", "michael phelps", "lebron james", "serena williams", 
    "roger federer", "lionel messi", "cristiano ronaldo",

    # Autres termes inappropriés
    "drogue", "cocaine", "alcoolique", "toxicomane",
    "hitler", "staline", "putin", "trump", "macron", "biden", "obama", 
    "politique", "religion", "secte", "cultes", "occultisme"
]

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
