// Initialisation de la configuration de chaque thème
const ThemeConfig = {
    "theme_carmin": ["#FF5257", "#FF8A8E"],
    "theme_fuchsia": ["#FA6BFA", "#FFA8FF"],
    "theme_lavande": ["#B266F9", "#D7A8FF"],
    "theme_vegetation": ["#0CBB5BFF", "#76E082"],
    "theme_menthe": ["#0ac3a7", "#76e8d6"],
    "theme_pierre_lune": ["#6aabd3", "#acdefd"], 
    "theme_framboise": ["#f14d84", "#ff80ab"],

    "theme_feu": ["#ffb82b", "#ff782f"],
    "theme_plage": ["#1498e4", "#fcaf6b"],
    "Hortensia": ["#3a91ff", "#f782f0"], 
    "Aurore": ["#a477fe", "#4ce58c"]
}
// init variable
let theme = "theme_azur"

function SelectedElement(idElement) {
    if (idElement) {
        document.querySelector(".selected").classList.remove("selected")
        document.getElementById(idElement).classList.add("selected")
    }
}

function colorTheme(theme, idElement) {
    if (theme == "theme_azur") { // si c'est le thème de base alors on réinitialise les variables
        document.documentElement.style.removeProperty("--COULEUR_ACCENT")
        document.documentElement.style.removeProperty("--COULEUR_ACCENT2")
    } else {
        let tableauTheme = ThemeConfig[theme] // on recherche le tableau du theme correspondant pour avoir accès au thème
        // on met à jour les variables
        document.documentElement.style.setProperty("--COULEUR_ACCENT", tableauTheme[0])
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", tableauTheme[1])
    }
    // maj dans la "BDD"
    localStorage.setItem("ColorActuelleUse", theme) 

    // maj de l'élément séléctionné
    SelectedElement(idElement)
    return
}

async function reinitialiserTheme() { // remmettre le thème par défaut
    // Demande de confirmation avant
    if (confirm("Êtes-vous sur de vouloir réinitialiser le thème ?")) {
        let Button = document.getElementById("reinitialiser") // Recup du bouton
        // Desactivation du button
        Button.disabled = true
        Button.textContent = "Réinitialisation..."
        
        // maj des valeurs dans la base de données
        localStorage.setItem("ColorActuelleUse", "theme_azur");
        localStorage.setItem("ToggleThemeComplet", "False")

        // Légère pause
        await new Promise(r => setTimeout(r, 650))

        // confirmation sauvegarde
        Button.textContent = "Réinitialisé"

        document.getElementById("toggle-theme-complet").checked = true // on désactive le toggle harmonie (valeur par défaut)

        colorTheme("theme_azur", "elem1") // lancement de la fonction pour remttre les couleurs de base et également le li correspondant en position selected (li : Azur)

        // Pause
        await new Promise(r => setTimeout(r, 650))
        
        // Desactivation du button
        Button.disabled = false
        Button.textContent = "Réinitialiser le thème"
    }
    return
}

function reappliquerThemesForShortcut() { // pour réappliquer le thème au shorcut quand le navigateur le stocke dans le BFCache (page outils)
    let PreferenceUser = localStorage.getItem("ToggleThemeComplet") // recup valeur dans le local storage
            
    if (PreferenceUser == "True") {
        // Recup des champs
        let ShortcutAdd = document.getElementById("icone-add")
        let ShortcutHistorique = document.getElementById("icone-historique")
        let ShortcutPause = document.getElementById("icone-pause")

        // Recup des icones
        let IconeShortcutAdd = document.querySelector(".fs-icon_add")
        let IconeShortcutHistorique = document.querySelector(".fs-icon_historique")
        let IconeShortcutPause = document.querySelector(".fs-icon_pause")

        // Recup variable css
        const Style = getComputedStyle(document.documentElement)

        const CouleurAccentHover = Style.getPropertyValue("--COULEUR_ACCENT_HOVER")
        const CouleurBackground = Style.getPropertyValue("--COULEUR_BACKGROUND")

        if (ShortcutAdd && ShortcutHistorique && ShortcutPause) {
                // Mise des couleurs si l'élément est existant
                ShortcutAdd.style.background = CouleurAccentHover
                IconeShortcutAdd.style.color = CouleurBackground
                            
                ShortcutHistorique.style.background = CouleurAccentHover
                IconeShortcutHistorique.style.color = CouleurBackground

                ShortcutPause.style.background = CouleurAccentHover
                IconeShortcutPause.style.color = CouleurBackground
            }
                
        // Recup des champs (!!! pour la page de charge d'entraînement)
        let ButtonAdd = document.getElementById("add")
        let IconeAdd = document.querySelector(".fs-icon_add")

        let ButtonHistorique = document.getElementById("historique")
        let IconeHistorique = document.querySelector(".fs-icon_historique")

        let ButtonPause = document.getElementById("statut")
        let IconePause = document.querySelector(".fs-icon_pause")
                                        
        let TextInterieurButton = document.querySelectorAll(".txt_plus")

        if (ButtonAdd && ButtonHistorique && ButtonPause) {                         
            // changement couleur text in button
            TextInterieurButton.forEach(TextButton => {
                TextButton.style.color = CouleurBackground                    
            });

            // Mise des couleurs si l'élément est existant
            ButtonAdd.style.background = CouleurAccentHover
            ButtonAdd.style.boxShadow = "none"
            IconeAdd.style.color = CouleurBackground
                            
            ButtonHistorique.style.background = CouleurAccentHover
            ButtonHistorique.style.boxShadow = "none"
            IconeHistorique.style.color = CouleurBackground

            ButtonPause.style.background = CouleurAccentHover
            ButtonPause.style.boxShadow = "none"
            IconePause.style.color = CouleurBackground
        }
    }

    return
}

function Preference() {
    // Chercher les valeur dans la bdd
    const ColorUser = localStorage.getItem("ColorActuelleUse")
    if (ColorUser) {
        colorTheme(ColorUser, null) // on met l'id du li du thème en null pour pas que la fonction SelectedElement mettent à jour le li du thème en buggant
    }

    // Appelle à la fonction pour restaurer le thème des shorcuts quand la page est stokée dans le BFCache
    reappliquerThemesForShortcut()
}

// ne pas mettre en addevenlister sinon on perd en perf
Preference() // on change les couleurs de la page web ou le user navigue