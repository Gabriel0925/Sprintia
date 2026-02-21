function CalculTranspiration(PoidsUser, DureeUser, ValueRpeUser) {
    // Initialisation des variables
    let DureeHeure = DureeUser/60 // Conversion de la durée en heure
    let CoefficientRpe = [0.4, 0.8, 1.2, 1.6]

    // Attribution de la valeur du RPE
    if (ValueRpeUser <= 3) {
        CoefficientRpe = CoefficientRpe[0]
    } else if (ValueRpeUser <= 6) {
        CoefficientRpe = CoefficientRpe[1]
    } else if (ValueRpeUser <= 8) {
        CoefficientRpe = CoefficientRpe[2]
    } else {
        CoefficientRpe = CoefficientRpe[3]
    }

    // Calcul
    let TranspirationEstimee = DureeHeure*CoefficientRpe*(PoidsUser/70)

    return TranspirationEstimee
}

function CalculHydratation(TranspirationEstimee) {
    // Conversion 
    TranspirationEstimee = parseFloat(TranspirationEstimee)
    // Calcul
    let HydratationEstimee = TranspirationEstimee*1.2
    return HydratationEstimee
}

function CalculHydratationTotale(PoidsUser, rehydratation) {
    // Fourchette pour un adulte sédentaire
    let ReferenceMin = 30 // 30 mL d'eau par kilo de poids de corps
    let ReferenceMax = 35

    // Application formule
    let HydratationMin = (PoidsUser*ReferenceMin)*0.8 // fois 0.8 car "Environ 20 % d'eau provient de vos repas"
    let HydratationMax = (PoidsUser*ReferenceMax)*0.8
    let HydratationRecommandee = (HydratationMin+HydratationMax)/2 // moyenne de la fourchette minimum, maximum

    // on ajoute la réhydratation
    HydratationRecommandee = HydratationRecommandee+rehydratation

    return HydratationRecommandee
}

function CalculGeneral() {
    let PoidsUser = parseFloat(document.getElementById("poids-user").value.trim().replace(",", "."))
    let DureeUser = parseInt(document.getElementById("duree-entrainement-user").value.trim())
    let ValueRpeUser = parseInt(document.querySelector(".slider progress").value)

    // Vérification des champs
    if (isNaN(PoidsUser) || isNaN(DureeUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.");
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

    // Appelle aux fonctions
    let ValueTranspirationEstimee = CalculTranspiration(PoidsUser, DureeUser, ValueRpeUser)
    let ValueTranspirationEstimeeMl = ValueTranspirationEstimee*1000
    let rehydratation = CalculHydratation(ValueTranspirationEstimeeMl)

    // Mise en variable pour passez à l'affichage
    let TranspirationEstimee = "Transpiration : " + "<strong>" + Math.round(ValueTranspirationEstimeeMl) + " mL"  + "</strong>"
    let Rehydratation = "Réhydratation : " + "<strong>" + Math.round(rehydratation) + " mL" + "</strong>"
    let HydratationToday = "Hydratation du jour : " + "<strong>" + Math.round(CalculHydratationTotale(PoidsUser, rehydratation)) + " mL" + "</strong>"
    let Interpretation = "<strong>Petit conseil :</strong> ne buvez pas tout d'un coup, essayer de boire un verre toutes les 10-20 minutes."

    // Affichage des champs
    let ChampResult = document.querySelectorAll(".score-imc")
    // Maj de l'interpretation
    document.querySelector(".zone-imc").innerHTML = Interpretation

    ChampResult[0].innerHTML = TranspirationEstimee
    ChampResult[1].innerHTML = Rehydratation
    ChampResult[2].innerHTML = HydratationToday
    return
}