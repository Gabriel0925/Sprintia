// Initialisation variable
let ColorActuelleUse = "theme_azur"

function maj_li_selected(id_li) {
    const old_selected_li = document.querySelector(".option-color.selected")
    if (old_selected_li) {
        old_selected_li.classList.remove("selected")
    }
    const new_selected_li = document.getElementById(id_li)
    if (new_selected_li) {
        new_selected_li.classList.add("selected")
    }
}

// Couleur d'acentuation
function color_theme(ColorActuelle, id_li) {
    if (ColorActuelle === "theme_carmin") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#fe3c35");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#f9645e");
        ColorActuelleUse = "theme_carmin"

    } else if (ColorActuelle === "theme_fuchsia") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#fa5bfa");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#ffa0ff");
        ColorActuelleUse = "theme_fuchsia"

    } else if (ColorActuelle === "theme_lavande") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#ae5ef9");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#d29eff");
        ColorActuelleUse = "theme_lavande"

    } else if (ColorActuelle === "theme_vegetation") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#0CBB5BFF");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#45ff99");
        ColorActuelleUse = "theme_vegetation"

    } else if (ColorActuelle === "theme_feu") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#ffb82b");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#ff5b1f");   
        ColorActuelleUse = "theme_feu"
        
    } else if (ColorActuelle === "theme_menthe") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#0ac3a7");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#4af6dc");
        ColorActuelleUse = "theme_menthe"
        
    } else if (ColorActuelle === "Hortensia") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#3a91ff");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#f782f0");  
        ColorActuelleUse = "Hortensia"
        
    } else if (ColorActuelle === "theme_plage") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#1498e4");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#fcaf6b");   
        ColorActuelleUse = "theme_plage"
        
    } else if (ColorActuelle === "Aurore") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#a477fe");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#4ce58c");   
        ColorActuelleUse = "Aurore"
        
    } else if (ColorActuelle === "theme_azur") {
        document.documentElement.style.removeProperty("--COULEUR_ACCENT");
        document.documentElement.style.removeProperty("--COULEUR_ACCENT2");        
        ColorActuelleUse = "theme_azur"
        
    } else if (ColorActuelle === "theme_pierre_lune") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#6aabd3");  
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#acdefd");
        ColorActuelleUse = "theme_pierre_lune" 
        
    } else if (ColorActuelle === "theme_framboise") {
        document.documentElement.style.setProperty("--COULEUR_ACCENT", "#f14d84");
        document.documentElement.style.setProperty("--COULEUR_ACCENT2", "#ff91b6");     
        ColorActuelleUse = "theme_framboise" 
      
    }
    
    localStorage.setItem("ColorActuelleUse", ColorActuelleUse);
    maj_li_selected(id_li)
}

// Thème par défaut
async function ReinitialiserTheme(id_li, value) {
    // Demande de confirmation avant
    if (confirm("Êtes-vous sur de vouloir réinitialiser le thème ?")) {
        let Button = document.getElementById("reinitialiser") // Recup du bouton
        // Desactivation du button
        Button.disabled = true
        Button.textContent = "Réinitialisation..."
        
        ColorActuelleUse = "theme_azur"
        localStorage.setItem("ColorActuelleUse", ColorActuelleUse);

        localStorage.setItem("ToggleThemeComplet", "False")

        // Légère pause
        await new Promise(r => setTimeout(r, 650))

        // confirmation sauvegarde
        Button.textContent = "Réinitialisé"

        document.getElementById("toggle-theme-complet").checked = true // on active/desactive les toggle pour les remttre par defaut
        user_preference() // relance de la fonction pour remettre le thème par defaut
        maj_li_selected("elem1") // on remet le li correspondant

        // Pause
        await new Promise(r => setTimeout(r, 650))
        
        // Desactivation du button
        Button.disabled = false
        Button.textContent = "Réinitialiser le thème"
    }
    return
}

function ReappliquerThemesForShortcut() { // pour réappliquer le thème au shorcut quand le navigateur le stocke dans le BFCache (page outils)
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

function user_preference() {
    localStorage.removeItem("ThemeActuel") // pour la maj Sprintia 4.0.1 car le theme clair est nerf

    // Chercher les valeur dans la bdd
    const ColorUser = localStorage.getItem("ColorActuelleUse")

    if (ColorUser) {
        color_theme(ColorUser)
    }

    // Appelle à la fonction pour restaurer le thème des shorcuts quand la page est stokée dans le BFCache
    ReappliquerThemesForShortcut()
}

// ça permet de lancer la fonction une fois que la page est chargée
// parce que si on enleves cela le javascript va modifier les buttons alors qu'ils ne sont pas encore créer
document.addEventListener("DOMContentLoaded", function() {
    // Pr restaure le selected du li
    let color_actuelle_id = {
        "theme_azur": "elem1",
        "theme_carmin": "elem2",
        "theme_fuchsia": "elem3",
        "theme_lavande": "elem4",
        "theme_vegetation": "elem5",
        "theme_feu": "elem6",
        "theme_menthe": "elem7",
        "theme_pierre_lune": "elem8",
        "theme_framboise": "elem9",
        "theme_plage": "elem10",
        "Hortensia": "elem11",
        "Aurore": "elem12"
    }
    let last_value_color = localStorage.getItem("ColorActuelleUse")
        
    // on cherche ds le dico    
    let id_li = color_actuelle_id[last_value_color]

    maj_li_selected(id_li)
})

function ThemeComplet(event) {
    let ToggleThemeComplet = event.target

    if (ToggleThemeComplet.checked) { // quand toggle est desactiver
        localStorage.setItem("ToggleThemeComplet", "False")
    } else { // quand toggle est activé
        localStorage.setItem("ToggleThemeComplet", "True")
    }

    return
}

// ne pas mettre en addevenlister sinon on perd en perf
user_preference()