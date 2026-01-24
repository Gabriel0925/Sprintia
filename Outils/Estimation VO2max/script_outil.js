function InterpretationVO2max(ResultVO2max, GenreUser, AgeUser){
    let Interpretation = [
        "Zone supérieure :<br>Votre VO₂max est supérieur à la moyenne pour votre tranche d'âge, ce qui indique une excellente capacité cardiovasculaire.",
        "Zone excellente :<br>Vous avez une VO₂max excellente pour votre âge, signe d'un très bon niveau de forme physique.",
        "Zone bonne :<br>Votre VO₂max est bonne pour votre âge, témoignant d'une condition physique solide.",
        "Zone moyenne :<br>Votre VO₂max se situe dans la moyenne pour votre tranche d'âge. Il y a de la marge pour progresser.",
        "Zone faible :<br>Votre VO₂max est faible pour votre âge. Essayez d'être moins sédentaire au quotidien."
    ]

    if (GenreUser == "homme") {
        if (AgeUser <= 19){
            if (ResultVO2max > 60){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 56) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 51) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 46) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else if (AgeUser <= 29) {
            if (ResultVO2max > 56){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 52) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 47) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 42) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else if (AgeUser <= 39) {
            if (ResultVO2max > 54){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 49) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 44) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 39) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else if (AgeUser <= 49) {
            if (ResultVO2max > 51){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 46) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 41) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 36) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else {
            if (ResultVO2max > 48){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 43) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 38) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 33) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        }
    } else {
        if (AgeUser <= 19){
            if (ResultVO2max > 55){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 50) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 45) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 40) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else if (AgeUser <= 29) {
            if (ResultVO2max > 50){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 46) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 42) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 38) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else if (AgeUser <= 39) {
            if (ResultVO2max > 48){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 44) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 40) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 35) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else if (AgeUser <= 49) {
            if (ResultVO2max > 45){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 41) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 37) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 32) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        } else {
            if (ResultVO2max > 42){
                Interpretation = Interpretation[0]
            } else if (ResultVO2max >= 38) {
                Interpretation = Interpretation[1]
            } else if (ResultVO2max >= 34) {
                Interpretation = Interpretation[2]
            } else if (ResultVO2max >= 30) {
                Interpretation = Interpretation[3]
            } else {
                Interpretation = Interpretation[4]
            }
        }
    }

    return Interpretation
}
function CalculVO2max() {
    // Récupérer la valeur des champs
    let GenreUser = document.getElementById("profil-user").value;
    let AgeUser = parseInt(document.getElementById("age-user").value
        .trim().replace(",", "."));
    let VmaUser = parseFloat(document.getElementById("vma-user").value
        .trim().replace(",", "."));

    // Vérification des champs
    if (isNaN(AgeUser) || isNaN(VmaUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (AgeUser < 13 || AgeUser >= 150) {
        alert("Valeur non valide, la valeur de l'âge doit être compris entre 13 et 149 ans.")
        return
    }
    if (VmaUser <= 0) {
        alert("Valeur non valide, la vma doit être supérieur à 0.")
        return
    }
    if (VmaUser >= 50) {
        alert("Valeur non valide, la vma doit être inférieur à 50.")
        return
    }

    // Calcul
    let ResultVO2max = VmaUser*3.5
    let VO2maxEstime = "VO₂max estimé : " + ResultVO2max.toFixed(1).replace(".", ",")

    // Affichage
    document.querySelector(".score-imc").textContent = VO2maxEstime

    let ZoneInterpretationVO2max = InterpretationVO2max(ResultVO2max, GenreUser, AgeUser)
    document.querySelector(".zone-imc").innerHTML = ZoneInterpretationVO2max
    return
}

function ComboBoxVO2max() {
    let AgeUser = parseInt(document.getElementById("age-user").value
        .trim().replace(",", "."));
    let VmaUser = parseFloat(document.getElementById("vma-user").value
        .trim().replace(",", "."));

    if (AgeUser || VmaUser) {
        CalculVO2max()
    }
}