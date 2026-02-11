// dico des interpretation
const InterpretationBienveillant = {
    "1": "Je n'ai <strong>pas encore assez de données</strong> pour calculer ton indulgence de course. J'ai hâte que tu enregistres ton premier entraînement de course dans Sprintia pour qu'on analyse ça ensemble.", 
    "2": "Tu cours <strong>moins depuis 7 jours</strong>, c'est dommage ! Si c'est un choix profite-en pour te reposer ou travailler d'autres aspects de la course comme le <strong>renforcement</strong> ou de la <strong>mobilité</strong>.", 
    "3": "Parfait ! <strong>Tu progresses</strong> grâce à ta <strong>régularité</strong> ainsi qu'à ta discipline, continue comme ça pour booster tes performances. Pour maximiser ta progression, pense toujours à <strong>varier tes allures</strong> d'entraînement.", 
    "4": "Attention, tu cours <strong>bien plus que d'habitude</strong> ! Si tu continues sur ce rythme tu risques de te <strong>blesser</strong>. P'tit conseil, <strong>réduis</strong> ton volume d'entraînement.", 
    // Pour les statut
    "5": "Statut : <strong>Vacances</strong><br>Profite de cette pause pour te ressourcer, te reposer, et reviens encore plus motivé·e pour battre tous tes records !", 
    "6": "Statut : <strong>Blessure</strong><br>Prends vraiment le temps de laisser ton corps se régénérer complètement, afin de revenir encore plus fort·e.", 
    "7": "Statut : <strong>Malade</strong><br>Ne va pas t'entraîner, ton organisme a besoin de récupérer pour le moment, mais dès que tu seras guéri·e tu pourras reprendre les entraînements.", 
    "8": "Statut : <strong>Suspension</strong><br>Profite-en pour te reposer, j'analyserai tes entraînements seulement quand tu seras prêt·e !"
}
const InterpretationStrictMotivant = {
    "1": "Je n'ai <strong>pas encore assez de données</strong> pour calculer ton indulgence de course. J'ai hâte que tu rentres ton premier entraînement de course dans Sprintia pour qu'on analyse ça ensemble.", 
    "2": "Tu cours <strong>moins depuis 7 jours</strong>. Fais attention si tu continues sur cette voie, tu risques de perdre du niveau rapidement ! Petit conseil pour limiter la casse, fais du <strong>renforcement</strong>.", 
    "3": "Parfait ! <strong>Tu progresses</strong> grâce à ta <strong>régularité</strong>. La régularité c'est la clé de la réussite donc, continue comme ça pour progresser. Mais attention, le plus dur n'est pas de progresser mais de continuer à progresser.", 
    "4": "Tu cours <strong>bien plus que d'habitude</strong> ! Si tu veux te <strong>blesser</strong>, tu es sur la bonne voie, ne joue pas avec le feu, arrête de courir pendant quelques jours, pour revenir plus fort.", 
    // Pour les statut
    "5": "Statut : <strong>Vacances</strong><br>Profite de cette pause pour te ressourcer, te reposer, et reviens encore plus motivé·e pour battre tous tes records !", 
    "6": "Statut : <strong>Blessure</strong><br>Prends vraiment le temps de laisser ton corps se régénérer complètement, afin de revenir encore plus fort·e.", 
    "7": "Statut : <strong>Malade</strong><br>Ne va pas t'entraîner, ton organisme a besoin de récupérer pour le moment, mais dès que tu seras guéri·e tu pourras reprendre les entraînements.", 
    "8": "Statut : <strong>Suspension</strong><br>Profite-en pour te reposer, j'analyserai tes entraînements seulement quand tu seras prêt·e !"
}
const InterpretationCopain = {
    "1": "Je n'ai <strong>pas encore assez de données</strong> pour calculer ton indulgence de course. J'ai hâte que tu rentres ton premier entraînement de course dans Sprintia pour qu'on analyse ça ensemble.", 
    "2": "Tu cours <strong>moins depuis 7 jours</strong>. Essaie de courir un peu plus, ne te relâche pas, sinon tu vas finir par perdre tout ton niveau et crois moi, tu vas t'en vouloir une fois qu'il sera trop tard.", 
    "3": "Bravo ! <strong>Tu progresses</strong> grâce à ton sérieux, ta concentration et ta détermination à toujours donner le meilleur de toi-même. Pour continuer à progresser, pense toujours à <strong>varier tes allures</strong> d'entraînement.", 
    "4": "Attention, tu cours <strong>bien plus que d'habitude</strong> ! J'ai l'impression que tu aimes un peu trop courir en ce moment, c'est bien, mais attention : moins tu es progressif·ve, plus tu risques de te blesser.", 
    // Pour les statut
    "5": "Statut : <strong>Vacances</strong><br>Profite de cette pause pour te ressourcer, te reposer, et reviens encore plus motivé·e pour battre tous tes records !", 
    "6": "Statut : <strong>Blessure</strong><br>Prends vraiment le temps de laisser ton corps se régénérer complètement, afin de revenir encore plus fort·e.", 
    "7": "Statut : <strong>Malade</strong><br>Ne va pas t'entraîner, ton organisme a besoin de récupérer pour le moment, mais dès que tu seras guéri·e tu pourras reprendre les entraînements.", 
    "8": "Statut : <strong>Suspension</strong><br>Profite-en pour te reposer, j'analyserai tes entraînements seulement quand tu seras prêt·e !"
}
const InterpretationGoMuscu = {
    "1": "Je n'ai <strong>pas encore assez de données</strong> pour calculer ton indulgence de course. J'ai hâte que tu rentres ton premier entraînement de course dans Sprintia pour qu'on analyse ça ensemble.", 
    "2": "Tu cours <strong>moins depuis 7 jours</strong>, attention, la course à pied c'est comme la musculation ça demande de la <strong>régularité</strong>. Ton coeur, c'est un muscle, il faut le travailler pour qu'il devienne meilleur.", 
    "3": "<strong>Tu progresses</strong>, parfait ! En plus de travailler tes muscles, tu travailles ton coeur, bien joué ! Pour continuer à progresser, pense toujours à <strong>varier tes allures</strong> d'entraînement.", 
    "4": "Tu cours <strong>bien plus que d'habitude</strong> ! Fais attention, si tu continues sur ce rythme tu risques de te <strong>blesser</strong> donc réduis ton volume kilométrique.", 
    // Pour les statut
    "5": "Statut : <strong>Vacances</strong><br>Profite de cette pause pour te ressourcer, te reposer, et reviens encore plus motivé·e pour battre tous tes records !", 
    "6": "Statut : <strong>Blessure</strong><br>Prends vraiment le temps de laisser ton corps se régénérer complètement, afin de revenir encore plus fort·e.", 
    "7": "Statut : <strong>Malade</strong><br>Ne va pas t'entraîner, ton organisme a besoin de récupérer pour le moment, mais dès que tu seras guéri·e tu pourras reprendre les entraînements.", 
    "8": "Statut : <strong>Suspension</strong><br>Profite-en pour te reposer, j'analyserai tes entraînements seulement quand tu seras prêt·e !"
}

async function RecupData() {
    // recup des datas d'entrainements
    let HistoriqueWorkoutDB = await db.entrainement.toArray()

    let TableauDate = HistoriqueWorkoutDB.map(elementDB => elementDB.date)
    let TableauSport = HistoriqueWorkoutDB.map(elementDB => elementDB.sport)
    let TableauDistance = HistoriqueWorkoutDB.map(elementDB => elementDB.distance)

    // setting date
    const DateActuelle = new Date()

    let DateMoins7J = new Date()
    DateMoins7J = DateMoins7J.setDate(DateActuelle.getDate() - 7) // pour le calcul des dates il faut les mettre en timestamp enleve le nb de j ici, ça renvoie ex: 1769014250809
    DateMoins7J = new Date(DateMoins7J).toISOString() // permet de recup "2026-01-21T17:13:53.151Z"
    // On prend que ce qui nous interesse donc la premiere partie
    DateMoins7J = DateMoins7J.split("T")[0] // on obtient "2026-01-21"

    let DateMoins28J = new Date() // voir commentaire au dessus pr explication
    DateMoins28J = DateMoins28J.setDate(DateActuelle.getDate() - 28) 
    DateMoins28J = new Date(DateMoins28J).toISOString()
    DateMoins28J = DateMoins28J.split("T")[0] 

    // Initialisation pour la boucle
    let compteur = 0
    let DistanceWorkout = 0
    let Tableau7J = []
    let Tableau28J = []

    TableauDate.forEach(elementDate => {
        // recup de la distance du workout
        DistanceWorkout = TableauDistance[compteur]

        if (elementDate >= DateMoins7J) {
            if (TableauSport[compteur] == "Course") {
                if (DistanceWorkout != null) {
                    Tableau7J.push(DistanceWorkout)
                    Tableau28J.push(DistanceWorkout)
                }
            }
        } else if (elementDate >= DateMoins28J) {
            if (TableauSport[compteur] == "Course") {
                if (DistanceWorkout != null) {
                    Tableau28J.push(DistanceWorkout)
                }
            }
        }

       compteur += 1 
    });

    // init pour la somme
    let Distance7J = 0
    let Distance28J = 0

    // passons a la somme
    Tableau7J.forEach(element => {
        Distance7J += element
    });
    Tableau28J.forEach(element => {
        Distance28J += element
    });

    // Affichage dans "Distance réel sur 7J"
    document.getElementById("reponse-algo-allure").textContent = Distance7J.toFixed(1).replace(".", ",") + " km"

    return {Distance7J, Distance28J}
}

async function CalculIndulgence() {
    // Initialisation coefficient
    const CoefFourchetteDebut = [1.18, 1.15, 1.12, 1.09, 1.06]
    const CoefFourchetteFin = [1.25, 1.2, 1.15, 1.12, 1.1]

    let IndulgenceDeCourseDebut = 0
    let IndulgenceDeCourseFin = 0

    // Calibration par semaine
    let {Distance7J, Distance28J} = await RecupData()
    Distance28J = Distance28J/4

    // Analyse pour avoir la fouchette de distance conseillée (les coef sont diférent en fonction de la distance)
    if (Distance28J <= 10) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[0]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[0]
    } else if (Distance28J <= 20) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[1]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[1]
    } else if (Distance28J <= 40) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[2]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[2]
    } else if (Distance28J <= 60) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[3]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[3]
    } else {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[4]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[4]
    }

    let ResultIndulgenceCourse = IndulgenceDeCourseDebut.toFixed(1).replace(".", ",") + " - " + IndulgenceDeCourseFin.toFixed(1).replace(".", ",") + " km"

    // Affichage du résultat
    document.getElementById("reponse-algo-indulgence").innerHTML = ResultIndulgenceCourse

    return {Distance7J, Distance28J, IndulgenceDeCourseFin}
}

async function InterpretationJRM(Distance7J, Distance28J, IndulgenceDeCourseFin) {
    // Recup du champs JRM
    let InterpretationParagraphe = document.getElementById("reponse-coach-indulgence")

    // On regarde le statut du user
    let HistoriqueDB = await db.statut_analyse.toArray()
    let StatutData = HistoriqueDB.map(statutBDD => statutBDD.statut).reverse() // reverse pour inverser la liste pour l'ordre

    // Déterminer le coach choisis du user
    let CoachUserDB = await db.JRM_Coach.toArray()
    let Interpretation = InterpretationBienveillant // attribution du style de coach a utilisé
    if (CoachUserDB.length > 0) {  // si le user a enregistré qqch alors on met le style du coach qu'il a choisis
        let TableauStyleCoach = CoachUserDB.map(elementDB => elementDB.style) // recup du style
        // On check le style de coach que le user a choisi et on attribue le dico correspondant
        if (TableauStyleCoach[0] == "Bienveillant") {
            Interpretation = InterpretationBienveillant
        } else if (TableauStyleCoach[0] == "Strict-Motivant") {
            Interpretation = InterpretationStrictMotivant
        } else if (TableauStyleCoach[0] == "Copain") {
            Interpretation = InterpretationCopain
        } else {
            Interpretation = InterpretationGoMuscu
        }
    }

    // Unit 
    let LastStatutUser = ""
    if (StatutData.length > 0) { // si il y a des datas
        // on prend l'index 0 pour avoir son dernier statut
        LastStatutUser = StatutData[0]
    } else {
        // si il n'y a pas de statut on le met sur actif
        LastStatutUser = "Actif·ve"
    }

    // Attribution d'une interpretation et ajout direct dans le champs corespondant en fonction du statut 'actif' == mode normal, mode quotidien
    if (LastStatutUser == "Vacances") {
        InterpretationParagraphe.innerHTML = Interpretation["5"]
    } else if (LastStatutUser == "Blessure") {
        InterpretationParagraphe.innerHTML = Interpretation["6"]   
    } else if (LastStatutUser == "Malade") {
        InterpretationParagraphe.innerHTML = Interpretation["7"]
    } else if (LastStatutUser == "Suspendre") {
        InterpretationParagraphe.innerHTML = Interpretation["8"]
    } else if (LastStatutUser == "Actif·ve") { // en mode normal
        // en fonction du résultat des calculs, attribution d'une interpretation
        if (Distance28J <= Distance7J && Distance7J <= IndulgenceDeCourseFin) {
            InterpretationParagraphe.innerHTML = Interpretation["3"]
        } else if (Distance7J > IndulgenceDeCourseFin) {
            InterpretationParagraphe.innerHTML = Interpretation["4"]
        } else {
            InterpretationParagraphe.innerHTML = Interpretation["2"]
        }
    }
}

async function Initialisation() {
    let {Distance7J, Distance28J, IndulgenceDeCourseFin} = CalculIndulgence()
    InterpretationJRM(Distance7J, Distance28J, IndulgenceDeCourseFin)
    return
}

window.addEventListener("DOMContentLoaded", () => {
    Initialisation()
}) 