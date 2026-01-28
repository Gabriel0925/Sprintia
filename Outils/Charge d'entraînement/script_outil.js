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
    
    return {ChargeDatas, DateDatas}
}

function InterpretationJRM(ChargeAigue, ChargeChronique, AnalysePossible) {
    // Initialisation 
    let Interpretation = "Sprintia n'a pas assez de données pour analyser votre charge d'entraînement. Vous avez juste besoin d'ajouter au moins 3 entraînements sur les 28 derniers jours pour que Sprintia analyse vos charge d'entraînement."
    let Ratio = 0

    // Si l'utilisateur a fait moins de 3 entrainements sur les 28 derniers jours on analyse pas
    if (AnalysePossible == false) {
        return Interpretation // on return l'analyse par défaut
    }

    // Dico des phrases
    const PhraseJRM = [
        "Statut : <strong>Désentraînement</strong><br>Votre condition physique semble décliner ! Essayez d'augmenter l'intensité de vos entraînements pour basculer en statut productif et améliorer vos performances.",
        "Statut : <strong>Productif</strong><br>Vous êtes entrain de progresser, bravo ! Vos entraînements portent leurs fruits, gardez cette régularité et cette discipline pour continuer de booster vos performances.",
        "Statut : <strong>Surentraînement</strong><br>Votre charge d'entraînement est significativement plus élevée que d'habitude, votre corps a du mal à suivre. Votre corps a besoin de quelques jours de repos pour récupérer."
    ]

    // Calcul du ratio
    ChargeChronique = ChargeChronique/4 // on met charge chronique par semaine pr le ratio
    Ratio = ChargeAigue/ChargeChronique

    if (Ratio <= 0.8) {
        Interpretation = PhraseJRM[0]
    } else if (Ratio <= 1.35) {
        Interpretation = PhraseJRM[1]
    } else if (Ratio >= 1.35) {
        Interpretation = PhraseJRM[2]
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
    let {ChargeDatas, DateDatas} = await RecupValueGraphique()
    
    let {ChargeAigue, ChargeChronique, AnalysePossible} = await CalculCharge()

    if (ChargeAigue) {
        document.getElementById("charge-7j").textContent = ChargeAigue
        document.getElementById("charge-28j").textContent = ChargeChronique
    }

    // Recup + affichage de l'interpretation
    // reconversion en int car c'est devenu un str quand j'ai fais toFixed(1)
    let Interpretation = InterpretationJRM(parseInt(ChargeAigue), parseInt(ChargeChronique), AnalysePossible)

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
        let CouleurAccentContrastee = StyleCSS.getPropertyValue("--COULEUR_ACCENT_CONTRASTER")
        let CouleurAccent = StyleCSS.getPropertyValue("--COULEUR_ACCENT")
        let CouleurTextPrincipal = StyleCSS.getPropertyValue("--COULEUR_TEXT_PRINCIPAL")

        const barCanvas = document.getElementById("barCanvas")
        const barChart = new Chart(barCanvas, {
                type:"line",
                data:{
                    labels: DateDatas,
                    datasets: [{
                        data: ChargeDatas,
                        borderColor : CouleurAccentContrastee, // Ligne des niveau couleur
                        backgroundColor: CouleurAccent,
                        fill: true, // Pour remplir le graphique de la couleur background
                        pointRadius: 7, // Taille du point
                        pointHoverRadius: 10,
                        pointBackgroundColor: CouleurAccentContrastee,
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