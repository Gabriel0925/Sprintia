function ZoneFcMAX() {
    // Récupérer la valeur des champs
    let AgeUser = parseInt(document.getElementById("age-user").value
        .trim());
    let FcMaxUser = parseInt(document.getElementById("fc-max-user").value
        .trim());

    // Initialisation des variables
    let DebutZone1 = 0
    let FinZone1 = 0
    let FinZone2 = 0
    let FinZone3 = 0
    let FinZone4 = 0
    let FcMax = 0
    
    let ResultAlgoBox1 = ""
    let ResultAlgoBox2 = ""
    let ResultAlgoBox3 = ""
    let ResultAlgoBox4 = ""
    let ResultAlgoBox5 = ""

    // Vérification des champs
    if (isNaN(AgeUser)) {
        alert("Erreur de saisie : le champ 'âge' doit être rempli.");
        return
    }
    if (AgeUser <= 0) {
        alert("Valeur non valide, l'âge doit être supérieur à 0.")
        return
    }

    // Choix de la valeur de Fc max en fonction de si le champs est remplit
    if (isNaN(FcMaxUser)) {
        if (AgeUser >= 150) {
            alert("Valeur non valide, la valeur des champs doivent être cohérentes.")
            return
        }
        // Formule de Tanaka
        FcMax = Math.round(208-0.7*AgeUser)
    } else {
        if (FcMaxUser <= 50) {
            alert("Valeur non valide, la FC max doit être supérieur à 50.")
            return
        }
        if (AgeUser >= 150 || FcMaxUser >= 250) {
            alert("Valeur non valide, la valeur des champs doivent être cohérentes.")
            return
        }
        FcMax = FcMaxUser
    }

    // Calcul

    DebutZone1 = Math.round(FcMax*0.5)
    FinZone1 = Math.round(FcMax*0.6)

    FinZone2 = Math.round(FcMax*0.7)

    FinZone3 = Math.round(FcMax*0.8)

    FinZone4 = Math.round(FcMax*0.9)

    ResultAlgoBox1 =  DebutZone1 + " - " + FinZone1
    ResultAlgoBox2 =  (FinZone1+1) + " - " + FinZone2
    ResultAlgoBox3 =  (FinZone2+1) + " - " + FinZone3
    ResultAlgoBox4 =  (FinZone3+1) + " - " + FinZone4
    ResultAlgoBox5 =  (FinZone4+1) + " - " + FcMax


    const BaliseTranche = document.querySelectorAll(".tranche-zone")
    BaliseTranche[0].textContent = ResultAlgoBox1;
    BaliseTranche[1].textContent = ResultAlgoBox2;
    BaliseTranche[2].textContent = ResultAlgoBox3;
    BaliseTranche[3].textContent = ResultAlgoBox4;
    BaliseTranche[4].textContent = ResultAlgoBox5;
    return
}
function ZoneFcReserve() {
    // Récupérer la valeur des champs
    let AgeUser = parseInt(document.getElementById("age-user").value
        .trim());
    let FcReposUser = parseInt(document.getElementById("fc-repos-user").value
        .trim());
    let FcMaxUser = parseInt(document.getElementById("fc-max-user").value
        .trim());

    // Initialisation des variables
    let DebutZone1 = 0
    let FinZone1 = 0
    let FinZone2 = 0
    let FinZone3 = 0
    let FinZone4 = 0

    let FcMax = 0
    let FcReserve = 0
    
    let ResultAlgoBox1 = ""
    let ResultAlgoBox2 = ""
    let ResultAlgoBox3 = ""
    let ResultAlgoBox4 = ""
    let ResultAlgoBox5 = ""

    // Vérification des champs
    if (isNaN(AgeUser) || isNaN(FcReposUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.");
        return
    }
    if (AgeUser <= 0) {
        alert("Valeur non valide, l'âge doit être supérieur à 0.")
        return
    }
    if (FcReposUser <= 15) {
        alert("Valeur non valide, la FC repos doit être supérieur à 15.")
        return
    }

    // Choix de la valeur de Fc max en fonction de si le champs est remplit
    if (isNaN(FcMaxUser)) {
        if (AgeUser >= 150 || FcReposUser >= 150) {
            alert("Valeur non valide, la valeur des champs doivent être cohérentes.")
            return
        }
        // Formule de Tanaka
        FcMax = Math.round(208-0.7*AgeUser)
    } else {
        if (FcMaxUser <= 50) {
            alert("Valeur non valide, la FC max doit être supérieur à 50.")
            return
        }
        if (FcReposUser >= FcMaxUser) {
            alert("Valeur non valide, la FC repos ne peut pas être supérieur à la FC max.")
            return
        }
        if (AgeUser >= 150 || FcReposUser >= 150 || FcMaxUser >= 250) {
            alert("Valeur non valide, la valeur des champs doivent être cohérentes.")
            return
        }
        FcMax = FcMaxUser
    }

    // Calcul

    FcReserve = FcMax - FcReposUser

    DebutZone1 = Math.round(FcReposUser+(FcReserve*0.5))
    FinZone1 = Math.round(FcReposUser+(FcReserve*0.6))

    FinZone2 = Math.round(FcReposUser+(FcReserve*0.7))

    FinZone3 = Math.round(FcReposUser+(FcReserve*0.8))

    FinZone4 = Math.round(FcReposUser+(FcReserve*0.9))

    ResultAlgoBox1 =  DebutZone1 + " - " + FinZone1
    ResultAlgoBox2 =  (FinZone1+1) + " - " + FinZone2
    ResultAlgoBox3 =  (FinZone2+1) + " - " + FinZone3
    ResultAlgoBox4 =  (FinZone3+1) + " - " + FinZone4
    ResultAlgoBox5 =  (FinZone4+1) + " - " + FcMax


    const BaliseTranche = document.querySelectorAll(".tranche-zone")
    BaliseTranche[0].textContent = ResultAlgoBox1;
    BaliseTranche[1].textContent = ResultAlgoBox2;
    BaliseTranche[2].textContent = ResultAlgoBox3;
    BaliseTranche[3].textContent = ResultAlgoBox4;
    BaliseTranche[4].textContent = ResultAlgoBox5;
    return
}

function MethodeChoisie() {
    const Methode = document.getElementById("methode-user").value
    const ChampFcMax = document.getElementById("fc-max-user")
    const ChampFcRepos = document.getElementById("fc-repos-user")
    const LabelFcRepos = document.getElementById("label-fc-user")

    if (Methode === "Max") {
        // supression/ activation des champs
        ChampFcMax.classList.remove("invisible")
        ChampFcRepos.classList.add("invisible")
        LabelFcRepos.classList.add("invisible")
    } else {
        ChampFcMax.classList.remove("invisible")
        ChampFcRepos.classList.remove("invisible")
        LabelFcRepos.classList.remove("invisible")
    }
    return
}

function ChoixFonction() {
    const Methode = document.getElementById("methode-user").value

    // Choix de la fonction en fonction de la méthode
    if (Methode === "Max") {
        ZoneFcMAX()
    } else {
        ZoneFcReserve()
    }
    return
}