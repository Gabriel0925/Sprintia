function removeDataAssocieProfil(dico) {
    const cleanDico = {}

    for (const key in dico) {
        // on prend tous sauf hydratation_estimee et transpiration_estimee, on enleve la charge d'entraînement car on la recalcule par la suite pour éviter les tricheurs
        if (key != "hydratation_estimee" && key != "transpiration_estimee" && key != "charge_entrainement") {
            cleanDico[key] = dico[key]
        }
    }
    return cleanDico
}

async function uploadFileSPRINTIA(event) {
    const fileSPRINTIA = event.target.files[0]
    let button = document.getElementById("button-import-SPRINTIA")

    if (fileSPRINTIA) {
        button.disabled = true
        button.textContent = "Importation..."

        try {
            let textFile = await fileSPRINTIA.text() // on récup le contenu du fichier en texte
            let dicoDataWorkout = JSON.parse(textFile)
            
            const dicoDataClean = removeValueUndefined(dicoDataWorkout) // toutes les valeurs en undefined sont enlever du dico
            const dicoDataUser = removeDataAssocieProfil(dicoDataClean)

            if (Object.keys(dicoDataUser).length < 1) {
                button.textContent = "Aucune donnée détectée"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 600))
            } else {
                // var de base
                const dateUserFormatee = new Date(dicoDataUser["date"])
                const dateActuelle = new Date()
                let workoutTime = dicoDataUser?.["duree"]??0
                let workoutRpe = dicoDataUser?.["rpe"]??1
                let noteEntrainement = dicoDataUser?.["note"]??""

                // vérification
                if (workoutRpe < 1) {workoutRpe=1} else if (workoutRpe>10) {workoutRpe=10}

                // on vérifie qu'il y a bien toutes les données necessaires aux fonctionnements
                if (workoutTime == 0 || workoutTime >= 1439.9833 || new Date(dicoDataUser["date"]) == "Invalid Date" || dateUserFormatee > dateActuelle ||
                        noteEntrainement.length > 500) {
                    button.textContent = "Fichier corrompu"
                    await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
                } else {
                    // on regarde si on a la possibilité d'ajouter les datas de hydratation_estimee et transpiration_estimee
                    let profilDB = await db.profil.get(1)
                    let transpirationEstimee = undefined
                    let hydratationEstimee = undefined

                    if (profilDB != undefined) {
                        let poidsUser = Number(profilDB.poids)
                        let coefficientRpe = [0.4, 0.8, 1.2, 1.6]

                        // Attribution de la valeur du RPE
                        if (workoutRpe <= 3) {
                            coefficientRpe = coefficientRpe[0]
                        } else if (workoutRpe <= 6) {
                            coefficientRpe = coefficientRpe[1]
                        } else if (workoutRpe <= 8) {
                            coefficientRpe = coefficientRpe[2]
                        } else {
                            coefficientRpe = coefficientRpe[3]
                        }

                        // Calcul
                        let dureeHeure = workoutTime/60
                        transpirationEstimee = Math.round((dureeHeure*coefficientRpe*(poidsUser/70))*1000)
                        hydratationEstimee = Math.round(transpirationEstimee*1.2)

                        dicoDataUser["transpiration_estimee"] = transpirationEstimee 
                        dicoDataUser["hydratation_estimee"] = hydratationEstimee 
                    }

                    // on recalcule la charge d'entraînement pour éviter aux users de tricher en modifiant le fichier
                    let chargeWorkout = 0
                    let coefRpe = {1:0.2, 2:0.4, 3:0.7, 4:1.1, 5:1.6, 6:2.3, 7:3.2, 8:4.5, 9:6.2, 10:8.5}
                    // Calcul Charge
                    chargeWorkout = Math.floor(workoutTime*coefRpe[workoutRpe])
                    // si la charge est inférieur à 1 alors on la met a 1
                    if (chargeWorkout < 1) {chargeWorkout = 1}
                    dicoDataUser["charge_entrainement"] = chargeWorkout 

                    // on recup l'id direct au moment de l'enregistrement grâce à add qui renvoie l'id
                    const idWorkout = await db.entrainement.add(dicoDataUser)

                    button.textContent = "Importé"
                    await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
                    window.location.href = `../../../entrainement/entrainement.html?workout=${idWorkout}`
                }
            }
        } catch(error) {
            console.log(error)
            button.textContent = "Une erreur s'est produite"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            button.textContent = "Importer fichier SPRINTIA"
            button.disabled = false
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const inputFileInvisible = document.getElementById("file-input-json")
    if (inputFileInvisible) {inputFileInvisible.addEventListener("change", (event) => {uploadFileSPRINTIA(event)})}
    
    const inputFile = document.getElementById("button-import-SPRINTIA")
    if (inputFile) {inputFile.addEventListener("click", () => {document.getElementById('file-input-json').click()})}
})