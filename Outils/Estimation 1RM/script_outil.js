function EstimationOneRep() {
    // Recup valeur des champs
    let ChargeUser = parseFloat(document.getElementById("charge-user").value.trim().replace(",", "."))
    let RepUser = parseInt(document.getElementById("rep-user").value.trim().replace(",", "."))
    let MethodeUser = document.getElementById("methode-user").value

    // Vérification des champs
    if (isNaN(ChargeUser) || isNaN(RepUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (ChargeUser <= 0 || RepUser <= 0) {
        alert("Valeur non valide, la charge et les répétitions doivent être un nombre supérieur à 0.")
        return
    }

    // Initialisation
    let Estimation1RM = 0

    // Calcul
    if (MethodeUser === "Epley") {
        Estimation1RM = ChargeUser*(1+(RepUser/30))
    } else {
        Estimation1RM = ChargeUser/(1.0278-(0.0278*RepUser))
    }

    let ResultEstimation = Estimation1RM.toFixed(1).replace(".", ",") + " kg"
    document.querySelector(".temps-recup").textContent = ResultEstimation
    return
}

function MethodeChoisie() {
    let ChargeUser = parseFloat(document.getElementById("charge-user").value.trim().replace(",", "."))
    let RepUser = parseFloat(document.getElementById("rep-user").value.trim().replace(",", "."))

    if (!ChargeUser || !RepUser) {
        return
    }

    EstimationOneRep()
    return
}