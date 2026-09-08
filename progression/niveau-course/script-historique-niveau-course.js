function ReturnDate(DateNiveauCourse) {
    let DateEuropeen = ""

    DateNiveauCourse = DateNiveauCourse.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = DateNiveauCourse[2] + "-" + DateNiveauCourse[1] + "-" + DateNiveauCourse[0]
    return DateEuropeen
}
async function RecupValueNiveauCourseGraphique() {
    // Initialisation 
    let TailleHardware = window.innerWidth
    let NbValeurRecup = -13

    // Logique de nb datas en fonction du devices
    if (TailleHardware <= 520) {
        NbValeurRecup = -4
    } else if (TailleHardware <= 640) {
        NbValeurRecup = -6
    } else if (TailleHardware <= 720) {
        NbValeurRecup = -7
    } else if (TailleHardware <= 790) {
        NbValeurRecup = -8
    } else if (TailleHardware <= 1000) {
        NbValeurRecup = -10
    }

    // Recup value Data
    const ValeurDB = await db.niveau_course.toArray()    
    
    // Trier par date 
    ValeurDB.sort((element1, element2) => { // En js on peut comparer 2 dates comme des maths
        if (element1.date < element2.date) return -1
        if (element1.date > element2.date) return 1
    })

    // map permet de retourner une nouvelle liste a partir d'une premiere liste et de prendre qu'une seule clé d'un objet
    // slice permet de découper un tableau pour en garder qu'une partie grace aux indices
    const NiveauDatas = ValeurDB.slice(NbValeurRecup).map(dataBDD => dataBDD.niveau_course_user) // -10 pr prendre les 1à dernieres valeur
    const DateDatas = ValeurDB.slice(NbValeurRecup).map(dataBDD => dataBDD.date)

    // Initialisation d'une liste de date avec le format européen
    let ListeDate = []
    let DateEuropeen = ""

    DateDatas.forEach(element => { // Parcours des dates
        DateEuropeen = ReturnDate(element)
        ListeDate.push(DateEuropeen) // Ajout à la liste des dates format européen
    });
    
    return {NiveauDatas, ListeDate}
}
async function graph() {
    // attendre la recup des datas
    let {NiveauDatas, ListeDate} = await RecupValueNiveauCourseGraphique()

    if (NiveauDatas.length <= 0) {
        NiveauDatas = [0, 0, 0]
        ListeDate = ["Janvier", "Février", "Mars"]
    }
    
    genererGraphiqueLine(ListeDate, NiveauDatas)
}

function ReturnDate(DateNiveauCourse) {
    let DateEuropeen = ""

    DateNiveauCourse = DateNiveauCourse.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = DateNiveauCourse[2] + "-" + DateNiveauCourse[1] + "-" + DateNiveauCourse[0]
    return DateEuropeen
}
async function remplirTableau() {
    // recup des datas 
    const dataDB = await db.niveau_course.orderBy("date").toArray()
    dataDB.reverse() // pour remmetre la datas la plus récente en haut du tableau
        
    let tableauHistorique = document.getElementById("tableau-historique") // Recup du tableau

    if (dataDB.length > 0) {
        document.getElementById("aucune-data").style.display = "none"
    } else {
        document.getElementById("aucune-data").style.display = "flex"
        tableauHistorique.style.display = 'none'
    }

    for (const data of dataDB) {
        // data contient le dico ex : {niveau_course_user: 72, date: '2026-01-25', id: 1}
        const newLine = tableauHistorique.insertRow()
        const colDate = newLine.insertCell(0)
        const colNiveau = newLine.insertCell(1)
        const colDistance = newLine.insertCell(2)
        const colAction = newLine.insertCell(3)

        // Remplir ligne
        colDate.textContent = ReturnDate(data.date)
        colNiveau.textContent = data.niveau_course_user.toString().replace(".", ",") // ne pas oublier de le mettre en str avant le replace
        if (data.distance != undefined) {
            colDistance.textContent = data.distance.toString().replace(".", ",")
        } else {
            colDistance.textContent = "-"
        }

        // Create button
        let btnModifier = document.createElement("button")
        btnModifier.textContent = "Modifier"
        colAction.appendChild(btnModifier)
        // Ajout de la class
        btnModifier.classList.add("table")
        
        let btnSupprimer = document.createElement("button")
        btnSupprimer.textContent = "Supprimer"
        colAction.appendChild(btnSupprimer)

        // Ajout de la class
        btnSupprimer.classList.add("table")

        // Ajout de la logique pour la suppresion
        btnSupprimer.addEventListener("click", async () => { // Ajout d'une "action" au bouton
            // confirmation avant suppression
            if (confirm("Supprimer ce niveau de course ?")) {
                await db.niveau_course.delete(data.id) // supprimer la data de la bdd
                await newLine.remove() // supprimer la ligne

                graph()

                // on recup les datas et on les affiche pour la zone pour le dernier niveau de course
                const lastLevelUser = await lastLevel()
                const zoneLevelUser = zoneLevel(lastLevelUser)

                // affichage du dernier niveau de course et de la zone
                document.getElementById("last-level-run").innerHTML = lastLevelUser.toString().replace(".", ",")
                document.getElementById("zone-last-level-run").innerHTML = zoneLevelUser

                let dataTableau = document.querySelectorAll("td") // Recup des lignes pour savoir quand il faut cacher le tableau
                let tableau = document.getElementById("tableau-historique") // recup du tableau

                if (dataTableau.length <= 0) {
                    // On cache tout
                    tableau.style.display = "none"
                    // on fais apparaitre le message comme quoi SPRINTIA n'a pas encore assez de données
                    document.getElementById("aucune-data").style.display = "flex"
                } 
                
                logoDynamique("Supprimé 🗑️")
            }
        })
        btnModifier.addEventListener("click", async () => {
            // on l'envoie à ajouter-recup mais avec un param
            window.location.href = `ajouter-niveau-course.html?edit=${data.id}`
        })
    }
}

// Pour recharger le graphique si c'est dans le BFCache
window.addEventListener("pageshow", (event) => {
    if (event.persisted) { // Si la page est dans le BFCache alors on relance le graphique
        graph()
    }
})
document.addEventListener("DOMContentLoaded", async () => {
    const segmentedButtonEvolution = document.getElementById("segmented-button-analyse")
    if (segmentedButtonEvolution) {segmentedButtonEvolution.addEventListener("click", () =>{window.location.href = 'niveau-course-analyse.html'})}
    
    // on recup les datas et on les affiche pour la zone pour le dernier niveau de course
    const lastLevelUser = await lastLevel()
    const zoneLevelUser = zoneLevel(lastLevelUser)

    // affichage du dernier niveau de course et de la zone
    document.getElementById("last-level-run").innerHTML = lastLevelUser.toString().replace(".", ",")
    document.getElementById("zone-last-level-run").innerHTML = zoneLevelUser

    graph()
    await remplirTableau()
})