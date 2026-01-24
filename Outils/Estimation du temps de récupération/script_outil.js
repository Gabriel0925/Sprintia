function EstimationTempsRecuperation() {
    // Recup valeur des champs
    let DureeUser = parseInt(document.getElementById("duree-entrainement-user").value.trim())
    let ValueRpeUser = parseInt(document.querySelector(".slider progress").value)
    let ProfilUser = document.getElementById("methode-user").value

    // Initialisation
    let CoefficientProfil = [1.35, 0.95, 0.65]

    // Calcul intensité (utilisation de pow pr que les RPE haut soit plus amplifiées que les petits rpe)
    ValueRpeUser = Math.pow(ValueRpeUser, 1.5) // ex : RPE=3 alors 3**1.5

    // Vérification des champs 
    if (isNaN(DureeUser)) {
        alert("Erreur de saisie : le champ 'Durée de l'entraînement' doit être rempli.");
        return
    }
    if (DureeUser <= 0) {
        alert("Valeur non valide, la durée votre entraî. doivent être un nombre supérieur à 0.")
        return
    }

    if (ProfilUser === "occasionnel") {
        CoefficientProfil = CoefficientProfil[0]
    } else if (ProfilUser === "regulier") {
        CoefficientProfil = CoefficientProfil[1]
    } else {
        CoefficientProfil = CoefficientProfil[2]
    }

    // Calcul
    let Charge = DureeUser*ValueRpeUser
    let TempsRecup = (Charge*CoefficientProfil)/15

    // Remise des valeurs plus logique
    if (TempsRecup > 120) TempsRecup = 120

    let Result = Math.round(TempsRecup) + " h"

    document.querySelector(".temps-recup").textContent = Result
}

function ComboBox() {
    // Recup valeur des champs
    let DureeUser = parseInt(document.getElementById("duree-entrainement-user").value.trim())
    let ValueRpeUser = parseInt(document.querySelector(".slider progress").value)

    if (isNaN(DureeUser) || isNaN(ValueRpeUser)) {
        return
    }

    EstimationTempsRecuperation()
}