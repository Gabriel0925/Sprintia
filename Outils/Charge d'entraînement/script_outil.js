function Initialisation() {
    text = "Sprintia n'a pas encore assez de données pour analyser votre charge d'entraînement. Pas de panique vous avez juste besoin d'ajouter un entraînement pour que Sprintia analyse vos entraînements."

    let initialisationJRM  = document.getElementById("reponse-coach-indulgence")
    if (initialisationJRM) {
        initialisationJRM.textContent = text
    }
    // attendre la recup des datas
    let ChargeDatas = [124, 289, 120, 123, 534]
    let DateDatas = [
        "19 janv. 26", 
        "19 janv. 26", 
        "19 janv. 26", 
        "19 janv. 26", 
        "19 janv. 26"
    ]
     

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


window.addEventListener("DOMContentLoaded", () => {
    Initialisation()
})