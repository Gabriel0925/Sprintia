async function uploadFileGPX(event) {
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

        // MARCHE
        "walking":"Marche",
        "walk":"Marche",
        "marche":"Marche",

        // RANDONNEE
        "hiking":"Randonnée",
        "hike":"Randonnée",
        "randonnée":"Randonnée",
        "randonnee":"Randonnée",

        // SPORT HIVER
        "skiing": "Ski",
        "ski": "Ski",
        "alpine_skiing": "Ski",
        "nordic_skiing": "Ski de fond",
        "snowboarding": "Snowboard",
        "snowboard": "Snowboard",

        // SPORT EAU
        "swimming":"Natation",
        "swim":"Natation",
        "natation":"Natation",
        "open_water_swimming":"Natation", // en eau libre
        "pool_swimming":"Natation", // en piscine
    }

    const fileGPX = event.target.files[0]
    let button = document.getElementById("button-import-gpx")

    if (fileGPX) {
        button.disabled = true
        button.textContent = "Importation..."

        try {
            let textFile = await fileGPX.text() // on récup le contenu du fichier en texte

            const gpx = new gpxParser() // création de l'objet de la bibliotheque gpxParser
            gpx.parse(textFile)

            // recup de la date
            const objetDate = new Date(gpx.metadata.time) // c'est un objet date JS
            const workoutDate = objetDate.toISOString().split("T")[0] // 2026-07-03

            // recup du sport
            const workoutSport = dicoNameSport[gpx.tracks[0]?.type?.toLowerCase().trim()] || "Libre" // renvoie running ou cycling

            // recup de la durée de l'entrainement
            const tracks=gpx.tracks[0]
            let workoutTimeMS = 0 // différence en ms

            // calcul de la durée de l'entrainement en parcourant tous les points GPS du fichier GPX
            for (let i=1; i<tracks.points.length; i++) {
                const pointTourPrecedent = tracks.points[i-1]
                const pointActuel= tracks.points[i]

                const differenceBetween2Points = new Date(pointActuel.time)- new Date(pointTourPrecedent.time)

                workoutTimeMS+=differenceBetween2Points
            }
            const workoutTime = workoutTimeMS/60000 // conversion des ms en min

            // recup des datas spé au sport
            const workoutDistance = Number(Number(gpx.tracks[0].distance.total/1000).toFixed(2)) // recup de la distance en m puis conversion en km
            let pointsGPS = gpx.tracks[0].points.map(point => ({x:point.lat, y:point.lon})) // on est obligé de mettre des parenthèses autour du dico pour pas que js crois que c'est du code à executer

            // Calcul du dénivelé car la lib gpxParser ne le fait pas correctement
            let workoutDenivele = 0
            const tolerance = 1.5 // tolérence de 1.5m pour le calcul du dénivelé
            let deniveleLastLap = undefined // on init la variable pour le calcul du dénivelé
            if (tracks.points.length > 0) {
                tracks.points.forEach(point => {
                    const altitudeNow = Number(point.ele ?? 0) // si ya pas d'altitude on met à 0

                    // si c'est le premier point on l'init
                    if (deniveleLastLap == undefined) {deniveleLastLap=altitudeNow}

                    if (altitudeNow-deniveleLastLap > tolerance) { // si la différence entre les deux points est supérieur à une hausse de 1.5m
                        workoutDenivele = workoutDenivele+(altitudeNow-deniveleLastLap)
                        deniveleLastLap = altitudeNow
                    } else if (altitudeNow-deniveleLastLap < -tolerance) { // si ça descend on met à jour le denivelé pour le tour suivant (-tolerance pour l'inverse de tolérence soit -1.5m)
                        deniveleLastLap = altitudeNow
                    }
                })
            }

            // nettoyage
            if (workoutDenivele == 0) {
                workoutDenivele = undefined
            } else {
                workoutDenivele = parseInt(workoutDenivele)
            }

            // calcul de l'allure moyenne ou de la vitesse en fonction du sport
            let workoutAllureMoy = 0
            let workoutVitesseMoy = 0
            if (workoutSport != "Libre") {
                if (workoutSport == "Course" || workoutSport == "Randonnée" || workoutSport == "Marche") {
                    if (workoutDistance > 0) {
                        // Calcul de l'allure en course à pied
                        workoutAllureMoy = workoutTime/workoutDistance // on obtient par exemple : 7.65

                        let min = Math.floor(workoutAllureMoy) // pour recup les minutes
                        let sec = Math.round((workoutAllureMoy%1)*60) // conversion du reste en seconde 
                        workoutAllureMoy = `${min}:${sec.toString().padStart(2, "0")}`
                    }
                } else if (workoutSport == "Vélo" || workoutSport == "Ski") { 
                    if (workoutDistance > 0) {
                        // conversion des min en heures
                        let workoutTimeHour = workoutTime/60
                        workoutVitesseMoy = Number((workoutDistance/workoutTimeHour).toFixed(2))
                    }
                }
            }
            if (workoutAllureMoy == 0) {workoutAllureMoy = undefined}
            if (workoutVitesseMoy == 0) {workoutVitesseMoy = undefined}

            // on essaye de recup la fc moy/max si les datas sont dans le fichier
            let workoutFcMoy = 0
            let workoutFcMax = 0
            let compteur = 0

            tracks.points.forEach(element => {
                let fcDuPoint = Number(element.extensions?.hr??undefined)

                // controle de la qualité des datas
                if (!isNaN(fcDuPoint)) { // !!! atention undefined en number -> NaN
                    if (fcDuPoint > workoutFcMax) { // pr trouver la fc max
                        workoutFcMax = fcDuPoint
                    }
                    // pr accumuler toutes les fc moy et diviser par la suite
                    workoutFcMoy += fcDuPoint
                    compteur += 1 // incré
                }
            });

            // calcul de la fc moy (somme de toutes les fc des tours/ nb tours)
            if (compteur > 0) {
                workoutFcMoy = Math.round(workoutFcMoy/compteur)
            }

// !!! à revoir !!!
            // calcul du RPE
            // formule ci dessous à améliorer parce qu'elle n'est pas prouvé scientifiquement
            let rpeWorkout = 1
            if (workoutFcMoy > 0 && workoutFcMax > 0) {// si ya des datas on calcule sinon on laisse à 1
                rpeWorkout = Math.round((workoutFcMoy/workoutFcMax)*10) || 1 // formule pour calculer le RPE : (FC moy / FC max) * 10
                if (rpeWorkout < 1) { // si inférieur à 1 on le met sur la valeur minimum (=1)
                    rpeWorkout = 1
                } else if (rpeWorkout > 10) { // si supérieur à 10 on le met sur la valeur max (=10)
                    rpeWorkout = 10
                }
            }
            let coefRpe = {1:0.2, 2:0.4, 3:0.7, 4:1.1, 5:1.6, 6:2.3, 7:3.2, 8:4.5, 9:6.2, 10:8.5}
            let chargeEntrainementWorkout = Math.floor(coefRpe[rpeWorkout]*workoutTime)
// !!! fin de à revoir !!!

            // on clean les datas fcMoy/max
            if (workoutFcMoy == 0) {workoutFcMoy=undefined}
            if (workoutFcMax == 0) {workoutFcMax=undefined}
            
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
                alert("Une erreur s'est produite lors de l'importation de la séance. Veuillez vérifier que votre fichier GPX contient des valeurs valides.")
                button.disabled = false
                button.textContent = "Importer GPX"
                return
            }

            // dernier nettoyage au cas ou ya pas de datas gps dans le fichier GPX
            if (pointsGPS.length <= 0 || pointsGPS == undefined) {pointsGPS=undefined} else {
                // filtrage des points gps
                pointsGPS = simplify(pointsGPS, 0.00002, false) // pas de haute qualité pour gagner en perf, tolérence de 2 mètres
            }

            // enregistrement des datas
            const dicoDatasWorkout = {
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

                points_gps:pointsGPS
            }
            if (workoutSport != "Libre") {
                dicoDatasWorkout["allure_moy"] = workoutAllureMoy
                dicoDatasWorkout["vitesse_moy"] = workoutVitesseMoy
                dicoDatasWorkout["denivele"] = workoutDenivele
            }

            const dicoDataClean = removeValueUndefined(dicoDatasWorkout) // toutes les valeurs en undefined sont enlever du dico

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
            button.textContent = "Importer GPX"
            button.disabled = false
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const inputFileInvisible = document.getElementById("file-input-gpx")
    if (inputFileInvisible) {inputFileInvisible.addEventListener("change", (event) => {uploadFileGPX(event)})}
    
    const inputFile = document.getElementById("button-import-gpx")
    if (inputFile) {inputFile.addEventListener("click", () => {document.getElementById('file-input-gpx').click()})}
})