function SelectionSport(value) { // Pr cacher les champs en fonction du sport choisi
    // Recup des champs + label des champs
    let ChampsDistance = document.getElementById("distance-entrainement-user")
    let ChampsDenivele = document.getElementById("denivele-entrainement-user")
    let ChampsMuscles = document.getElementById("muscle-entrainement-user")

    let LabelDistance = document.getElementById("invisible1")
    let LabelDenivele = document.getElementById("invisible2")
    let LabelMucles = document.getElementById("invisible3")

    // Adaptation des champs en fonction du sport
    if (value == "Libre") {
        ChampsDistance.style.display = "none"
        ChampsDenivele.style.display = "none"
        ChampsMuscles.style.display = "none"
        
        LabelDistance.style.display = "none"
        LabelDenivele.style.display = "none"
        LabelMucles.style.display = "none"

    } else if (value == "Course" || value == "Velo" || value == "Marche") {
        ChampsDistance.style.display = "block"
        ChampsDenivele.style.display = "block"
        ChampsMuscles.style.display = "none"
        
        LabelDistance.style.display = "block"
        LabelDenivele.style.display = "block"
        LabelMucles.style.display = "none"

    } else if (value == "Musculation") {
        ChampsDistance.style.display = "none"
        ChampsDenivele.style.display = "none"
        ChampsMuscles.style.display = "block"
        
        LabelDistance.style.display = "none"
        LabelDenivele.style.display = "none"
        LabelMucles.style.display = "block"
    }

    return
}

function GenererNbAleatoire() {
    // Nb aléatoire
    let NombreAleatoire = Math.random() // renvoie aléatoirement entre 0 et 1 (ex : 0.5890953759539541)
    NombreAleatoire = Math.floor(NombreAleatoire*10) //fois 10 et nb arrondi pour avoir par exemple 5.8 puis 5 grace a l'arrondi

    return NombreAleatoire
}

function JrmCoach() {
    // Recup du champs coach
    let SectionCoach = document.getElementById("reponse-coach")

    // Phrase JRM
    const CoachBienveillant = {
        0: [
            "Alors cette séance ? Tout s'est bien passé ?",
            "Bravo ! Vous avez assuré aujourd'hui ! J'espère que cette séance vous a fais du bien mentalement et physiquement.",
            "Une séance de plus, un pas de plus !",
            "La séance de sport était bonne ? Bonnes sensations ?",
            "Vous avez kiffé ou souffert ?",
            "Vous avez gagné votre dodo/votre repas ?",
            "Ça vous avez boosté ou vidé ?",
            "Vous venez de vous défouler ! Vous êtes content de votre séance ?",
            "Vous êtes content·e de votre séance ou vous êtes déçu·e ?",
            "Vous avez cru que vous alliez lâcher ?"
        ],
        1: [
            "Chaque effort compte. Ne lâchez rien ! La discipline est la clé des plus grands objectifs !",
            "Si vous voulez un conseil, la régularité est toujours meilleure que l'intensité. Il vaut mieux faire 3 petites séances qu'une grosse séance par semaine.",
            "Peu importe les chiffres, ce qui compte, c’est que vous ayez pris du temps pour faire votre sport !",
            "Top la séance, mais il faut continuer à se perfectionner pour continuer à progresser !",
            "Sans nos rêves nous sommes morts·es ! Alors croiyez en vos rêves.",
            "Vous savez où vous êtes et vous savez où vous voulez aller donc continuez à travailler !",
            "C'est votre mental qui doit guider votre corps et non l'inverse !",
            "Parfois, pendant le sport on peut galérer mais pensez toujours à l'après effort !",
            "Apprenez du passé et concentrez-vous sur le futur !",
            "Ne vous comparez pas aux autres, comparez vous à la version que vous êtiez hier !"
        ],
        2: [
            "Peu importe le sport, le renforcement musculaire peut vous permettre de prévenir les blessures,...",
            "Après une séance de sport, le mieux pour votre corps c'est de boire de l'eau. Cela permet à votre corps de récupérer plus rapidement.",
            "Sachez qu'il ne faut pas négligez les baskets que vous utilisez quand vous faîtes du sport !",
            "Après un entraînement comme celui-ci je vous conseille de prendre une banane ou des amandes !",
            "C'est quand vous êtes dans le dur que vous progressez vraiment !",
            "Si vous avez une douleur, ça sert à rien de forcer dessus ! Reposez-vous et revenez plus fort·e !",
            "Faites des étirements légers avant de vous coucher, ça permettra à votre corps de récupérer plus vite !",
            "Quand vous avez la flemme de faire du sport, mettez-vous en tenue dès que vous vous levez",
            "Donnez l'exemple sans rien attendre en retour ! Motivez vos amis·es,...",
            "Les progrès ça se construit séance après séance et aujourd'hui vous venez d'en ajouter une de plus à votre parcours ! Félicitations !"
        ]
    }

    // générer le paragraphe
    let NombreAleatoire = 0
    let PhraseDico = ""
    let ParagrapheCoach = ""

    for (let i = 0; i <= 2; i++) {
        NombreAleatoire = GenererNbAleatoire()
        PhraseDico = CoachBienveillant[i][NombreAleatoire]

        ParagrapheCoach += PhraseDico + " "
    }

    SectionCoach.textContent = ParagrapheCoach

    return
}

async function RegistrationWorkout() {
    // Recup du bouton
    let BoutonSauvegarde = document.getElementById("button-sauvegarder")

    // Recup valeur des champs
    let SportWorkoutUser = document.getElementById("profil-sport").value.trim()
    let DateWorkoutUser = document.getElementById("date-entrainement-user").value
    let NameWorkoutUser = document.getElementById("nom-entrainement-user").value.trim()
    let DureeWorkoutUser = parseInt(document.getElementById("duree-entrainement-user").value.trim())
    let ValueRpeUser = parseInt(document.querySelector(".slider progress").value)

    // Initialisation
    let DistanceWorkoutUser = null
    let DeniveleWorkoutUser = null
    let MusclesWorkoutUser = null

    // Initialisation
    let ChargeWorkout = 0

    // Vérification
    if (!DateWorkoutUser || !DureeWorkoutUser || !NameWorkoutUser) {
        alert("Veuillez remplir tous les champs du formulaire.")
        return
    }
    if (DureeWorkoutUser <= 0) {
        alert("Valeur non valide, la durée doit être un nombre supérieur à 0.")
        return
    }
    if (NameWorkoutUser.length >= 80) {
        alert("Le champs sport ne doit pas dépasser 50 caractères.")
        return
    }

    // Recup en fonction du sport
    if (SportWorkoutUser == "Course" || SportWorkoutUser == "Velo" || SportWorkoutUser == "Marche") {
        // Recup champs
        DistanceWorkoutUser = parseFloat(document.getElementById("distance-entrainement-user").value.trim())
        DeniveleWorkoutUser = parseInt(document.getElementById("denivele-entrainement-user").value.trim())

        // Vérifications
        if (isNaN(DistanceWorkoutUser) || isNaN(DeniveleWorkoutUser)) {
            alert("Veuillez remplir tous les champs du formulaire.")
            return
        }
        if (DistanceWorkoutUser <= 0) {
            alert("Valeur non valide, la distance doit être un nombre supérieur à 0.")
            return
        }
        if (DeniveleWorkoutUser < 0) {
            alert("Valeur non valide, le denivelé doit être un nombre positif.")
            return
        }
    } else if (SportWorkoutUser == "Musculation") {
        // Recup champs
        MusclesWorkoutUser = document.getElementById("muscle-entrainement-user").value.trim()

        // Verifications
        if (!MusclesWorkoutUser) {
            alert("Veuillez remplir tous les champs du formulaire.")
            return
        }
        if (MusclesWorkoutUser.length > 150) {
            alert("Les muscles travaillés ne doivent pas dépasser 150 caractères !")
            return
        }
    }

    // desactivation du bouton
    BoutonSauvegarde.disabled = true 
    BoutonSauvegarde.textContent = "Sauvegarde..."

    // Calcul Charge
    ChargeWorkout = DureeWorkoutUser*ValueRpeUser

    // Sauvegarde
    await db.entrainement.add({
        sport: SportWorkoutUser,
        date: DateWorkoutUser,
        nom: NameWorkoutUser,
        duree: DureeWorkoutUser,
        rpe: ValueRpeUser,
        distance: DistanceWorkoutUser,
        denivele: DeniveleWorkoutUser,
        muscles_travailles: MusclesWorkoutUser,
        charge_entrainement: ChargeWorkout
    })

    // Pause
    await new Promise(r => setTimeout(r, 1000))
    // Remise bouton etat normal
    BoutonSauvegarde.textContent = "Sauvegarder"

    // Renvoie vers historique d'entraînement
    window.location.href = "historique_entrainement.html"

    return
}

window.addEventListener("DOMContentLoaded", () => {
    SelectionSport("Libre")
    JrmCoach()
})