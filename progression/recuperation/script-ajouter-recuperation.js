let ChampDate = document.getElementById("date-recuperation")
let DateActuelle = new Date().toISOString() // ça renvoie ça "2026-01-24T13:55:37.171Z"
// Enlever la partie qui nous interrese pas
DateActuelle = DateActuelle.split("T") // ['2026-01-24', '13:57:55.505Z']
DateActuelle = DateActuelle[0] // '2026-01-24'

ChampDate.max = DateActuelle // bloque la saisi de date dans le futur
ChampDate.value = DateActuelle

let modificationData = false // variable pour savoir si on est en train de modifier une data ou pas
let idRecupModif = undefined

// pour détecter si lorsqu'on est dans le formulaire il y a un appuie sur la touche entrée
let formKeyEntry = document.querySelector(".form")
formKeyEntry.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        saveRecuperation()
    }
})

async function saveRecuperation() {
    // recup
    let champsDate = document.getElementById("date-recuperation").value
    let champsFcRepos = parseInt(document.getElementById("fc-repos-recuperation").value)
    let button = document.getElementById("button-sauvegarder")

    // verif des champs
    if (!champsDate || !champsFcRepos || isNaN(champsFcRepos)) {
        alert("Les champs avec '*' sont obligatoire, vous devez les remplir.")
        return
    }

    try {
        // Prépa date pour les comparer ensuite
        const dateUserFormatee = new Date(champsDate)
        const dateActuelle = new Date()
        if (dateUserFormatee > dateActuelle) { // Comparaison de 2 dates
            alert("La date ne peut pas être dans le future.")
            return
        }

        if (champsFcRepos <= 0) {
            alert("Valeur non valide, la FC repos doit être un nombre supérieur à 0.")
            return
        }
        if (champsFcRepos < 20 || champsFcRepos > 140) {
            alert("Valeur non valide, la fréquence cardiaque de repos doit être un nombre compris entre 20 et 140 bpm.")
            return
        }

        if (modificationData != true){ // si on modifie ça sert a rien de mettre le message "vous avez déjà enregistré une récupération"
            // vérification si il y a deja une data ce jour ci
            let dataToday = await db.recuperation
                .where("date")
                .equals(champsDate)
                .toArray()

            if (dataToday.length > 0) {
                let confirmUpdate = confirm("Vous avez déjà enregistré une récupération pour cette date. Voulez-vous la remplacer ?")
                if (!confirmUpdate) {
                    return
                } else {
                    await db.recuperation
                        .where("date")
                        .equals(champsDate) // pour trouver la data qui à la date de la var champsDate
                        .delete() // supprime pour la save par la suite
                }
            }
        }

        if (modificationData == true) {
            // modification de la recup
            if (idRecupModif != undefined) {
                await db.recuperation.put({
                    id:idRecupModif,
                    date:champsDate,
                    fc_repos:champsFcRepos
                })
            } else {
                alert("Une erreur est survenue lors de la modification de votre récupération, veuillez réessayer.")
                return
            }
        } else {
            // sauvegarde
            await db.recuperation.add({
                date:champsDate,
                fc_repos:champsFcRepos
            })
        }

        // Transmet l'info au user
        button.disabled = true 
        button.textContent = "Sauvegarde..."

        button.textContent = "Sauvegardé"
        await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
        window.location.href = `recuperation.html` 
    } catch(error) {
        console.log(error)
        button.textContent = "Une erreur s'est produite"
        await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
    } finally {
        button.textContent = "Sauvegarder"
        button.disabled = false
    }
}

async function editRecuperation() {            
    const parametreURL = window.location.search // on recherche si il y a un param dans l'URL (ex : ?edit=7)
    let tableauSeparation = parametreURL.split("=") // exemple ['?edit', '7']

    if (tableauSeparation.length == 2) { // vérification si il y a bien 2 partie
        // conversion de l'id en int
        const ID = parseInt(tableauSeparation[1])

        // Recup des datas du workout
        if (ID) {
            const dataRecuperation = await db.recuperation.get(ID)

            if (dataRecuperation) {
                // remplissage du formulaire avec les datas
                document.getElementById("date-recuperation").value = dataRecuperation.date
                document.getElementById("fc-repos-recuperation").value = dataRecuperation.fc_repos
            } else {
                window.location.href = `recuperation.html` // si jamais il n'y a pas de data avec l'id dans l'URL on retourne à la page de liste des récupérations
            }

            // maj des textes de la page
            document.getElementById("title-page").textContent = "Modifier la récupération"

            // maj var
            modificationData = true
            idRecupModif = dataRecuperation.id
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const buttonSave = document.getElementById("button-sauvegarder")
    if (buttonSave) {buttonSave.addEventListener("click", saveRecuperation)}

    editRecuperation()
})