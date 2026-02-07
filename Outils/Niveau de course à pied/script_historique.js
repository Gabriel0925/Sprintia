function ReturnDate(DateNiveauCourse) {
    let DateEuropeen = ""

    DateNiveauCourse = DateNiveauCourse.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = DateNiveauCourse[2] + "-" + DateNiveauCourse[1] + "-" + DateNiveauCourse[0]
    return DateEuropeen
}

async function RecupValueNiveauCourse() {
    // Recup value Data
    const ValeurDB = await db.niveau_course.toArray()

    // Trier par date 
    ValeurDB.sort((element1, element2) => { // En js on peut comparer 2 dates comme des maths
        if (element1.date < element2.date) return -1
        if (element1.date > element2.date) return 1
    })

    // map permet de retourner une nouvelle liste a partir d'une premiere liste et de prendre qu'une seule clé d'un objet
    let DateDatas = ValeurDB.map(dataBDD => dataBDD.date)
    // Reverse pour mettre a lenvers les données pour que ds le tableau plus on descend plus c'est des valeurs ancienne
    DateDatas = DateDatas.reverse()

    // Initialisation d'une liste de date avec le format européen
    let ListeDate = []
    let DateEuropeen = ""

    DateDatas.forEach(element => { // Parcours des dates
        DateEuropeen = ReturnDate(element)
        ListeDate.push(DateEuropeen) // Ajout à la liste des dates format européen
    });

    let NiveauDatas = ValeurDB.map(dataBDD => dataBDD.niveau_course_user)
    NiveauDatas = NiveauDatas.reverse()

    let idDatas = ValeurDB.map(dataBDD => dataBDD.id)
    idDatas = idDatas.reverse()
    
    return {idDatas, NiveauDatas, ListeDate}
}

async function RemplirTableau() {
    // Recup des valeur dans bdd
    let {idDatas, NiveauDatas, ListeDate} = await RecupValueNiveauCourse()

    // Recup du tableau
    let TableauHistorique = document.getElementById("tableau-historique")

    if (NiveauDatas.length > 0) {
        TableauHistorique.classList.add("visible")
        document.getElementById("text-informatif").style.display = "none"
    } else {
        document.getElementById("cacher-title1").style.display = "none"
        document.getElementById("cacher-title2").style.display = "none"
        return
    }

    let compteur = 0
    ListeDate.forEach(Date => {
        // Créer nouvelle ligne
        let NouvelleLigne = TableauHistorique.insertRow()

        // Créer une nouvelle ligne
        let ColonneDate = NouvelleLigne.insertCell(0)
        let ColonneNiveau = NouvelleLigne.insertCell(1)
        let ColonneButtonSupprimer = NouvelleLigne.insertCell(2)

        // Remplir ligne
        ColonneDate.textContent = Date
        ColonneNiveau.textContent = NiveauDatas[compteur].toString().replace(".", ",") // ne pas oublier de le mettre en str avant le replace

        // Create button
        let BoutonSupprTableau = document.createElement("button")
        BoutonSupprTableau.textContent = "Supprimer"
        ColonneButtonSupprimer.appendChild(BoutonSupprTableau)

        // Ajout de la class
        BoutonSupprTableau.classList.add("tableau")

        const EtapeBoucle = compteur // Grâce a const la variable ne change jamais donc chaque bouton enregistre sa ligne en fonction de letape de la bouclz
        // Ajout de la logique pour la suppresion
        BoutonSupprTableau.addEventListener("click", async () => { // Ajout d'une "action" au bouton
            // confirmation avant suppression
            if (confirm("Supprimer ce niveau de course ?")) {
                await db.niveau_course.delete(idDatas[EtapeBoucle]) // supprimer la data de la bdd
                await NouvelleLigne.remove() // supprimer la ligne
                GenererGraphique()

                let DataTableau = document.querySelectorAll("td") // Recup des lignes pour savoir quand il faut cacher le tableau
                let Tableau = document.getElementById("tableau-historique") // recup du tableau
                let h2elem1 = document.getElementById("cacher-title1") // pour cacher le titre "Graphique"
                let h2elem2 = document.getElementById("cacher-title2") // pour cacher le titre "Votre historique"

                if (DataTableau.length == 0) {
                    // On cache tout
                    Tableau.style.display = "none"
                    h2elem1.style.display = "none"
                    h2elem2.style.display = "none"
                    // on fais apparaitre le message comme quoi sprintia n'a pas encore assez de données
                    document.getElementById("text-informatif").style.display = "block"
                    // destruction du graphique
                    if (barChart) { // le graph est créer dans le !!-- script_outil.js --!!
                        barChart.destroy() // destruction du graphique qu'il y a dans script_outil.js
                        document.getElementById("conteneur-graphique").style.display = "none" // on cache le conteneur du graphique
                    }    
                }
            }
        })

        compteur+=1
    });

    return
}

window.addEventListener("DOMContentLoaded", () => {
    RemplirTableau()
})