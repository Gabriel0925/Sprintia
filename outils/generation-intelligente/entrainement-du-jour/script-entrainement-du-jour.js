const dicoSeances = {
    "course": {
        "facile": bddSeancesCourseFacile, 
        "modere": bddSeancesCourseModere, 
        "difficile": bddSeancesCourseDifficile, 
    },
    "velo": {
        "facile": bddSeancesVeloFacile, 
        "modere": bddSeancesVeloModere, 
        "difficile": bddSeancesVeloDifficile, 
    },
    "natation": {
        "facile": bddSeancesNatationFacile, 
        "modere": bddSeancesNatationModere, 
        "difficile": bddSeancesNatationDifficile, 
    }
}
let lastNbAleatoireGenerate = undefined

function selectItem(elt, nameComponent) {
    let lastSelected = document.querySelector(nameComponent+".selected")
    
    if (lastSelected) {
        lastSelected.classList.remove("selected")
        if (elt) {
            elt.classList.add("selected")
        }
    }   
}
function generateNbAleatoire(min, max) {
    let nbGenerate = Math.floor(Math.random() * (max - min + 1)) + min // formule via Gemini
    let compteur = 0

    while (nbGenerate === lastNbAleatoireGenerate) {
        nbGenerate = Math.floor(Math.random() * (max - min + 1)) + min // formule via Gemini

        if (compteur > 10) {break} // si plus de 10 tirage alors on sort de la boucle
        compteur+=1
    }

    return nbGenerate
}


function createUiEchauffement(instruction_echauffement, containerWorkoutGenerate) {
    // création des elt
    let sectionEchauffement = document.createElement("section")
    sectionEchauffement.classList.add("label-workout-day")
    let textEchauffement = document.createElement("p")
    textEchauffement.classList.add("text-label")
    let timeEchauffement = document.createElement("p")
    timeEchauffement.classList.add("instruction-label")

    // remplissage des elt
    textEchauffement.innerHTML = "Échauffement"
    timeEchauffement.innerHTML = instruction_echauffement["volume"][0] + " " + instruction_echauffement["volume"][1]

    // ajout sur la page
    containerWorkoutGenerate.appendChild(sectionEchauffement)
    sectionEchauffement.appendChild(textEchauffement)
    sectionEchauffement.appendChild(timeEchauffement)
}
function createUiRetourAuCalme(instruction_retour_au_calme, containerWorkoutGenerate) {
    // création des elt
    let sectionRetourAuCalme = document.createElement("section")
    sectionRetourAuCalme.classList.add("label-workout-day")
    sectionRetourAuCalme.classList.add("without-border")
    let textRetourAuCalme = document.createElement("p")
    textRetourAuCalme.classList.add("text-label")
    let timeRetourAuCalme = document.createElement("p")
    timeRetourAuCalme.classList.add("instruction-label")

    // remplissage des elt
    textRetourAuCalme.innerHTML = "Retour au calme"
    timeRetourAuCalme.innerHTML = instruction_retour_au_calme["volume"][0] + " " + instruction_retour_au_calme["volume"][1]

    // ajout sur la page
    containerWorkoutGenerate.appendChild(sectionRetourAuCalme)
    sectionRetourAuCalme.appendChild(textRetourAuCalme)
    sectionRetourAuCalme.appendChild(timeRetourAuCalme)
}
function createUiFractionne(instruction_fractionne, containerWorkoutGenerate) {
    if (instruction_fractionne["plusieurs_blocs"] == true) {
        let structure_blocs = instruction_fractionne["structure_blocs"]

        structure_blocs.forEach(element => {
            if (element["type"] == "recuperation") { // phase de récup entre les blocs
                createUiRecuperation(element, containerWorkoutGenerate) //appelle à la fonction qui va créer l'interface
            } else { // la phase d'effort
                // création des elt
                let sectionFractionne = document.createElement("section")
                sectionFractionne.classList.add("fractionne-workout-day")
                let paragrapheRepetition = document.createElement("p")
                paragrapheRepetition.classList.add("nb-repetitions")
                let divRepetition = document.createElement("div")
                divRepetition.classList.add("container-structure")
                let paragrapheDureeRep = document.createElement("p")
                paragrapheDureeRep.classList.add("duree-repetition")
                let paragrapheDureeRecup = document.createElement("p")
                paragrapheDureeRecup.classList.add("duree-recuperation")

                // remplissage des elt
                paragrapheRepetition.innerHTML = "Répéter <strong>" + element["nombre_repetitions"] + "</strong> fois"
                paragrapheDureeRep.innerHTML = element["volume_effort"][0] + " " + element["volume_effort"][1] + " (effort)"
                paragrapheDureeRecup.innerHTML = element["volume_recuperation"][0] + " " + element["volume_recuperation"][1] + " (récupération)"

                // ajout sur la page
                containerWorkoutGenerate.appendChild(sectionFractionne)
                sectionFractionne.appendChild(paragrapheRepetition)
                sectionFractionne.appendChild(divRepetition)
                divRepetition.appendChild(paragrapheDureeRep)
                divRepetition.appendChild(paragrapheDureeRecup)
            }
        });

    } else if (instruction_fractionne["plusieurs_blocs"] == false) {
        // création des elt
        let sectionFractionne = document.createElement("section")
        sectionFractionne.classList.add("fractionne-workout-day")
        let paragrapheRepetition = document.createElement("p")
        paragrapheRepetition.classList.add("nb-repetitions")
        let divRepetition = document.createElement("div")
        divRepetition.classList.add("container-structure")
        let paragrapheDureeRep = document.createElement("p")
        paragrapheDureeRep.classList.add("duree-repetition")
        let paragrapheDureeRecup = document.createElement("p")
        paragrapheDureeRecup.classList.add("duree-recuperation")

        // remplissage des elt
        paragrapheRepetition.innerHTML = "Répéter " + instruction_fractionne["nombre_repetitions"] + " fois"
        paragrapheDureeRep.innerHTML = instruction_fractionne["volume_effort"][0] + " " + instruction_fractionne["volume_effort"][1] + " (effort)"
        paragrapheDureeRecup.innerHTML = instruction_fractionne["volume_recuperation"][0] + " " + instruction_fractionne["volume_recuperation"][1] + " (récupération)"

        // ajout sur la page
        containerWorkoutGenerate.appendChild(sectionFractionne)
        sectionFractionne.appendChild(paragrapheRepetition)
        sectionFractionne.appendChild(divRepetition)
        divRepetition.appendChild(paragrapheDureeRep)
        divRepetition.appendChild(paragrapheDureeRecup)
    }
}
function createUiEffort(instruction_repetition, containerWorkoutGenerate) {
    // création des elt
    let sectionEffort = document.createElement("section")
    sectionEffort.classList.add("label-workout-day")
    let textEffort = document.createElement("p")
    textEffort.classList.add("text-label")
    textEffort.classList.add("phase-effort")
    let timeEffort = document.createElement("p")
    timeEffort.classList.add("instruction-label")
    timeEffort.classList.add("phase-effort")

    // remplissage des elt
    textEffort.innerHTML = "Effort"
    timeEffort.innerHTML = instruction_repetition["volume_effort"][0] + " " + instruction_repetition["volume_effort"][1]

    // ajout sur la page
    containerWorkoutGenerate.appendChild(sectionEffort)
    sectionEffort.appendChild(textEffort)
    sectionEffort.appendChild(timeEffort)
}
function createUiRecuperation(instruction_recuperation, containerWorkoutGenerate) {
    // création des elt
    let sectionRecuperation = document.createElement("section")
    sectionRecuperation.classList.add("label-workout-day")
    let textRecuperation = document.createElement("p")
    textRecuperation.classList.add("text-label")
    textRecuperation.classList.add("phase-recuperation")
    let timeRecuperation = document.createElement("p")
    timeRecuperation.classList.add("instruction-label")
    timeRecuperation.classList.add("phase-recuperation")

    // remplissage des elt
    textRecuperation.innerHTML = "Récupération"
    timeRecuperation.innerHTML = instruction_recuperation["volume_recuperation"][0] + " " + instruction_recuperation["volume_recuperation"][1]

    // ajout sur la page
    containerWorkoutGenerate.appendChild(sectionRecuperation)
    sectionRecuperation.appendChild(textRecuperation)
    sectionRecuperation.appendChild(timeRecuperation)
}

function interfaceWorkout(selectedWorkout) {
    // on supprime le contenu actuelle de la page grâce au container et aussi au balise h1,...
    let lastContainerStructureWorkout = document.querySelector(".container-workout-generate")
    if (lastContainerStructureWorkout) {
        lastContainerStructureWorkout.remove()
    }
    document.querySelector("h1").innerHTML = ""
    if (document.querySelectorAll("h2").length > 0) { // si il y a des h2 on les supprime
        document.querySelectorAll("h2").forEach(elt => {
            elt.remove()
        })
    }
    // on fait pareil pour les p avec la classe "text"
    if (document.querySelectorAll("p.text").length > 0) {
        document.querySelectorAll("p.text").forEach(elt => {
            elt.remove()
        })
    }

    // création d'un conteneur globale pour la structure de l'entrainement
    let containerWorkoutGenerate = document.createElement("section")
    containerWorkoutGenerate.classList.add("container-workout-generate")
    document.body.appendChild(containerWorkoutGenerate)
    
    // ajout du titre et de la description de l'entrainement
    document.querySelector("h1").innerHTML = selectedWorkout["title"]
    let descriptionWorkout = document.createElement("p")
    descriptionWorkout.classList.add("text")
    descriptionWorkout.innerHTML = selectedWorkout["description"]
    containerWorkoutGenerate.appendChild(descriptionWorkout)
    
    // ajout d'un h2 pour structurer la page
    let titleH2 = document.createElement("h2")
    titleH2.textContent = "Résumé de l'entraînement"
    containerWorkoutGenerate.appendChild(titleH2)

    // ajout des données de base de l'entrainement : durée + charge d'entraînement
    let structureHTML = `
        <section class="container-block">

                <div class="container-block-data">
                    <p class="container-block-data-header">Durée</p>
                    <p class="container-block-data-data">${selectedWorkout["informations"]["duree_totale"]}</p>
                </div>
                <div class="container-block-data">
                    <p class="container-block-data-header">RPE</p>
                    <p class="container-block-data-data">${selectedWorkout["informations"]["rpe"]} <small>/10</small></p>
                </div>
                <div class="container-block-data">
                    <p class="container-block-data-header">Charge d'entraînement</p>
                    <p class="container-block-data-data">~ ${selectedWorkout["informations"]["charge_entrainement"]} <small>CE</small></p>
                </div>

        </section>
    `
    containerWorkoutGenerate.innerHTML += structureHTML // ajout des datas de base dans le body html

    // ajout d'un h2 pour structurer la page
    let titleH2Num2 = document.createElement("h2")
    titleH2Num2.textContent = "Structure de l'entraînement"

    // changement des marges pour avoir un bon équillibre dans la page
    titleH2Num2.style.margin = 0
    titleH2Num2.style.marginTop = "var(--SPACE_M)"
    titleH2Num2.style.marginBottom = "var(--SPACE_S_SMALL)"
    containerWorkoutGenerate.appendChild(titleH2Num2)

    let structureWorkout = selectedWorkout["structure"]
    const dicoFunctionUI = { // chaque fonction a pour but de créer l'interface
        "echauffement": createUiEchauffement,
        "fractionne": createUiFractionne,
        "effort": createUiEffort,
        "recuperation": createUiRecuperation,
        "retour_au_calme": createUiRetourAuCalme,
    }
    for (const eltWorkout in structureWorkout) { // eltWorkout c'est la clé du dico
        const dataForThisKey = structureWorkout[eltWorkout] // on cherche les bonnes datas dans le dico
        //console.log(eltWorkout, " / ", dataForThisKey)

        // on appelle la bonne fonction et on créer l'interface
        dicoFunctionUI[eltWorkout](dataForThisKey, containerWorkoutGenerate) // on lance la fonction avec les bons param
    }

    let containerCenterMarge = document.createElement("div")
    containerCenterMarge.classList.add("container-center-marge")

    let buttonCOROS = document.createElement("button") // bouton Open in COROS
    buttonCOROS.classList.add("size-block")
    buttonCOROS.innerHTML = "Ouvrir dans COROS"
    buttonCOROS.addEventListener("click", () => {
        window.open(selectedWorkout["lien"], '_blank')  
    })

    containerWorkoutGenerate.appendChild(containerCenterMarge)
    containerCenterMarge.appendChild(buttonCOROS)

    window.scrollTo({top:0, behavior: "smooth"}) // scroll vers le haut de la page

    // on rend visible le bouton flottant
    document.querySelector(".container-command").style.display = "block"
}


async function generationWorkout() {
    let button = document.getElementById("button-generation-entrainements")
    button.disabled = true
    button.textContent = "Génération..."

    try {
        const sportChoice = document.querySelector(".round-input-item.sport.selected").id
        const dureeChoice = document.querySelector(".round-input-item.duree.selected").id
        const intensityChoice = document.querySelector(".round-input-item.intensity.selected").id

        // on récupère le dico des séances en fonction du sport et de l'intensité (qui se trouve dans le fichier 'bdd-entrainement.js')
        const bddWorkout = dicoSeances[sportChoice][intensityChoice]
        // on recup le tableau des séances en fonction de la séances
        const tableauWorkout = bddWorkout[dureeChoice] // on trouve l'étendu des entraînements

        // on trouve un entrainement aléatoirement
        const nbAleatoire = generateNbAleatoire(0, tableauWorkout.length - 1)
        lastNbAleatoireGenerate = nbAleatoire
        const selectedWorkout =  tableauWorkout[nbAleatoire] // recup de l'entrainement tiré au sort avec la structure de l'entrainement et le lien vers COROS

        if (selectedWorkout) {
            // appelle à la fonction qui va générer l'interface
            interfaceWorkout(selectedWorkout)
        }
        
        // on enleve tout le contenu de la page
        document.querySelector(".container-item-workout-day").style.display = "none"
        document.querySelector(".container-center-marge").style.display = "none"

        window.scrollTo({top:0, behavior: "instant"}) // scroll vers le haut de la page

        button.textContent = "Généré"
        await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))        
        //window.location.href = ``
    } catch(error) {
        console.log(error)
        button.textContent = "Une erreur s'est produite"
        await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
    } finally {
        button.textContent = "Générer un entraînement"
        button.disabled = false
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let duree25 = document.getElementById("25")
    if (duree25) {duree25.addEventListener("click", function() {selectItem(duree25, '.round-input-item.duree')})}
    let duree50 = document.getElementById("50")
    if (duree50) {duree50.addEventListener("click", function() {selectItem(duree50, '.round-input-item.duree')})}
    
    let sportCourse = document.getElementById("course")
    if (sportCourse) {sportCourse.addEventListener("click", function() {selectItem(this, '.round-input-item.sport')})}
    let sportVelo = document.getElementById("velo")
    if (sportVelo) {sportVelo.addEventListener("click", function() {selectItem(this, '.round-input-item.sport')})}
    let sportNatation = document.getElementById("natation")
    if (sportNatation) {sportNatation.addEventListener("click", function() {selectItem(this, '.round-input-item.sport')})}
    
    let intensiterFacile = document.getElementById("facile")
    if (intensiterFacile) {intensiterFacile.addEventListener("click", function() {selectItem(this, '.round-input-item.intensity')})}
    let intensiterModere = document.getElementById("modere")
    if (intensiterModere) {intensiterModere.addEventListener("click", function() {selectItem(this, '.round-input-item.intensity')})}
    let intensiterDifficile = document.getElementById("difficile")
    if (intensiterDifficile) {intensiterDifficile.addEventListener("click", function() {selectItem(this, '.round-input-item.intensity')})}

    let iconRefreshToolbar = document.querySelector(".icon_refresh")
    if (iconRefreshToolbar) {
        iconRefreshToolbar.addEventListener("click", () => {
            if(confirm('En générant un nouvel entraînement, celui-ci ne sera plus accessible. Êtes-vous sûr de vouloir continuer ?')){
                generationWorkout()
            }
        })
    }
    
    let buttonGeneration = document.getElementById("button-generation-entrainements")
    if (buttonGeneration) {buttonGeneration.addEventListener("click", generationWorkout)}
})