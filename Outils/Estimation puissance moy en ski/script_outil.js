function EstimationPuissanceSki() {
    // Récupération de la valeur des champs
    let PoidsUser = parseFloat(document.getElementById("poids-user").value.trim().replace(",", "."))
    let TailleUser = parseFloat(document.getElementById("taille-user").value.trim().replace(",", "."))
    let DureeUser = parseInt(document.getElementById("duree-user").value.trim())
    let DeniveleUser = parseInt(document.getElementById("denivele-user").value.trim())

    // Vérification des champs
    if (isNaN(PoidsUser) || isNaN(DureeUser) || isNaN(DeniveleUser) || isNaN(TailleUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (PoidsUser <= 0 || DureeUser <= 0 || TailleUser <= 0) {
        alert("Valeur non valide, le poids, la durée et la taille doivent être supérieur à 0.")
        return
    }
    if (DeniveleUser <= 0) {
        alert("Valeur non valide, le dénivelé négatif correspond à la hauteur totale de votre descente (ex : 500 pour une descente de 500m).")
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

    // Calcul
    let PoidsEquipement = 3+(TailleUser*0.04) // le 3 vient des poids fixe comme les gants, casque, baton,...
    
    let PuissanceMoy = ((PoidsUser+PoidsEquipement)*9.81*DeniveleUser)/(DureeUser*60)
    let ResultPuissance = "Puissance moy. : " + "<strong>" + Math.round(PuissanceMoy) + " W" + "</strong>"
    // utilisation d'un rapport, donc l'unité est Watts/kg
    let NbZone = PuissanceMoy/PoidsUser

    // Initialisation
    let Zone = ""

    // Attribution des zones
    if (NbZone < 4) {
        Zone = "<strong>Découverte :</strong><br>Rythme tranquille vous préférez être prudent·e et vous avez raison ou alors vous admirez les paysages (ou les 2) !"
    } else if (NbZone <= 8) {
        Zone = "<strong>Niveau moyen :</strong><br>Rythme intermédiaire, vous êtes dans la moyenne. Vous maîtrisez vos virages,..."
    }  else if (NbZone <= 12) {
        Zone = "<strong>Supérieur·e :</strong><br>Vous vous engagez réellement, vous coupez vos virages,... Je suis sûr que vous n'avez même pas admiré le paysage. Mais vous avez un très bon niveau, bravo !"
    } else {
        Zone = "<strong>Élite :</strong><br>Vous avez optimisé·e tous les moindres petits détails pour vous améliorer et gagner quelques centièmes de secondes, bravo !"
    } 

    document.querySelector(".score-imc").innerHTML = ResultPuissance
    document.querySelector(".zone-imc").innerHTML = Zone

    return
}