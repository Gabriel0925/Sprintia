function EstimationPuissanceMax() {
    // Recup valeur des champs
    let PoidsUser = parseFloat(document.getElementById("poids-user").value.trim().replace(",", "."))
    let VitesseMaxUser = parseFloat(document.getElementById("vmax-user").value.trim().replace(",", "."))

    // Vérification des champs
    if (isNaN(PoidsUser) || isNaN(VitesseMaxUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (PoidsUser <= 0 || VitesseMaxUser <= 0) {
        alert("Valeur non valide, le poids et la vitesse maximale doivent être supérieur à 0.")
        return
    }
    if (PoidsUser >= 1000) {
        alert("Valeur non valide, le poids doit être un nombre inférieur à 1000.")
        return
    }
    if (VitesseMaxUser >= 200) {
        alert("Valeur non valide, la vitesse maximale doit être un nombre inférieur à 200.")
        return
    }

    // Conversion des km/h en m/s
    let VitesseMS = VitesseMaxUser/3.6

    // Initialisation
    let Coefficient = 2.7 // C'est le facteur de coût énergétique situé en 3 et 4 selon les études mais plus représentatif avec 2,7

    // Calcul
    let Puissance = PoidsUser*(Coefficient*VitesseMS)
    let ResultPuissance = "Puissance max. : " + "<strong>" + Math.round(Puissance) + " W"  + "</strong>"
    // utilisation d'un rapport, donc l'unité est Watts/kg
    let NbZone = Puissance/PoidsUser

    // Initialisation
    let Zone = ""

    // Attribution des zones
    if (NbZone < 10) {
        Zone = "<strong>Correct :</strong><br>Vous avez une bonne base, mais je suis sûr que vous pouvez encore vous améliorer."
    } else if (NbZone <= 15) {
        Zone = "<strong>Bon :</strong><br>Vous avez une foulée très dynamique et vous dépassez la moyenne des coureurs et coureuses, bravo !"
    }  else if (NbZone <= 20) {
        Zone = "<strong>Excellent :</strong><br>Vous avez développé une très grosse puissance ce qui indique que vous êtes très explosif·ve sur un sprint, bravo !"
    } else {
        Zone = "<strong>Supérieur·e :</strong><br>Vous avez un niveau hors-norme, votre puissance est impressionnante !"
    } 

    // Affichage
    document.querySelector(".score-imc").innerHTML = ResultPuissance
    document.querySelector(".zone-imc").innerHTML = Zone

    return
}