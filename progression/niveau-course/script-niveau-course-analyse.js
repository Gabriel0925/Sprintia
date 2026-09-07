// variable pour les 2 premieres fonctions
let distanceMin = 1000
let distanceMax = 3900
function calculLevelRun(distanceUser) {
    // Calcul VMA + VO2max
    let distanceM = distanceUser*1000 // km en metres

    if (distanceM <= distanceMin) {
        return 20
    } else if (distanceM >= distanceMax) {
        return 100
    } else {
        return Number((20+((distanceM-distanceMin)/(distanceMax-distanceMin))*80).toFixed(1))
    }
}
function calculDistanceLevel(levelRun) {
    if (levelRun == "--") { // quand il n'y a pas de datas
        return "--"
    } else {
        // on sait que : 20+((distanceM-distanceMin)/(distanceMax-distanceMin))*80 = levelRun
        // on veut la var nommé distanceM donc on isole cette variable dans l'équation et on trouve
        return Math.floor(distanceMin+((levelRun-20)/80)*(distanceMax-distanceMin)) // la distance est en metres pr info
    }
}

async function lastLevel() {
    const tableauLastLevel = await db.niveau_course
        .orderBy("date")
        .reverse() // pour recup le dernier level et non le premier
        .limit(1) // on limite à 1 pour récup le dernier level
        .toArray()

    if (tableauLastLevel.length >= 1) {
        return tableauLastLevel[0].niveau_course_user // on return que le niveau de course
    } else {
        return "--"
    }
}
function zoneLevel(LevelUser) {
    const dicoZone = {36:"Débutant·e", 52:"Intermédiaire", 68:"Avancé·e", 84:"Supérieur·e", 100:"Expert·e"}

    if (LevelUser != "--") {
        for (const [key, value] of Object.entries(dicoZone)) {
            if (LevelUser <= key) {
                return value
            }
        }
    } else { // quand il n'y a pas de données de dernier niveau
        return "Pas assez de données"
    }
}

function estimateVMA(distancelastLeverUser) {
    if (distancelastLeverUser != "--") {
        // on part de la vitesse moy et on ajoute un facteur de 90% car le user ne peut pas maintenir sa VMA à 100% sur 12 min
        return Number(((distancelastLeverUser/200)/0.9).toFixed(1)) // on prend un chiffre apres la virgule et on remet en nombre pour les calculs suivants
    } else { // quand il n'y a pas de datas
        return "--"
    }
}
function estimateVO2max(vmaEstimee) {
    if (vmaEstimee != "--") {return Number((vmaEstimee*3.5).toFixed(1))} // calcul que si il y a des datas
    else {return "--"}
}
async function estimateRFTPW(vo2maxEstimee) {
    if (vo2maxEstimee != "--") { // calcul que si il y a des datas
        let rFTPw = (vo2maxEstimee*0.82)/11.5 // formule de Stryd ou les équations de Daniels & Scardina
        // détermination du poid du user
        const dataProfilUser = await db.profil.toArray()
        let poidsUser = 0
        // si le user a configuré son profil alors on pourra calculer le rFTPw si il l'a pas config alors ça fera rFTPw*0 et si c'est égale à 0 on affiche "--"
        if (dataProfilUser.length > 0) {poidsUser = Number(dataProfilUser[0].poids)}

        rFTPw = Number((rFTPw*poidsUser).toFixed(1))
        if (rFTPw == 0) {return "--"} else {return rFTPw}
    } else {return "--"}
}
function estimateAllureSeuil(vmaEstimee) {
    if (vmaEstimee == "--") {return "--:--"} // quand il n'y a pas de datas on return la valeur de base du HTML

    // on prend 85% de la VMA estimée (c'est le standart dans les plans d'entrainement)
    const vitesseSeuil = vmaEstimee*0.85 // en km/h
    const tempsDecimal = 60/vitesseSeuil

    // on convertit le temps decimal en min:sec
    const minAllureSeuil = Math.floor(tempsDecimal) // on recup la partie entiere du temps décimal
    let secAllureSeuil = Math.round((tempsDecimal-minAllureSeuil)*60) // on obtient les secondes
    secAllureSeuil = secAllureSeuil.toString().padStart(2, "0") // pour obtenir 09 au lieu de 9
    
    return minAllureSeuil+":"+secAllureSeuil
}

function predicteurCourse(vmaEstimee) {
    if (vmaEstimee == "--") {return ["--", "--", "--", "--", "--", "--", "--"]} // quand il n'y a pas de datas on return la valeur de base du HTML on return 7x "--" car il y a 7 prédictions
    const coef = [0.97, 0.84, 0.80, 0.74, 0.68] // coef pour un coureur équillibré
    
    // estimation des temps de course
    let time400m = 0.4/(vmaEstimee*coef[0]) // "(vmaEstimee*coef[0])" pour calculer la vitesse moyenne
    let time800m = 0.8/(vmaEstimee*coef[0])
    let time1km = 1/(vmaEstimee*coef[0])
    let time5km = 5/(vmaEstimee*coef[1]) //
    let time10km = 10/(vmaEstimee*coef[2])
    let timeSemiMarathon = 21.0975/(vmaEstimee*coef[3])
    let timeMarathon = 42.195/(vmaEstimee*coef[4])

    const tableauTime = [time400m*60, time800m*60, time1km*60, time5km*60,
        time10km*60, timeSemiMarathon*60, timeMarathon*60] // conversion des secondes en minutes

    let tableauTimePredict = []
    tableauTime.forEach(element => {
        tableauTimePredict.push(dureeFormatee(element, null))
    });

    return tableauTimePredict
}

function conversionAllure(zone){    
    // extraction des minutes, secondes
    let minutes = Math.floor(zone)
    let secondes = Math.round((zone-minutes)*60)
    if (secondes === 60) {secondes = 0; minutes += 1}

    return [minutes, secondes]
}

const containerBaliseTranchePuissance = document.querySelector(".container-box.zone-puissance")
const baliseTranchePuissance = document.querySelectorAll(".container-box.zone-puissance .small-zone-result-result")

const containerBaliseTrancheAllure = document.querySelector(".container-box.zone-allure")
const baliseTrancheAllure = document.querySelectorAll(".container-box.zone-allure .small-zone-result-result")
function zonesAllure(vmaEstimee) {
    containerBaliseTranchePuissance.style.display = "none"
    containerBaliseTrancheAllure.style.display = "flex"

    if (vmaEstimee == "--") {
        // renvoie ça si il ya des datas : '16 km/h' si ya pas de datas (et donc que le user n'a pas config son profil) "--"
        vmaEstimee = document.getElementById("vma-estimee").textContent // '16 km/h'

        if (vmaEstimee != "--  km/h") {
            vmaEstimee = Number(vmaEstimee.split(" ")[0].replace(",", ".")) // 16 en number
        } else {
            return
        }
    }

    if (vmaEstimee == "--") {return} // quand il n'y a pas de datas on return rien car ça laisse la base qu'il y avait dans le HTML

    // init des variables pr la boucle
    const tableauCoef = [0.65, 0.75, 0.85, 0.95, 0.95] // coef pr la boucle (même coef pour les 2 derniers elt car par ex : zone 6 = 346-384W/zone 7 = > 348W)
    let memoireLastLap = 0 // pour garder en mémoire le resultat du tour d'avant de la boucle for
    let memoire2LastLap = 0
    let compteur = 0 // pour chercher dans le tableau de balise tranche et mettre le resultat au bon endroit

    for (const elt of tableauCoef) { // parcour du tableau
        if (memoire2LastLap == -1) { // si on a les secondes qui sont egale à moins 1 exemple : 5:-1
            memoireLastLap = memoireLastLap-1 // on eleve 1 au min ce qui donne 4:-1
            memoire2LastLap = 59 // on remplace -1 par 59 donc -> 4:59
        }

        if (compteur == tableauCoef.length-1) { // pr le dernier on affiche diféremment
            const resultFinZone = 60/(vmaEstimee*elt) // calcul de la fin de la zone concernée grâce au tableau
            let minutesSecondesZone = conversionAllure(resultFinZone)
            // Recup des datas qui sont dans une liste
            let minutesZone = minutesSecondesZone[0]
            let secondesZone = minutesSecondesZone[1]
              
            const resultClean = "< " + memoireLastLap + ":" + (memoire2LastLap+1).toString().padStart(2, "0") // mise en forme différente
            baliseTrancheAllure[compteur].textContent = resultClean // affichage

            break // on arrete la boucle car c'était le dernier coef
        }

        const resultFinZone = 60/(vmaEstimee*elt) // calcul de la fin de la zone concernée grâce au tableau
        let minutesSecondesZone = conversionAllure(resultFinZone)
        // Recup des datas qui sont dans une liste
        let minutesZone = minutesSecondesZone[0]
        let secondesZone = minutesSecondesZone[1]

        if (compteur == 0) {
            baliseTrancheAllure[compteur].textContent = "> " + minutesZone + ":" + secondesZone.toString().padStart(2, "0")
        } else {
            // préparation d'un résultat clean pour l'afficher par la suite
            const resultClean = memoireLastLap + ":" + memoire2LastLap.toString().padStart(2, "0") + " - " + minutesZone + ":" + secondesZone.toString().padStart(2, "0")
            baliseTrancheAllure[compteur].textContent = resultClean // affichage 
        }

        memoireLastLap = minutesZone // mise en mémoire de ce tour pour le tour suivant
        memoire2LastLap = secondesZone-1 // mise en mémoire 2 de ce tour pour le tour suivant
        compteur+=1 // incrémentation
    }
}
function zonesPuissance(rFTPwEstimee) {
    containerBaliseTranchePuissance.style.display = "flex"
    containerBaliseTrancheAllure.style.display = "none"

    if (rFTPwEstimee == "--") {
        // renvoie ça si il ya des datas : '255,6  W' si ya pas de datas (et donc que le user n'a pas config son profil) "--"
        rFTPwEstimee = document.getElementById("rFTPw-estimee").textContent // '255,6  W'

        if (rFTPwEstimee != "--  W") {
            rFTPwEstimee = Number(rFTPwEstimee.split(" ")[0].replace(",", ".")) // 255.6 en number
        } else {
            alert("Pour accéder à vos zones de puissance, veuillez configuer votre profil ou ajouter des données dans le niveau de course.")
            // remise à 0 de cette partie de la page pour pas que le user accede au zone de puissance alors qu'il n'a pas config son profil
            containerBaliseTranchePuissance.style.display = "none"
            containerBaliseTrancheAllure.style.display = "flex"
            document.getElementById("segmented-button-allure").click()
            return
        }
    }

    // init des variables pr la boucle
    const tableauCoef = [0.8, 0.88, 0.95, 1.05, 1.15, 1.28, 1.28] // coef pr la boucle (même coef pour les 2 derniers elt car par ex : zone 6 = 346-384W/zone 7 = > 348W)
    let memoireLastLap = 0 // pour garder en mémoire le resultat du tour d'avant de la boucle for
    let compteur = 0 // pour chercher dans le tableau de balise tranche et mettre le resultat au bon endroit

    for (const elt of tableauCoef) { // parcour du tableau
        if (compteur == tableauCoef.length-1) { // pr le dernier on affiche diféremment
            const resultClean = "> " + memoireLastLap // mise en forme différente
            baliseTranchePuissance[compteur].textContent = resultClean // affichage
            break // on arrete la boucle car c'était le dernier coef
        }

        const resultFinZone = Math.round(rFTPwEstimee*elt) // calcul de la fin de la zone concernée grâce au tableau
        const resultClean = (memoireLastLap+1) + " - " + resultFinZone // préparation d'un résultat clean pour l'afficher par la suite
        baliseTranchePuissance[compteur].textContent = resultClean // affichage 

        memoireLastLap = resultFinZone // mise en mémoire de ce tour pour le tour suivant
        compteur+=1 // incrémentation
    }
}

async function manageAnalyse() {
    // calcul du niveau et de la distance du dernier niveau de course sur user
    const lastLevelUser = await lastLevel()
    const zoneLevelUser = zoneLevel(lastLevelUser)
    const distancelastLeverUser = calculDistanceLevel(lastLevelUser)

    // calcul de la VMA, VO2max et allure seuil estimée
    const vmaEstimee = estimateVMA(distancelastLeverUser)
    const vo2maxEstimee = estimateVO2max(vmaEstimee)
    const rFTPwEstimee = await estimateRFTPW(vo2maxEstimee)
    const allureSeuilEstimee = estimateAllureSeuil(vmaEstimee)

    // prédiction des temps de course de l'utilisateur pour le 5,10,21,42km
    const [temps400m, temps800m, temps1km, temps5km, temps10km, 
        tempsSemiMarathon, tempsMarathon] = predicteurCourse(vmaEstimee)

    // calcul et affichage des zones d'allure pour gagner en perf et éviter de refaire une boucle for par la suite
    zonesAllure(vmaEstimee)

    return [lastLevelUser, zoneLevelUser, distancelastLeverUser, vmaEstimee, vo2maxEstimee, rFTPwEstimee, allureSeuilEstimee, 
        temps400m, temps800m, temps1km, temps5km, temps10km, tempsSemiMarathon, tempsMarathon]
}

async function displayOnScreen() {
    // recup des datas
    const [lastLevelUser, zoneLevelUser, distancelastLeverUser, vmaEstimee, vo2maxEstimee, rFTPwEstimee, allureSeuilEstimee, 
        temps400m, temps800m, temps1km, temps5km, temps10km, tempsSemiMarathon, tempsMarathon] = await manageAnalyse()

    // affichage du dernier niveau de course et de la zone
    document.getElementById("last-level-run").innerHTML = lastLevelUser.toString().replace(".", ",")
    document.getElementById("zone-last-level-run").innerHTML = zoneLevelUser

    // affichage des métriques de base
    document.getElementById("vma-estimee").innerHTML = vmaEstimee.toString().replace(".", ",") + "  <small>km/h</small>"
    document.getElementById("vo2max-estimee").innerHTML = vo2maxEstimee.toString().replace(".", ",") 
    document.getElementById("rFTPw-estimee").innerHTML = rFTPwEstimee.toString().replace(".", ",") + "  <small>W</small>"
    document.getElementById("allure-seuil-estimee").innerHTML = allureSeuilEstimee + "  <small>/km</small>"

    // affichage des temps prédit pour les différentes distance
    document.getElementById("time-400m").innerHTML = temps400m
    document.getElementById("time-800m").innerHTML = temps800m
    document.getElementById("time-1km").innerHTML = temps1km
    document.getElementById("time-5km").innerHTML = temps5km
    document.getElementById("time-10km").innerHTML = temps10km
    document.getElementById("time-semi-marathon").innerHTML = tempsSemiMarathon
    document.getElementById("time-marathon").innerHTML = tempsMarathon

    if (document.getElementById("rFTPw-estimee").textContent == "--  W") {
        document.getElementById("rFTPw-estimee").addEventListener("click", () => {
            alert("Pour avoir accès à votre rFTPw veuillez configurer votre profil.")
        });
    }

}

document.addEventListener("DOMContentLoaded", () => {
    const containerBoxAllure = document.querySelector(".container-box zone-allure")
    if (containerBoxAllure) {containerBoxAllure.style.display='none'}

    const segmentedButtonPuissance = document.getElementById("segmented-button-watts")
    if (segmentedButtonPuissance) {
        segmentedButtonPuissance.addEventListener("click", () =>{
            document.getElementById('segmented-button-watts').classList.add('actif')
            document.getElementById('segmented-button-allure').classList.remove('actif')
            zonesPuissance('--')
        })
    }
        
    const segmentedButtonAllure = document.getElementById("segmented-button-allure")
    if (segmentedButtonAllure) {
        segmentedButtonAllure.addEventListener("click", () =>{
            document.getElementById('segmented-button-watts').classList.remove('actif')
            document.getElementById('segmented-button-allure').classList.add('actif')
            zonesAllure('--')
        })
    }

    const segmentedButtonEvolution = document.getElementById("segmented-button-evolution")
    if (segmentedButtonEvolution) {segmentedButtonEvolution.addEventListener("click", () =>{window.location.href = 'niveau-course-evolution.html'})}
    
    verificationURL() // pour lancer le logo dynamique quand le user a enregistré un niveau de course
    displayOnScreen()
})