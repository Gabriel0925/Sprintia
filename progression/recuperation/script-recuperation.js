const week = ["Di", "Lu", "Ma", "Me", "Je", "Ve", "Sa"]
// dico pour savoir quelle jour a va chercher ex on est vendredi qui est à l'index 5 dans la liste ci-dessus
// donc on doit prendre les 5 derniers jours, il nous faut Vendredi, Jeudi, Mercredi, Mardi, Lundi, Dimanche, Samedi
// et ces jours la ils sont dans ce dico avec la liste qui possède les index [5, 4, 3, 2, 1, 0, 6]
const dicoNumDay = {
    0:[0, 6, 5, 4, 3, 2, 1],
    1:[1, 0, 6, 5, 4, 3, 2],
    2:[2, 1, 0, 6, 5, 4, 3],
    3:[3, 2, 1, 0, 6, 5, 4],
    4:[4, 3, 2, 1, 0, 6, 5],
    5:[5, 4, 3, 2, 1, 0, 6],
    6:[6, 5, 4, 3, 2, 1, 0]
}

// dico pour les interpretations du coach en fonction du style de coach
const dicoInterpretation = {
    "Bienveillant": [
        "Pour analyser ta récupération du jour, j'ai besoin de <strong>7 données de récupération</strong> sur les 30 derniers jours pour pouvoir comparer ta FC repos du jour à ta moyenne habituelle des 30 derniers jours.",
        "Ta FC repos du jour est <strong>inférieure à ta moyenne habituelle</strong>, c'est un très bon signe ! Ça signifie que tu es en forme et que tu es prêt·e à affronter un entraînement intense aujourd'hui si tu le souhaites.",
        "Ta FC repos du jour est dans la <strong>moyenne habituelle</strong>. Ça signifie que tu peux faire une séance aujourd'hui (si tu le souhaites) et que ton corps a bien récupéré de tes dernières séances d'entraînement. Garde cette <strong>régularité</strong> et tu verras que les résultats seront au rendez-vous !",
        "Ta FC repos du jour indique que ton corps <strong>n'a pas encore récupéré</strong> de tes dernières séances d'entraînement. Je te conseille donc de <strong>ne pas t'entraîner</strong> aujourd'hui pour que ton corps récupère et que tu puisses retourner au plus tôt t'entraîner."
    ],
    "Strict-Motivant": [
        "Pour analyser ta récupération du jour, j'ai besoin de <strong>7 données de récupération</strong> sur les 30 derniers jours pour pouvoir comparer ta FC repos du jour à ta moyenne habituelle des 30 derniers jours.",
        "Ta FC repos du jour est <strong>plus basse que d'habitude</strong>. C'est parfait, tu es en pleine forme ! Profite de ce <strong>pic de forme</strong> pour te dépasser et mettre un max d'intensité dans ta séance du jour.",
        "Ta FC repos du jour est <strong>stable</strong>. Ton corps a fait le job pour récupérer, c'est bien. Tu peux t'entraîner normalement, mais ne t'endors pas sur tes acquis, reste bien <strong>concentré·e sur tes objectifs</strong>.",
        "Ta FC repos est <strong>trop élevée</strong>. Ton corps est fatigué·e et tu n'es pas au top. Ne joue pas avec le feu, aujourd'hui c'est <strong>repos obligatoire</strong> pour ne pas risquer la blessure, ça serait bête."
    ],
    "Copain": [
        "Pour analyser ta récupération du jour, j'ai besoin de <strong>7 données de récupération</strong> sur les 30 derniers jours pour pouvoir comparer ta FC repos du jour à ta moyenne habituelle des 30 derniers jours.",
        "Ta FC repos du jour est <strong>bien basse</strong>, franchement c'est top ! Tu pètes la forme, c'est le moment idéal pour aller te donner à fond, rien ne peut t'arrêter aujourd'hui.",
        "Ta FC repos est dans la <strong>normale</strong>. C'est cool, ça veut dire que tu as bien récupéré de tes efforts passés. Tu peux aller t'entraîner sans problème si tu avez prévu une séance aujourd'hui.",
        "Ta FC repos du jour est <strong>un peu haute</strong>. Je pense que ton corps a besoin de repos. Prends une <strong>journée de repos</strong>, pour aider ton corps à se régénérer, c'est plus prudent et ça te permettra de revenir plus fort·e !"
    ],
    "Go-muscu": [
        "Pour analyser ta récupération du jour, j'ai besoin de <strong>7 données de récupération</strong> sur les 30 derniers jours pour pouvoir comparer ta FC repos du jour à ta moyenne habituelle des 30 derniers jours.",
        "Ta FC repos est <strong>super basse</strong> ! Ton cardio est au top et ton système nerveux est prêt·e à <strong>pousser lourd</strong>. C'est le moment de tout casser à la salle, profite de cette énergie pour aller à <strong>l'échec</strong> !",
        "Ta FC repos est <strong>stable</strong>, c'est carré ! Ton corps a bien récupéré, tu peux aller t'entraîner sereinement. N'oublie pas, la <strong>régularité</strong> c'est ce qui te permettra de prendre du muscle sur le long terme.",
        "Ta FC repos est <strong>un peu haute</strong> aujourd'hui. Ton corps galère à récupérer. N'oublie pas que le <strong>muscle se construit quand tu te reposes</strong> et aujourd'hui, ça semble être le jour parfait pour te reposer."
    ]
}

// date
let numeroDuJour = new Date()
numeroDuJour = numeroDuJour.getDay() // pour récupérer le numéro de la semaine, exemple 0 pour Dimanche
let listeIndex7derniersJours = dicoNumDay[numeroDuJour] // recup de la liste dans le dico
listeIndex7derniersJours = listeIndex7derniersJours.reverse() // on inverse la liste pour que ça soit dans le bon ordre pour le graphique
let thisWeekForGraphic = []

// parcours de la liste et ajout des jours en fonction de l'index de la liste hérité du dicoNumDay
listeIndex7derniersJours.forEach(element => {
    thisWeekForGraphic.push(week[element])
});

let dateToday = createObjetDate(0)
let dateMoins7J =createObjetDate(7)
let dateMoins30J = createObjetDate(30)

function returnDate(dateRecup) {
    let DateEuropeen = ""

    dateRecup = dateRecup.split("-")
    // Inversion de la date de "2026-01-12" à "12-01-2026"
    DateEuropeen = dateRecup[2] + "-" + dateRecup[1] + "-" + dateRecup[0]
    return DateEuropeen
}

async function jrmCoach() {
    // maj du contenu de certaines partie de la page
    let zoneReponseCoach = document.getElementById("reponse-coach")
    let zoneNameCoach = document.getElementById("nom-coach")
    
    let interpretation = dicoInterpretation["Bienveillant"][0] // quand il n'y a pas de data
    zoneReponseCoach.innerHTML = interpretation // init
    
    // pr le nom du coach
    let CoachUserDB = await db.JRM_Coach.toArray()
    if (CoachUserDB.length > 0) { // Si il y a des datas on recup le nom et l'avatar et on l'affiche dans le coach JRM
        let NomCoach = CoachUserDB.map(elementDB => elementDB.nom)
        let AvatarCoach = CoachUserDB.map(elementDB => elementDB.avatar)
                
        zoneNameCoach.innerHTML =  AvatarCoach + " " + "<strong>" + NomCoach + "</strong>"
    }

    // recup des 30 derniers jours de datas
    const historiqueData30J = await db.recuperation.where("date").aboveOrEqual(dateMoins30J).toArray()

    if (historiqueData30J.length > 0) {
        // calcul de la moy des 30 derniers jours
        // init pour la boucle
        let sommeFcRepos = 0
        historiqueData30J.forEach(element => {
            sommeFcRepos += element.fc_repos
        });
        let moyenne30J = Math.round(sommeFcRepos/historiqueData30J.length)

        // affichage de la moyenne des 30 derniers jours
        document.getElementById("fc-repos-moyenne-30j").innerHTML = `${moyenne30J}  <small>bpm</small>`

        // on regarde si on peut mettre à jour la FC repos du user
        const profilDB = await db.profil.toArray()
        if (profilDB.length > 0) { // si le user a configurer son profil alors on peut peut etre faire la maj auto
            let fcReposProfilUser = profilDB[0].fc_repos

            if (fcReposProfilUser != moyenne30J) {
                let majAutoProfil = localStorage.getItem("majAutoProfil") || "True" // si pas de data alors on met undefined

                // si la maj auto est activé alors on met à jour la FC repos du profil sinon on ne fait rien
                if (majAutoProfil == "True") { // si le toggle maj auto profil est activé alors on met à jour
                    // avant de modifier il faut vérifier si l'id 1 a déja des datas si oui on update sinon on fais rien
                    let profilExists = await db.profil.get(1)

                    if (profilExists) {
                        await db.profil.put({
                            id: 1,
                            sexe: profilDB[0].sexe,
                            age: profilDB[0].age,
                            taille: profilDB[0].taille,
                            poids: profilDB[0].poids,
                            fc_repos: moyenne30J
                        })
                    }

                }
            }

        }

        if (historiqueData30J.length >= 7) {
            // recup de la FC repos du jour
            let fcReposToday = await db.recuperation.where("date").aboveOrEqual(dateToday).toArray()
            if (fcReposToday.length > 0) {
                fcReposToday = fcReposToday[0].fc_repos

                // on recup le style de coach du user
                let styleCoach = await db.JRM_Coach.toArray()
                if (styleCoach.length <= 0) {
                    styleCoach = "Bienveillant"
                } else {
                    styleCoach = styleCoach[0].style
                }

                // calcul de l'écart
                let ecartToday = parseInt(fcReposToday-moyenne30J)

                if (ecartToday <= -3) { // inf ou egale à -3
                    interpretation = dicoInterpretation[styleCoach][1]
                } else if (ecartToday >= 4) { // si ecart est entre ]-3;4] -> normale
                    interpretation = dicoInterpretation[styleCoach][3]
                } else { // si plus grand que 4 alors fatigue ou surentrainement
                    interpretation = dicoInterpretation[styleCoach][2]
                }

                zoneReponseCoach.innerHTML = interpretation

            }
        }
    } else {
        document.getElementById("fc-repos-moyenne-30j").innerHTML = `--  <small>bpm</small>`
    }

    return
}
async function remplissageTableau() {
    // recup du tableau et de toutes les datas dans l'ordre pour remplir le tableau
    let tableauHistorique = document.getElementById("tableau-historique")
    let dateMoins7J = createObjetDate(7) // appelle à la fonction
    const historiqueDataUser = await db.recuperation.where("date").above(dateMoins7J).toArray()

    // Pr vider toutes les lignes du tableau (sauf lentete)
    document.querySelector("tbody").innerHTML = ""

    historiqueDataUser.reverse() // on inverse pour que ça soit du plus récent au plus ancien

    if (historiqueDataUser.length <= 0) {
        // on cache le tableau
        tableauHistorique.style.display = "none"
        // on fais apparaitre le message comme quoi SPRINTIA n'a pas encore assez de données
        document.getElementById("aucune-data").style.display = "flex"
        document.querySelector(".carousel.table").style.display = "none"

        const allDataRecup = await db.recuperation.toArray()
        if (allDataRecup.length <= 0) {
            document.querySelector(".container-center-marge").style.display = "none"
        }

        return
    }

    historiqueDataUser.forEach(elt => {
        // Structure du tableau
        // creation d'une nouvelle ligne
        let newline = tableauHistorique.insertRow()
        // creation des colonnes
        let colonneDate = newline.insertCell(0)
        let colonneFcRepos = newline.insertCell(1)
        let colonneAction = newline.insertCell(2)

        // remplissage
        colonneDate.textContent = returnDate(elt.date)
        colonneFcRepos.textContent = elt.fc_repos

        let btnModifier = document.createElement("button")
        btnModifier.textContent = "Modifier"
        colonneAction.appendChild(btnModifier)
        // Ajout de la class
        btnModifier.classList.add("table")

        // ajout d'un bouton supprimer et modifier
        let btnSupprimer = document.createElement("button")
        btnSupprimer.textContent = "Supprimer"
        colonneAction.appendChild(btnSupprimer)
        // Ajout de la class
        btnSupprimer.classList.add("table")

        // on lie les boutons à des actions
        btnSupprimer.addEventListener("click", async () => {
            // confirmation avant suppression
            if (confirm("Supprimer votre récupération du " + returnDate(elt.date) + " ?")) {
                await db.recuperation.delete(elt.id)
                await newline.remove() // supprimer la ligne
                // maj de la fonction pour recharger les datas sans recharger la page
                await init("graph")

                let dataTableau = document.querySelectorAll("td") // Recup des lignes pour savoir quand il faut cacher le tableau
                let tableau = document.getElementById("tableau-historique") // recup du tableau

                if (dataTableau.length <= 0) {
                    // On cache tout
                    tableau.style.display = "none"
                    // on fais apparaitre le message comme quoi SPRINTIA n'a pas encore assez de données
                    document.getElementById("aucune-data").style.display = "flex"
                    document.querySelector(".carousel.table").style.display = "none"

                    const allDataRecup = await db.recuperation.toArray()
                    if (allDataRecup.length <= 0) {
                        document.querySelector(".container-center-marge").style.display = "none"
                    }
                } 

                // transmission de l'info au user
                logoDynamique("Supprimé 🗑️")
            }
        })
        btnModifier.addEventListener("click", async () => {
            // on l'envoie à ajouter-recup mais avec un param
            window.location.href = `ajouter-recuperation.html?edit=${elt.id}`
        })

    });
    
    return
}
async function init(role) {
    // recup des datas pour le graphique
    const historique = await db.recuperation.where("date").above(dateMoins7J).toArray()
    
    // init pr la boucle
    let dicoDataFormatee = {} // structure "Jour":FC_repos exemple : "M":43
    historique.forEach(element => {
        let dateElt = new Date(element.date) // création d'un objet en fonction de la date de la données
        let numDateElt = dateElt.getDay() // recup du jour exemple: Mercredi -> 2

        // week[numDateElt] pour récupérer un jour à la place du numéro exemple pour mercredi = 2 -> M
        dicoDataFormatee[week[numDateElt]] = element.fc_repos
    });

    // pour faire une copie du tableau et non pas modifier le tableau
    let tableauFcRepos = thisWeekForGraphic.slice() // exemple : ['D', 'L', 'M', 'M', 'J', 'V', 'S']
    // parcours du dico
    Object.entries(dicoDataFormatee).forEach(([day, fcRepos]) => { // day = par ex: D pour Dimanche
        if (thisWeekForGraphic.includes(day)) { // si le day est dans le tableau des 7 derniers jours pr le graphique alors
            // on garde en mémoire sa position
            let positionDay = thisWeekForGraphic.indexOf(day)
            // et on remplace dans notre nouveau tableau qui copie le "thisWeekForGraphic" exemple :
            // on passe de ça ['D', 'L', 'M', 'M', 'J', 'V', 'S'] à ça ['D', 'L', 'M', 'M', 'J', 'V', 34] donc on remplace par la FC repos
            tableauFcRepos[positionDay] = fcRepos
        }
    });

    let tableauFcReposComplete = [] // nouveau tableau qui remplacera le "tableauFcRepos" par la suite
    tableauFcRepos.forEach(element => { // parcours du tableau
        // on convertit en number au moins si c'est pas un chiffre la valeur sera en isNan et donc on pourra mettre 0 à la place du lettre
        element = Number(element) 

        if (isNaN(element)) {
            tableauFcReposComplete.push(0)
        } else {
            tableauFcReposComplete.push(Number(element))
        }
    });
    // en gros la boucle si dessus permet de passer de ça ['D', 'L', 'M', 'M', 'J', 'V', 34] à [0, 0, 0, 0, 0, 0, 34]

    // mise à jour de la valeur de la FC repos du jour 
    let fcReposToday = await db.recuperation.where("date").aboveOrEqual(dateToday).toArray()
    if (fcReposToday.length > 0) {
        fcReposToday = fcReposToday[0].fc_repos
    } else {
        fcReposToday = "--"
    }
    document.getElementById("fc-repos-today").innerHTML = `${fcReposToday}  <small>bpm</small>`

    // generation du graphique
    genererGraphiqueLine(thisWeekForGraphic, tableauFcReposComplete)

    // si le role est init ça veut dire que la page vient de se charger donc on remplit le tableau
    // par contre si le user supprime une ligne du tableau on ne recharge pas le tableau
    if (role == "init") {
        // remplissage du tableau
        await remplissageTableau()
    }

    // pour l'interpretation et changer le nom du coach
    await jrmCoach()

    return
}


document.addEventListener("DOMContentLoaded", () => {
    const visuelInformation = document.getElementById("aucune-data")
    if (visuelInformation) {visuelInformation.style.display="none"}

    const buttonPlus = document.getElementById("button_plus")
    if (buttonPlus) {buttonPlus.addEventListener("click", () => {window.location.href = 'historique-recuperation.html'})}

    const buttonBriefing = document.getElementById("button-SPRINTIA-briefing")
    if (buttonBriefing){buttonBriefing.addEventListener("click", () => {windowsBriefing('Analyser ma récupération')})}

    init("init")
})
// Pour recharger le graphique si c'est dans le BFCache
window.addEventListener("pageshow", (event) => {
    if (event.persisted) { // Si la page est dans le BFCache alors on relance le graphique
        init("bfcache")
    }
})