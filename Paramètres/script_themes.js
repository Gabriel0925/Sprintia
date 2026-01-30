// Initialisation variable
let ThemeActuel = "Sombre"
let ColorActuelleUse = "theme_azur"


// Thèmes
function mode(event) {
    const toggle = event.target;
    if (toggle.checked) { 
        document.documentElement.style.setProperty("--COULEUR_BACKGROUND", "#FFFFFF");
        document.documentElement.style.setProperty("--COULEUR_BACKGROUND_CARD", "#e9e9e9ff");
        document.documentElement.style.setProperty("--COULEUR_BACKGROUND_CARD_HOVER", "#d5d1d1");

        document.documentElement.style.setProperty("--COULEUR_TEXT_PRINCIPAL", "#010101");
        document.documentElement.style.setProperty("--COULEUR_TEXT_SECONDAIRE", "#757479");

        document.documentElement.style.setProperty("--COULEUR_LUMIERE_CARD", "#efefef");
 
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_0", "#0f759d");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_1", "#e70e32");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_2", "#cc25cf");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_3", "#8e29e1ff");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_4", "#197b41");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_5", "#1f7c76");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_6", "#5b7286");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_7", "#fa2d72");

        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D1", "#146fdd");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D2", "#f358e9");

        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D3", "#0077be");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D4", "#f4a460");

        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D5", "#8153ff");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D6", "#00cf56");

        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D7", "#f9a81c");
        document.documentElement.style.setProperty("--COULEUR_PASTILLES_D8", "#e73f01");
        
        document.documentElement.style.setProperty("--URL_FLECHE_ICON", 'url("../Outils/Icons/icon_fleche_clair.svg")');
        document.documentElement.style.setProperty("--URL_FLECHE_ICON_REVERSE", 'url("../Outils/Icons/icon_fleche_sombre.svg")');
        
        ThemeActuel = "Clair"
        localStorage.setItem("ThemeActuel", "Clair");   
    } else {
        document.documentElement.style.removeProperty("--COULEUR_BACKGROUND");
        document.documentElement.style.removeProperty("--COULEUR_BACKGROUND_CARD");
        document.documentElement.style.removeProperty("--COULEUR_BACKGROUND_CARD_HOVER");

        document.documentElement.style.removeProperty("--COULEUR_LUMIERE_CARD");

        document.documentElement.style.removeProperty("--COULEUR_TEXT_PRINCIPAL");
        document.documentElement.style.removeProperty("--COULEUR_TEXT_SECONDAIRE");

        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_0");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_1");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_2");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_3");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_4");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_5");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_6");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_7");

        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D1");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D2");

        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D3");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D4");

        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D5");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D6");

        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D7");
        document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D8");

        document.documentElement.style.removeProperty("--URL_FLECHE_ICON");
        document.documentElement.style.removeProperty("--URL_FLECHE_ICON_REVERSE");

        ThemeActuel = "Sombre"
        localStorage.setItem("ThemeActuel", "Sombre");
    }
        
    color_theme(ColorActuelleUse, "PasToucher")
}
function dark_mode() {
    document.documentElement.style.removeProperty("--COULEUR_BACKGROUND");
    document.documentElement.style.removeProperty("--COULEUR_BACKGROUND_CARD");
    document.documentElement.style.removeProperty("--COULEUR_BACKGROUND_CARD_HOVER");

    document.documentElement.style.removeProperty("--COULEUR_LUMIERE_CARD");

    document.documentElement.style.removeProperty("--COULEUR_TEXT_PRINCIPAL");
    document.documentElement.style.removeProperty("--COULEUR_TEXT_SECONDAIRE");

    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_0");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_1");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_2");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_3");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_4");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_5");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_6");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_7");

    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D1");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D2");

    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D3");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D4");

    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D5");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D6");

    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D7");
    document.documentElement.style.removeProperty("--COULEUR_PASTILLES_D8");

    document.documentElement.style.removeProperty("--URL_FLECHE_ICON");
    document.documentElement.style.removeProperty("--URL_FLECHE_ICON_REVERSE");

    ThemeActuel = "Sombre"
    localStorage.setItem("ThemeActuel", "Sombre");
    
    color_theme(ColorActuelleUse, "PasToucher")
}
function light_mode() {
    document.documentElement.style.setProperty("--COULEUR_BACKGROUND", "#FFFFFF");
    document.documentElement.style.setProperty("--COULEUR_BACKGROUND_CARD", "#e9e9e9ff");
    document.documentElement.style.setProperty("--COULEUR_BACKGROUND_CARD_HOVER", "#d5d1d1");

    document.documentElement.style.setProperty("--COULEUR_LUMIERE_CARD", "#efefef");

    document.documentElement.style.setProperty("--COULEUR_TEXT_PRINCIPAL", "#010101");
    document.documentElement.style.setProperty("--COULEUR_TEXT_SECONDAIRE", "#757479");
 
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_0", "#0f759d");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_1", "#e70e32");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_2", "#cc25cf");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_3", "#8e29e1ff");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_4", "#197b41");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_5", "#1f7c76");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_6", "#5b7286");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_7", "#fa2d72");

    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D1", "#146fdd");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D2", "#f358e9");

    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D3", "#0077be");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D4", "#f4a460");

    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D5", "#8153ff");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D6", "#00cf56");

    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D7", "#f9a81c");
    document.documentElement.style.setProperty("--COULEUR_PASTILLES_D8", "#e73f01");
        
    document.documentElement.style.setProperty("--URL_FLECHE_ICON", 'url("../Outils/Icons/icon_fleche_clair.svg")');
    document.documentElement.style.setProperty("--URL_FLECHE_ICON_REVERSE", 'url("../Outils/Icons/icon_fleche_sombre.svg")');
        
    ThemeActuel = "Clair"
    localStorage.setItem("ThemeActuel", "Clair");
    
    color_theme(ColorActuelleUse, "PasToucher")
}

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
    // si il ne faut pas toucher à l'id par exemple quand on switch du mode clair au sombre
    if (id_li !== "PasToucher") {
        maj_li_selected(id_li)
    }

    if (ThemeActuel === "Sombre") {
        if (ColorActuelle === "theme_carmin") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#fe504a");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#ff7b77");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#FF6B66");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FF9591");
            ColorActuelleUse = "theme_carmin"

        } else if (ColorActuelle === "theme_fuchsia") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#ff6aff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#ffa6ff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#fe9afe");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FFC2FF");
            ColorActuelleUse = "theme_fuchsia"

        } else if (ColorActuelle === "theme_lavande") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#ba6fff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#cd97ff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#D6A6FF");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#E6C7FF");
            ColorActuelleUse = "theme_lavande"

        } else if (ColorActuelle === "theme_vegetation") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#0CBB5BFF");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#60f3a2");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#3DFF94");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#99fdc9");
            ColorActuelleUse = "theme_vegetation"

        } else if (ColorActuelle === "theme_feu") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#ffb41f");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#e73f01");   
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#ffd170");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FF7547"); 
            ColorActuelleUse = "theme_feu"
        
        } else if (ColorActuelle === "theme_menthe") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#0ac3a7");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#68e8d4");    
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#42f7dc");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#9cfdf0");
            ColorActuelleUse = "theme_menthe"
        
        } else if (ColorActuelle === "Hortensia") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#3a91ff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#f782f0");  
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#85BBFF");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FBAEFA");  
            ColorActuelleUse = "Hortensia"
        
        } else if (ColorActuelle === "theme_plage") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#1498e4");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#fcaf6b");   
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#65C0F5");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FFD0A6"); 
            ColorActuelleUse = "theme_plage"
        
        } else if (ColorActuelle === "Aurore") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#a477fe");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#4ce58c");   
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#C9ADFF");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#82F2B2"); 
            ColorActuelleUse = "Aurore"
        
        } else if (ColorActuelle === "theme_azur") {
            document.documentElement.style.removeProperty("--COULEUR_ACCENT");
            document.documentElement.style.removeProperty("--COULEUR_ACCENT_HOVER");    
            document.documentElement.style.removeProperty("--COULEUR_ACCENT_CONTRASTER");    
            document.documentElement.style.removeProperty("--COULEUR_ACCENT_CONTRASTER_HOVER");    
            ColorActuelleUse = "theme_azur"
        
        } else if (ColorActuelle === "theme_pierre_lune") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#7bb8de");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#b5dff9");    
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#c4e8ff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#D6EDFD"); 
            ColorActuelleUse = "theme_pierre_lune" 
        
        } else if (ColorActuelle === "theme_framboise") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#ea5084");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#ff80aa"); 
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#FF88B0");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FFB3CC");      
            ColorActuelleUse = "theme_framboise" 
      
        }
    } else {
        if (ColorActuelle === "theme_carmin") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#e70e32");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#f6455f"); 
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#bb102d");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#e61b3d");
            ColorActuelleUse = "theme_carmin" 
        
        } else if (ColorActuelle === "theme_fuchsia") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#cc25cf");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#f76ff9"); 
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#a520a7");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#d22ed5"); 
            ColorActuelleUse = "theme_fuchsia"
        
        } else if (ColorActuelle === "theme_lavande") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#8e29e1ff");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#bc73f8");  
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#7122b2");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#8f2fdf");
            ColorActuelleUse = "theme_lavande"
        
        } else if (ColorActuelle === "theme_vegetation") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#197b41");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#19bc5d");  
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#156736");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#1d8a48");
            ColorActuelleUse = "theme_vegetation"
        
        } else if (ColorActuelle === "theme_feu") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#f9a81c");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#e73f01");   
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#E07A00");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#C23501"); 
            ColorActuelleUse = "theme_feu"  
        
        } else if (ColorActuelle === "theme_menthe") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#1f7c76");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#32bbb2");  
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#1B6C67");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#21867f"); 
            ColorActuelleUse = "theme_menthe"
        
        } else if (ColorActuelle === "Hortensia") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#146fdd");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#f358e9");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#105dba");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#d14bc8");
            ColorActuelleUse = "Hortensia"
        
        } else if (ColorActuelle === "theme_plage") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#0077be");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#f4a460");    
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#005f96");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#d58b4f");
            ColorActuelleUse = "theme_plage"
        
        } else if (ColorActuelle === "Aurore") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#7746fd");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#00cf56");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#613cc7");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#02ab48");
            ColorActuelleUse = "Aurore"
        
        } else if (ColorActuelle === "theme_azur") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#0f759d");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#1d9ed0"); 
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#0a5979");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#0F759D");
            ColorActuelleUse = "theme_azur" 
        
        } else if (ColorActuelle === "theme_pierre_lune") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#5b7286");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#739cbd"); 
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#485b6b");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#607a91");
            ColorActuelleUse = "theme_pierre_lune" 
        
        } else if (ColorActuelle === "theme_framboise") {
            document.documentElement.style.setProperty("--COULEUR_ACCENT", "#fe1e69"); 
            document.documentElement.style.setProperty("--COULEUR_ACCENT_HOVER", "#fc6b9b");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER", "#DF1A5C");
            document.documentElement.style.setProperty("--COULEUR_ACCENT_CONTRASTER_HOVER", "#FE1E69");  
            ColorActuelleUse = "theme_framboise" 
        
        } 
    }
    localStorage.setItem("ColorActuelleUse", ColorActuelleUse);
}

// Thème par défaut
function theme_defaut(id_li) {
    ThemeActuel = "Sombre"
    localStorage.setItem("ThemeActuel", "Sombre");
    
    ColorActuelleUse = "theme_azur"
    localStorage.setItem("ColorActuelleUse", ColorActuelleUse);

    // Remise du toogle sur desactiver
    localStorage.setItem("ToggleThemeComplet", "False")
    
    location.reload()
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

        const CouleurAccent = Style.getPropertyValue("--COULEUR_ACCENT")
        const CouleurBackground = Style.getPropertyValue("--COULEUR_BACKGROUND")

        if (ShortcutAdd && ShortcutHistorique && ShortcutPause) {
            // Mise des couleurs si l'élément est existant
            ShortcutAdd.style.background = CouleurAccent
            IconeShortcutAdd.style.color = CouleurBackground
                    
            ShortcutHistorique.style.background = CouleurAccent
            IconeShortcutHistorique.style.color = CouleurBackground

            ShortcutPause.style.background = CouleurAccent
            IconeShortcutPause.style.color = CouleurBackground

            }
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
            ButtonAdd.style.background = CouleurAccent
            ButtonAdd.style.boxShadow = "none"
            IconeAdd.style.color = CouleurBackground
                    
            ButtonHistorique.style.background = CouleurAccent
            ButtonHistorique.style.boxShadow = "none"
            IconeHistorique.style.color = CouleurBackground

            ButtonPause.style.background = CouleurAccent
            ButtonPause.style.boxShadow = "none"
            IconePause.style.color = CouleurBackground

        }

    return
}

function user_preference() {
    // Chercher les valeur dans la bdd
    const ThemeUser = localStorage.getItem("ThemeActuel")
    const ColorUser = localStorage.getItem("ColorActuelleUse")

    if (ThemeUser === "Clair") {
        light_mode() 
    } else {
        // Si rien n'est sauvegardé ou si c le mode sombre
        dark_mode()
    }

    if (ColorUser) {
        color_theme(ColorUser)
    }

    // Appelle à la fonction pour restaurer le thème des shorcuts quand la page est stokée dans le BFCache
    ReappliquerThemesForShortcut()
}

// ça permet de lancer la fonction une fois que la page est chargée
// parce que si on enleves cela le javascript va modifier les buttons alors qu'ils ne sont pas encore créer
document.addEventListener("DOMContentLoaded", function() {
    // Pr restaurer la position du toggle
    let toggle_value = document.getElementById("toggle-mode")
    let last_value_theme = localStorage.getItem("ThemeActuel")
    // Si il y a une valeur au toggle et que le theme est clair alors on met le toggle sur true avec mon css le toggle est en position desactiver
    if (toggle_value && last_value_theme === "Clair") {
        toggle_value.checked = true
    }

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


user_preference()