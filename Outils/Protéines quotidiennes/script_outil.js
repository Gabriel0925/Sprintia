function EstimationProteines() {
    // Recupération des datas des champs
    let ObjectifUser = document.getElementById("objectif-user").value
    let PoidsUser = parseFloat(document.getElementById("poids-user").value.trim().replace(",", "."))

    // Vérification des champs
    if (isNaN(PoidsUser)) {
        alert("Erreur de saisie : le champ 'Poids' doit être rempli.");
        return
    }
    if (PoidsUser <= 0) {
        alert("Valeur non valide, le poids doit être un nombre supérieur à 0.")
        return
    }
    if (PoidsUser >= 1000) {
        alert("Valeur non valide, le poids doit être un nombre inférieur à 1000.")
        return
    }

    // Initialisation
    let Coefficient = 0

    // Attribution des coefficients
    if (ObjectifUser === "Meilleure") {
        Coefficient = 1
    } else if (ObjectifUser === "Maintien") {
        Coefficient = 1.7
    } else if (ObjectifUser === "Minimum") {
        Coefficient = 0.8
    } else if (ObjectifUser === "Perte-poids") {
        Coefficient = 2
    } else {
        // Objectif : Prise de masse
        Coefficient = 2
    }

    // Calcul
    let ResultProteines = PoidsUser*Coefficient

    let Result = Math.floor(ResultProteines) + " g/jour"

    document.querySelector(".temps-recup").textContent = Result
    return
}

function ComboBox() {
    let PoidsUser = document.getElementById("poids-user").value

    if (!PoidsUser) {
        return
    }
    EstimationProteines()
    return
}