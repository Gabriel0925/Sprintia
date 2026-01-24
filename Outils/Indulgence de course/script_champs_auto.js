function ReinitialisationOutil() {
    // Restauration des toggle par défaut
    localStorage.removeItem("SauvegardeIDC")
    localStorage.removeItem("DateSauvegardeIDC")
    
    // On supprime des datas
    localStorage.removeItem("FourchetteDistance")
    localStorage.removeItem("RecentDistance28J")
    localStorage.removeItem("RecentDistance7J")
    localStorage.removeItem("CoachInterpretation")
    localStorage.removeItem("FourchetteDistance")
    localStorage.removeItem("DateValueSauvegardeIDC")

    // Rechargement de la page pour assurer un bon rétablissement
    location.reload()
    
    return
}

function SauvegardeAuto() { // toggle sauvegarde auto
    const ToggleSauvegarde = event.target
    
    if (ToggleSauvegarde.checked) { // quand toggle est désactivé
        // sauvegarde en false
        localStorage.setItem("SauvegardeIDC", "False")

        // Desactivation d'une option si le toggle est desactiver  on cache la date sauvegarde
        document.getElementById("explication-fonction-date-afficher").style.display = "none"
        document.getElementById("conteneur-fonction-date-afficher").style.display = "none"
    } else { // quand toggle est activé
        localStorage.setItem("SauvegardeIDC", "True")

        // Desactivation d'une option
        document.getElementById("explication-fonction-date-afficher").style.display = "block"
        document.getElementById("conteneur-fonction-date-afficher").style.display = "flex" // mettre flex pour son conteneur !
    }

    return
}

function SauvegardeDate() { // Toggle sauvegarder date
    const ToggleSauvegardeDate = event.target

    if (ToggleSauvegardeDate.checked) { // Quand toggle est desactiver
        localStorage.setItem("DateSauvegardeIDC", "False")
    } else {
        localStorage.setItem("DateSauvegardeIDC", "True")
    }
    return
}

function Initialisation() {
    let ToggleSauvegarde = document.getElementById("toggle-sauvegarde-auto")
    let ToggleSauvegardeDate = document.getElementById("toggle-sauvegarde-date")

    let SauvegardeIDC = localStorage.getItem("SauvegardeIDC")
    let SauvegardeDateIDC = localStorage.getItem("DateSauvegardeIDC")

    if (SauvegardeIDC == null) {
        localStorage.setItem("SauvegardeIDC", "True")
    }

    if (SauvegardeIDC == "False") {
        ToggleSauvegarde.checked = true

        // Desactivation d'une option
        document.getElementById("explication-fonction-date-afficher").style.display = "none"
        document.getElementById("conteneur-fonction-date-afficher").style.display = "none"
    }

    if (SauvegardeDateIDC == "False") {
        ToggleSauvegardeDate.checked = true
    }
}
window.addEventListener("DOMContentLoaded", () => {
    // Mise en place du toggle pour le mettre en position activer ou desactiver
    Initialisation()
})