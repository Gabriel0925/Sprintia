function Score(DistanceUser) {
    // Calcul VMA + VO2max
    let DistanceM = DistanceUser*1000 // km en metres
    let DistanceMin = 1000
    let DistanceMax = 3900
    let ScoreCourse = 0

    if (DistanceM <= DistanceMin) {
        ScoreCourse = 20
    } else if (DistanceM >= DistanceMax) {
        ScoreCourse = 100
    } else {
        ScoreCourse = 20+((DistanceM-DistanceMin)/(DistanceMax-DistanceMin))*80
    }

    return ScoreCourse.toFixed(1).replace(".", ",")
}

function Zone(ScoreCourse) {
    let Score = parseFloat(ScoreCourse)
    // Initialisation
    let Result = ""
    
    // Détermination
    if (Score <= 36) {
        Result = "Débutant·e"
    } else if (Score <= 52) {
        Result = "Intermédiaire"
    } else if (Score <= 68) {
        Result = "Avancé·e"
    } else if (Score <= 84) {
        Result = "Supérieur·e"
    } else {
        Result = "Expert·e"
    }

    return Result
}

function StartNiveau() {
    // Recup datas
    let DistanceUser = parseFloat(document.getElementById("distance-user").value.trim().replace(",", "."))

    // Vérification
    if (isNaN(DistanceUser)) {
        alert("Erreur de saisie : le champs distance doit être rempli.")
        return
    }
    if (DistanceUser <= 0) {
        alert("Valeur non valide, la distance doit être supérieur à 0.")
        return
    }
    if (DistanceUser >= 7) {
        alert("Valeur non valide, la distance doit être inférieur à 7.")
        return
    }

    // Calcul
    let ScoreCourse = Score(DistanceUser)
    let Interpretation = Zone(ScoreCourse)

    // Affichage
    document.querySelector(".temps-recup").textContent = ScoreCourse
    document.querySelector(".score-imc").textContent = "Niveau : " + Interpretation
    return
}


// Ajouter des datas
async function SauvegardeNiveauCourse() {
    // Recup bouton
    let BoutonLimite1Clic = document.getElementById("button-sauvegarde-niveau")


    // Recup valeur niveau
    let NiveauCourseUser = parseFloat(document.querySelector(".temps-recup").innerHTML.trim())

    // verification
    if (NiveauCourseUser <= 0) {
        alert("Veuillez d'abord calculer votre niveau de course avant de vouloir le sauvegarder.")
        return
    }

    BoutonLimite1Clic.disabled = true // Pour empeche que le user clique 2 fois
    // signe d'enregistrement pr le user
    BoutonLimite1Clic.textContent = "Chargement..."

    // Recup de la date
    let DateNow = new Date()

    // Formatage de la date
    const DateFormatee = DateNow.toLocaleDateString("fr-FR",
        {
            day: "numeric",
            month: "short", // short permet de recup jan. a la place de janvier
            year: "2-digit" // Pr avoir que 26 au lieu de 2026
        })

    // Ajout datas
    await db.niveau_course.add({
        niveau_course_user: NiveauCourseUser,
        date: DateFormatee
    })

    // Pause
    await new Promise(r => setTimeout(r, 1000))
    // remise etat normal
    BoutonLimite1Clic.textContent = "Sauvegarder mon niveau"
    BoutonLimite1Clic.disabled = false // Réactivation du bouton

    location.reload()
}

async function RecupValueNiveauCourseGraphique() {
    // Initialisation 
    let TailleHardware = window.innerWidth
    let NbValeurRecup = -13

    // Logique de nb datas en fonction du devices
    if (TailleHardware <= 380) {
        NbValeurRecup = -4
    } else if (TailleHardware <= 520) {
        NbValeurRecup = -5
    } else if (TailleHardware <= 640) {
        NbValeurRecup = -7
    } else if (TailleHardware <= 720) {
        NbValeurRecup = -9
    } else if (TailleHardware <= 790) {
        NbValeurRecup = -10
    } else if (TailleHardware <= 1000) {
        NbValeurRecup = -11
    } 

    // Recup value Data
    const ValeurDB = await db.niveau_course.toArray()

    // map permet de retourner une nouvelle liste a partir d'une premiere liste et de prendre qu'une seule clé d'un objet
    // slice permet de découper un tableau pour en garder qu'une partie grace aux indices
    const NiveauDatas = ValeurDB.slice(NbValeurRecup).map(dataBDD => dataBDD.niveau_course_user) // -10 pr prendre les 1à dernieres valeur
    const DateDatas = ValeurDB.slice(NbValeurRecup).map(dataBDD => dataBDD.date)
    
    return {NiveauDatas, DateDatas}
}

// Récup les variables css
let RootCSS = document.documentElement
let StyleCSS = getComputedStyle(RootCSS)
// Recup variable css
let CouleurAccentContrastee = StyleCSS.getPropertyValue("--COULEUR_ACCENT_CONTRASTER")
let CouleurAccent = StyleCSS.getPropertyValue("--COULEUR_ACCENT")
let CouleurTextPrincipal = StyleCSS.getPropertyValue("--COULEUR_TEXT_PRINCIPAL")

// Pour le Graphique
async function GenererGraphique() {
    // attendre la recup des datas
    let {NiveauDatas, DateDatas} = await RecupValueNiveauCourseGraphique()
    
    if (NiveauDatas.length > 0) { // Si il y a niveau data il y a forcement date data
        // Ajout de la class pr le faire apparaitre
        document.getElementById("conteneur-graphique").classList.add("visible")

        const barCanvas = document.getElementById("barCanvas")
        const barChart = new Chart(barCanvas, {
            type:"line",
            data:{
                labels: DateDatas,
                datasets: [{
                    data: NiveauDatas,
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
                        ticks: {
                            color: CouleurTextPrincipal, 
                            font: {size: 13}
                        },
                        beginAtZero: true, // Pr commencer à 0
                    },
                    x: { // idem pour abscisse
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

GenererGraphique()