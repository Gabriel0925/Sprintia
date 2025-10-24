# Bienvenue sur Sprintia

## Sommaire
- [ℹ️ Petite information](#ℹ️-petite-information)
- [📌 Sprintia c'est quoi ?](#-sprintia-cest-quoi-)
- [⚡ Fonctionnalités principales](#-fonctionnalités-principales)
- [💻 Compatibilité](#-compatibilité)
- [📚 Guide rapide d’installation](#-guide-rapide-dinstallation)
- [🛡️ Antivirus](#️-conseil-si-tu-as-un-antivirus)
- [🔔 Projet cloturé](#-projet-cloturé)
- [🤔 Pour les curieux·ses](#-pour-les-curieuxses)

## ℹ️ Petite information

Dans le monde du sport, un coach est un partenaire de confiance. C'est pour cette raison que j'ai choisi de te tutoyer dans l'application Sprintia et dans ce README. L'objectif est de créer une relation plus proche et personnelle avec toi, comme celle que tu aurais avec un coach sportif.

## 📌 Sprintia c'est quoi ?

Sprintia est conçue pour t'aider avant et après un entraînement grâce à des algorithmes 100 % gratuits. Que tu sois un sportif débutant, confirmé, expert,... Sprintia t’aide à progresser sans te blesser.

## ⚡ Fonctionnalités principales

### Charge d'entraînement
La charge d'entraînement sert à optimiser ta progression sans te cramer, en trouvant le juste équilibre entre l'effort fourni et la récupération nécessaire.

![Capture d'écran de Sprintia](<Images/Charge d'entraînement.png>)

### Indulgence de course
L’indulgence de course t’aide à ajuster ton kilométrage des 7 derniers jours pour rester dans une progression optimale, sans dépasser ta limite.

![Capture d'écran de Sprintia](<Images/Indulgence de course.png>)

### Prédicteur de performance
Le prédicteur de performance te permet d'estimer tes temps sur n'importe quelle distance (5 km, 10 km, semi-marathon, marathon) à partir de tes courses récentes.

![Capture d'écran de Sprintia](<Images/Prédicteur de performance.png>)

### JRM Coach
Un coach entièrement personnalisable. Crée ton propre coach : choisis son nom, son style et même son avatar. Ton coach, à ton image, pour te motiver au quotidien !

![Capture d'écran de Sprintia](<Images/JRM Coach.png>)

## 💻 Compatibilité

Sprintia est une application de bureau (desktop app), compatible avec les PC qui tournent sous Windows.

(💡 Info pour les curieux·ses : le code est aussi utilisable sur Linux et macOS, voir la dernière section).

## 📚 Guide rapide d’installation

### 1️⃣ Installation et Premier Lancement

◉ Télécharge le dossier compressé **"Sprintia-V3.2.zip"** disponible sur mon GitHub.

◉ Ensuite, tu vas dans tes téléchargements. Fais un clic-droit sur **"Sprintia-V3.2.zip"** puis **"Extraire tout"**. Dans la fenêtre qui s'ouvrira, clique sur **"Parcourir"** et sélectionne **"Documents"**.

◉ Maintenant, rends-toi dans tes documents, puis dans le dossier Sprintia. Double-clique sur **"Sprintia.exe"**.

⚠️ **Alerte Sécurité Windows :** Si une fenêtre de ce type (voir ci-dessous) apparaît, pas de panique ! C'est parce que Microsoft ne reconnaît pas encore Sprintia.

![Capture d'écran de la fenêtre de sécurité Windows](<Images/Windows Security.png>)

◉ Clique sur **"Informations complémentaires"**, puis sur **"Exécuter quand même"** (ceci n'apparaîtra qu'une seule fois).

Et voilà ! Tu peux désormais utiliser Sprintia, bon entraînement 😉.

### 2️⃣ Faire un raccourci bureau (optionnel mais pratique)

◉ Rends-toi dans le dossier Sprintia (dans tes Documents). Fais un clic-droit sur **"Sprintia.exe"** puis **"Afficher d'autres options"** puis **"Envoyer vers"** puis clique sur **"Bureau (créer un raccourci)"**.

◉ Va sur ton bureau. Tu verras un fichier nommé **"Sprintia.exe - Raccourci"**. Fais un clic-droit dessus puis **"Renommer"** et renomme le **"Sprintia"** (ça sera plus propre).

◉ Bravo ! Tu n’auras plus qu’à double-cliquer sur le raccourci pour lancer l'application.

## 🛡️ Conseil si tu as un antivirus 

Tu utilises un antivirus (Norton, Avast, etc.) ? Pour éviter que ton antivirus bloque "Sprintia.exe", je te conseille de faire ça ⬇️

◉ Ajoute le dossier "Sprintia" (qu'il y a dans tes "Documents" sur ton PC) à la liste d'exclusions de ton logiciel antivirus.

👉 Besoin d'aide pour la procédure ? Tu peux demander à [ChatGPT](https://chatgpt.com/) en lui disant : "Comment exclure le dossier Documents\Sprintia de [nom de ton antivirus]".

## 🔔 Projet cloturé

La version finale (V3.2) marque la fin du développement de Sprintia.
L’application est désormais fournie en l’état, sans mises à jour ultérieures.

## 🤔 Pour les curieux·ses

L’intégralité du code de Sprintia est disponible dans le dossier "Code source". 
Donc pour installer Sprintia sur Linux ou sur macOS, tu dois :

◉ Avoir Python installé sur ton ordinateur (ou l’installer si ce n’est pas déjà fait)

◉ Télécharger tous les fichiers du code source et les mettre dans un dossier nommé "Sprintia".

◉ Une fois à l'intérieur du dossier, fais un clic-droit puis "Ouvrir dans un Terminal".

◉ Installe les dépendances nécessaires avec cette commande :
    ```
    pip install -r requirements.txt
    ```

◉ Une fois les bibliothèques installées, lance l'application :
    ```
    python main.py
    ```
