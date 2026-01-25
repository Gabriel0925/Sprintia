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

    let NiveauDatas = ValeurDB.map(dataBDD => dataBDD.niveau_course_user)
    NiveauDatas = NiveauDatas.reverse()

    let idDatas = ValeurDB.map(dataBDD => dataBDD.id)
    idDatas = idDatas.reverse()
    
    return {idDatas, NiveauDatas, DateDatas}
}

async function RemplirTableau() {
    // Recup des valeur dans bdd
    let {idDatas, NiveauDatas, DateDatas} = await RecupValueNiveauCourse()

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
    DateDatas.forEach(Date => {
        // Créer nouvelle ligne
        let NouvelleLigne = TableauHistorique.insertRow()

        // Créer une nouvelle ligne
        let ColonneDate = NouvelleLigne.insertCell(0)
        let ColonneNiveau = NouvelleLigne.insertCell(1)
        let ColonneButtonSupprimer = NouvelleLigne.insertCell(2)

        // Remplir ligne
        ColonneDate.textContent = Date
        ColonneNiveau.textContent = NiveauDatas[compteur]

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
                location.reload()
            }
        })

        compteur+=1
    });

    return
}

window.addEventListener("DOMContentLoaded", () => {
    RemplirTableau()
})