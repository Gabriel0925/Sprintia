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
        alert("Tu es en vacances et tu t'entraînes quand même ! Tu es très discipliné·e mais va y tranquille les vacances c'est fait pour ça aussi.")
    } else if (LastStatutUser == "Blessure") {
        alert("Attention ! Tu as signalé une blessure. Faire un entraînement va aggraver ta blessure, privilégie la récupération pour pouvoir revenir plus fort·e.")
    } else if (LastStatutUser == "Malade") {
        alert("Tu as signalé que tu étais malade, ce n'est pas très mature de faire un entraînement, ton organisme a besoin de repos pour guérir. Si tu tiens à ton entraînement, essaie de faire un entraînement léger en intensité.")
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
            "Bravo ! Tu as assuré aujourd'hui ! J'espère que cette séance t'a fais du bien mentalement et physiquement.",
            "Une séance de plus, un pas de plus !",
            "La séance de sport était bonne ? Bonnes sensations ?",
            "T'as kiffé ou souffert ?",
            "Tu as gagné ton dodo/ton repas ?",
            "Ça t'a boosté ou vidé ?",
            "Tu viens de te défouler ! T'es content de ta séance ?",
            "Tu es content·e de ta séance ou tu es déçu·e ?",
            "Tu as cru que tu allais lâcher ?"
        ],
        1: [
            "Chaque effort compte. Ne lâche rien ! La discipline est la clé des plus grands objectifs !",
            "Si tu veux un conseil, la régularité est toujours meilleure que l'intensité. Il vaut mieux faire 3 petites séances qu'une grosse séance par semaine.",
            "Peu importe les chiffres, ce qui compte, c’est que tu as pris du temps pour faire ton sport !",
            "Top la séance, mais il faut continuer à se perfectionner pour continuer à progresser !",
            "Sans nos rêves nous sommes morts·es ! Alors crois en tes rêves.",
            "Tu sais où tu es et tu sais où tu veux aller donc continue à travailler !",
            "C'est ton mental qui doit guider ton corps et non l'inverse !",
            "Parfois, pendant le sport on peut galérer mais pense toujours à l'après effort !",
            "Apprends du passé et concentre-toi sur le futur !",
            "Ne te compare pas aux autres, compare-toi à la version que tu étais hier !"
        ],
        2: [
            "Peu importe le sport, le renforcement musculaire peut te permettre de prévenir les blessures,...",
            "Après une séance de sport, le mieux pour ton corps c'est de boire de l'eau. Ça permet à ton corps de récupérer plus rapidement.",
            "Sache qu'il ne faut pas négliger les baskets que tu utilises quand tu fais du sport !",
            "Après un entraînement comme celui-ci je te conseille de prendre une banane ou des amandes !",
            "C'est quand tu es dans le dur que tu progresses vraiment !",
            "Si tu as une douleur, ça sert à rien de forcer dessus ! Repose-toi et reviens plus fort·e !",
            "Fais des étirements légers avant de te coucher, ça permettra à ton corps de récupérer plus vite !",
            "Quand tu as la flemme de faire du sport, met-toi en tenue dès que tu te lèves. Ça serait bête de l'enlever le soir sans avoir fait son sport.",
            "Donne l'exemple sans rien attendre en retour ! Motive tes amis·es à faire du sport, c'est super important pour eux.",
            "Les progrès ça se construit séance après séance et aujourd'hui tu viens d'en ajouter une de plus à ton parcours ! Félicitations !"
        ]
    }

    const CoachStrictMotivant = {
        0: [
            "Enfin, tu as terminé ta séance ! J'espère que tu en es satisfait.",
            "J'espère que tu t'es donné·e à fond pendant cet entraînement !",
            "Alors, d'après toi, tu trouves que tu as fait un bon entraînement ?",
            "Bien joué pour cette séance, mais garde cette même régularité dans tes entraînements.",
            "Tu penses avoir réussi ton entraînement ? Le plus important, c'est d'avoir pris du plaisir à faire cette séance.",
            "Cette séance ne t'a pas trop posé problème ?",
            "J'espère que cette séance t'a fait du bien physiquement et mentalement.",
            "Tu as tout donné ? J'espère parce que si je pouvais je te ferais cracher tes poumons lors du prochain entraînement.",
            "Tu ne t'es pas trop endormi·e pendant cette séance ? Je rigole bien sûr !",
            "J'adore ta régularité, j'espère que tu resteras sur cette voie."
        ],
        1: [
            "Tu sais qu'il vaut mieux faire des erreurs à l'entraînement plutôt qu'en compétition. Les erreurs font partie de la réussite.",
            "Tu sais que faire des erreurs, c'est une chance et c'est souvent ça qui mène des athlètes à la réussite.",
            "Ne regrette jamais tes dernières performances ? Sache que tu es allé·e t'entraîner, et rien que ça, ce n'est pas une habitude pour tout le monde, donc crois en toi ! Les résultats arriveront...",
            "Regarde tout ce que tu as accompli dans le passé et pense à ce que tu pourrais faire dans le futur !",
            "C'est dans le dur que tu progresses vraiment et c'est à ce moment là qu'on voit qui on est.",
            "Ne te compare pas aux autres ! Compare-toi à la personne que tu étais hier !",
            "Si c’était facile, tout le monde ferait du sport. Mais toi, tu n'es pas tout le monde.",
            "Ne regrette jamais une séance, regrette seulement celles que tu as zappées.",
            "La douleur est temporaire, mais la fierté de t'être dépassé·e, elle, reste à vie.",
            "Quand tu crois que tu n'as plus rien à donner, en réalité tu as encore 20% de réserve. C’est là que tout se joue. Alors, essaie de toujours puiser dans cette réserve lors de tes séances intensives."
        ],
        2: [
            "Avoir un objectif en tête permet de gagner en régularité et en discipline, si tu manques de régularité tu sais ce qui te reste à faire.",
            "Ton corps s’ennuie vite, essaie de changer de séance toutes les semaines pour continuer à progresser.",
            "Mange des repas équilibrés, protéinés avec des glucides sains et des légumes et trust the process.",
            "Si tu as des courbatures, c'est bien, mais si tu as une douleur fais une pause ! Par contre, si c'est juste la flemme, bouge-toi.",
            "1 répétition de plus ? C’est une victoire. Fête ça, mais reste focus sur tes objectifs.",
            "Avant de commencer une séance, saute, bouge, fais monter ton cardio pour éviter de te blesser bêtement !",
            "Bois avant d’avoir soif, sinon c’est déjà trop tard. Ton corps est une machine, tu dois lui donner de l'essence pour la faire fonctionner.",
            "Quand ton cerveau te dit d'arrêter, c’est là qu’il faut pousser. La différence entre toi et les autres ? Eux écoutent cette voix, mais toi, tu la domptes.",
            "Tu n'as pas besoin d’être le/la plus fort·e ou le/la plus rapide aujourd’hui. Mais si tu es le/la plus régulier·e, tu finiras par tous les écraser. N'oublie jamais que les performances ça se construit.",
            "Rappelle-toi toujours où tu es et regarde où tu veux aller."
        ]
    }

    const CoachCopain = {
        0: [
            "Tu t'es bien entraîné·e ?",
            "Alors cet entraînement ? Tu as encore cartonné ?",
            "Tu t'es donné à fond j'espère !",
            "Hey, ça va ?! Pas trop fatigué·e !",
            "Mais non !! Ça va toi ? Alors cette séance pas trop compliquée ?",
            "Aujourd'hui, c'était entraînement pour toi et pour moi c'est analyse.",
            "Hello, encore un entraînement ! Bravo ! ",
            "Je suis sûr que tu as assuré !",
            "Comment ça va ? Pas trop dur cette séance ?",
            "Tu t'es épuisé·e ou alors tu t'es juste reposé·e sur tes acquis ?"
        ],
        1: [
            "Pendant une séance si tu galères, pense à une personne que tu aimes bien ou à ton idole, ça t'aidera à dépasser tes limites.",
            "Pense toujours à l'après entraînement quand tu galères ! Imagine-toi en train de bouffer un gros tacos ou faire quelque chose qui te fait plaisir.",
            "J'espère que tu as tout donné sur le terrain ! Tu es cap de faire 10 pompes après cette sortie ?",
            "Tous les soirs au lieu d'être sur ton tel, fais 10 pompes, 10 abdos et 10 squats ! Tu verras tes performances vont nettement s'améliorer.",
            "Tu as foiré ta séance ? Pas grave ! Après tout tu es quand même allé·e t'entraîner, bien joué.",
            "En vrai, une séance de sport c'est quoi dans votre vie ? C'est pas grand chose donc prenez toujours ce temps.",
            "Continue à travailler, concentre-toi et tu vas tous les choquer ! Dont moi !",
            "Pour toujours être motivé et progresser, fais évoluer tes séances pour ne pas rentrer dans l'habitude.",
            "La clé de la réussite c'est la concentration, la discipline et le dépassement de soi.",
            "Compare-toi toujours à la personne que tu étais hier ! Ça doit être ton plus grand rival !"
        ],
        2: [
            "Le plus important dans le sport, c'est la régularité; la motivation c'est juste cool pour les premières semaines.",
            "Après une séance comme celle-ci, tu as le droit à une récompense, tu le mérites, par contre je te laisse choisir ta récompense. ",
            "Si tu ne t'es pas donné·e à fond lors de cet entraînement, bah pense à te donner à fond la prochaine fois !",
            "Tu connais le 80/20 ? Pour une prépa c'est le top. Tu dois faire 80% du temps de ton entraînement à faible intensité et 20% du temps en effort intense.",
            "Je te donne un défi pour ton prochain entraînement : teste la séance pyramide en course à pied. Renseigne-toi sur cette séance et test si tu es cap.",
            "La nutrition ça joue aussi dans tes performances. Donc, essaie toujours de manger des aliments non transformés.",
            "Essaie de boire 2 à 3 verres d'eau après cet entraînement, ça permettra à ton corps de récupérer plus vite.",
            "J'espère qu'avant cet entraînement tu t'es échauffé·e, parce que l'échauffement c'est crucial !",
            "Gére ton effort dès le début de ton entraînement : ne pars pas à fond sur les premières répétitions pour éviter de te cramer dès le départ.",
            "Laisse du temps à ton corps pour récupérer, ça lui fera du bien et tu seras moins fatigué·e."
        ]
    }

    const CoachGoMuscu = {
        0: [
            "Tu as senti une douleur quelque part ? Si oui, parle-en à un médecin, ça sert à rien de forcer comme un·e bourrin·ne.",
            "Tu es allé·e à l'échec ou alors tu t'es aidé de l'élan pour finir ta répétition ?",
            "Tu as battu ton PR ? Si oui : tu es une machine ! Si non : ne t'inquiète pas, la prochaine fois, tu vas tout péter !",
            "Tu as bu assez d’eau pendant ta séance ? J'espère que oui sinon, va boire maintenant !",
            "Tu as écouté de la musique pendant ta séance ? Parce que moi, je sais qu'une bonne playlist, ça fait +20% de performance.",
            "Tu as fait tes étirements ? Non ? Tu es en train de préparer tes courbatures pour demain. Va t'étirer, ça prend 5 minutes.",
            "Demain, n'oublie pas, c'est le Leg Day. Pour les nuls en anglais, ça veut dire : 'la séance consacrée aux jambes'",
            "Tu as fait un échauffement avant ou tu as fait ta séance directement comme un·e bourrin·ne ? Parce que moi, je sais que l’échauffement, c’est +50% de performance !",
            "Tu es content·e de ta séance ou tu es déçu·e ? Si tu es déçu·e n'oublie jamais que le plus important c'est d'avoir fait sa séance et d'avoir pris du plaisir.",
            "Tu as mangé des protéines après ta séance ? J'espère parce que c'est pas comme ça que tu vas devenir énorme et sec·he !"
        ],
        1: [
            "La discipline, c’est la clé. Et toi, tu as cette clé qui va te permettre de tout exploser !",
            "Le mental est plus important que les muscles, j'espère que tu n'écoutes pas cette voix dans ta tête qui te dit d'arrêter.",
            "Un effort de plus, c’est un pas de plus vers tes objectifs. Continue comme ça !",
            "100% d’efforts, 0% de regrets. Tu es sur la bonne voie, champion·ne !",
            "La souffrance, c’est temporaire. Les résultats, eux, restent. Tu es très fort·e. Pour continuer d'être au sommet, va pousser de la fonte demain.",
            "Tu fais de la muscu, alors prouve-le ! Fais 20 pompes là maintenant ! Non, je ne rigole pas allez bouge-toi.",
            "Je vous lance un petit défi : ce soir avant d'aller te coucher tu feras 10 pompes, 10 squats et 10 dips et seulement après tu pourras aller dormir !",
            "Chaque goutte de sueur perdue, c’est un pas de plus vers la version de toi énorme et sec·he.",
            "Tu connais le '7-7-7' ? Non ? C'est un circuit à faire après une séance : 7 Burpees, 7 Pompes, 7 Squats sautés, je te mets au défi de réussir ce circuit.",
            "Ne compare jamais ton physique aux autres, compare-le à la version de ton corps d'hier !"
        ],
        2: [
            "Tu sais ce que c'est d'avoir le pump ? C'est quand tu ressens la congestion de ton muscle pendant une séance.",
            "Tu connais le programme : 'Push, Pull, Legs' ? Non ? Bah demande à Gemini peut-être que tu vas comprendre.",
            "Les protéines après l’entraînement, c'est le top ! Oeufs, poulet, fromage blanc... Tu as l’embarras du choix !",
            "Après un entraînement comme celui-ci, je te conseille de prendre une banane ou des amandes !",
            "Les glucides, c’est ton carburant pour ta séance de muscu tu as le choix entre : des pâtes complètes, du riz,...",
            "La récupération c’est sacré. Dors 7 à 8h par nuit, tes muscles te diront merci.",
            "Évite les sucres rapides avant le sport, privilégie les sucres lents. En gros, ça veut dire que tu ne dois pas prendre un soda par contre, prends un fruit.",
            "Respire bien pendant l’effort. Inspire par le nez, expire par la bouche. Tu es une machine !",
            "Hydrate-toi avant, pendant et après l’effort. L’eau, c’est ton meilleur allié !",
            "Les muscles ça se construit séance après séance, et aujourd'hui tu viens d'en ajouter une de plus à ton parcours ! Félicitations !"
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

function conversionMinutes(DureeWorkoutUser) {
    if (DureeWorkoutUser.includes(":")) {
        let FormatDuree = DureeWorkoutUser.split(":")
        if (FormatDuree.length == 3) {
            if (FormatDuree[0].length == 2 && FormatDuree[1].length == 2 && FormatDuree[2].length == 2) {
                // Extraction des heures minutes et secondes
                let heures = parseInt(FormatDuree[0])
                let minutes = parseInt(FormatDuree[1])
                let secondes = parseInt(FormatDuree[2])

                // Vérification que le user a bien saisis les infos
                if (heures > 59 || minutes > 59 || secondes > 59) {
                    alert("Le format de la durée doit être hh:mm:ss avec hh, mm et ss inférieur à 60.")
                    DureeWorkoutUser = null // on met sur null pour pouvoir savoir qu'il y a eu une erreur et qu'il faut arreter la fonction RegistrationWorkout
                    return DureeWorkoutUser
                }

                // Conversion de la durée en minutes
                DureeWorkoutUser = (heures*60) + minutes + (secondes/60)
                // La vérification de la durée maximum/minimum se fait dans la fonction RegistrationWorkout
                return DureeWorkoutUser
                
            } else {
                alert("Le format de la durée doit être hh:mm:ss avec hh, mm et ss avec 2 chiffres.")
                DureeWorkoutUser = null // on met sur null pour pouvoir savoir qu'il y a eu une erreur et qu'il faut arreter la fonction RegistrationWorkout
                return DureeWorkoutUser
            }
        } else {
            alert("Veuillez respecter le format 'Heure:Minute:Seconde' (hh:mm:ss) pour le champ durée.")
            DureeWorkoutUser = null // on met sur null pour pouvoir savoir qu'il y a eu une erreur et qu'il faut arreter la fonction RegistrationWorkout
            return DureeWorkoutUser
        }
    } else {
        alert("Veuillez respecter le format 'Heure:Minute:Seconde' (hh:mm:ss) pour le champ durée.")
        DureeWorkoutUser = null // on met sur null pour pouvoir savoir qu'il y a eu une erreur et qu'il faut arreter la fonction RegistrationWorkout
        return DureeWorkoutUser
    }

}

async function RegistrationWorkout() {
    // Recup du bouton
    let BoutonSauvegarde = document.getElementById("button-sauvegarder")

    // Recup valeur des champs
    let SportWorkoutUser = document.getElementById("profil-sport").value.trim()
    let DateWorkoutUser = document.getElementById("date-entrainement-user").value
    let NameWorkoutUser = document.getElementById("nom-entrainement-user").value.trim()
    let DureeWorkoutUser = document.getElementById("duree-entrainement-user").value.trim()
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
    DureeWorkoutUser = conversionMinutes(DureeWorkoutUser)
    if (DureeWorkoutUser == null) {
        return
    }
    if (DureeWorkoutUser <= 0) {
        alert("Valeur non valide, la durée doit être un nombre supérieur à 0.")
        return
    }
    if (DureeWorkoutUser > 1439) {
        alert("La durée de votre entraînement doit être inférieur à 23h59m.")
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
    ChargeWorkout = Math.floor(DureeWorkoutUser*ValueRpeUser)

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
    window.location.href = "historique_entrainement.html?workoutregister" // on met un param dans l'URL

    return
}

window.addEventListener("DOMContentLoaded", () => {
    VerificationParam()
})