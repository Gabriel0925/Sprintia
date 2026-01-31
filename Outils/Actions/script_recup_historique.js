// Init for function Afficher data
let NbCardsWorkoutAfficher = 0
let HistoriqueComplet = []

async function Init() {
    // Recup de l'historique
    let HistoriqueDB = await db.entrainement.toArray() // recup de toutes les datas
    // Trier par date 
    HistoriqueDB.sort((element1, element2) => { // En js on peut comparer 2 dates comme des maths
        if (element1.date < element2.date) return 1
        if (element1.date > element2.date) return -1
    })

    SauvegardeHistorique(HistoriqueDB)
    return
}

function ReturnDate(DateWorkout) {
    let DateEuropeen = ""

    DateWorkout = DateWorkout.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = DateWorkout[2] + "-" + DateWorkout[1] + "-" + DateWorkout[0]
    return DateEuropeen
}

function HTMLCard(CardWorkout, workout, DateEuropeen) {
    let StructureHTML = `          
        <div class="data-workout-column">
            <p class="name-workout">
                ${workout.nom}
            </p>
            <p class="sport-date-workout">
                ${workout.sport} · ${DateEuropeen}
            </p>
            <p class="charge-workout">
                Charge d'entraînement : <strong>${workout.charge_entrainement}</strong>
            </p>
        </div>
        <div class="data-workout-paire">
            <p class="duree-workout">
                Duree : <strong>${workout.duree} min</strong>
            </p>
            <p class="rpe-workout">
                RPE : <strong>${workout.rpe}</strong>
            </p>
        </div>
    `

    if (workout.sport == "Course" || workout.sport == "Velo" || workout.sport == "Marche") {
        StructureHTML += `
            <div class="data-workout-paire">
                <p class="duree-workout">
                    Distance : <strong>${workout.distance} km</strong>
                </p>
                <p class="rpe-workout">
                    Dénivelé : <strong>${workout.denivele} m</strong>
                </p>
            </div>
        `
    } else if (workout.sport == "Musculation") {
        StructureHTML += `
            <div class="data-workout-paire">
                <p class="muscles-workout">
                    ${workout.muscles_travailles}
                </p>
            </div>
        `
    }

    StructureHTML += `
        <div class="action-button-card-workout">
            <button>
                <i class="fs-icon_modifier"></i>
                Modifier
            </button>
            <button>
                <i class="fs-icon_supprimer"></i>
                Supprimer
            </button>
        </div>
    `

    CardWorkout.innerHTML = StructureHTML

    let BoutonSupprimer = CardWorkout.querySelector(".fs-icon_supprimer").parentElement // parent element pour ne pas prendre que l'icone
    let BoutonModifier = CardWorkout.querySelector(".fs-icon_modifier").parentElement 
                
    // Ajout de la logique pour la suppresion
    BoutonSupprimer.addEventListener("click", async () => { // Ajout d'une "action" au bouton
       // Demande de confirmation avant
        if (confirm(`Supprimer l'entraînement "${workout.nom}" ?`)) {
            await db.entrainement.delete(workout.id) // supprimer la data de la bdd
            CardWorkout.remove() // supprimer la ligne
        }
        location.reload()
    })

    BoutonModifier.addEventListener("click", async () => { // Ajout d'une "action" au bouton
        alert("Cette fonctionnalité sera disponible lors de futures betas.")
    })

    let CardWorkoutHTML = CardWorkout

    return CardWorkoutHTML
}

async function SauvegardeHistorique(HistoriqueDB) {
    HistoriqueDB.forEach(element => {
        HistoriqueComplet.push(element)
    });
    await AfficherData()
    return
}

async function AfficherData() {
    // Cacher le text comme quoi il n'y a pas dentrainement enregistrer
    if (HistoriqueComplet.length > 0) {
        document.getElementById("text-informatif").style.display = "none"
    } 
    // Cacher le bouton si il n'y a plus d'element a charger
    if (HistoriqueComplet.length <= NbCardsWorkoutAfficher) {
        document.getElementById("button_afficher_plus").style.display = "none"
    }

    const ConteneurCardsWorkout = document.getElementById("liste-workouts")

    // Coupage des datas pr le nb limite de cards
    let HistoriqueNecessaire = HistoriqueComplet.slice(NbCardsWorkoutAfficher, NbCardsWorkoutAfficher+12)
    NbCardsWorkoutAfficher += 12

    // Creation structure HTML
    HistoriqueNecessaire.forEach(workout => {
        const CardWorkout = document.createElement("div")

        CardWorkout.classList.add("cards-history-workout")

        // Inversion de la date de "2026-01-12" à "12-01-2026"
        let DateEuropeen = ReturnDate(workout.date)

        let CardWorkoutHTML = HTMLCard(CardWorkout, workout, DateEuropeen)
        ConteneurCardsWorkout.appendChild(CardWorkoutHTML)

    });

    return
}

window.addEventListener("DOMContentLoaded", async () => {
    await Init()
})