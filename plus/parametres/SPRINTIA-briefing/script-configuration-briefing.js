function favoriteIA(idElement) {
    let eltSelected = document.querySelectorAll(".choice-item.selected")
    let eltNow = document.getElementById(idElement)

    if (eltSelected.length > 0) { // si un élément est déjà séléctionné
        eltSelected[0].classList.remove("selected")
    }
    if (eltNow) {
        eltNow.classList.add("selected")
        localStorage.setItem("iaFavorite", idElement)
    }
    
}

function reinitialiserBriefing(btn) {
    if (confirm("Êtes-vous sur de vouloir restaurer les paramètres par défaut de SPRINTIA Briefing ?")) {
        btn.textContent = "Réinitialisation..."
        btn.disabled = true
        
        // --- IA Favorite ---
        localStorage.removeItem("iaFavorite") // on supprimer de la bdd
        favoriteIA("vibe") // on appelle la fonction comme si il y avait eu un click sur l'elt vibe


        // --- Personnalisation des prompts ---
        document.getElementById("toggle-personnalite-coach").checked = false
        localStorage.removeItem("personnaliteCoachBriefing")


        // --- Niveaux d'analyse ---
        // restauration du select en modere
        document.getElementById("niveaux-analyse-user").value = "modere"
        localStorage.removeItem("niveauAnalyseIA") // maj dans le local storage
        
        setTimeout(() => {
            btn.textContent = "Réinitialisé"
        }, 650);
        
        setTimeout(() => {
            btn.textContent = "Réinitialisation Briefing"
            btn.disabled = false
        }, 1300);
    }
}

function personnaliteCoach(event) {
    if (event.target.checked) {
        localStorage.setItem("personnaliteCoachBriefing", false)
    } else {
        localStorage.setItem("personnaliteCoachBriefing", true)
    }
}

function restaureSettings() {
    // --- IA Favorite ---
    let iaFavoriteUser = localStorage.getItem("iaFavorite")

    if (iaFavoriteUser != null) { // si il y a des datas
        document.getElementById(iaFavoriteUser).classList.add("selected")
    } else {
        document.getElementById("vibe").classList.add("selected")
    }

    // --- Personnalisation des prompts ---
    const personnaliteCoachUser = localStorage.getItem("personnaliteCoachBriefing")
    if (personnaliteCoachUser == "false") { // si le user à désactiver la fonction
        document.getElementById("toggle-personnalite-coach").checked = true
    } else { // si il l'a activé
        document.getElementById("toggle-personnalite-coach").checked = false
    }


    // --- Niveaux d'analyse ---
    let niveauAnalyseUser = localStorage.getItem("niveauAnalyseIA")
    if (niveauAnalyseUser == null) {niveauAnalyseUser = "modere"} // par défaut c'est le niveau modere
    // restauration du select
    document.getElementById("niveaux-analyse-user").value = niveauAnalyseUser
}

document.addEventListener("DOMContentLoaded", () => {
    const allItemIA = document.querySelectorAll(".choice-item")
    if(allItemIA) {
        let compteurAllItem = 0
        let tableauOrdreIA = ["vibe", "gemini", "chat-gpt", "claude", "meta-ai", "perplexity", "grok", "copilot", "deepseek", "ia-locale"]

        allItemIA.forEach(element => {
            let iaAssocier = tableauOrdreIA[compteurAllItem]

            element.addEventListener("click", () => {
                favoriteIA(iaAssocier)
            })

            compteurAllItem+=1
        });
    }

    const togglePersonnaliteCoach = document.getElementById("toggle-personnalite-coach")
    if (togglePersonnaliteCoach) {togglePersonnaliteCoach.addEventListener("click", (event) => {personnaliteCoach(event)})}

    const buttonReinitialiser = document.getElementById("reinitialiser-briefing")
    if (buttonReinitialiser) {buttonReinitialiser.addEventListener("click", function() {reinitialiserBriefing(this)})}

    const selectNiveauxAnalyse = document.getElementById("niveaux-analyse-user")
    if (selectNiveauxAnalyse) {selectNiveauxAnalyse.addEventListener("change", (event) => {localStorage.setItem('niveauAnalyseIA', event.target.value)})}

    restaureSettings()
})