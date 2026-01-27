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
    let Interpretation = "Sprintia n'a pas encore assez de données pour analyser votre charge d'entraînement. Pas de panique vous avez juste besoin d'ajouter 5 entraînements pour que Sprintia analyse vos entraînements."
    let Ratio = 0

    // Vérif si possible d'analyser
    if (AnalysePossible == false) {
        return Interpretation
    }

    // Dico des phrases
    const PhraseJRM = [
        "Vous êtes en train de perdre du niveau, attention !<br>Vous pourriez augmenter l'intensité de vos entraînements si vous voulez basculer en mode progression optimale et améliorer vos performances.",
        "Charge idéale pour améliorer vos performances !<br>Continuez comme ça pour progresser ! Gardez cette même régularité dans vos entraînements pour rester en mode progression optimale.",
        "Risque élevé de blessure !<br>Prenez quelques jours de pause pour laisser votre corps récupérer et réduire les risques de blessure."
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
    DateMoins7J = DateMoins7J.setDate(DateActuelle.getDate() - 7)
    let DateMoins28J = new Date()
    DateMoins28J = DateMoins28J.setDate(DateActuelle.getDate() - 7)

    let DateBoucle = ""

    // Recup data BDD
    let HistoriqueDB = await db.entrainement.toArray() // recup de toutes les datas

    let ChargeAigueLi = HistoriqueDB.map(data => data.charge_entrainement)
    let DateLi = HistoriqueDB.map(data => data.date)

    ChargeAigueLi.forEach(DataCharge => {
        DateBoucle = DateLi[compteur]

        if (DateBoucle >= DateMoins28J) {
            Charge.push(DataCharge)
            DateCharge.push(DateBoucle)
        }

        compteur += 1
    });

    // A completer
    let AnalysePossible = true
    if (Charge.length < 4) {
        AnalysePossible = false
    }

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