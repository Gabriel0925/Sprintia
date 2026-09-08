async function uploadFileTCX(event) {
    const dicoNameSport = { // init dico pr les sports
        // COURSE A PIED
        "running":"Course",
        "run":"Course",
        "course":"Course",
        "course à pied":"Course",
        "course a pied":"Course",
        "trail":"Course",
        "treadmill":"Course", // Tapis de course

        // VELO
        "cycling":"Vélo",
        "biking":"Vélo",
        "bike":"Vélo",
        "velo":"Vélo",
        "vélo":"Vélo",
        "mountain_biking":"Vélo",
        "vtt":"Vélo",
        "indoor_cycling":"Vélo", // home-trainer
        "gravel":"Vélo",
        
        // OTHER
        "other":"Libre"
    }

    const fileTCX = event.target.files[0]
    let button = document.getElementById("button-import-tcx")

    if (fileTCX) {
        button.disabled = true
        button.textContent = "Importation..."

        try {
            let textFile = await fileTCX.text() // on récup le contenu du fichier en texte
            
            const parser = new DOMParser() // création d'un objet pr transformer le txt en DOM
            const xmlDoc = parser.parseFromString(textFile, "text/xml") // transformation du texte en document XML c'est un langage équivalent à HTML

            //console.log(xmlDoc)

            const dataLap = xmlDoc.getElementsByTagName("Lap")
            const tableauDataLap = Array.from(dataLap) // transformation des balises en tableau js pr les laps

            // Recup du sport et de la date
            const workoutSport = dicoNameSport[xmlDoc.querySelector("Activity").getAttribute("Sport").toLowerCase()] || "Libre" // si le sport n'est pas dans le dico on le met en Libre
            let xmlDate = xmlDoc.querySelector("Id").textContent // on obtient ça : 2026-03-28T08:08:56Z
            let tableauXmlDate = xmlDate.split("T") // ["2026-03-28", "08:08:56Z"]
            const workoutDate = tableauXmlDate[0] // 2026-03-28

            // Init pour la boucle
            let workoutTime = 0
            let workoutDistance = 0
            let workoutFcMoy = 0
            let workoutFcMax = 0
            let workoutMaximumSpeed = 0

            let workoutDenivele = 0
            let deniveleLastLap = undefined

            let lapPointGps = []

            // Boucle qui parcoure tous les lap de l'entraînement et qui convertit par exemple des metres au km directement
            tableauDataLap.forEach(element => {
                // l'opérateur ?. permet de ne pas faire planter le code si la balise n'est pas présente dans le TCX et donc prendre 0 à la place
                workoutTime += Number(element.querySelector("TotalTimeSeconds")?.textContent ?? 0) // on ne convertit pas ici car lors du calcul de la FC moyenne on va diviser par le temps total de l'entrainement en secondes
                workoutDistance += Number(element.querySelector("DistanceMeters")?.textContent ?? 0)/1000 // conversion des m en km

                // Récup des BPM moyen et max de l'entraînement
                // formule pr la fc moy d'un entrainement : (FC moy du lap * durée du lap en secondes) / durée totale de l'entrainement en secondes
                workoutFcMoy += Number(element.querySelector("AverageHeartRateBpm Value")?.textContent??0)*Number(element.querySelector("TotalTimeSeconds")?.textContent??0)

                let fcMaxLap = Number(element.querySelector("MaximumHeartRateBpm Value")?.textContent ?? 0)
                if (fcMaxLap > workoutFcMax) {
                    workoutFcMax = fcMaxLap
                }

                // recup de la vitesse max si cette donnée est présente sinon ça vaut 0
                let maximumSpeedLap = Number(element.querySelector("MaximumSpeed")?.textContent??0)*3.6 // conversion des m/s en km/h
                if (maximumSpeedLap > workoutMaximumSpeed) {
                    workoutMaximumSpeed = maximumSpeedLap
                }

                // recup du dénivelé si il est présent
                const pointsAltitudeLap = element.querySelectorAll("AltitudeMeters") // du lap actuel uniquement
                const tolerance = 1.5 // tolérence de 1.5m pour le calcul du dénivelé
                pointsAltitudeLap.forEach(elt => {
                    const altitudeNow = Number(elt?.textContent ?? 0)

                    // si c'est le premier point on l'init
                    if (deniveleLastLap == undefined) {deniveleLastLap=altitudeNow}

                    if (altitudeNow-deniveleLastLap > tolerance) { // si la différence entre les deux points est supérieur à une hausse de 1.5m
                        workoutDenivele = workoutDenivele+(altitudeNow-deniveleLastLap)
                        deniveleLastLap = altitudeNow
                    } else if (altitudeNow-deniveleLastLap < -tolerance) { // si ça descend on met à jour le denivelé pour le tour suivant (-tolerance pour l'inverse de tolérence soit -1.5m)
                        deniveleLastLap = altitudeNow
                    }
                })

                // recupéré les points gps
                const pointGpsLap = element.querySelectorAll("Trackpoint")
                pointGpsLap.forEach(elt => {
                    const timeTrackpoint = elt.querySelector("Time")?.textContent??undefined
                    const latitudePoint = Number(elt.querySelector("Position LatitudeDegrees")?.textContent ?? undefined)
                    const longitudePoint = Number(elt.querySelector("Position LongitudeDegrees")?.textContent ?? undefined)

                    // un number en undefined ça renvoie NaN
                    if (!isNaN(latitudePoint) && !isNaN(longitudePoint)) {
                        lapPointGps.push({x:latitudePoint, y:longitudePoint})
                    }
                })
            });

            // nettoyage des datas
            if (workoutFcMax == 0) {workoutFcMax=undefined}
            if (workoutMaximumSpeed == 0) {workoutMaximumSpeed=undefined}
            if (workoutDenivele == 0) {workoutDenivele=undefined} else {
                workoutDenivele = Math.floor(workoutDenivele) // clean data
            }

            // derniere étape pour le calcul de la fc moyenne
            if (workoutFcMoy == 0) {workoutFcMoy = undefined} else {
                workoutFcMoy = Math.round(workoutFcMoy/workoutTime) // rappel de la formule : (FC moy du lap * durée du lap en secondes) / durée totale de l'entrainement en secondes
            }

            // conversion des secondes en minutes pour la durée de l'entrainement
            workoutTime = workoutTime/60

            // arrondi des valeurs de distance et du vitesse max
            if (workoutDistance != 0 && workoutDistance != undefined) {workoutDistance = Number(workoutDistance.toFixed(2))} else {workoutDistance = undefined}
            if (workoutMaximumSpeed != 0 && workoutMaximumSpeed != undefined) {workoutMaximumSpeed = Number(workoutMaximumSpeed.toFixed(2))} else {workoutMaximumSpeed = undefined}

            // calcul de l'allure moyenne ou de la vitesse en fonction du sport
            let workoutAllureMoy = 0
            let workoutVitesseMoy = 0
            if (workoutSport != "Libre") {
                if (workoutSport == "Course" && workoutDistance > 0) {
                    // Calcul de l'allure en course à pied
                    workoutAllureMoy = workoutTime/workoutDistance // on obtient par exemple : 7.65

                    let min = Math.floor(workoutAllureMoy) // pour recup les minutes
                    let sec = Math.round((workoutAllureMoy%1)*60) // conversion du reste en seconde 
                    workoutAllureMoy = `${min}:${sec.toString().padStart(2, "0")}`

                } else if (workoutSport == "Vélo" && workoutDistance > 0) {
                    // conversion des min en heures
                    let workoutTimeHour = workoutTime/60
                    workoutVitesseMoy = Number((workoutDistance/workoutTimeHour).toFixed(2))

                }
            }
            if (workoutAllureMoy == 0) {workoutAllureMoy = undefined}
            if (workoutVitesseMoy == 0) {workoutVitesseMoy = undefined}

// !!! à revoir !!!
            // calcul du RPE
            // formule ci dessous à améliorer parce qu'elle n'est pas prouvé scientifiquement
            let rpeWorkout = Math.round((workoutFcMoy/workoutFcMax)*10) || 1 // formule pour calculer le RPE : (FC moy / FC max) * 10
            if (rpeWorkout < 1) { // si inférieur à 1 on le met sur la valeur minimum (=1)
                rpeWorkout = 1
            } else if (rpeWorkout > 10) { // si supérieur à 10 on le met sur la valeur max (=10)
                rpeWorkout = 10
            }
            
            let coefRpe = {1:0.2, 2:0.4, 3:0.7, 4:1.1, 5:1.6, 6:2.3, 7:3.2, 8:4.5, 9:6.2, 10:8.5}
            let chargeEntrainementWorkout = Math.floor(coefRpe[rpeWorkout]*workoutTime)
// !!! fin de à revoir !!!

            // Calcul de la transpiration
            let profilDB = await db.profil.get(1)
            let transpirationEstimee = 0
            let hydratationEstimee = 0

            if (profilDB != undefined) {
                let poidsUser = Number(profilDB.poids)
                let dureeHeure = workoutTime/60 // Conversion de la durée en heure
                let coefficientRpe = [0.4, 0.8, 1.2, 1.6]

                // Attribution de la valeur du RPE
                if (rpeWorkout <= 3) {coefficientRpe = coefficientRpe[0]} 
                else if (rpeWorkout <= 6) {coefficientRpe = coefficientRpe[1]}
                else if (rpeWorkout <= 8) {coefficientRpe = coefficientRpe[2]}
                else {coefficientRpe = coefficientRpe[3]}

                // Calcul
                transpirationEstimee = Math.round((dureeHeure*coefficientRpe*(poidsUser/70))*1000)
                hydratationEstimee = Math.round(transpirationEstimee*1.2)
            } else {
                transpirationEstimee = undefined
                hydratationEstimee = undefined
            }

            // si la durée ou la date de l'entrainement n'est pas définie ou égale à 0 on enregistre rien
            if (workoutTime == 0 || new Date(workoutDate) == "Invalid Date") {
                alert("Une erreur s'est produite lors de l'importation de la séance. Veuillez vérifier que votre fichier TCX contient des valeurs valides.")
                button.disabled = false
                button.textContent = "Importer TCX"
                return
            }

            // dernier nettoyage au cas ou ya pas de datas gps dans le fichier GPX
            if (lapPointGps.length <= 0 || lapPointGps == undefined) {lapPointGps=undefined} else {
                // filtrage des points gps
                lapPointGps = simplify(lapPointGps, 0.00002, false) // pas de haute qualité pour gagner en perf, tolérence de 2 mètres
            }

            // enregistrement des datas recup dans la BDD 
            let dicoDataBase = {
                sport: workoutSport,
                nom: workoutSport+" le "+workoutDate.split("-")[2]+"/"+workoutDate.split("-")[1].padStart(2, "0"), // exemple : Course le 28/04
                date: workoutDate,
                duree: workoutTime,     
                rpe: rpeWorkout,
                fc_moy: workoutFcMoy,
                fc_max: workoutFcMax,
                
                distance:workoutDistance,

                charge_entrainement: chargeEntrainementWorkout,
                transpiration_estimee: transpirationEstimee,
                hydratation_estimee: hydratationEstimee,

                points_gps: lapPointGps
            }
            if (workoutSport != "Libre") {
                // ajout des datas spé à la couse et au vélo
                dicoDataBase["allure_moy"] = workoutAllureMoy
                dicoDataBase["vitesse_moy"] = workoutVitesseMoy
                dicoDataBase["vitesse_max"] = workoutMaximumSpeed
                dicoDataBase["denivele"] = workoutDenivele
            }
            const dicoDataClean = removeValueUndefined(dicoDataBase) // toutes les valeurs en undefined sont enlever du dico

            // on recup l'id direct au moment de l'enregistrement grâce à add qui renvoie l'id
            const idWorkout = await db.entrainement.add(dicoDataClean)

            button.textContent = "Importé"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
            window.location.href = `../../../entrainement/entrainement.html?workout=${idWorkout}` 
        } catch(error) {
            console.log(error)
            button.textContent = "Une erreur s'est produite"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            button.textContent = "Importer TCX"
            button.disabled = false
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const inputFileInvisible = document.getElementById("file-input-tcx") 
    if (inputFileInvisible) {inputFileInvisible.addEventListener("change", (event) => {uploadFileTCX(event)})}
    
    const inputFile = document.getElementById("button-import-tcx")
    if (inputFile) {inputFile.addEventListener("click", () => {document.getElementById('file-input-tcx').click()})}
})