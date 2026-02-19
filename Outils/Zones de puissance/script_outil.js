function zonePuissance() {
    //recup value champs
    let rFTPwUser = parseFloat(document.getElementById("rFTPw-user").value.trim().replace(",", "."))

    // Vérification
    if (isNaN(rFTPwUser)) {
        alert("Veuillez remplir le champ rFTPw.")
        return
    }
    if (rFTPwUser <= 0) {
        alert("Votre rFTPw doit être supérieur un nombre positif supérieur à 0.")
        return
    }

    
    // Calcul 
    let DebutZone1 = 0
    let FinZone1 = Math.round(rFTPwUser*0.8)

    let FinZone2 = Math.round(rFTPwUser*0.88)

    let FinZone3 = Math.round(rFTPwUser*0.95)

    let FinZone4 = Math.round(rFTPwUser*1.05)

    let FinZone5 = Math.round(rFTPwUser*1.15)

    let FinZone6 = Math.round(rFTPwUser*1.28)

    // mise en variable de l'affichage
    ResultAlgoBox1 = DebutZone1 + " - " + FinZone1
    ResultAlgoBox2 = (FinZone1+1) + " - " + FinZone2
    ResultAlgoBox3 = (FinZone2+1) + " - " + FinZone3
    ResultAlgoBox4 = (FinZone3+1) + " - " + FinZone4
    ResultAlgoBox5 = (FinZone4+1) + " - " + FinZone5
    ResultAlgoBox6 = (FinZone5+1) + " - " + FinZone6
    ResultAlgoBox7 = "> " + (FinZone6+1)

    // affichage
    const BaliseTranche = document.querySelectorAll(".tranche-zone")
    BaliseTranche[0].textContent = ResultAlgoBox1
    BaliseTranche[1].textContent = ResultAlgoBox2
    BaliseTranche[2].textContent = ResultAlgoBox3
    BaliseTranche[3].textContent = ResultAlgoBox4
    BaliseTranche[4].textContent = ResultAlgoBox5
    BaliseTranche[5].textContent = ResultAlgoBox6
    BaliseTranche[6].textContent = ResultAlgoBox7

    return
}