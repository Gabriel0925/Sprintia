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

function PassageHeure(minutes) {
    let Heure = Math.floor(minutes/60) // Arrondi à l'entier inférieur
    let MinutesRestante = minutes-60*Heure

    // Initialisation
    let Result = ""
    if (Heure < 1) { // Si l'heure est inférieur à 1 on affiche que les minutes pour ne pas afficher 0h 23min
        Result = minutes + "min"
    } else { // Sinon on affiche tous
        Result = Heure + "h " + MinutesRestante.toString().padStart(1, "0") + "m"
    }
            
    return Result
}

// init pour le logo dynamique
let Timer1 = 0
let Timer2 = 0

function HTMLCard(CardWorkout, workout, DateEuropeen, DureeFormatee) {
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
                Duree : <strong>${DureeFormatee}</strong>
            </p>
            <p class="rpe-workout">
                RPE : <strong>${workout.rpe}</strong>
            </p>
        </div>
    `

    if (workout.sport == "Course" || workout.sport == "Vélo" || workout.sport == "Marche") {
        StructureHTML += `
            <div class="data-workout-paire">
                <p class="duree-workout">
                    Distance : <strong>${workout.distance.toString().replace(".", ",")} km</strong>
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

            // timeout remis a 0 (suppresion plutot)
            clearTimeout(Timer1)
            clearTimeout(Timer2)
            document.getElementById("a-logo").classList.remove("return", "pin-message")
            
            // petite récompense pour le user
            document.getElementById("a-logo").classList.add("pin-message")

            document.getElementById("a-logo").textContent = "Supprimé 🗑️";

            Timer1 = setTimeout(() => { 
                document.getElementById("a-logo").classList.add("return") // a ré-ajoute une class pour qu'il y est une animation de retour
                document.getElementById("a-logo").textContent = "Sprintia"; // on raffiche Sprintia
            }, 2500); // on laisse le message pendant 2,5s pour que le user est le temps de le lire

            Timer2 = setTimeout(() => {
                // remise à l'état initial, on supprime les 2 class qu'on a mis dès la fin du setTimeout au dessus
                document.getElementById("a-logo").classList.remove("return")
                document.getElementById("a-logo").classList.remove("pin-message")
            }, 3100) // durée choisis à la main
        }
        
        const NbCardStatut = document.querySelectorAll(".cards-history-workout")
        if (NbCardStatut.length == 0) { // si il n'y a pas de card alors on remet le message comme quoi il faut ajouter des datas et on enleve le bouton afficher plus
            document.getElementById("text-informatif").style.display = "block"
            document.getElementById("button_afficher_plus").style.display = "none"
        }
    })

    BoutonModifier.addEventListener("click", async () => { // Ajout d'une "action" au bouton edit
        window.location.href = `ajouter_entraînement.html?edit=${workout.id}` // mettre un parametre dans l'URL
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
    if (HistoriqueComplet.length <= 12) {
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
        let DureeFormatee = PassageHeure(workout.duree)

        let CardWorkoutHTML = HTMLCard(CardWorkout, workout, DateEuropeen, DureeFormatee)
        ConteneurCardsWorkout.appendChild(CardWorkoutHTML)
    });

    // animation du dynamic logo pour féliciter le user
    const ParamURL = window.location.search
    const TableauSeparation = ParamURL.split("?")
    
    if (TableauSeparation.length > 1 && TableauSeparation[1] == "workoutregister") {
        // timeout remis a 0 (suppresion plutot)
        clearTimeout(Timer1)
        clearTimeout(Timer2)
        document.getElementById("a-logo").classList.remove("return", "pin-message")
        
        // petite récompense pour le user
        document.getElementById("a-logo").classList.add("pin-message")

        document.getElementById("a-logo").textContent = "Bien joué·e 🔥";

        Timer1 = setTimeout(() => { 
            document.getElementById("a-logo").classList.add("return") // a ré-ajoute une class pour qu'il y est une animation de retour
            document.getElementById("a-logo").textContent = "Sprintia"; // on raffiche Sprintia
        }, 2500); // on laisse le message pendant 2,5s pour que le user est le temps de le lire

        Timer2 = setTimeout(() => {
            // remise à l'état initial, on supprime les 2 class qu'on a mis dès la fin du setTimeout au dessus
            document.getElementById("a-logo").classList.remove("return")
            document.getElementById("a-logo").classList.remove("pin-message")
        }, 3100) // durée choisis à la main
    }

    return
}

window.addEventListener("DOMContentLoaded", async () => {
    await Init()
})