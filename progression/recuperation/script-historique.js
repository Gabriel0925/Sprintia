function returnDate(dateRecup) {
    let DateEuropeen = ""

    dateRecup = dateRecup.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = dateRecup[2] + "-" + dateRecup[1] + "-" + dateRecup[0]
    return DateEuropeen
}

async function remplissageTableau() {
    // recup du tableau et de toutes les datas dans l'ordre pour remplir le tableau
    let tableauHistorique = document.getElementById("tableau-historique")
    const historiqueDataUser = await db.recuperation.orderBy("date").toArray()

    historiqueDataUser.reverse() // on inverse pour que ça soit du plus récent au plus ancien

    if (historiqueDataUser.length <= 0) {
        // on cache le tableau
        tableauHistorique.style.display = "none"
        // on fais apparaitre le message comme quoi SPRINTIA n'a pas encore assez de données
        document.getElementById("aucune-data").style.display = "flex"
        return
    }

    historiqueDataUser.forEach(elt => {
        // Structure du tableau
        // creation d'une nouvelle ligne
        let newline = tableauHistorique.insertRow()
        // creation des colonnes
        let colonneDate = newline.insertCell(0)
        let colonneFcRepos = newline.insertCell(1)
        let colonneAction = newline.insertCell(2)

        // remplissage
        colonneDate.textContent = returnDate(elt.date)
        colonneFcRepos.textContent = elt.fc_repos

        let btnModifier = document.createElement("button")
        btnModifier.textContent = "Modifier"
        colonneAction.appendChild(btnModifier)
        // Ajout de la class
        btnModifier.classList.add("table")

        // ajout d'un bouton supprimer et modifier
        let btnSupprimer = document.createElement("button")
        btnSupprimer.textContent = "Supprimer"
        colonneAction.appendChild(btnSupprimer)
        // Ajout de la class
        btnSupprimer.classList.add("table")

        // on lie les boutons à des actions
        btnSupprimer.addEventListener("click", async () => {
            // confirmation avant suppression
            if (confirm("Supprimer votre récupération du " + returnDate(elt.date) + " ?")) {
                await db.recuperation.delete(elt.id)
                await newline.remove() // supprimer la ligne

                let dataTableau = document.querySelectorAll("td") // Recup des lignes pour savoir quand il faut cacher le tableau
                let tableau = document.getElementById("tableau-historique") // recup du tableau

                if (dataTableau.length <= 0) {
                    // On cache tout
                    tableau.style.display = "none"
                    // on fais apparaitre le message comme quoi SPRINTIA n'a pas encore assez de données
                    document.getElementById("aucune-data").style.display = "flex"
                } 

                // transmission de l'info au user
                logoDynamique("Supprimé 🗑️")
            }
        })
        btnModifier.addEventListener("click", async () => {
            // on l'envoie à ajouter-recup mais avec un param
            window.location.href = `ajouter-recuperation.html?edit=${elt.id}`
        })

    });
}

document.addEventListener("DOMContentLoaded", () =>  {
    const visuelInformation = document.getElementById("aucune-data")
    if (visuelInformation) {visuelInformation.style.display="none"}

    remplissageTableau()
})