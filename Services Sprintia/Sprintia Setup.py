import subprocess
import sys # Pour être sur d'installer le bon "pip"
from tkinter import messagebox
import webbrowser

def installation_des_bibliothèques():
    bibliothèques = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    try:
        subprocess.run(bibliothèques, check=True)
        messagebox.showinfo("Info", "Les bibliothèques nécessaires à Sprintia ont été installées ! Tu peux maintenant lancer l'application Sprintia !")
    except subprocess.CalledProcessError:
        messagebox.showwarning("Erreur", "L'installation des bibliothèques nécessaires à Sprintia a échoué ! Vérifie ta connexion internet.")
    except FileNotFoundError:
        reponse = messagebox.askokcancel("Info", "Python n'a pas été trouvé. Veux-tu aller l'installer ?")
        if reponse:
            url = "https://www.python.org/downloads/"
            webbrowser.open(url)

def hello():                
    reponse = messagebox.askyesno("Bienvenue sur Sprintia Setup", "Pour fonctionner correctement, Sprintia a besoin d'installer quelques bibliothèques sur ton ordinateur. Souhaites-tu les installer ?")
    if reponse:
        installation_des_bibliothèques()
    else:
        messagebox.showwarning("Attention", "Si tu refuses, tu risques de ne même pas pouvoir ouvrir Sprintia. Relance le programme, si tu veux installer les bibliothèques nécessaire à Sprintia.")

hello()