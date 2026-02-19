function ZoneVitesse() {
    // Récupérer la valeur des champs
    let VmaUser = parseFloat(document.getElementById("vma-user").value
        .trim().replace(",", "."));
    let VitesseMaxUser = parseFloat(document.getElementById("vitesse-max-user").value
        .trim().replace(",", "."));

    // Initialisation des variables
    let DebutZone1 = 0
    let FinZone1 = 0
    let FinZone2 = 0
    let FinZone3 = 0
    let FinZone4 = 0

    let VitesseMax = 0
    
    let ResultAlgoBox1 = ""
    let ResultAlgoBox2 = ""
    let ResultAlgoBox3 = ""
    let ResultAlgoBox4 = ""
    let ResultAlgoBox5 = ""
    let Coefficent = []

    // Vérification des champs
    if (isNaN(VmaUser)) {
        alert("Erreur de saisie : le champ 'vma' doit être rempli.");
        return
    }
    if (VmaUser <= 0 || VmaUser >= 50) {
        alert("Valeur non valide, la VMA doit être compris entre 0 et 50.");
        return
    }

    if (isNaN(VitesseMaxUser)) {
        Coefficent = [0.65, 0.75, 0.85, 0.95]
        VitesseMax = Math.round(VmaUser*1.35)
    } else {
        Coefficent = [0.5, 0.65, 0.80, 0.90]
        if (VitesseMaxUser <= 0 || VitesseMaxUser >= 50) {
            alert("Valeur non valide, la vitesse max doit être compris entre 0 et 50.");
            return
        }
        VitesseMax = VitesseMaxUser
    }

    // Calcul
    DebutZone1 = "0,0"
    FinZone1 = VitesseMax*Coefficent[0]
    FinZone2 = VitesseMax*Coefficent[1]
    FinZone3 = VitesseMax*Coefficent[2]
    FinZone4 = VitesseMax*Coefficent[3]

    ResultAlgoBox1 =  DebutZone1 + " - " + FinZone1.toFixed(1).replace(".", ",") 
    ResultAlgoBox2 =  (FinZone1+0.1).toFixed(1).replace(".", ",") + " - " + FinZone2.toFixed(1).replace(".", ",")
    ResultAlgoBox3 =  (FinZone2+0.1).toFixed(1).replace(".", ",") + " - " + FinZone3.toFixed(1).replace(".", ",")
    ResultAlgoBox4 =  (FinZone3+0.1).toFixed(1).replace(".", ",") + " - " + FinZone4.toFixed(1).replace(".", ",")

    if (VitesseMaxUser) {
        ResultAlgoBox5 =  (FinZone4+0.1).toFixed(1).replace(".", ",") + " - " + VitesseMax.toFixed(1).replace(".", ",")
    } else {
        ResultAlgoBox5 =   "> " + FinZone4.toString().replace(".", ",")
    }

    const BaliseTranche = document.querySelectorAll(".tranche-zone")
    BaliseTranche[0].innerHTML = ResultAlgoBox1;
    BaliseTranche[1].innerHTML = ResultAlgoBox2;
    BaliseTranche[2].innerHTML = ResultAlgoBox3;
    BaliseTranche[3].innerHTML = ResultAlgoBox4;
    BaliseTranche[4].innerHTML = ResultAlgoBox5;

    // Maj de l'unité au cas ou le user aura fais conversion puis re-valider
    const UnitTranche = document.querySelectorAll(".unite-zone")
    UnitTranche[0].textContent = "km/h";
    UnitTranche[1].textContent = "km/h";
    UnitTranche[2].textContent = "km/h";
    UnitTranche[3].textContent = "km/h";
    UnitTranche[4].textContent = "km/h";

    // Changement bouton 
    let ButtonConversion = document.getElementById("conversion")
    ButtonConversion.textContent = "Convertir en allure"

    ButtonConversion.onclick = ZoneAllure

    return
}

function ConversionAllure(Zone){    
    // Extraction des minutes, secondes
    let Minutes = Math.floor(Zone)
    let Secondes = Math.round((Zone-Minutes)*60)

    if (Secondes === 60) {
        Secondes = 0
        Minutes += 1
    }
    return [Minutes, Secondes]
}

function ZoneAllure() {
    // Récupérer la valeur des champs
    let VmaUser = parseFloat(document.getElementById("vma-user").value
        .trim().replace(",", "."));
    let VitesseMaxUser = parseFloat(document.getElementById("vitesse-max-user").value
        .trim().replace(",", "."));

    // Initialisation des variables
    let DebutZone1 = 0
    let FinZone1 = 0
    let FinZone2 = 0
    let FinZone3 = 0
    let FinZone4 = 0

    let VitesseMax = 0
    
    let ResultAlgoBox1 = ""
    let ResultAlgoBox2 = ""
    let ResultAlgoBox3 = ""
    let ResultAlgoBox4 = ""
    let ResultAlgoBox5 = ""
    let Coefficent = []

    // Vérification des champs
    if (isNaN(VmaUser)) {
        alert("Erreur de saisie : le champ 'vma' doit être rempli.");
        return
    }
    if (VmaUser <= 0 || VmaUser >= 50) {
        alert("Valeur non valide, la VMA doit être compris entre 0 et 50.");
        return
    }

    // Prise en compte de la vmax si elle y est sinon on s'en fous
    if (isNaN(VitesseMaxUser)) {
        Coefficent = [0.65, 0.75, 0.85, 0.95]
        VitesseMax = Math.round(VmaUser*1.35)
    } else {
        Coefficent = [0.5, 0.65, 0.80, 0.90]
        if (VitesseMaxUser <= 0 || VitesseMaxUser >= 50) {
            alert("Valeur non valide, la vitesse max doit être compris entre 0 et 50.");
            return
        }
        VitesseMax = VitesseMaxUser
    }

    // Calcul (avec la remise en allure)
    DebutZone1 = "0:00"
    FinZone1 = 60/(VitesseMax*Coefficent[0])
    // Conversion
    let MinutesSecondesZone1 = ConversionAllure(FinZone1)
    // Recup des datas qui sont dans une liste
    let MinutesZone1 = MinutesSecondesZone1[0]
    let SecondesZone1 = MinutesSecondesZone1[1]

    FinZone2 = 60/(VitesseMax*Coefficent[1])
    // Conversion
    let MinutesSecondesZone2 = ConversionAllure(FinZone2)
    // Recup des datas qui sont dans une liste
    let MinutesZone2 = MinutesSecondesZone2[0]
    let SecondesZone2 = MinutesSecondesZone2[1]

    FinZone3 = 60/(VitesseMax*Coefficent[2])
    // Conversion
    let MinutesSecondesZone3 = ConversionAllure(FinZone3)
    // Recup des datas qui sont dans une liste
    let MinutesZone3 = MinutesSecondesZone3[0]
    let SecondesZone3 = MinutesSecondesZone3[1]

    FinZone4 = 60/(VitesseMax*Coefficent[3])
    // Conversion
    let MinutesSecondesZone4 = ConversionAllure(FinZone4)
    // Recup des datas qui sont dans une liste
    let MinutesZone4 = MinutesSecondesZone4[0]
    let SecondesZone4 = MinutesSecondesZone4[1]

    let FinZone5 = 60/(VitesseMax)
    // Conversion
    let MinutesSecondesZone5 = ConversionAllure(FinZone5)
    // Recup des datas qui sont dans une liste
    let MinutesZone5 = MinutesSecondesZone5[0]
    let SecondesZone5 = MinutesSecondesZone5[1]

    // Resultat ds des variable plus conversion en string + padstart pr qu'a chaque fois on est 2 chiffres et eviter davoir 5:5 mais uniquement pr les secondes
    ResultAlgoBox1 =  DebutZone1 + " - " + MinutesZone1 + ":" + SecondesZone1.toString().padStart(2, "0")
    ResultAlgoBox2 =  MinutesZone1 + ":" + SecondesZone1.toString().padStart(2, "0") + " - " + MinutesZone2 + ":" + SecondesZone2.toString().padStart(2, "0")
    ResultAlgoBox3 =  MinutesZone2 + ":" + SecondesZone2.toString().padStart(2, "0") + " - " + MinutesZone3 + ":" + SecondesZone3.toString().padStart(2, "0")
    ResultAlgoBox4 =  MinutesZone3 + ":" + SecondesZone3.toString().padStart(2, "0") + " - " + MinutesZone4 + ":" + SecondesZone4.toString().padStart(2, "0")
    ResultAlgoBox5 =  MinutesZone4 + ":" + SecondesZone4.toString().padStart(2, "0") + " - " + MinutesZone5 + ":" + SecondesZone5.toString().padStart(2, "0")

    if (VitesseMaxUser) {
        ResultAlgoBox5 =  MinutesZone4 + ":" + SecondesZone4.toString().padStart(2, "0") + " - " + MinutesZone5 + ":" + SecondesZone5.toString().padStart(2, "0")
    } else {
        ResultAlgoBox5 =   "> " + MinutesZone4 + ":" + SecondesZone4.toString().padStart(2, "0")
    }

    // On affiche les resultats
    const BaliseTranche = document.querySelectorAll(".tranche-zone")
    BaliseTranche[0].innerHTML = ResultAlgoBox1;
    BaliseTranche[1].innerHTML = ResultAlgoBox2;
    BaliseTranche[2].innerHTML = ResultAlgoBox3;
    BaliseTranche[3].innerHTML = ResultAlgoBox4;
    BaliseTranche[4].innerHTML = ResultAlgoBox5;

    // Maj de l'unité
    const UnitTranche = document.querySelectorAll(".unite-zone")
    UnitTranche[0].textContent = "/km";
    UnitTranche[1].textContent = "/km";
    UnitTranche[2].textContent = "/km";
    UnitTranche[3].textContent = "/km";
    UnitTranche[4].textContent = "/km";

    // Changement bouton 
    let ButtonConversion = document.getElementById("conversion")
    ButtonConversion.textContent = "Convertir en vitesse"

    ButtonConversion.onclick = ZoneVitesse

    return
}