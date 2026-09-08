const dicoSport = {
    "Run": "Course",
    "Bike": "Vélo", "MountainBike": "Vélo",
    "Walk": "Marche",
    "Hike": "Randonnée",
    "Swim": "Natation",
    "Strength": "Musculation",
    "Rowing": "Rameur d'intérieur",
    "XC-Ski": "Ski", "NordicSki": "Ski",
    "Other": "Libre", "Custom": "Libre"
}

function conversionMinutesTP(dureeWorkoutUser) {
    // petite vérif pr s'assurer
    if (dureeWorkoutUser != undefined) {
        // training peaks renvoie 1.5 heure donc on le repasse en minutes -> 90 minutes
        try {
            return Number(dureeWorkoutUser)*60
        } catch {
            return undefined
        }
    } else {
        return undefined
    }
}

async function uploadFileTP(event) {
    const fileCSV = event.target.files[0]
    let button = document.getElementById("button-import-TP")

    if (fileCSV) {
        button.disabled = true
        button.textContent = "Importation..."

        try {
            // on lit le fichier et on convertit en texte
            const readFile = await fileCSV.text()
            
            const ligneFile = Papa.parse(readFile) 
            // on extrait uniquement la partie data du dico car les erreurs et meta on s'en fou
            let dataHistoriqueEntrainement = ligneFile["data"]
            // on récupere les entetes (ex : ["Sport,Duree,RPE"])  on supprimme l'élément à l'index 0 et on supprime que 1 élément
            const enteteFile = dataHistoriqueEntrainement.splice(0, 1)[0] // index 0 car splice va renvoyer [["elem1", "elem2"]]

            // recup des index
            let indexSportWorkout = enteteFile.indexOf("WorkoutType")
            let indexDateWorkout = enteteFile.indexOf("WorkoutDay")
            let indexNomWorkout = enteteFile.indexOf("Title")
            let indexDureeWorkout = enteteFile.indexOf("TimeTotalInHours")
            let indexRpe = enteteFile.indexOf("Rpe")

            let indexFcMoy = enteteFile.indexOf("HeartRateAverage")
            let indexFcMax = enteteFile.indexOf("HeartRateMax")

            let indexDistanceWorkout = enteteFile.indexOf("DistanceInMeters")

            let nbWorkoutImporter = 0 // compteur pour compter le nombre d'entraînement importé
            let profilDB = await db.profil.get(1) // pour des calculs de transpiration,... par la suite
            for (const elt of dataHistoriqueEntrainement) {
                // recup des datas
                let sportWorkout = elt?.[indexSportWorkout] ?? undefined
                let dateWorkout = elt?.[indexDateWorkout]??undefined
                let nomWorkout = elt?.[indexNomWorkout]??undefined
                let dureeWorkout = elt[indexDureeWorkout]??undefined
                let rpeWorkout = Number(elt[indexRpe]) || undefined

                let fcMoyWorkout = parseInt(elt[indexFcMoy]) || undefined
                let fcMaxWorkout = parseInt(elt[indexFcMax]) || undefined

                let distanceWorkout = Number(Number(elt[indexDistanceWorkout]).toFixed(2)) || undefined

                if (elt.length <= 1) { // car la derniere ligne du CSV renvoie ça [''] et length == 1
                    //pass
                } else {
                    // on adapte le nom du sport donné par TP à SPRINTIA
                    sportWorkout = dicoSport?.[sportWorkout] ?? "Libre"

                    if (nomWorkout != undefined) {
                        if (nomWorkout.length > 40) {
                            nomWorkout = sportWorkout+" le "+dateWorkout.split("-")[2]+"/"+dateWorkout.split("-")[1].padStart(2, "0") // exemple : Course le 28/04
                        }
                    } else {
                        nomWorkout = sportWorkout+" le "+dateWorkout.split("-")[2]+"/"+dateWorkout.split("-")[1].padStart(2, "0") // exemple : Course le 28/04
                    }

                    if (dureeWorkout != undefined) {                        
                        // passage du format hh:mm:ss en minutes pour la durée
                        dureeWorkout = conversionMinutesTP(dureeWorkout)
                    }

                    if (dureeWorkout == undefined || dureeWorkout <= 0 || new Date(dateWorkout) == "Invalid Date") {
                        continue // on passe au tour suivant
                    } else {
                        nbWorkoutImporter+=1 // incrémentation
                    }

                    distanceWorkout = distanceWorkout*10**(-3) // conversion des mètres en km
                    
                    // calcul de l'allure moyenne ou de la vitesse en fonction du sport
                    let allureMoyWorkout = 0
                    let vitesseMoyWorkout = 0
                    if (sportWorkout != "Libre") {
                        if (distanceWorkout != undefined && distanceWorkout > 0) {
                            if (sportWorkout == "Course" || sportWorkout == "Marche" || sportWorkout == "Randonnée") {
                                // Calcul de l'allure en course à pied
                                allureMoyWorkout = dureeWorkout/distanceWorkout // on obtient par exemple : 7.65

                                let min = Math.floor(allureMoyWorkout) // pour recup les minutes
                                let sec = Math.round((allureMoyWorkout%1)*60) // conversion du reste en seconde 
                                allureMoyWorkout = `${min}:${sec.toString().padStart(2, "0")}`
                            } else if (sportWorkout == "Vélo" || sportWorkout == "Ski") {
                                // conversion des min en heures
                                let workoutTimeHour = dureeWorkout/60
                                vitesseMoyWorkout = Number((distanceWorkout/workoutTimeHour).toFixed(2))
                            }
                        } else {distanceWorkout=undefined}
                    }
                    if (allureMoyWorkout == 0) {allureMoyWorkout = undefined}
                    if (vitesseMoyWorkout == 0) {vitesseMoyWorkout = undefined}

                    // netttoyage data
                    if (rpeWorkout == "" || rpeWorkout == undefined) {rpeWorkout = 1} else {rpeWorkout = parseInt(rpeWorkout)}
                    if (rpeWorkout > 10) {rpeWorkout=10} // petite sécurité
                    
                    let coefRpe = {1:0.2, 2:0.4, 3:0.7, 4:1.1, 5:1.6, 6:2.3, 7:3.2, 8:4.5, 9:6.2, 10:8.5}
                    let chargeEntrainementWorkout = Math.floor(coefRpe[rpeWorkout]*dureeWorkout)
                    if (chargeEntrainementWorkout < 1) {chargeEntrainementWorkout = 1} // petite sécurité

                    // Calcul de la transpiration
                    let transpirationEstimee = 0
                    let hydratationEstimee = 0

                    if (profilDB != undefined) {
                        let poidsUser = Number(profilDB.poids)
                        let dureeHeure = dureeWorkout/60 // Conversion de la durée en heure
                        let coefficientRpe = [0.4, 0.8, 1.2, 1.6]

                        // Attribution de la valeur du RPE
                        if (rpeWorkout <= 3) {
                            coefficientRpe = coefficientRpe[0]
                        } else if (rpeWorkout <= 6) {
                            coefficientRpe = coefficientRpe[1]
                        } else if (rpeWorkout <= 8) {
                            coefficientRpe = coefficientRpe[2]
                        } else {
                            coefficientRpe = coefficientRpe[3]
                        }

                        // Calcul
                        transpirationEstimee = Math.round((dureeHeure*coefficientRpe*(poidsUser/70))*1000)
                        hydratationEstimee = Math.round(transpirationEstimee*1.2)
                    } else {
                        transpirationEstimee = undefined
                        hydratationEstimee = undefined
                    }

                    // dico de base
                    let dicoBase = {
                        sport: sportWorkout,
                        date: dateWorkout,
                        nom: nomWorkout,
                        duree: dureeWorkout,
                        rpe: rpeWorkout,
                        fc_moy: fcMoyWorkout,
                        fc_max: fcMaxWorkout,
                        distance: distanceWorkout,
                        transpiration_estimee: transpirationEstimee,
                        hydratation_estimee:hydratationEstimee,
                        charge_entrainement: chargeEntrainementWorkout
                    }

                    // on ajoute les données de sport spécifique
                    if (sportWorkout != "Libre") {
                        dicoBase["allure_moy"] = allureMoyWorkout
                        dicoBase["vitesse_moy"] = vitesseMoyWorkout
                    }

                    const dicoDataClean = removeValueUndefined(dicoBase)
                    await db.entrainement.add(dicoDataClean)
                }
            }

            button.textContent = `${nbWorkoutImporter} entraînements importés`
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
            window.location.href = "../../../index.html?workoutimport" // redirection vers l'historique d'entrainement après l'importation 
        } catch(error) {
            console.log(error)
            button.textContent = "Une erreur s'est produite"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            button.textContent = "Importer CSV"
            button.disabled = false
        }
    }

}

document.addEventListener("DOMContentLoaded", () => {
    const inputFileInvisible = document.getElementById("file-input-TP")
    if (inputFileInvisible) {inputFileInvisible.addEventListener("change", (event) => {uploadFileTP(event)})}
    
    const inputFile = document.getElementById("button-import-TP")
    if (inputFile) {inputFile.addEventListener("click", () => {document.getElementById('file-input-TP').click()})}
})