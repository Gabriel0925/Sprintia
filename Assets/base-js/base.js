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


// maj local storage de Sprintia 4.0 à 4.0.1
localStorage.removeItem("ThemeActuel") // car le choix de thème clair ou sombre a été nerf