const BddNomData = { // sport avec les id correspondant aux champs de datas spécifique aux sports
    "id": ["id", ""],
    "sport": ["Sport", ""],
    "date": ["Date", ""],
    "nom": ["Nom", ""],
    "duree": ["Durée", ""],
    "rpe": ["RPE", "/10"],
    "fc_moy": ["FC moyenne", "bpm"],
    "fc_max": ["FC maximum", "bpm"],
    "distance": ["Distance", ["km", "m"]],
    "denivele": ["Dénivelé", "m"],
    "allure_moy": ["Allure moyenne", ["/km", "/500m", "/100m"]],
    "vitesse_moy": ["Vitesse moyenne", "km/h"],
    "vitesse_max": ["Vitesse maximum", "km/h"],
    "cadence_moy": ["Cadence moyenne", ["ppm", "tpm", "cpm"]], 
    "nb_pas": ["Pas", ""],
    "altitude_max": ["Altitude maximum", "m"],
    "nb_coups": ["Nombre de coups", ""],
    "nb_sets": ["Nombre de sets", ""],
    "vitesse_smash": ["Vitesse de smash", "km/h"],
    "nb_points": ["Nombre de points", ""],
    "nb_combats": ["Nombre de combats", ""],
    "nb_victoires": ["Nombre de victoires", ""],
    "nb_defaites": ["Nombre de défaites", ""],
    "nb_chutes": ["Nombre de chutes", ""],
    "score": ["Score", ""],
    "nb_services": ["Nombre de services", ""],
    "nb_smash": ["Nombre de smash", ""],
    "nb_reps": ["Nombre de reps", ""],
    "nb_series": ["Nombre de séries", ""],
    "poids_total": ["Poids total", "kg"],
    "coups_rame": ["Coups de rame", ""],
    "nb_longueurs": ["Nombre de longueurs", ""],
    "nb_positions": ["Nombre de positions", ""],
    "longueur_bassin": ["Longueur du bassin", "m"],
    "nb_tours": ["Nombre de tours", ""],
    "serie_max": ["Séries maximum", ""],
    "nb_descentes": ["Nombre de descentes", ""],
    "voies_effectuees": ["Voies effectuées", ""],
    "difficulte_max": ["Difficulté maximum", ""],
    "muscles_travailles": ["Muscles travaillés", ""],
    "charge_entrainement": ["Charge d'entraînement", "CE"],
    "transpiration_estimee": ["Transpiration estimée", "mL"],
    "hydratation_estimee": ["Réhydratation conseillée", "mL"]
}
let idWorkout = undefined

function carteGPS(data, latlngs) {
    let fullscreen = false
    let centerButtonContainer = null;
        // Récupération des couleurs
        const couleurTexte = getComputedStyle(document.documentElement).getPropertyValue('--COLOR_ACCENT').trim();

        // Affichage de la carte initiale
        const mapElement = document.getElementById('map');
        mapElement.className = 'map-normal';

        var map = L.map('map', {
            preferCanvas: true, // param pr améliorer les perf
            zoomControl: false,
            dragging: false, 
            scrollWheelZoom: false,
            doubleClickZoom: false, 
            touchZoom: false
        }).setView([17.387140, 78.491684], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: "&copy; <a href='http://osm.org/copyright' target='_blank'>OpenStreetMap</a> contributors",
            maxZoom: 22, // on limite le user sur le zoom
            maxNativeZoom: 19 // pr éviter que Leaflet fasse des requetes pour recharger la carte alors qu'il n'y a plus de carte à afficher
        }).addTo(map);

        // Définition du bouton "Centrer"
        let CenterTace = L.Control.extend({
            options: { position: 'topright' },
            onAdd: function(map) {
                var div = L.DomUtil.create('div', 'my-control');
                var iconInDiv = L.DomUtil.create("i", "icon_position", div)

                L.DomEvent.on(div, 'click', function(e) {
                    L.DomEvent.stopPropagation(e);
                    if (typeof polyline !== 'undefined') map.fitBounds(polyline.getBounds(), {padding: [30,30]});
                });

                // On mémorise le conteneur HTML et on le cache par défaut (mode normal)
                centerButtonContainer = div;
                centerButtonContainer.style.display = 'none';

                return div;
            }
        });

        // Définition du bouton "Plein écran / Quitter"
        let BouttonFullscreen = L.Control.extend({  
            options: { position: 'topright' },
            
            onAdd: function(map) {
                var div = L.DomUtil.create('div', 'my-control');
                var iconInDiv = L.DomUtil.create("i", "icon_fullscreen", div)
                iconInDiv.id = 'btn-fullscreen'

                L.DomEvent.on(div, 'click', function(e) {
                    L.DomEvent.stopPropagation(e); 

                    if (fullscreen == false) {
                        mapElement.className = 'map-fullscreen';
                        
                        map.dragging.enable();    
                        map.scrollWheelZoom.enable();
                        map.doubleClickZoom.enable();
                        map.touchZoom.enable();
                        
                        iconInDiv.classList.remove("icon_fullscreen")
                        iconInDiv.classList.add("icon_fullscreen_exit")
                        fullscreen = true;

                        // AFFICHE le bouton Centrer
                        if (centerButtonContainer) centerButtonContainer.style.display = 'block';

                        setTimeout(() => { 
                            map.invalidateSize(); 
                            if (typeof polyline !== 'undefined') map.fitBounds(polyline.getBounds(), {padding: [30,30]});
                        }, 50);
                    }
                    else {
                        mapElement.className = 'map-normal';

                        map.dragging.disable();
                        map.scrollWheelZoom.disable();
                        map.doubleClickZoom.disable();
                        map.touchZoom.disable()
                        
                        iconInDiv.classList.remove("icon_fullscreen_exit")
                        iconInDiv.classList.add("icon_fullscreen")
                        fullscreen = false;

                        // CACHE le bouton Centrer
                        if (centerButtonContainer) centerButtonContainer.style.display = 'none';

                        setTimeout(() => { 
                            mapElement.removeAttribute('style'); 
                            map.invalidateSize(); 
                            if (typeof polyline !== 'undefined') map.fitBounds(polyline.getBounds(), {padding: [30,30]});
                        }, 60); 
                    }
                }, this);
                return div;
            }
        });

        map.on('click', function(e) {
            if (fullscreen == false && !e.originalEvent.target.closest('.my-button-class')) {
                mapElement.className = 'map-fullscreen';
                
                const monBouton = document.getElementById('btn-fullscreen');
                monBouton.classList.remove("icon_fullscreen")
                monBouton.classList.add("icon_fullscreen_exit")
                
                map.dragging.enable();           
                map.scrollWheelZoom.enable();    
                map.doubleClickZoom.enable();

                fullscreen = true;

                // AFFICHE le bouton Centrer lors du clic global
                if (centerButtonContainer) centerButtonContainer.style.display = 'block';

                setTimeout(() => { 
                    map.invalidateSize(); 
                    if (typeof polyline !== 'undefined') map.fitBounds(polyline.getBounds(), {padding: [30,30]});
                }, 50);
            }
        });

        let ControlBoutonExitMap = new BouttonFullscreen().addTo(map);
        let ControlCenterTace = new CenterTace().addTo(map);

        // Traçage du relevé gps
        var polyline = L.polyline(latlngs, { color: couleurTexte }).addTo(map);

        // Markers d'arrivée et de fin de la trace
        L.marker(latlngs[0], { title: 'start' }).addTo(map);
        L.marker(latlngs[latlngs.length - 1], { title: 'stop' }).addTo(map);

        // Zoom initial sur le tracé
        map.fitBounds(polyline.getBounds(), {padding: [30,30]});
}

function afficherData(dataWorkout) {
    const dicoDescriptionRPE = {
        1:["Facile", "#1fff80"], 2:["Facile", "#1fff80"], 3:["Facile", "#1fff80"],
        4:["Modéré", "#e7e625"], 5:["Modéré", "#e7e625"], 6:["Modéré", "#e7e625"],
        7:["Difficile", "#ff4b4c"], 8:["Difficile", "#ff4b4c"],
        9:["Effort maximal", "#9386f1"], 10:["Effort maximal", "#9386f1"]
    }

    // ajout des datas aux éléments existant
    document.getElementById("nom-workout").textContent = dataWorkout.nom
    document.querySelector(".detail-entrainement").innerHTML = `<strong>${dataWorkout.sport}</strong><br>${formatEuropeenDate(dataWorkout.date)}`

    document.getElementById("duree").innerHTML = dureeFormatee(dataWorkout.duree)
    document.getElementById("charge").innerHTML = dataWorkout.charge_entrainement + "<small>CE</small>"

    document.getElementById("value-rpe").innerHTML = dataWorkout.rpe
    document.getElementById("value-rpe").style.background = dicoDescriptionRPE[dataWorkout.rpe][1]
    document.getElementById("description-rpe").innerHTML = dicoDescriptionRPE[dataWorkout.rpe][0]
    document.getElementById("description-rpe").style.color = dicoDescriptionRPE[dataWorkout.rpe][1]

    // Structure de base de la page entrainement
    let structureHTML = `<section class="container-block">`

    // initialisation de 2 tableaux
    const tableauDataNotDisplay = ["id", "Nom", "Sport", "Date", "Durée", "RPE", "Charge d'entraînement", "Transpiration estimée", "Réhydratation conseillée"]
    const tableauDataSeule = ["Muscles travaillés", "Score", "Voies effectuées"]
    let sixSeven = false
    let latlngs = null;

    // on parcourt les datas de l'entraînement (c un dico donc on recup la cle et la valeur)
    Object.entries(dataWorkout).forEach(([cle, valeur]) => {
        if (cle=="note" || cle=="points_gps") { // les points gps on les affiche sur la carte
            if (cle == "points_gps") {
                // on recup les points x et y du dico pointsGPS enregistré dans la bdd, on le met dans un tableau
                latlngs = valeur.map(pointGPS => [pointGPS.x, pointGPS.y])
            } 
            // si c'est la note on ne fais rien on le fera plus tard
        } else {
            const nomUniteData = BddNomData[cle] // on récupère le nom et l'unité de la data 
            const nomData = nomUniteData[0] // on récupère le nom de la data ex: muscles_travailles => Muscles travaillés

            let typeValeur = typeof(valeur) // on recup le type de la valeur
            if (typeValeur == "number") { // si c'est un number alors
                valeur = Number(valeur) // on convertit en nombre
                if (isNaN(valeur)) { // et si la valeur est NaN (=quand le user met rien dans le champs lors de l'enregistrement de datas)
                    valeur = null // on met sur null pour que la condition ci-dessous n'affiche pas cette data
                }
                if (valeur != null && valeur == 67) {sixSeven=true}
            }
            
            // initialisation
            let uniteData = ""
            if (cle == "cadence_moy") { // si la datas c'est cadence moy on prend ppm ou tpm ou cpm en fonction du sport
                if (dataWorkout.sport == "Course") {
                    uniteData = nomUniteData[1][0] // on récupère l'unité de la data  => ppm
                } else if (dataWorkout.sport == "Vélo" || dataWorkout.sport == "Corde à sauter") {
                    uniteData = nomUniteData[1][1] // on récupère l'unité de la data => tpm
                } else { // si c'est du rameur, aviron,...
                    uniteData = nomUniteData[1][2] // on récupère l'unité de la data => cpm
                }

            } else if (cle == "distance") {
                if (dataWorkout.sport == "Natation" || dataWorkout.sport == "Rameur d'intérieur" || dataWorkout.sport == "Aviron" || dataWorkout.sport == "Paddle") {
                    uniteData = nomUniteData[1][1] // on récupère l'unité de la data  => m
                    if (valeur != null) { // on passe des kilomètres en metres
                        valeur = Number(valeur) // on convertit en nombre pour etre sur
                        valeur = valeur*1000
                        valeur= valeur.toFixed(1).toString().replace(".", ",")
                    }
                } else {
                    uniteData = nomUniteData[1][0] // on récupère l'unité de la data  => km
                    if (valeur != null) { // on passe des kilomètres en metres
                        valeur = Number(valeur) // on convertit en nombre pour etre sur
                        valeur = valeur.toFixed(2).toString().replace(".", ",")
                    }
                }

            } else if (cle == "allure_moy") {
                if (dataWorkout.sport == "Natation") {
                    uniteData = nomUniteData[1][2] // on récupère l'unité de la data  => /100m 
                } else if (dataWorkout.sport == "Rameur d'intérieur" || dataWorkout.sport == "Aviron" || dataWorkout.sport == "Paddle") {
                    uniteData = nomUniteData[1][1] // on récupère l'unité de la data  => /500m 
                } else {
                    uniteData = nomUniteData[1][0] // on récupère l'unité de la data  => /km 
                }

            } else if (cle=="vitesse_max" || cle=="vitesse_moy" || cle=="poids_total") {
                uniteData = nomUniteData[1]
                if (valeur!=null) {
                    valeur = Number(valeur).toFixed(2).toString().replace(".", ",")
                } 

            } else {
                uniteData = nomUniteData[1] // on récupère l'unité de la data ex: distance => km
            }

            if (valeur != null || valeur != undefined) { // si il y a une datas en undefined ou null alors on n'affiche pas cette datas
                // on regarde si le nom de la data n'est pas dans le tableau car le nom, la date, le sport est dans la structure de base de la page html
                if (tableauDataNotDisplay.includes(nomData)) { 
                    // pass
                } else {
                    if (tableauDataSeule.includes(nomData)) { // on check si c'est une data qu'on doit afficher seul ou pas 
                        //si il y a que une seule data  dans l'entraînement alors on met direct dans le container data qu'on a crée au tout début
                        // je sais pas comment le faire ??!! 



                        // on referme d'abord la section container-block on la rouvre puis on la referme
                        structureHTML += `</section>

                            <section class="container-block">
                                <div class="container-block-data">
                                    <p class="container-block-data-header">${nomData}</p>
                                    <p class="container-block-data-data">${valeur} <small>${uniteData}</small></p>
                                </div>
                            </section>

                            <section class="container-block">`

                    } else {
                        // si c'est un data normal alors on met la div correspondante
                        structureHTML += `
                            <div class="container-block-data">
                                <p class="container-block-data-header">${nomData}</p>
                                <p class="container-block-data-data">${valeur} <small>${uniteData}</small></p>
                            </div>
                        `
                    }
                }

            }
        }

    });

    structureHTML += `</section>` // on referme

    // nettoyage de la page pour les container-data-block vide, par exemple quand on remplit uniquement le champs "Muscles travaillés" et qu'il n'y a pas de data de FC
    structureHTML = structureHTML.replaceAll(`<section class="container-block"></section>`, "")

    // on ajoute au conteneur
    document.querySelector(".page-entrainement").innerHTML = structureHTML

    // on affiche iniquement si il y a des relevées gps
    if (latlngs != null) {
        carteGPS(dataWorkout, latlngs)
    } else {
        document.getElementById("map").style.display = "none"
    }

    // si il n'y a pas de stats détaillé
    if (document.querySelector(".page-entrainement").innerHTML == `<section class="container-block"></section>` ||
        document.querySelector(".page-entrainement").innerHTML == ``) {
        document.getElementById("title-stats-detaillees").style.display = "none"
        document.querySelector(".page-entrainement").style.display = "none"
        document.querySelector("button.briefing").style.setProperty("margin-top", "var(--SPACE_L)")
    }

    // réhydratation conseillée
    if (dataWorkout.hydratation_estimee && dataWorkout.hydratation_estimee != undefined) {
        document.getElementById("rehydratation").innerHTML = dataWorkout.hydratation_estimee + " <small>mL</small>"
    }
    // transpiration estimée
    if (dataWorkout.hydratation_estimee && dataWorkout.hydratation_estimee != undefined) {
        document.getElementById("transpiration").innerHTML = dataWorkout.transpiration_estimee + " <small>mL</small>"
    }

    // on remplit le champs note entrainement si il y a du contenu dans la BDD
    if (dataWorkout.note != undefined && dataWorkout.note) {
        if (document.getElementById("note-entrainement")) { // on check si il y a un champs note sur la page
            document.getElementById("note-entrainement").value = dataWorkout.note
        }
    }

    if (sixSeven==true) {logoDynamique("SIX-SEVEN")}

    return
}

function apparitionButton() {
    // on recup et affiche le bouton sauvegarder
    let buttonSave = document.getElementById("button-sauvegarder-note-workout")
    buttonSave.style.display = "block"
}

async function saveDescription() {
    let noteWorkout = document.getElementById("note-entrainement").value.trim()
    let buttonSave = document.getElementById("button-sauvegarder-note-workout")

    // message au user
    buttonSave.disabled = true
    buttonSave.textContent = "Sauvegarde..."
    
    // ne pas faire put sinon ça remplace update va rajouter cette data
    await db.entrainement.update(idWorkout, {
        note:noteWorkout
    })

    buttonSave.textContent = "Sauvegardé"
    await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))

    buttonSave.disabled = false
    buttonSave.textContent = "Sauvegarder la note"
    buttonSave.style.display = "none"

    return
}

async function dicoWithoutID(dico) {
    return dico.map((workout) =>{
        // on sépare l'id du reste des données de l'entrainement
        const {id, ...autreStats} = workout
        return autreStats
    })
}
async function exporterData(dataWorkout) {
    let button = document.getElementById("button-partager-entrainement")
    
    if (dataWorkout) {
        button.innerHTML = "<i class='icon_partage'></i> En cours..."
        button.disabled = true

        try {
            // on enleve l'id du dico
            dataWorkout = await dicoWithoutID([dataWorkout]) // on met le dico dans un tableau car notre fonction est adapté pour les tableau pr use map
            
            // !!! ATTENTION désormais dataWorkout c'est un tableau plus un dico !!!

            // transformation en texte JSON
            const transformationTextJSON = JSON.stringify(dataWorkout[0], null, 2)
            
            // on clean le titre du fichier et on enleve les signes interdit pour un nom de fichier
            let nameFile = dataWorkout[0].nom
                                .replaceAll(" ", "-")
                                .replaceAll("/", "")
                                .replaceAll('\\', "") // on met 2 "\\" car si on met 1 "\" ça va bugger pour régler le probleme (d'après Gemini) il faut en mettre 2
                                .replaceAll(":", "")
                                .replaceAll("*", "")
                                .replaceAll("?", "")
                                .replaceAll('"', "")
                                .replaceAll("<", "")
                                .replaceAll(">", "")
                                .replaceAll("|", "") + "-SPRINTIA.text"

            let fileWorkoutData = new File([transformationTextJSON], nameFile, {type: "text/plain"}) // on crée le fichier (txt) car le navigateur bloque les fichiers JSON

            // on vérifie si le navigateur est compatible avec navigator.share et on vérifie aussi si il sait partager un fichier
            if (navigator.canShare && navigator.canShare({files: [fileWorkoutData]})) {
                await navigator.share({files:[fileWorkoutData], // on met dans un tableau car navigator.share peut permettre d'envoyer plusieurs fichier [fichier1, fichier2,...]
                    title:"Sauvegarde SPRINTIA"})            
                
                button.innerHTML = "<i class='icon_partage'></i> Partagé"
            } else {
                alert("Votre navigateur est incompatible avec le partage de fichier !")
            }
            
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))

        } catch(error) {
            if (error.name== "AbortError") { // ça veut dire que le user à fermer le menu de partage sans envoyer le fichier
                button.innerHTML = "<i class='icon_partage'></i> Annulé"
            } else {
                console.log(error) // affichage de l'erreur en console
                button.innerHTML = "<i class='icon_partage'></i> Erreur !"
            }
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            button.innerHTML = "<i class='icon_partage'></i> Partager l'entraî."
            button.disabled = false 
        }
    }
}

async function initialisation() {
    // ?workout=id
    const settingURL = window.location.search // recup des parametres de l'URL de la page 

    if (settingURL) { // on vérifie qu'il y a un setting avant de faire un split
        const tableauSeparation = settingURL.split("=") // ["?workout", "id"]
        
        if (tableauSeparation.length == 2) { // vérification pour éviter d'essayer de prendre l'index 1 alors qu'il y a que l'index 0 ou alors qu'il 5 index
            idWorkout = parseInt(tableauSeparation[1]) // on recup l'id

            // recup des datas de l'entraînement
            if (idWorkout != undefined) {
                let dataWorkout = await db.entrainement.get(idWorkout) // ça renvoie un dico avec toutes les datas date, durée,...
            
                if (dataWorkout == null) { // si il n'y a pas d'entrainement avec l'id dans l'URL alors on renvoie à la page historique dentrainement pour éviter d'afficher une page vide
                    location.href = "../index.html"
                    return
                }

                // ajout de la structure html
                afficherData(dataWorkout)

                // on donne un role au bouton
                let buttonPartageWorkout = document.getElementById("button-partager-entrainement")
                let buttonModifier = document.getElementById("button-modifier")
                let buttonSupprimer = document.getElementById("button-supprimer")

                buttonSupprimer.addEventListener("click", async () => { // Ajout d'une "action" au bouton
                    // Demande de confirmation avant
                    if (confirm(`Supprimer l'entraînement "${dataWorkout.nom}" ?`)) {
                        await db.entrainement.delete(dataWorkout.id) // supprimer la data de la bdd
                        // retour à l'historique d'entraînement
                        window.location.href = `../index.html`       
                    }
                })

                buttonModifier.addEventListener("click", async () => { // Ajout d'une "action" au bouton edit
                    window.location.href = `ajouter-entrainement.html?edit=${dataWorkout.id}` // mettre un parametre dans l'URL
                })
                buttonPartageWorkout.addEventListener("click", async () => {
                    await exporterData(dataWorkout)
                })
            }
            
        }
    }
    else { // si il y a pas de parametres dans l'URL on renvoie vers l'historique pour éviter d'afficher une page vide
        location.href = "../index.html"
    }
    
    return
}

document.addEventListener("DOMContentLoaded", () => {
    const buttonBriefing = document.getElementById("briefing_entrainement")
    if (buttonBriefing) {buttonBriefing.addEventListener("click", () => {windowsBriefing("Approfondir l'analyse")})}

    const infoRehydratation = document.getElementById("rehydratation")
    if (infoRehydratation) {
        infoRehydratation.addEventListener("click", function() {
            if (infoRehydratation.textContent == '-- mL') {
                alert('Pour obtenir une estimation de réhydratation conseillée veuillez configurer votre profil.')
            }
        })
    }
    const infoTranspiration = document.getElementById("transpiration")
    if (infoTranspiration) {
        infoTranspiration.addEventListener("click", function() {
            if (infoTranspiration.textContent == '-- mL') {
                alert('Pour obtenir une estimation de votre transpiration veuillez configurer votre profil.')
            }
        })
    }

    const noteEntrainement = document.getElementById("note-entrainement")
    if (noteEntrainement) {noteEntrainement.addEventListener("click", apparitionButton)}

    const buttonSaveNoteWorkout = document.getElementById("button-sauvegarder-note-workout")
    if (buttonSaveNoteWorkout) {buttonSaveNoteWorkout.addEventListener("click", saveDescription)}

    initialisation()
}) 