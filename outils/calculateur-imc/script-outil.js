function calculIMC() {
    // Récupérer la valeur du champ
    let poidsUser = parseFloat(document.getElementById("poids-user").value)
    let tailleUser = parseFloat(document.getElementById("taille-user").value)

    // Vérification des champs
    if (isNaN(poidsUser)|| isNaN(tailleUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (poidsUser <= 0 || tailleUser <= 0) {
        alert("Valeur non valide, le poids et la taille doivent être un nombre supérieur à 0.")
        return
    }
    if (poidsUser >= 1000) {
        alert("Valeur non valide, le poids doit être un nombre inférieur à 1000.")
        return
    }
    if (tailleUser >= 350) {
        alert("Valeur non valide, la taille doit être un nombre inférieur à 350.")
        return
    }

    // Calcul en appliquant la formule
    let imcResult = poidsUser/((tailleUser/100)**2) // conversion des cm en m pour la taille

    // détermination de l'interpretation
    const palierInterpretation = [
        {"imcMax":18.5, "interpretation":"<strong>Zone maigreur :</strong><br>D'après l'IMC vous êtes super actif·ve mais si vous vous sentez mal le mieux serait de consulter un médecin !"},
        {"imcMax":25, "interpretation":"<strong>Zone de corpulence normale :</strong><br>Parfait, d'après l'IMC vous êtes équilibré·e, continuez comme ça !"},
        {"imcMax":30, "interpretation":"<strong>Zone de surpoids :</strong><br>D'après l'IMC vous êtes en surpoids mais je suis sûr que vous avez juste trop de muscles et ça l'IMC ne peut pas le savoir !"},
        {"imcMax":35, "interpretation":"<strong>Zone obésité modérée :</strong><br> Un petit changement d'habitude aujourd'hui fera une grande différence demain ! Si vous vous sentez mal le mieux serait de consulter un médecin !"},
        {"imcMax":40, "interpretation":"<strong>Zone d'obésité sévère :</strong><br>Si vous vous sentez bien c'est le plus important, ne vous comparez pas aux autres comparez-vous à la personne que vous étiez hier !"},
        {"imcMax":Infinity, "interpretation":"<strong>Zone d'obésité morbide :</strong><br>Vous vous améliorez de jour en jour mais si vous vous sentez mal le mieux serait de consulter un médecin !"}
    ]

    // parcours du tableau de dico
    for (const palier of palierInterpretation) {
        if (imcResult <= palier["imcMax"]) { // si l'imc est inf aux palier alors on affiche les résultats (resultat imc + interpretation)
            document.querySelector(".zone-result-name-result").innerHTML = "Votre IMC : <strong>" + imcResult.toFixed(1).replace(".", ",") + "</strong>"
            document.querySelector(".zone-result-interpretation").innerHTML = palier["interpretation"]
            break
        }
    }

    return
}

document.addEventListener("DOMContentLoaded", async () => {
    await remplissageChamps(["taille-user", "poids-user"])
    
    const buttonCalcul = document.getElementById("button-calcul-imc")
    if (buttonCalcul) {buttonCalcul.addEventListener("click", calculIMC)}

    if (document.getElementById("taille-user").value && document.getElementById("poids-user").value && !isNaN(document.getElementById("taille-user").value) && !isNaN(document.getElementById("poids-user").value)) {
        document.getElementById("button-calcul-imc").click()
    }

    // pour détecter si lorsqu'on est dans le formulaire il y a un appuie sur la touche entrée
    let formKeyEntry = document.querySelector(".form")
    formKeyEntry.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            calculIMC()
        }
    })
})
