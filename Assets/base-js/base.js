// Pour gérer l'ouverture/fermeture du menu hamburger
const burgerMenuButton = document.querySelector('.burger-menu-button')
const burgerMenuButtonIcon = document.querySelector('.burger-menu-button i')
const burgerMenu = document.querySelector('.burger-menu')

burgerMenuButton.onclick = function() {
    burgerMenu.classList.toggle('open')
    const isOpen = burgerMenu.classList.contains('open')
    burgerMenuButtonIcon.classList = isOpen ? 'fs-icon_fermer' : 'fs-icon_menu'
}

window.onclick = function (event) { // on track les click sur la page complete
    let TrackClickBurgerMenuButton = burgerMenuButton.contains(event.target) // pour tracker si il y a un click sur le bouton si oui = true sinon = false
    let TrackClickBurgerMenuOpen = burgerMenu.contains(event.target)
    
    if (TrackClickBurgerMenuButton == false && TrackClickBurgerMenuOpen == false) { // si tu as cliqué autre part que sur le bouton fermer ou sur/dans le burger-menu
        // on referme le burgermenu
        burgerMenu.classList.remove("open")
        burgerMenuButtonIcon.classList.add("fs-icon_menu")
    }
}

// Pr gérer le BFCache
window.addEventListener("pageshow", (event) => {
    // Pour contrer le BFCache parce qu'il mettait en cache mes anciennes pages pour éviter de les recharger mais ça causait probleme pour les thèmes
    if (event.persisted) { // event.persisted = quand la page est dans le cache
        // forcer de lancer la fonction qui charge le thème quand on fait un retour donc quand la page viens du BFCache
        user_preference()
    }
});


// Pour la mise à jour du local storage
function majLocalStorage(versionStockee) {
    // migration de 4.0.0 à 4.0.1
    if (versionStockee == "4.0.0") {
        localStorage.removeItem("ThemeActuel") // car le choix de thème clair ou sombre a été nerf
        localStorage.removeItem("DisplayConseil") // car les astuces sur la page d'accueil ont été supprimé

        let tableauOutilPin = localStorage.getItem("OutilsPin")

        if (tableauOutilPin != null) { // si il y a rien dans le local storage (=null) on ne fait rien
            tableauOutilPin = JSON.parse(tableauOutilPin) // transformation en objet js

            tableauOutilPin.forEach(element => {
                if (element == "Estimation de la transpiration") { // si dans le local storge des outil pin il y a estimation de la transpi alors on le remplace par le nouveau nom de l'outil
                    let indexElement = tableauOutilPin.indexOf(element)
                    tableauOutilPin[indexElement] = "Hydratation post-séance" // nouveau nom de l'outil
                    localStorage.setItem("OutilsPin", JSON.stringify(tableauOutilPin))
                }
            });
        }

        localStorage.setItem("VersionLocalStorage", "4.0.1")
        versionStockee = "4.0.1" // maj de la variable pour enchaine avec les futures if de nouvelle version
    }
    
    // écrire les futures maj dans un if en dessous 

    return
}

const versionActuelle = "4.0.1"
let versionStockee = localStorage.getItem("VersionLocalStorage") || "4.0.0"

if (versionStockee != versionActuelle) {
    majLocalStorage(versionStockee)
}