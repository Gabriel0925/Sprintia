// Pour gérer l'ouverture/fermeture du menu hamburger
const burgerMenuButton = document.querySelector('.burger-menu-button')
const burgerMenuButtonIcon = document.querySelector('.burger-menu-button i')
const burgerMenu = document.querySelector('.burger-menu')

burgerMenuButton.onclick = function() {
    burgerMenu.classList.toggle('open')
    const isOpen = burgerMenu.classList.contains('open')
    burgerMenuButtonIcon.classList = isOpen ? 'fs-icon_fermer' : 'fs-icon_menu'
}


function afficher_plus(lieu) {
    // Pour le nb de card a ajouter
    let NbCardAjoutee = 9
    let NbCardBase = 9
    let NbCardTotal = 0

    // la fonction gère plusieur lieu ds le site
    const CardNouveautes = document.querySelectorAll(".card-nouveautes:not(.visible)")
    const CardOutils = document.querySelectorAll(".card-outil:not(.visible)")

    const ButtonAfficherPlus = document.getElementById("button_afficher_plus") 

    // Initialisation
    const Lieu = [CardNouveautes, CardOutils]
    let CardLieu = ""
    // Attribution en fonction du lieu
    if (lieu === "nouveautes") {CardLieu = Lieu[0]} else if (lieu === "outils") {CardLieu = Lieu[1]}

    // tant que i est inférieur à NbCardAjoutee la boucle ne s'arrete pas. "i++" permet de faire plus 1 à chaque fois
    for (let i = 0; i < NbCardAjoutee; i++) {
        // CardOutils est une liste
        if (CardLieu[i]) {
            CardLieu[i].classList.add("visible")
        } else {
            ButtonAfficherPlus.classList.add("absent")
            break
        }

        // mise à jour du compteur
        NbCardTotal += 1
    }

    if (lieu === "outils") {
        const NbCardLastSession = sessionStorage.getItem("NbCardOutilSave")
        if (NbCardLastSession) {
            NbCardTotal = parseInt(NbCardLastSession) + NbCardBase
        } else {
            NbCardTotal = NbCardTotal + NbCardBase
        }
        sessionStorage.setItem("NbCardOutilSave", NbCardTotal)
    } else {
        const NbCardLastSession = sessionStorage.getItem("NbCardNouveauteSave")
        if (NbCardLastSession) {
            NbCardTotal = parseInt(NbCardLastSession) + NbCardBase
        } else {
            NbCardTotal = NbCardTotal + NbCardBase
        }
        sessionStorage.setItem("NbCardNouveauteSave", NbCardTotal)
    }

    return
}

function SprintiaBeta() {
    let Logo = document.querySelector("div.logo a")

    Logo.textContent = "Sprintia Alpha"
    return
}

window.addEventListener("DOMContentLoaded", () => {
    SprintiaBeta()
})

window.addEventListener("pageshow", (event) => {
    // Pour contrer le BFCache parce qu'il mettait en cache mes anciennes pages pour éviter de les recharger mais ça causait probleme pour les thèmes
    if (event.persisted) { // forcer un reload quand on fait un retour donc quand la page viens du BFCache
        window.location.reload()
    }
})