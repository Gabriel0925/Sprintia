function Calcul() {
    let AgeUser = parseInt(document.getElementById("age-user").value.trim())
    let PoidsUser = parseFloat(document.getElementById("poids-user").value.trim().replace(",", "."))

    // Vérification champs
    if (isNaN(AgeUser) || isNaN(PoidsUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
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
    if (AgeUser < 6 || AgeUser >= 150) {
        alert("Valeur non valide, la valeur de l'âge doit être compris entre 6 et 149 ans.")
        return
    }

    // init
    // Fourchette pour un adulte sédentaire
    let ReferenceMin = 30 // 30 mL d'eau par kilo de poids de corps
    let ReferenceMax = 35

    // si le user a moins de 14 ans alors il a besoin de plus d'eau
    if (AgeUser < 14) {
        // chiffre fondée sur des recommandations d'organismes de santé reconnus, comme l'EFSA (Autorité européenne de sécurité des aliments) et l'OMS.
        ReferenceMin = 50
        ReferenceMax = 60
    }

    // Application formule
    let HydratationMin = (PoidsUser*ReferenceMin)*0.8 // fois 0.8 car "Environ 20 % d'eau provient de vos repas"
    let HydratationMax = (PoidsUser*ReferenceMax)*0.8
    let HydratationRecommandee = (HydratationMin+HydratationMax)/2 // moyenne de la fourchette minimum, maximum

    // Affichage
    document.querySelector(".temps-recup").textContent = Math.round(HydratationRecommandee) + " mL/jour" 

    return
}