function CalculIMC() {
    // Récupérer la valeur du champ
    let PoidsUser = parseFloat(document.getElementById("poids-user").value
        .trim().replace(",", "."));
    let TailleUser = parseFloat(document.getElementById("taille-user").value
        .trim().replace(",", "."));


    // Initialisation des variables
    let IMC = 0
    let InterpretationZoneImc = ""

    // Vérification des champs
    if (isNaN(PoidsUser)|| isNaN(TailleUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.");
        return
    }
    if (PoidsUser <= 0 || TailleUser <= 0) {
        alert("Valeur non valide, le poids et la taille doivent être un nombre supérieur à 0.")
        return
    }
    if (PoidsUser >= 1000) {
        alert("Valeur non valide, le poids doit être un nombre inférieur à 1000.")
        return
    }
    if (TailleUser >= 350) {
        alert("Valeur non valide, la taille doit être un nombre inférieur à 350.")
        return
    }

    // Conversion
    TailleUser = TailleUser/100

    // Calcul
    IMC = PoidsUser / (TailleUser**2)

    if (IMC <= 18.5) {
        InterpretationZoneImc = "<strong>Zone maigreur :</strong><br>D'après l'IMC vous êtes super actif·ve mais si vous vous sentez mal le mieux serait de consulter un médecin !"
    } else if (IMC <= 25) {
        InterpretationZoneImc = "<strong>Zone de corpulence normale :</strong><br>Parfait, d'après l'IMC vous êtes équilibré·e, continuez comme ça !"
    } else if (IMC <= 30) {
        InterpretationZoneImc = "<strong>Zone de surpoids :</strong><br>D'après l'IMC vous êtes en surpoids mais je suis sûr que vous avez juste trop de muscles et ça l'IMC ne peut pas le savoir !"
    } else if (IMC <= 35) {
        InterpretationZoneImc = "<strong>Zone obésité modérée :</strong><br> Un petit changement d'habitude aujourd'hui fera une grande différence demain ! Si vous vous sentez mal le mieux serait de consulter un médecin !"
    } else if (IMC <= 40) {
        InterpretationZoneImc = "<strong>Zone d’obésité sévère :</strong><br>Si vous vous sentez bien c'est le plus important, ne vous comparez pas aux autres comparez-vous à la personne que vous étiez hier !"
    } else {
        InterpretationZoneImc = "<strong>Zone d’obésité morbide :</strong><br>Vous vous améliorez de jour en jour mais si vous vous sentez mal le mieux serait de consulter un médecin !"
    }

    IMC = "Votre IMC : " + "<strong>" + IMC.toFixed(1).replace(".", ",") + "</strong>"
    document.querySelector(".score-imc").innerHTML = IMC;
    document.querySelector(".zone-imc").innerHTML = InterpretationZoneImc;
    return
}