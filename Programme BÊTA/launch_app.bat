REM REM c'est pour les commentaires
@echo off

title Lancement de Sprintia
pip install --upgrade customtkinter matplotlib seaborn pillow

python "%~dp0main.py"
REM "%~dp0" c'est pour obtenir le chemin du dossier ou se trouve le fichier .bat
REM "%~dp0main.py" c'est pour lancer main.py qui se trouve dans le même dossier que Sprintia.bat