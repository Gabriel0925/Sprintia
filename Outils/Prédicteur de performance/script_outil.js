function TempsEstime() {
    // Récupérer la valeur du champ
    // .trim() équivalent de .strip() en python
    let VmaUSER = parseFloat(document.getElementById("vma-user").value
        .trim().replace(",", "."));
    let DistanceUser = parseFloat(document.getElementById("distance-user").value
        .trim().replace(',', '.'));
    const ProfilUser = document.getElementById("profil-user").value
    

    // Initialisation des variables
    let VitesseMoyenne = 0
    let Profil = ""
    let TempsEstime = 0

    let Heure = 0

    let Minute = 0
    let MinuteEstimee = 0

    let Seconde = 0
    let SecondeEstimee = 0

    let ResultAlgo = 0

    const SprintCoef = [1, 0.96, 0.88, 0.78, 0.71, 0.64]
    const EquilibreCoef = [0.97, 0.93, 0.84, 0.80, 0.74, 0.68]
    const EndurantCoef = [0.9, 0.88, 0.87, 0.85, 0.79, 0.75]
    
    // Vérification des champs
    if (isNaN(VmaUSER) || isNaN(DistanceUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.");
        return
    }
    if (VmaUSER <= 0 || DistanceUser <= 0) {
        alert("Valeur non valide, la vma et la distance doivent être supérieur à 0.")
        return
    }
    if (VmaUSER >= 50) {
        alert("Valeur non valide, la vma doit être inférieur à 50.")
        return
    }
    if (DistanceUser >= 50) {
        alert("Le Prédicteur de performance ne peut pas prédire un temps au delà de 50 km.")
        return
    }

    // Attribution d'une liste en fonction du profil
    if (ProfilUser === "Sprint") {
        Profil = SprintCoef
    } else if (ProfilUser === "Equilibre") {
        Profil = EquilibreCoef
    } else {
        Profil = EndurantCoef
    }

    // Calcul
    if (DistanceUser <= 1.5) {
        VitesseMoyenne = VmaUSER*Profil[0]
    } else if (DistanceUser <= 3.0) {
        VitesseMoyenne = VmaUSER*Profil[1]
    } else if (DistanceUser <= 5.0) {
        VitesseMoyenne = VmaUSER*Profil[2]
    } else if (DistanceUser <= 10.0) {
        VitesseMoyenne = VmaUSER*Profil[3]
    } else if (DistanceUser <= 22.0) {
        VitesseMoyenne = VmaUSER*Profil[4]
    } else {
        VitesseMoyenne = VmaUSER*Profil[5]
    }

    TempsEstime = DistanceUser/VitesseMoyenne

    // Extraction des heures, minutes, secondes
    Heure = Math.floor(TempsEstime) // Math.floor arrondi à un entier
    
    Minute = (TempsEstime-Heure)*60 // Calcul des minutes restantes
    MinuteEstimee = Math.floor(Minute)
    
    Seconde = (Minute-MinuteEstimee)*60
    SecondeEstimee = Math.round(Seconde) // Arrondi à l'entier le plus proche

    // Ajustement des resultats
    if (SecondeEstimee === 60) {
        SecondeEstimee = "00";
        MinuteEstimee += 1;
    }
    if (MinuteEstimee === 60) {
        MinuteEstimee = "00";
        Heure += 1;
    }

    // Meilleur lisibilité pour le user, numéros à 2 chiffres
    Heure = Heure.toString().padStart(2, "0") // Conversion en string puis ajout du "0"
    MinuteEstimee = MinuteEstimee.toString().padStart(2, "0")
    SecondeEstimee = SecondeEstimee.toString().padStart(2, "0")

    ResultAlgo = Heure + ":" + MinuteEstimee + ":" + SecondeEstimee

    document.getElementById("reponse-algo-temps").textContent = ResultAlgo
    return VitesseMoyenne
}

function Allure(VitesseMoyenne) {
    let AllureEntrainement = 0
    let Minute = 0
    let Seconde = 0

    // Calcul de l'allure moyenne
    let AllureBase = 60 / VitesseMoyenne
    // Conversion pr passer de 4,5 à 4:30
    let MinutesBase = Math.floor(AllureBase)
    let SecondesBase = Math.round((AllureBase-MinutesBase)*60)

    // Meilleur lisibilité pour le user, numéros à 2 chiffres
    Minute = MinutesBase.toString().padStart(2, "0")
    Seconde = SecondesBase.toString().padStart(2, "0")

    AllureEntrainement = Minute + ":" + Seconde

    document.getElementById("reponse-algo-allure").textContent = AllureEntrainement
    return
}

function AlgoPredicteur(Lieu) {
    // Vérification des champs pour éviter de mettre a jour le resultat alors qu'il n'a pas rempli tt les champs
    if (Lieu === "select") {
        let VmaUSER = parseFloat(document.getElementById("vma-user").value
            .trim().replace(",", "."));
        let DistanceUser = parseFloat(document.getElementById("distance-user").value
            .trim().replace(',', '.'));

        if (isNaN(VmaUSER) || isNaN(DistanceUser)) {
            return
        }
    }
    VitesseMoyenne = TempsEstime()
    Allure(VitesseMoyenne)
}
