function typeRunner(value) {
    // enregistrement du type de coureur
    localStorage.setItem("typeCoureur", value)
    return
}

document.addEventListener("DOMContentLoaded", () => {
    const selectTypeRunner = document.getElementById("type-coureur-user")
    if (selectTypeRunner) {selectTypeRunner.addEventListener("change", (event) => {typeRunner(event.target.value)})}
})

window.onload = function() {
    // Affichage du type de coureur enregistré
    const typeCoureur = localStorage.getItem("typeCoureur")
    if (typeCoureur) {
        document.getElementById("type-coureur-user").value = typeCoureur
    }
}