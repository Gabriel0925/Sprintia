let DureeTotalSemaine = 0

async function RecupData() {
    // Initialisation
    DureeTotalSemaine = 0 // Variable deja défini en haut du script (remise à 0)
    let DureeTotalSemaine2 = 0
    let DureeTotalSemaine3 = 0
    let DureeTotalSemaine4 = 0
    
    // Date recup
    let dateMoins7J = createObjetDate(7)
    let dateMoins14J = createObjetDate(14)
    let dateMoins21J = createObjetDate(21)
    let dateMoins28J = createObjetDate(28)

    // Recup data in BDD
    const HistoriqueDB = await db.entrainement.where("date").aboveOrEqual(dateMoins28J).toArray()

    // Trier par date 
    HistoriqueDB.sort((element1, element2) => { // En js on peut comparer 2 dates comme des maths
        if (element1.date < element2.date) return 1
        if (element1.date > element2.date) return -1
    })

    // Recup valeur qui nous interesse
    let DureeDataSemaine = HistoriqueDB.map(data => data.duree)
    let DateDataSemaine = HistoriqueDB.map(data => data.date)

    // Unit
    let TableauDureeSemaine = [] 
    let TableauDureeSemaine2 = [] 
    let TableauDureeSemaine3 = [] 
    let TableauDureeSemaine4 = [] 
    let compteur = 0

    DateDataSemaine.forEach(element => { // Parcours des dates
        if (element >= dateMoins7J) {
    TableauDureeSemaine.push(DureeDataSemaine[compteur]) // tableau pour la durée des 7 derniers jours
        } else if (element >= dateMoins14J) {
    TableauDureeSemaine2.push(DureeDataSemaine[compteur]) // tableau pour la durée des 14 derniers jours (on ne compte pas les séances des 7 premiers jours) 
        } else if (element >= dateMoins21J) {
    TableauDureeSemaine3.push(DureeDataSemaine[compteur]) // tableau pour la durée des 28 derniers jours (on ne compte pas les séances des 14 premiers jours)
        } else if (element >= dateMoins28J) {
    TableauDureeSemaine4.push(DureeDataSemaine[compteur]) // tableau pour la durée des 28 derniers jours (on ne compte pas les séances des 14 premiers jours)
        }

        compteur += 1
    });

    // 3 boucles pour ajouter les durée pr savoir jai fais combien de temps de sport les 7 derniers jours,...
    TableauDureeSemaine.forEach(element => { 
        DureeTotalSemaine += element
    })  
    TableauDureeSemaine2.forEach(element => {
        DureeTotalSemaine2 += element
    })
    TableauDureeSemaine3.forEach(element => {
        DureeTotalSemaine3 += element
    })
    TableauDureeSemaine4.forEach(element => {
        DureeTotalSemaine4 += element
    })

    const TableauPourGraphique = [Math.floor(DureeTotalSemaine4), Math.floor(DureeTotalSemaine3), Math.floor(DureeTotalSemaine2), Math.floor(DureeTotalSemaine)]

    return TableauPourGraphique
}

async function graph() {
    // recup des datas
    let TableauPourGraphique = await RecupData()

    genererGraphiqueLine(["S-4", "S-3", "S-2", "S-1"], TableauPourGraphique)
}

window.addEventListener("DOMContentLoaded", () => {
    graph()
})

// Pour recharger le graphique si c'est dans le BFCache
window.addEventListener("pageshow", (event) => {
    if (event.persisted) { // Si la page est dans le BFCache alors on relance le graphique
        graph()
    }
})

document.addEventListener("DOMContentLoaded", async () => {
    // écouteur d'event
    const buttonBriefing = document.querySelector("button.briefing")
    if (buttonBriefing) {buttonBriefing.addEventListener("click", () => {windowsBriefing("Analyser mes tendances")})}


    // --- Charge d'entrainement ---
    // recup des valeurs grâce au fichier "script-charge-entrainement.js"
    const [chargeTotale7j, chargeTotale28j, nbEntrainement28j, nombreWeekLissage, cibleUserMin, cibleUserMax, 
            ratioChargeUser, statutUser, analyse, nameCoach, avatarCoach] = await manageCalcul()
    // affichage des valeurs
    document.getElementById("charge-7j").innerHTML = chargeTotale7j + " <small>CE</small>"
    document.getElementById("statut-charge-entrainement").innerHTML = statutUser

    // --- Récupération ---
    const tableauLastRecuperation = await db.recuperation
        .where("date")
        .aboveOrEqual(createObjetDate(0))
        .toArray()
    let lastRecuperation = "--"
    if (tableauLastRecuperation.length > 0) {lastRecuperation = tableauLastRecuperation[0].fc_repos}
    document.getElementById("data-recuperation").innerHTML = lastRecuperation + " <small>bpm</small>"


    // --- Indulgence de course ---
    const data7jCourse = await db.entrainement
    .where("date")
    .aboveOrEqual(dateMoins7j) // la var "dateMoins7j" est créer dans le script-charge-entrainement.js
    .toArray()
    let sommeDist7j = 0
    for (const elt of data7jCourse) {
        if (elt.sport == "Course") {
            if (!isNaN(elt.distance)) {
                sommeDist7j+=Number(elt.distance)
            }
        }
    }
    document.getElementById("data-dist-7j").innerHTML = sommeDist7j.toFixed(1).replace(".", ",") + " <small>km</small>"

    // --- Niveau de course ---
    const lastLevelUser = await lastLevel()
    const zoneLevelUser = zoneLevel(lastLevelUser)
    document.getElementById("dernier-niveau-course").innerHTML = lastLevelUser.toString().replace(".", ",") + " <small>/100</small>"
    document.getElementById("zone-dernier-niveau-course").innerHTML = zoneLevelUser

})