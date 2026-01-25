async function AfficherData() {
    // Recup de l'historique
    let HistoriqueDB = await db.entrainement.toArray() // recup de toutes les datas

    if (HistoriqueDB.length > 0) {
        document.getElementById("text-informatif").style.display = "none"
    }

    const ConteneurCardsWorkout = document.getElementById("liste-workouts")
    
    // Remise à 0 du conteneur
    ConteneurCardsWorkout.innerHTML = ""

    // Creation structure HTML
    HistoriqueDB.forEach(workout => {
        const CardWorkout = document.createElement("div")

        CardWorkout.classList.add("cards-history-workout")


        let StructureHTML = `          
            <div class="data-workout-column">
                <p class="name-workout">
                    ${workout.nom}
                </p>
                <p class="sport-date-workout">
                    ${workout.sport} · ${workout.date}
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

        if (workout.sport == "Course") {
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
        })

        BoutonModifier.addEventListener("click", async () => { // Ajout d'une "action" au bouton
            alert("Cette fonctionnalité sera disponible lors de futures betas.")
        })


        ConteneurCardsWorkout.appendChild(CardWorkout)

    });

    return
}

window.addEventListener("DOMContentLoaded", () => {
    AfficherData()
})