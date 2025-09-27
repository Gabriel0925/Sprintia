import subprocess
import sys
import urllib.request

try:
    # J'envoie une requête HTTP à Google
    # Si j'ai une réponse (invisible pr le user) ça veut dire je suis co à internet
    urllib.request.urlopen("https://www.google.com")
    bibliothèques = [sys.executable, "-m", "pip", "install", "--upgrade", "customtkinter", "matplotlib", "seaborn", "pillow", "tkcalendar"]
    subprocess.run(bibliothèques)
    subprocess.run("python main.py")
except Exception:        
    subprocess.run("python main.py")
    
