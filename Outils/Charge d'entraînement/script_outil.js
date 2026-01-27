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

async function Initialisation() {
    text = "Sprintia n'a pas encore assez de données pour analyser votre charge d'entraînement. Pas de panique vous avez juste besoin d'ajouter un entraînement pour que Sprintia analyse vos entraînements."

    let initialisationJRM  = document.getElementById("reponse-coach-indulgence")
    if (initialisationJRM) {
        initialisationJRM.textContent = text
    }


    // attendre la recup des datas
    let {ChargeDatas, DateDatas} = await RecupValueGraphique()

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