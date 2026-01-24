function EstimationVMA() {
    // Recup datas des champs
    let TestUsers = document.getElementById("test-user").value
    let DistanceUser = parseFloat(document.getElementById("distance-user").value.replace(",", ".").trim())
    let DureeUser = parseInt(document.getElementById("duree-user").value.trim())

    // Vérifications des champs
    if (isNaN(DistanceUser) || isNaN(DureeUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (DistanceUser <= 0 || DureeUser <= 0) {
        alert("Valeur non valide, la distance et la durée doivent être supérieur à 0.")
        return
    }
    if (DistanceUser >= 30) {
        alert("L'estimation VMA ne peut pas prédire un VMA avec une distance supérieur à 30 km.'")
        return
    }

    // Initialisation
    let Coefficient = [0.95, 0.92, 0.89, 0.82, 0.77]
    let DistanceM = 0
    let VmaEstimee = 0
    let VitesseMoyenne = 0

    // Calcul en fonction du test choisis
    if (TestUsers === "demi-cooper") {
        DistanceM = DistanceUser*1000
        VmaEstimee = DistanceM/100
    } else if (TestUsers === "cooper") {
        DistanceM = DistanceUser*1000
        VmaEstimee = DistanceM/200
    } else if (TestUsers === "luc-leger") {
        VmaEstimee = DistanceUser/(DureeUser/60)
    } else {
        VitesseMoyenne = DistanceUser/(DureeUser/60) // Vitesse moyenne en km/h
        if (DistanceUser <= 3.5) {
            Coefficient = Coefficient[0]
        } else if (DistanceUser <= 6) {
            Coefficient = Coefficient[1]
        } else if (DistanceUser <= 12) {
            Coefficient = Coefficient[2]
        } else if (DistanceUser <= 22) {
            Coefficient = Coefficient[3]
        } else {
            Coefficient = Coefficient[4]
        }
        VmaEstimee = VitesseMoyenne/Coefficient
    }

    // Arrondi
    VmaEstimee = VmaEstimee.toFixed(1).replace(".", ",") + " km/h"

    document.querySelector(".temps-recup").textContent = VmaEstimee
    return
}

function RemplirChamps() {
    // Recup datas des champs
    let TestUsers = document.getElementById("test-user").value

    // Maj des champs en fonction du test choisi
    if (TestUsers === "demi-cooper") {
        let ChampsDistance = document.getElementById("distance-user")
        ChampsDistance.value = ""
        ChampsDistance.readOnly = false // Pour désactiver la modification


        let ChampsDuree = document.getElementById("duree-user")
        ChampsDuree.value = 6
        ChampsDuree.readOnly = true 

    } else if (TestUsers === "cooper") {
        let ChampsDistance = document.getElementById("distance-user")
        ChampsDistance.value = ""
        ChampsDistance.readOnly = false // Pour désactiver la modification

        let ChampsDuree = document.getElementById("duree-user")
        ChampsDuree.value = 12
        ChampsDuree.readOnly = true

    } else if (TestUsers === "luc-leger") {
        let ChampsDistance = document.getElementById("distance-user")
        ChampsDistance.value = 2
        ChampsDistance.readOnly = true
        
        let ChampsDuree = document.getElementById("duree-user")
        ChampsDuree.value = ""
        ChampsDuree.readOnly = false

    } else {
        let ChampsDistance = document.getElementById("distance-user")
        ChampsDistance.value = ""
        ChampsDistance.readOnly = false
        
        let ChampsDuree = document.getElementById("duree-user")
        ChampsDuree.value = ""
        ChampsDuree.readOnly = false
    }

    return
}

// Initialisation du champs de base lors du chargement de la page
let ChampsDuree = document.getElementById("duree-user")
ChampsDuree.value = 6
ChampsDuree.readOnly = true 