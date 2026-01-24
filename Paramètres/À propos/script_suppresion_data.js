async function SupprimerDatas() {
    let ButtonReinitialiser = document.getElementById("reinitialiser-sprintia")
    ButtonReinitialiser.textContent = "Cette fonctionnalité n'est pas encore disponible dans cette beta"
    // Pause
    await new Promise(r => setTimeout(r, 2500))
    // remise etat normal
    ButtonReinitialiser.textContent = "Réinitialiser Sprintia"
    return
}