
let dateMoins7J = createObjetDate(7)
let dateMoins30J = createObjetDate(30)
let dateMoins90J = createObjetDate(90)
let dateMoins365J = createObjetDate(365)

// var globale pour la date et le sport
let dateDemandee = dateMoins7J
let sportDemandee = "Course"

async function statistiquesParSport(sportForFunction) {
    // recup data des derniers jours en fonction de la date
    const historiqueDBStats = await db.entrainement.where("date").aboveOrEqual(dateDemandee).toArray() // la var dateChoisie change en fonction du selected dans l'interface

    // maj de la variable globale
    sportDemandee = sportForFunction

    // init du compteur pour compter le nb d'entrainement
    let compteurNbEntrainement = 0
    let compteurDuree = 0
    let compteurDistance = 0

    historiqueDBStats.forEach(element => {
        // si le sport dans la BDD est égale aux sport de la navbar stats par sport
        if (element.sport == sportDemandee) {
            // si il y a une durée et qu'elle est utilisable alors on ajoute
            if (element.duree != undefined && !isNaN(Number(element.duree))) {
                compteurDuree += Number(element.duree)

                // si la distance n'est pas en undefined ou autre alors on l'ajoute
                if (element.distance != undefined && !isNaN(element.distance)) {
                    compteurDistance += element.distance
                }
            
                compteurNbEntrainement += 1 // maj de la variable pr compter le nombre d'entrainement en course par exemple
            }

        }
    });

    // remplissage des champs
    document.getElementById("duree-sport").textContent = dureeFormatee(compteurDuree, null)
    document.getElementById("nb-entrainement-sport").textContent = compteurNbEntrainement.toLocaleString('fr-FR')

    if (sportDemandee == "Natation") { // si c'est de la natation alors on met en metre
        compteurDistance = compteurDistance*1000
        document.getElementById("distance-sport").innerHTML = compteurDistance.toFixed(1).replace(".", ",") + ' <small>m</small>'
    } else {
        document.getElementById("distance-sport").innerHTML = compteurDistance.toFixed(2).replace(".", ",") + ' <small>km</small>'
    }
}
        
async function init(dateChoisie) {
    // recup data des derniers jours en fonction de la date
    const historiqueDB = await db.entrainement.where("date").aboveOrEqual(dateChoisie).toArray() // la var dateChoisie change en fonction du selected dans l'interface

    // maj de la var global
    dateDemandee = dateChoisie

    // quand il n'y a pas de datas
    if (historiqueDB.length <= 0) {
        document.querySelector(".sports-pratiques").style.display = "none"
        document.getElementById("message-not-datas").style.display = "block"
        document.getElementById("message-tips-graph").style.display = "none"

        // remise à 0 des champs pr éviter d'avoir des anciennes datas lors d'une autre période
        document.getElementById("duree").textContent = "00:00"
        document.getElementById("charge-entrainement").textContent = "0 CE"
        document.getElementById("nb-entrainement").textContent = "0"

        // pareil pour les datas dans les sports spé
        document.getElementById("duree-sport").textContent = "00:00"
        document.getElementById("nb-entrainement-sport").textContent = "0"
        document.getElementById("distance-sport").textContent = "0 km"

        document.getElementById("barCanvas").style.display = "none"
        return
    } else { 
        // si le user n'a pas de datas sur les 7 derniers jours et qu'il veut afficher les stats des 30j 
        // il faut remettre le graph et le message visible sinon le graph ne sera pas là
        document.querySelector(".sports-pratiques").style.display = "block"
        document.getElementById("message-not-datas").style.display = "none"
        document.getElementById("message-tips-graph").style.display = "block"
        document.getElementById("barCanvas").style.display = "block"
    }

    // Tableau des entraînements en fonction de ce qu'a choisis le user comme date (7J, 30J, 365J)
    let tableauDuree = historiqueDB.map(elt => elt.duree)
    let tableauSport = historiqueDB.map(elt => elt.sport)
    let tableauCharge = historiqueDB.map(elt => elt.charge_entrainement)

    // init pr la boucle
    let dureeEntrainementUser = 0
    let chargeEntrainementUser = 0
    let compteur = 0

    tableauDuree.forEach(element => { // boucle pour faire la somme de la durée et de la charge d'entraînement
        dureeEntrainementUser += element
        chargeEntrainementUser += tableauCharge[compteur]

        compteur+=1
            });

            dureeEntrainementUser = dureeFormatee(dureeEntrainementUser, null) // conversion au format hh:mm:ss ou mm:ss

            // remplissage des champs
            document.getElementById("duree").textContent = dureeEntrainementUser
            // .toLocaleString('fr-FR') pour passer de 10000 -> 10 000
            document.getElementById("charge-entrainement").innerHTML = chargeEntrainementUser.toLocaleString('fr-FR') + ' <small>CE</small>'
            document.getElementById("nb-entrainement").textContent = tableauDuree.length.toLocaleString('fr-FR')
            
            let DicoNbEntrainementSport = {} // init pour les futures boucles ex : {"Course":3} 3 pour le nb d'entrainement en course
            tableauSport.forEach(elt => {
        if (!DicoNbEntrainementSport[elt]) { // si il n'y a pas ce sport dans le dico alors on le init à 1
            DicoNbEntrainementSport[elt] = 1
        } else { // sinon on prend le nombre d'activité dans le dico et on lui ajoute 1
            let nbActuelSport = DicoNbEntrainementSport[elt]
            let newNbSport = nbActuelSport+1
            DicoNbEntrainementSport[elt] = newNbSport
        }
    });

    let nbTotaleEntrainement = 0 // init pour compter le nombre d'entraînement totale pour préparer la prochaine boucle
    Object.entries(DicoNbEntrainementSport).forEach(([sport, nbWorkout]) => {
        nbTotaleEntrainement += nbWorkout
    })
            
    // init de 2 tableaux
    let pourcentageSport = []
    let labelSport = []
    Object.entries(DicoNbEntrainementSport).forEach(([sport, nbEntrainement]) => {
        // calcul du pourcentage ex : 10 entrainements totale (donc 10 entrainements c'est 100%) -> dont 2 entrainements de course
        // donc (2*100)/10
        let pourcentageDeCeSport = (nbEntrainement*100)/nbTotaleEntrainement

        // ajout de la data dans les tableaux
        pourcentageSport.push(pourcentageDeCeSport.toFixed(2))
        labelSport.push(sport)
    })

    // genereation du graphique
    genererGraphiqueDoughnut(labelSport, pourcentageSport)

    // remplissage des stats par sport
    await statistiquesParSport(sportDemandee)
}

document.addEventListener("DOMContentLoaded", () => {
    const segmentedButtonSemaine = document.getElementById("semaine")
    if (segmentedButtonSemaine) {
        segmentedButtonSemaine.addEventListener("click", () => {
            document.querySelector('.segmented-button.duree .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('semaine').classList.add('actif')
            init(dateMoins7J)
        })
    }
    const segmentedButtonMois = document.getElementById("mois")
    if (segmentedButtonMois) {
        segmentedButtonMois.addEventListener("click", () => {
            document.querySelector('.segmented-button.duree .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('mois').classList.add('actif')
            init(dateMoins30J)
        })
    }
    const segmentedButton3Mois = document.getElementById("trois-mois")
    if (segmentedButton3Mois) {
        segmentedButton3Mois.addEventListener("click", () => {
            document.querySelector('.segmented-button.duree .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('trois-mois').classList.add('actif')
            init(dateMoins90J)
        })
    }
    const segmentedButtonAnnee = document.getElementById("annee")
    if (segmentedButtonAnnee) {
        segmentedButtonAnnee.addEventListener("click", () => {
            document.querySelector('.segmented-button.duree .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('annee').classList.add('actif')
            init(dateMoins365J)
        })
    }


    const segmentedButtonCourse = document.getElementById("sport-course")
    if (segmentedButtonCourse) {
        segmentedButtonCourse.addEventListener("click", () => {
            document.querySelector('.segmented-button.stats-sport .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('sport-course').classList.add('actif')
            statistiquesParSport('Course')
        })
    }
    const segmentedButtonVelo = document.getElementById("sport-velo")
    if (segmentedButtonVelo) {
        segmentedButtonVelo.addEventListener("click", () => {
            document.querySelector('.segmented-button.stats-sport .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('sport-velo').classList.add('actif')
            statistiquesParSport('Vélo')
        })
    }
    const segmentedButtonNatation = document.getElementById("sport-natation")
    if (segmentedButtonNatation) {
        segmentedButtonNatation.addEventListener("click", () => {
            document.querySelector('.segmented-button.stats-sport .segmented-button-button.actif').classList.remove('actif')
            document.getElementById('sport-natation').classList.add('actif')
            statistiquesParSport('Natation')
        })
    }

    // on cache le message comme quoi il n'y a pas de données
    const messagePasDatas = document.getElementById("message-not-datas")
    if (messagePasDatas) {messagePasDatas.style.display="none"}

    init(dateMoins7J)
})