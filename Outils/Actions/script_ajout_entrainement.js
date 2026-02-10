let IdEditWorkout = null // init variable globale

async function MessagePrevention() {
    // Check du statut du user
    let HistoriqueDB = await db.statut_analyse.toArray()

    let StatutData = HistoriqueDB.map(statutBDD => statutBDD.statut).reverse() // reverse pour inverser la liste pour l'ordre

    // Unit 
    let LastStatutUser = ""
    if (StatutData.length > 0) {
        // on prend l'index 0 pour avoir son dernier statut
        LastStatutUser = StatutData[0]
    } else {
        // si il n'y a pas de statut on le met sur actif
        LastStatutUser = "Actif·ve"
    }
    
    // Vérif + message de prévention
    if (LastStatutUser == "Vacances") {
        alert("Vous êtes en vacances et vous vous entraînez quand même ! Vous êtes très discipliné·e mais allez-y tranquille les vacances c'est fait pour ça aussi.")
    } else if (LastStatutUser == "Blessure") {
        alert("Attention ! Vous avez signalé une blessure. Faire un entraînement va aggraver votre blessure, privilégiez la récupuration pour pouvoir revenir plus fort·e.")
    } else if (LastStatutUser == "Malade") {
        alert("Vous êtes malade, ce n'est pas très mature de faire un entraînement, votre organisme a besoin de repos pour guérir. Si vous tenez à votre entraînement, essayer de faire un entraînement léger en intensité.")
    }
            
    return
}

async function VerificationParam() {
    const ParametreURL = window.location.search // on recherche si il y a un param dans l'URL (ex : ?edit=7)
    let TableauSeparation = ParametreURL.split("=") // exemple ['?edit', '7']

    if (TableauSeparation.length == 2) { // vérification si il y a bien 2 partie
        // conversion de l'id en int
        const ID = parseInt(TableauSeparation[1])

        // Recup des datas du workout
        if (ID) { 
            // on change la variable globale
            IdEditWorkout = ID
            const WorkoutDB = await db.entrainement.get(ID) // la méthode .get permet de recup direct les datas de l'id coresspondant
            // on commence par changer le H1 de la page
            document.getElementById("title-page").textContent = "Modification de l'entraînement"
            document.getElementById("coach-ajoute-entrainement").style.display = "none"

            // remplissage des champs
            document.getElementById("profil-sport").value = WorkoutDB.sport
            document.getElementById("date-entrainement-user").value = WorkoutDB.date
            document.getElementById("nom-entrainement-user").value = WorkoutDB.nom
            document.getElementById("duree-entrainement-user").value = WorkoutDB.duree

            // remettre le RPE sur bonne position
            document.querySelector(".slider input").value = WorkoutDB.rpe
            document.querySelector(".slider progress").value = WorkoutDB.rpe
            document.querySelector(".slider-value").textContent = WorkoutDB.rpe

            // Remettre les champs adaptée au sport
            SelectionSport(WorkoutDB.sport)

            // Remplissage des champs de sport particulier
            if (WorkoutDB.distance) {
                document.getElementById("distance-entrainement-user").value = WorkoutDB.distance
                if (WorkoutDB.denivele) {
                    document.getElementById("denivele-entrainement-user").value = WorkoutDB.denivele
                }
            } else if (WorkoutDB.muscles_travailles) {
                document.getElementById("muscle-entrainement-user").value = WorkoutDB.muscles_travailles
            }

        }
    } else {        
        SelectionSport("Libre")
        await JrmCoach()
        await MessagePrevention()
    }

    return
}

function SelectionSport(value) { // Pr cacher les champs en fonction du sport choisi
    // Recup des champs + label des champs
    let DivCoteCote = document.getElementById("dynamique-div")
    let ChampsMuscles = document.getElementById("muscle-entrainement-user")
    let LabelMuscles = document.getElementById("label-invisible")

    // Adaptation des champs en fonction du sport
    if (value == "Libre") {
        DivCoteCote.classList.add("invisible")
        ChampsMuscles.style.display = "none"
        LabelMuscles.style.display = "none"

    } else if (value == "Course" || value == "Vélo" || value == "Marche") {
        DivCoteCote.classList.remove("invisible")
        ChampsMuscles.style.display = "none"
        LabelMuscles.style.display = "none"

    } else if (value == "Musculation") {
        DivCoteCote.classList.add("invisible")
        ChampsMuscles.style.display = "block"
        LabelMuscles.style.display = "block"
    }

    return
}

function GenererNbAleatoire() {
    // Nb aléatoire
    let NombreAleatoire = Math.random() // renvoie aléatoirement entre 0 et 1 (ex : 0.5890953759539541)
    NombreAleatoire = Math.floor(NombreAleatoire*10) //fois 10 et nb arrondi pour avoir par exemple 5.8 puis 5 grace a l'arrondi

    return NombreAleatoire
}

async function JrmCoach() {
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
            "Quand vous avez la flemme de faire du sport, mettez-vous en tenue dès que vous vous levez.",
            "Donnez l'exemple sans rien attendre en retour ! Motivez vos amis·es,...",
            "Les progrès ça se construit séance après séance et aujourd'hui vous venez d'en ajouter une de plus à votre parcours ! Félicitations !"
        ]
    }

    const CoachStrictMotivant = {
        0: [
            "Enfin, vous avez terminé votre séance ! J'espère que vous en êtes satisfait.",
            "J'espère que vous vous êtes donné·e à fond pendant cet entraînement !",
            "Alors, d'après vous, vous trouvez que vous avez fait un bon entraînement ?",
            "Bien joué pour cette séance, mais gardez cette même régularité dans vos entraînements.",
            "Vous pensez avoir réussi votre entraînement ? Le plus important, c'est d'avoir pris du plaisir.",
            "Cette séance vous a pas trop posé problème ?",
            "J'espère que cette séance vous a fait du bien physiquement et mentalement.",
            "Vous avez tout donné ? J'espère parce que c'est la base !",
            "Vous ne vous êtes pas trop endormi·e·s pendant cette séance ? Je rigole bien sûr !",
            "J'adore votre régularité, j'espère que vous resterez sur la bonne voie."
        ],
        1: [
            "Vous savez qu'il vaut mieux faire des erreurs à l'entraînement plutôt qu'en compétition. Les erreurs font partie de la réussite.",
            "Vous savez que faire des erreurs, c'est une chance et c'est souvent ça qui mène des athlètes à la réussite.",
            "Vous regrettez vos dernières performances ? Sachez que vous êtes allé·e vous entraîner, c'est le plus important.",
            "Regardez tout ce que vous avez accompli dans le passé et pensez au futur !",
            "C'est dans le dur que vous progressez vraiment et c'est à ce moment là qu'on voit qui on est.",
            "Ne vous comparez pas aux autres ! Comparez vous à la personne que vous étiez hier !",
            "Si c’était facile, tout le monde le ferait. Mais vous, vous n’êtes pas tout le monde.",
            "Ne regrettez jamais une séance, regrettez seulement celles que vous avez zappées.",
            "La douleur est temporaire, mais la fierté de vous êtes dépassé·e, elle, reste à vie.",
            "Quand vous croyez que vous n'avez plus rien à donner, vous avez encore 20% de réserve. C’est là que tout se joue. Alors, allez les chercher."
        ],
        2: [
            "Avoir un objectif en tête permet de gagner en régularité et en discipline, si vous manquez de régularité vous savez ce qui vous reste à faire.",
            "Votre corps s’ennuie vite, essayez de changer de séance toutes les semaines pour continuer à progresser.",
            "Mangez des repas équilibrés, protéinés avec des glucides sains et des légumes et trust the process.",
            "Si vous avez des courbatures, c'est bien, mais si vous avez une douleur faites une pause ! Par contre, si c'est juste la flemme, bougez-vous.",
            "1 répétition de plus ? C’est une victoire. Fêtez ça, mais restez ·e sur vos objectifs.",
            "Avant de commencer une séance, sautez, bougez, faites monter votre cardio pour éviter de vous blesser bêtement !",
            "Buvez avant d’avoir soif, sinon c’est déjà trop tard. Votre corps est une machine, vous devez lui donner de l'essence pour la faire fonctionner.",
            "Quand votre cerveau vous dit d'arrêter, c’est là qu’il faut pousser. La différence entre vous et les autres ? Eux écoutent cette voix, mais vous, vous la domptez.",
            "Vous n’avez pas besoin d’être le/la plus fort·e ou le/la plus rapide aujourd’hui. Mais si vous êtes le/la plus régulier·e, vous les écraserez tous sur le long terme. Les performances ça se construit.",
            "Rappelez-vous toujours où vous êtes et regardez où vous voulez aller."
        ]
    }

    const CoachCopain = {
        0: [
            "Vous vous êtes bien entraîné·e ?",
            "Alors cet entraînement ? Vous avez encore cartonné ?",
            "Vous vous êtes donné à fond j'espère !",
            "Hey, ça va ?! Pas trop fatigué·e !",
            "Mais non !! Alors cette séance pas trop compliquée ?",
            "Aujourd'hui, c'était entraînement !",
            "Hello, encore un entraînement ! Bravo ! ",
            "Je suis sûr que vous avez assuré !",
            "Comment ça va ? Pas trop dur cette séance ?",
            "Vous êtes épuisé·e ou alors vous vous êtes juste reposé·e sur vos acquis ?"
        ],
        1: [
            "Pendant une séance si vous galèrez, pensez à une personne que vous aimez bien ça vous aidera à dépasser vos limites.",
            "Pensez toujours à l'après entraînement quand vous galérez ! Imagine-vous entrain de bouffer un gros tacos.",
            "J'espère que vous avez tout donné sur le terrain ! Vous êtes cap de faire 10 pompes après cette sortie ?",
            "Tous les soirs au lieu d'être sur votre tel, faites 10 pompes, 10 abdos et 10 squats ! Vous verrez vos performances vont nettement s'améliorer.",
            "Vous avez loupé votre séance ? Pas grave ! Après tout vous êtes quand même allé·e vous entraîner, bien joué.",
            "En vrai, une séance de sport c'est quoi dans votre vie ? C'est pas grand chose donc prenez toujours ce temps.",
            "Continuez à travailler, concentrez-vous et vous allez tous les choquer ! Dont moi !",
            "Pour toujours être motivé et progresser, faites évoluer vos séances pour ne pas rentrer dans l'habitude.",
            "La clé de la réussite c'est la concentration, la discipline et le dépassement de soi.",
            "Comparez-vous toujours à la personne que vous étiez hier ! C'est votre rival !"
        ],
        2: [
            "Le plus important dans le sport, c'est la régularité, la motivation c'est juste cool pour les premières semaines.",
            "Après une séance comme celle-ci vous avez le droit à une récompense, vous le méritez, par contre je vous laisse choisir votre récompense. ",
            "Si vous ne vous êtes pas donné·e à fond pour cet entraînement, bah pensez à vous donner à fond la prochaine fois !",
            "Vous connaissez le 80/20 pour une prépa ? Vous devez faire 80% du temps de votre entraînement à faible intensité et 20% du temps en effort intense.",
            "Je vous donne un défi pour votre prochain entraînement : testez la séance pyramide en course à pied. Renseignez-vous sur cette séance et testez si vous êtes cap.",
            "La nutrition ça joue aussi dans vos performances. Donc, essayez toujours de manger des aliments non-transformés.",
            "Essayez de boire 2 à 3 verres d'eau après cet entraînement, ça permettra à votre corps de récupérer plus vite.",
            "J'espère qu'avant cet entraînement vous vous êtes échauffé·e parce que l'échauffement c'est crucial !",
            "Gérez votre effort dès le début de votre entraînement : ne partez pas à fond sur les premières répétitions pour éviter de vous cramer dès le départ.",
            "Laissez du temps à votre corps pour récupérer, ça lui fera du bien et vous serez moins fatigué·e."
        ]
    }

    const CoachGoMuscu = {
        0: [
            "Vous avez senti une douleur quelque part ? Si oui, parlez-en à un médecin, ça sert à rien de forcer comme un bourrin·ne.",
            "Vous êtes allé·e à l'échec ou alors vous vous êtes aidé de l'élan pour finir votre répétition ?",
            "Vous avez battu votre PR ? Si oui : vous êtes une machine ! Si non : vous inquiétez pas, la prochaine fois, vous allez tout péter !",
            "Vous avez bu assez d’eau pendant votre séance ? J'espère que oui sinon => buvez maintenant !",
            "Vous avez écouté de la musique pendant votre séance ? Parce que moi, je sais qu'une bonne playlist, ça fait +20% de performance.",
            "Vous avez fait vos étirements ? Non ? Vous êtes entrain de préparer vos courbatures pour demain. Allez vous étirer, ça prend 5 minutes.",
            "Demain, n'oubliez pas, c'est le Leg Day. Pour les nuls en anglais ça veut dire : 'la séance consacrée aux jambes'",
            "Vous avez fait un échauffement avant ou vous avez fait votre séance directement comme un bourrin ? Parce que moi, je sais que l’échauffement, c’est +50% de performance !",
            "Vous êtes content·e de votre séance ou vous êtes déçu·e ?",
            "Vous avez mangé des protéines après votre séance ? J'espère parce que c'est pas comme ça que vous allez devenir énorme et sec !"
        ],
        1: [
            "La discipline, c’est la clé. Et vous, vous avez la clé pour tout exploser !",
            "Le mental est plus important que les muscles, j'espère que vous n'écoutez pas cette voix dans votre tête qui vous dit d'arrêter.",
            "Un effort de plus, c’est un pas de plus vers vos objectifs. Continuez comme ça !",
            "100% d’efforts, 0% de regrets. Vous êtes sur la bonne voie, champion·ne !",
            "La souffrance, c’est temporaire. Les résultats, eux, restent. Vous êtes très fort·e, pour continuer d'être au sommet, allez poussez de la fonte demain.",
            "Vous faites de la muscu, alors prouvez-le ! Faites 20 pompes là maintenant ! Non, je ne rigole pas allez bougez-vous.",
            "Je vous lance un petit défi : ce soir avant d'aller vous coucher vous faites 10 pompes, 10 squats et 10 dips et après vous pourrez aller dormir !",
            "Chaque goutte de sueur perdue, c’est un pas de plus vers la version de vous énorme et sec.",
            "Vous connaissez le '7-7-7' ? Non ? C'est un circuit à faire après une séance : 7 Burpees, 7 Pompes, 7 Squats sautés, je vous mets au défi de réussir ce circuit.",
            "Ne comparez jamais votre physique aux autres, comparez-le à la version de votre corps d'hier !"
        ],
        2: [
            "Vous savez ce que c'est d'avoir le pump ? C'est quand vous ressentez la congestion de votre muscle pendant une séance.",
            "Vous connaissez le programme : 'Push, Pull, Legs' ? Non ? Bah demandez à Gemini peut être que vous allez comprendre.",
            "Les protéines après l’entraînement, c'est le top ! Oeufs, poulet, fromage blanc... Vous avez l’embarras du choix !",
            "Après un entraînement comme celui-ci je vous conseille de prendre une banane ou des amandes !",
            "Les glucides, c’est votre carburant pour votre séance de muscu vous avez le choix entre : des pâtes complètes, du riz,...",
            "La récupération c’est sacré. Dormez 7 à 8h par nuit, vos muscles vous diront merci.",
            "Évitez les sucres rapides avant le sport, privilégiez des sucres lents. Un fruit, oui. Un soda, non.",
            "Respirez bien pendant l’effort. Inspirez par le nez, expirez par la bouche. Vous êtes une machine !",
            "Hydratez-vous avant, pendant et après l’effort. L’eau, c’est votre meilleur allié !",
            "Les muscles ça se construit séance après séance et aujourd'hui vous venez d'en ajouter une de plus à votre parcours ! Félicitations !"
        ]
    }
    
    // Déterminer le coach choisis du user
    let CoachUserDB = await db.JRM_Coach.toArray()
    let StyleCoachUser = CoachBienveillant // attribution du style de coach a utilisé
    if (CoachUserDB.length > 0) {  // si le user a enregistré qqch alors on met le style du coach qu'il a choisis
        let TableauStyleCoach = CoachUserDB.map(elementDB => elementDB.style) // recup du style
        // On check le style de coach que le user a choisi et on attribue le dico correspondant
        if (TableauStyleCoach[0] == "Bienveillant") {
            StyleCoachUser = CoachBienveillant
        } else if (TableauStyleCoach[0] == "Strict-Motivant") {
            StyleCoachUser = CoachStrictMotivant
        } else if (TableauStyleCoach[0] == "Copain") {
            StyleCoachUser = CoachCopain
        } else {
            StyleCoachUser = CoachGoMuscu
        }
    }

    // générer le paragraphe
    let NombreAleatoire = 0
    let PhraseDico = ""
    let ParagrapheCoach = ""

    for (let i = 0; i <= 2; i++) {
        NombreAleatoire = GenererNbAleatoire() // nb aléatoire
        PhraseDico = StyleCoachUser[i][NombreAleatoire] // recherche dans le dico

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

    // Prépa date pour comparer
    const DateUserFormatee = new Date(DateWorkoutUser)
    const DateActuelle = new Date()

    // Initialisation
    let ChargeWorkout = 0

    // Vérification
    if (!DateWorkoutUser || !DureeWorkoutUser || !NameWorkoutUser) {
        alert("Veuillez remplir tous les champs du formulaire.")
        return
    }
    if (DateUserFormatee > DateActuelle) { // Comparaison de 2 dates
        alert("La date ne peut pas être dans le future.")
        return
    }
    if (DureeWorkoutUser <= 0) {
        alert("Valeur non valide, la durée doit être un nombre supérieur à 0.")
        return
    }
    if (DureeWorkoutUser > 1439) {
        alert("La durée de votre entraînement ne doit pas dépasser 1439 minutes (23h 59min).")
        return
    }

    // Recup en fonction du sport
    if (SportWorkoutUser == "Course" || SportWorkoutUser == "Vélo" || SportWorkoutUser == "Marche") {
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
        if (DistanceWorkoutUser > 1000) {
            alert("La distance de votre entraînement ne doit pas dépasser 1000 kilomètres.")
            return
        }
        if (DeniveleWorkoutUser < 0) {
            alert("Valeur non valide, le denivelé doit être un nombre positif.")
            return
        }
        if (DeniveleWorkoutUser > 10000) {
            alert("Le dénivelé de votre entraînement ne doit pas dépasser 10 000 m.")
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
    }

    // desactivation du bouton
    BoutonSauvegarde.disabled = true 
    BoutonSauvegarde.textContent = "Sauvegarde..."

    // Calcul Charge
    ChargeWorkout = DureeWorkoutUser*ValueRpeUser

    // Sauvegarde
    if (IdEditWorkout != null) {
        await db.entrainement.put({
            id: IdEditWorkout,
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
    }
    else {
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
    }

    // Pause
    await new Promise(r => setTimeout(r, 1000))
    // Remise bouton etat normal
    BoutonSauvegarde.textContent = "Sauvegarder"

    // Renvoie vers historique d'entraînement
    window.location.href = "historique_entrainement.html"

    return
}

window.addEventListener("DOMContentLoaded", () => {
    VerificationParam()
})