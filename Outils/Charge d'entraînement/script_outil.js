// Initialisation de la variable du graphique pour que le code ce rappelle de l'ancien graphique "stockée" dans le BFCache 
// Pr éviter de superposer un graphique
let barChart = null

function ReturnDate(DateWorkout) {
    let DateEuropeen = ""

    DateWorkout = DateWorkout.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = DateWorkout[2] + "-" + DateWorkout[1] + "-" + DateWorkout[0]
    return DateEuropeen
}

async function RecupValueGraphique() {
    // Initialisation 
    let TailleHardware = window.innerWidth
    let NbValeurRecup = -13

    // Logique de nb datas en fonction du devices
    if (TailleHardware <= 520) {
        NbValeurRecup = -4
    } else if (TailleHardware <= 640) {
        NbValeurRecup = -6
    } else if (TailleHardware <= 720) {
        NbValeurRecup = -7
    } else if (TailleHardware <= 790) {
        NbValeurRecup = -8
    } else if (TailleHardware <= 1000) {
        NbValeurRecup = -10
    } 

    // Recup value Data
    const ValeurDB = await db.entrainement.toArray()    
    
    // Trier par date 
    ValeurDB.sort((element1, element2) => { // En js on peut comparer 2 dates comme des maths
        if (element1.date < element2.date) return -1
        if (element1.date > element2.date) return 1
    })

    // map permet de retourner une nouvelle liste a partir d'une premiere liste et de prendre qu'une seule clé d'un objet
    // slice permet de découper un tableau pour en garder qu'une partie grace aux indices
    const ChargeDatas = ValeurDB.slice(NbValeurRecup).map(dataBDD => dataBDD.charge_entrainement) // -10 pr prendre les 10 dernieres valeur
    const DateDatas = ValeurDB.slice(NbValeurRecup).map(dataBDD => dataBDD.date)

    // initialisation d'une liste qui contiendra les dates pour le graphique
    let ListeDate = []
    let DateEuropeen = ""

    // remise des dates au format français
    DateDatas.forEach(element => {
        DateEuropeen = ReturnDate(element)
        ListeDate.push(DateEuropeen)
    });
    
    return {ChargeDatas, ListeDate}
}

async function InterpretationJRM(ChargeAigue, ChargeChronique, AnalysePossible) {
    // Initialisation 
    let Interpretation = "Sprintia n'a pas assez de données pour analyser votre charge d'entraînement. Vous avez juste besoin d'ajouter au moins 3 entraînements sur les 28 derniers jours pour que Sprintia analyse votre charge d'entraînement."
    let Ratio = 0

    // Si l'utilisateur a fait moins de 3 entrainements sur les 28 derniers jours on analyse pas
    if (AnalysePossible == false) {
        return Interpretation // on return l'analyse par défaut
    }

    // Dico des phrases
    const PhraseJRMBienveillant = [
        "Statut : <strong>Désentraînement</strong><br>Ta condition physique semble décliner ! Essaie d'augmenter l'intensité de tes entraînements pour basculer en statut productif et améliorer tes performances.",
        "Statut : <strong>Productif</strong><br>Tu es en train de progresser, bravo ! Tes entraînements portent leurs fruits, garde cette régularité et cette discipline pour continuer de booster tes performances.",
        "Statut : <strong>Surentraînement</strong><br>Ta charge d'entraînement est significativement plus élevée que d'habitude, ton corps a du mal à suivre, il a besoin de quelques jours de repos pour récupérer."
    ]
    const PhraseJRMStrictMotivant = [
        "Statut : <strong>Désentraînement</strong><br>Ta condition physique est en train de diminuer ! Si tu souhaites améliorer tes performances, il est plus que temps d'augmenter l'intensité de tes futurs entraînements.",
        "Statut : <strong>Productif</strong><br>Tu progresses, félicitations ! Tes entraînements portent leurs fruits, continue à mettre autant d'intensité qu'actuellement lors de tes futurs entraînements.",
        "Statut : <strong>Surentraînement</strong><br>Tu risques la blessure et blessure égale perte de niveau donc arrête de jouer avec le feu et repose-toi pendant quelques jours."
    ]
    const PhraseJRMCopain = [
        "Statut : <strong>Désentraînement</strong><br>Je suis désolé mais là tu abuses, tu devrais augmenter l'intensité de tes entraînements sinon tous tes efforts passés vont disparaître en quelques semaines.",
        "Statut : <strong>Productif</strong><br>Bravo, tu progresses ! Tous tes efforts sont en train de payer, continue de t'entraîner de cette façon, ça semble être positif pour ta progression.",
        "Statut : <strong>Surentraînement</strong><br>Tu t'entraînes plus que d'habitude, ton corps semble galérer à se régénérer. Petit conseil, fais une pause de quelques jours."
    ]
    const PhraseJRGoMuscu = [
        "Statut : <strong>Désentraînement</strong><br>Tu régresses là ! Il ne faut pas hésiter à faire 1 ou 2 répétitions en plus sur tes séries pour pouvoir augmenter ton RPE et par conséquent ta charge d'entraînement.",
        "Statut : <strong>Productif</strong><br>GG, tu progresses, je vois que tu mets une bonne intensité pendant tes séances, continue comme ça. Tu n'as presque plus besoin de moi.",
        "Statut : <strong>Surentraînement</strong><br>Ton corps n'arrive pas à bien récupérer de tes entraînements récents, n'oublie jamais que le muscle se construit au repos, pas à la salle, repose-toi un peu avant d'aller à la salle."
    ] 

    const PhraseJRMStatut = [
        "Statut : <strong>Vacances</strong><br>Profite de cette pause pour te ressourcer, apprécier les moments en famille, te reposer. Mais n'oublie pas de revenir encore plus motivé·e pour battre tous tes records !",
        "Statut : <strong>Blessure</strong><br>Prends vraiment le temps de laisser ton corps se régénérer complètement, afin de revenir encore plus fort·e que jamais.",
        "Statut : <strong>Malade</strong><br>Ne va pas t'entraîner, ton organisme a besoin de récupérer pour le moment, mais dès que tu seras guéri·e tu pourras reprendre tes entraînements.",
        "Statut : <strong>Suspension</strong><br>Profite-en pour te reposer, j'analyserai tes entraînements seulement quand tu seras prêt·e !"
    ]

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

    if (LastStatutUser == "Vacances") {
        Interpretation = PhraseJRMStatut[0]

    } else if (LastStatutUser == "Blessure") {
        Interpretation = PhraseJRMStatut[1]
        
    } else if (LastStatutUser == "Malade") {
        Interpretation = PhraseJRMStatut[2]
        
    } else if (LastStatutUser == "Suspendre") {
        Interpretation = PhraseJRMStatut[3]
        
    } else if (LastStatutUser == "Actif·ve") {
        // Calcul du ratio
        ChargeChronique = ChargeChronique/4 // on met charge chronique par semaine pr le ratio
        Ratio = ChargeAigue/ChargeChronique

        // Déterminer le coach choisis du user
        let CoachUserDB = await db.JRM_Coach.toArray()
        let StyleCoachUser = PhraseJRMBienveillant // attribution du style de coach a utilisé pour l'interpretation
        if (CoachUserDB.length > 0) {  // si le user a enregistré qqch alors on met le style du coach qu'il a choisis
            let TableauStyleCoach = CoachUserDB.map(elementDB => elementDB.style) // recup du style
            // On check le style de coach que le user a choisi et on attribue le tableau correspondant
            if (TableauStyleCoach[0] == "Bienveillant") {
                StyleCoachUser = PhraseJRMBienveillant
            } else if (TableauStyleCoach[0] == "Strict-Motivant") {
                StyleCoachUser = PhraseJRMStrictMotivant
            } else if (TableauStyleCoach[0] == "Copain") {
                StyleCoachUser = PhraseJRMCopain
            } else {
                StyleCoachUser = PhraseJRGoMuscu
            }
        }

        if (Ratio <= 0.8) { // Interpretation en fonction du ratio
            Interpretation = StyleCoachUser[0]
        } else if (Ratio <= 1.35) {
            Interpretation = StyleCoachUser[1]
        } else if (Ratio >= 1.35) {
            Interpretation = StyleCoachUser[2]
        }
    }

    return Interpretation
}

async function CalculCharge() {
    // Initialisation 
    let ChargeAigue = 0
    let ChargeChronique = 0
    let compteur = 0
    let compteur2 = 0
    let Charge = []
    let DateCharge = []

    // Date recup
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

    // initialisation avt boucle
    let DateBoucle = ""

    // Recup data BDD
    let HistoriqueDB = await db.entrainement.toArray() // recup de toutes les datas

    // recup des datas sous forme de liste
    let ChargeAigueLi = HistoriqueDB.map(data => data.charge_entrainement)
    let DateLi = HistoriqueDB.map(data => data.date)

    ChargeAigueLi.forEach(DataCharge => { // parcour des datas de charge
        DateBoucle = DateLi[compteur]

        if (DateBoucle >= DateMoins28J) { // on ajoute la charge et la date de la charge entrai. dans la liste (les 28 derniers jours)
            Charge.push(DataCharge)
            DateCharge.push(DateBoucle)
        }

        compteur += 1 // maj compteur pr l'index
    });

    // ajout d'une condition pour éviter que Sprintia analyse la charge alors que l'utilisateur n'a pas assez d'entraînement sur les 28 derniers j
    // donc prepa de variable pour la fonction l'interpretationJRM()
    let AnalysePossible = true // initialisation

    if (Charge.length < 3) { // verif si on peut analyser
        AnalysePossible = false
    }

    // parcours des dates pour faire une liste avec la charge des 7 derniers jours et une autre li avec la charge des 28 derniers jours
    DateCharge.forEach(DateEntrainement => {
        if (DateEntrainement >= DateMoins7J) { 
            ChargeAigue = ChargeAigue + parseFloat(Charge[compteur2])
            ChargeChronique = ChargeChronique + parseFloat(Charge[compteur2])

        } else if (DateEntrainement >= DateMoins28J) {
            ChargeChronique = ChargeChronique + parseFloat(Charge[compteur2])

        }

        compteur2 += 1
    });

    // Arrondi
    ChargeAigue = ChargeAigue.toFixed(1).replace(".", ",")
    ChargeChronique = ChargeChronique.toFixed(1).replace(".", ",")

    return {ChargeAigue, ChargeChronique, AnalysePossible}
}

async function Initialisation() {
    // recup zone html ou il y a linterpretation JR%
    let HTMLInterpretationJRM  = document.getElementById("reponse-coach-indulgence")

    // recup des charges plus interpretation et affichage
    let {ChargeDatas, ListeDate} = await RecupValueGraphique()
    
    let {ChargeAigue, ChargeChronique, AnalysePossible} = await CalculCharge()

    if (ChargeAigue) {
        document.getElementById("charge-7j").textContent = ChargeAigue
        document.getElementById("charge-28j").textContent = ChargeChronique
    }

    // Recup + affichage de l'interpretation
    // reconversion en int car c'est devenu un str quand j'ai fais toFixed(1)
    let Interpretation = await InterpretationJRM(parseInt(ChargeAigue), parseInt(ChargeChronique), AnalysePossible)

    if (Interpretation && HTMLInterpretationJRM) {
        HTMLInterpretationJRM.innerHTML = Interpretation
    }

    // Generation Graphique
    if (ChargeDatas.length > 0) { // Si il y a chargedata data il y a forcement date data
        // Ajout de la class pr le faire apparaitre
        document.getElementById("conteneur-graphique").classList.add("visible")

        // Récup les variables css
        let RootCSS = document.documentElement
        let StyleCSS = getComputedStyle(RootCSS)
        // Recup variable css
        let CouleurAccentHover = StyleCSS.getPropertyValue("--COULEUR_ACCENT_HOVER")
        let CouleurAccent = StyleCSS.getPropertyValue("--COULEUR_ACCENT")
        let CouleurTextPrincipal = StyleCSS.getPropertyValue("--COULEUR_TEXT_PRINCIPAL")

        const barCanvas = document.getElementById("barCanvas")
        barChart = new Chart(barCanvas, {
                type:"line",
                data:{
                    labels: ListeDate,
                    datasets: [{
                        data: ChargeDatas,
                        borderColor : CouleurAccentHover, // Ligne des niveau couleur
                        backgroundColor: CouleurAccent,
                        fill: true, // Pour remplir le graphique de la couleur background
                        pointRadius: 8, // Taille du point
                        pointHoverRadius: 10,
                        pointBackgroundColor: CouleurAccentHover,
                        pointBorderWidth: 0
                    }]
                },
                options: {
                    responsive: true, // Activation du responsive
                    maintainAspectRatio: false, // Tres important pour responsive sur mobile
                    
                    plugins: {
                        legend: {
                            display: false // Masque la legende qui sert a rien dans mon cas
                        }
                    },
                    
                    scales: {
                        y: { // COuleur + taille des txt sur axe des ordonnées
                            grid: {
                                display: false // pr enlever la grille sur l'axe y (et x voir plus bas)
                            },
                            ticks: {
                                color: CouleurTextPrincipal, 
                                font: {size: 13}
                            },
                            beginAtZero: true, // Pr commencer à 0
                        },
                        x: { // idem pour abscisse
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: CouleurTextPrincipal,
                                font: {size: 13}
                            }
                        }
                    }
                }
            })
        }
}


window.addEventListener("DOMContentLoaded", () => {
    Initialisation()
})

// Pour recharger le graphique si c'est dans le BFCache
window.addEventListener("pageshow", (event) => {
    if (event.persisted) { // Si la page est dans le BFCache alors on relance le graphique
        Initialisation()
    }
})