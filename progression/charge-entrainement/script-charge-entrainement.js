const statutAvailable = ["Désentraînement", "Maintien", "Productif", "Surentraînement", "Pas de statut"]
const dicoAnalyse = {
    "Bienveillant": {
        "Désentraînement": "Ta condition physique semble décliner ! Essaie d'augmenter l'intensité de tes entraînements pour basculer en statut productif et améliorer tes performances.",
        "Maintien": "Ta forme est stable ! Tu maintiens ton niveau actuel. Si tu veux franchir une étape, tu as juste à augmenter une peu ta charge d'entraînement pour atteindre la cible des 7 derniers jours.",
        "Productif": "Tu es en train de progresser, bravo ! Tes entraînements portent leurs fruits, garde cette régularité et cette discipline pour continuer de booster tes performances.",
        "Surentraînement": "Ta charge d'entraînement est significativement plus élevée que d'habitude, ton corps a du mal à suivre, il a besoin de quelques jours de repos pour récupérer."
    },
    "Strict-Motivant": {
        "Désentraînement": "Ta condition physique est en train de diminuer ! Si tu souhaites améliorer tes performances, il est plus que temps d'augmenter l'intensité de tes futurs entraînements.",
        "Maintien": "Tu es en train de stagner ! C'est suffisant pour ne pas régresser, mais si tu veux de vrais résultats essaye d'atteindre la cible des 7 derniers jours pour passer en statut productif.",
        "Productif": "Tu progresses, félicitations ! Tes entraînements portent leurs fruits, continue à mettre autant d'intensité qu'actuellement lors de tes futurs entraînements.",
        "Surentraînement": "Tu risques la blessure et blessure égale perte de niveau donc arrête de jouer avec le feu et repose-toi pendant quelques jours."
    },
    "Copain": {
        "Désentraînement": "Je suis désolé·e mais là tu abuses, tu devrais augmenter l'intensité de tes entraînements sinon tous tes efforts passés vont disparaître en quelques semaines.",
        "Maintien": "Tranquille tu maintiens ton niveau actuel, c'est une bonne chose ! Pour passer en statut productif il te suffit d'augmenter un tout petit peu ta charge d'entraînement des 7 derniers jours.",
        "Productif": "Bravo, tu progresses ! Tous tes efforts sont en train de payer, continue de t'entraîner de cette façon, ça semble être positif pour ta progression.",
        "Surentraînement": "Tu t'entraînes plus que d'habitude, ton corps semble galérer à se régénérer. Petit conseil, fais une pause de quelques jours."
    },
    "Go-muscu": {
        "Désentraînement": "Tu régresses là ! Il ne faut pas hésiter à faire 1 ou 2 répétitions en plus sur tes séries pour pouvoir augmenter ton RPE et par conséquent ta charge d'entraînement.",
        "Maintien": "Attention tu es en pleine zone de confort ! Monte un peu les poids ou rajoute plus d'intensité si tu veux aller chercher le statut productif.",
        "Productif": "GG, tu progresses, je vois que tu mets une bonne intensité pendant tes séances, continue comme ça. Tu n'as presque plus besoin de moi.",
        "Surentraînement": "Ton corps n'arrive pas à bien récupérer de tes entraînements récents, n'oublie jamais que le muscle se construit au repos, pas à la salle, repose-toi un peu avant d'aller à la salle."
    }
}

// variable globale
const dateActuelle = new Date()
let dateMoins7j = createObjetDate(7)
let dateMoins14j = createObjetDate(14)
let dateMoins21j = createObjetDate(21)
let dateMoins28j = createObjetDate(28)

async function sommeCharge7j() {
    // recup des datas des 7 derniers jours
    const historique = await db.entrainement
        .where("date")
        .aboveOrEqual(dateMoins7j)
        .toArray();

    const tableauCharge7j = historique.map(elt => elt.charge_entrainement); // création d'un tableau avec uniquement les charges des entrainements

    let chargeTotale7j = 0;
    for (const chargeLap of tableauCharge7j) {chargeTotale7j += chargeLap}; // somme de toutes les charges

    return Math.floor(chargeTotale7j);
};
async function periodeSommeCharge14j() {
    // recup des datas des 7 derniers jours
    const historique = await db.entrainement
        .where("date")
        .between(dateMoins14j, dateMoins7j, true, false) // false pour ne pas prendre la borne
        .toArray();

    const tableauCharge14j = historique.map(elt => elt.charge_entrainement); // création d'un tableau avec uniquement les charges des entrainements

    let chargeTotale14j = 0;
    for (const chargeLap of tableauCharge14j) {chargeTotale14j += chargeLap}; // somme de toutes les charges

    return Math.floor(chargeTotale14j);
};
async function periodeSommeCharge21j() {
    // recup des datas des 7 derniers jours
    const historique = await db.entrainement
        .where("date")
        .between(dateMoins21j, dateMoins14j, true, false) // false pour ne pas prendre la borne
        .toArray();

    const tableauCharge21j = historique.map(elt => elt.charge_entrainement); // création d'un tableau avec uniquement les charges des entrainements

    let chargeTotale21j = 0;
    for (const chargeLap of tableauCharge21j) {chargeTotale21j += chargeLap}; // somme de toutes les charges

    return Math.floor(chargeTotale21j);
};
async function periodeSommeCharge28j() {
    // recup des datas des 7 derniers jours
    const historique = await db.entrainement
        .where("date")
        .between(dateMoins28j, dateMoins21j, true, false) // false pour ne pas prendre la borne
        .toArray();

    const tableauCharge21j = historique.map(elt => elt.charge_entrainement); // création d'un tableau avec uniquement les charges des entrainements

    let chargeTotale21j = 0;
    for (const chargeLap of tableauCharge21j) {chargeTotale21j += chargeLap}; // somme de toutes les charges

    return Math.floor(chargeTotale21j);
};
async function sommeCharge28j() {
    // recup des datas des 7 derniers jours
    const historique = await db.entrainement
        .where("date")
        .aboveOrEqual(dateMoins28j)
        .toArray();

    const tableauCharge28j = historique.map(elt => elt.charge_entrainement); // création d'un tableau avec uniquement les charges des entrainements

    let chargeTotale28j = 0;
    for (const chargeLap of tableauCharge28j) {chargeTotale28j += chargeLap}; // somme de toutes les charges

    return [Math.floor(chargeTotale28j), tableauCharge28j.length];
};
async function algorithmeLissageWeek() {
    const requeteFirstWorkout = await db.entrainement
        .orderBy("date")
        .limit(1) // pour récupérer qu'un entrainement et vu qu'on le classe par ordre de date ça sera le premier entraî. du user
        .toArray();
    // on extraie le premier entrainement du tableau
    const firstWorkout = requeteFirstWorkout[0] || undefined;

    let jourEcouler = 28; // init avant le if

    if (firstWorkout != undefined) {
        let dateFirstWorkout = firstWorkout.date; // on a la date exemple "2026-02-18"
        let dateFirstObject = new Date(dateFirstWorkout); // on crée un object date avec la date du premier entrainement pour pouvoir faire la différence ensuite
    
        // calcul de la différence en milliseconde
        const differenceMillisecondes = dateActuelle - dateFirstObject;
        // conversion en jours
        jourEcouler = Math.floor(differenceMillisecondes/(1000*60*60*24)); // dans 1 secondes il y a 1000 ms, dans 1min il y a 60sec, dans 1heure il y a 60m et dans une journée il y a 24h
        // ---- algorithme de lissage ----
        // si le user a moins de 28 jours de datas sur SPRINTIA alors au lieu de diviser par 4 la charge chronique on divise par le nombre de semaine ou le user a de la datas
        // exemple : le premier entrainement du user est il y a 21 jours, 21j = 3 semaines donc charge_chronique/3 ou lieu de charge_chronique/4 ce qui permet d'avoir une bonne fiabilité si le user a tres peu de data dans SPRINTIA
    };

    let nbSemaine = Math.ceil(jourEcouler/7);
    if (nbSemaine<1) { // petite sécurité pour que le nombre de semaine ne soit pas inférieur à 1 semaine
        nbSemaine = 1;
    };
    if (nbSemaine>4) { // petite sécurité pour que le nombre de semaine ne soit pas supérieur à 4 semaine (=28j)
        nbSemaine = 4;
    };

    return nbSemaine;
};
function cible(chargeTotale28j, nombreWeekLissage) { // la cible permet de guider l'utilisateur pour qu'il soit en statut productif
    let cibleMin = 0.95*(chargeTotale28j/nombreWeekLissage);
    let cibleMax = 1.35*(chargeTotale28j/nombreWeekLissage);

    return [cibleMin, cibleMax];
}
function ratio(chargeTotale7j, chargeTotale28j, nombreWeekLissage) {
    return chargeTotale7j/(chargeTotale28j/nombreWeekLissage) // nombreWeekLissage c'est le nombre de semaine
};

function statut(ratioChargeUser, nbEntrainement28j) {
    let statutUser = undefined;

    // si il y a moins de 3 entrainements on ne détermine pas de statut
    if (nbEntrainement28j < 3) {return statutAvailable[4]}

    if (ratioChargeUser <= 0.8) {
        statutUser = statutAvailable[0]; // désentrainement
    } else if (ratioChargeUser <= 0.95) {
        statutUser = statutAvailable[1]; // maintien
    } else if (ratioChargeUser <= 1.35) {
        statutUser = statutAvailable[2]; // productif
    } else if (ratioChargeUser >= 1.35) {
        statutUser = statutAvailable[3]; // surentrainement
    } else {
        statutUser = statutAvailable[4]
    }

    return statutUser;
};
async function interpretation(statutUser) {
    // initialisation si il n'y a pas de données
    let analyse = `Je n'ai <strong>pas assez de données</strong> pour analyser ta charge d'entraînement. Tu as juste besoin d'ajouter au moins 
                    <strong>3 entraînements sur les 28 derniers jours</strong>. J'attends avec impatience tes premiers entraînements.`;

    // pour la partie gestion de la personnalité du coach de l'utilisateur
    let coachUserDB = await db.JRM_Coach.get(1); // si ya pas de data ça renvoie undefined
    let styleCoachUser = "Bienveillant"; // on init sur Bienveillant si le user a laisser le choix de base
    let avatarCoach = "";
    let nameCoach = "JRM Coach";
    if (coachUserDB != undefined) {
        styleCoachUser = coachUserDB.style; // attribution du coach choisi par le user à la variable nommé "styleCoachUser"

        // attribution du nom pour pouvoir l'afficher dans une autre fonction et éviter de faire une autre requete
        nameCoach = coachUserDB.nom;
        avatarCoach = coachUserDB.avatar
    };

    if (statutUser != statutAvailable[4]) {analyse = dicoAnalyse[styleCoachUser][statutUser]};
 
    return [analyse, avatarCoach, nameCoach]; // on return aussi le nom/avatar du coach pour l'afficher ensuite
};

// c'est la fonction qui permet de récupérer toutes les datas nécéssaire pour l'affichage, c'est elle qui lance toutes les fonctions
async function manageCalcul(graphique) {
    // partie nombre/chiffre
    const chargeTotale7j = await sommeCharge7j();
    const periodeChargeTotale14j = await periodeSommeCharge14j();
    const periodeChargeTotale21j = await periodeSommeCharge21j();
    const periodeChargeTotale28j = await periodeSommeCharge28j();
    const [chargeTotale28j, nbEntrainement28j] = await sommeCharge28j();

    // partie pour les calculs grace aux résults des charges des différentes semaines
    const nombreWeekLissage = await algorithmeLissageWeek(); // algo de lissage pour améliorer la progression de l'algo quand le user a peu de données
    const [cibleUserMin, cibleUserMax] = cible(chargeTotale28j, nombreWeekLissage);
    const ratioChargeUser = ratio(chargeTotale7j, chargeTotale28j, nombreWeekLissage);

    // partie francais avec le statut et l'interpretation
    const statutUser = statut(ratioChargeUser, nbEntrainement28j);
    const [analyse, avatarCoach, nameCoach] = await interpretation(statutUser);

    if (graphique == true) {
        // on balance les valeurs dans le graphique
        genererGraphiqueLine(["S-4", "S-3", "S-2", "S-1"], [periodeChargeTotale28j, periodeChargeTotale21j, periodeChargeTotale14j, chargeTotale7j])
    }
    
    return [chargeTotale7j, chargeTotale28j, nbEntrainement28j, nombreWeekLissage, cibleUserMin, cibleUserMax, ratioChargeUser, statutUser, analyse, avatarCoach, nameCoach];
};


async function displayOnScreen() {
    // recup de toutes les données
    const [chargeTotale7j, chargeTotale28j, nbEntrainement28j, nombreWeekLissage, cibleUserMin, cibleUserMax, 
        ratioChargeUser, statutUser, analyse, avatarCoach, nameCoach] = await manageCalcul(true); // true pour dire que ça lance la fonction pour le graphique

    // affichage du nom et de l'avatar du coach
    document.getElementById("nom-coach").innerHTML = avatarCoach + " " + "<strong>" + nameCoach + "</strong>"


    if (nbEntrainement28j < 3) {
        // affichage + mise en forme de l'analyse
        document.getElementById("reponse-coach-indulgence").innerHTML =  `Je n'ai <strong id="statut-ce">pas assez de données</strong> pour analyser ta charge d'entraînement. Tu as juste besoin d'ajouter au moins 
                    <strong>3 entraînements sur les 28 derniers jours</strong>. J'attends avec impatience tes premiers entraînements.`

    } else {
        // affichage + mise en forme de l'analyse
        document.getElementById("reponse-coach-indulgence").innerHTML =  `Statut : <strong id="statut-ce">${statutUser}</strong><br>${analyse}`

        // affichage de la cible et de la charge 7j et 28j
        document.getElementById("cible-charge-7j").innerHTML = "Cible : " + parseInt(cibleUserMin) + " - " + parseInt(cibleUserMax)
    }
    
    // affichage de la charge 7j et 28j
    document.getElementById("charge-7j").innerHTML = parseInt(chargeTotale7j)
    document.getElementById("charge-28j").innerHTML = parseInt(chargeTotale28j)

};


document.addEventListener("DOMContentLoaded", () => {
    const buttonBriefing = document.getElementById("button-SPRINTIA-briefing")
    if (buttonBriefing) {buttonBriefing.addEventListener("click", () => {windowsBriefing("Analyser ma CE")})}

    displayOnScreen()
})
// Pour recharger le graphique si c'est dans le BFCache
window.addEventListener("pageshow", (event) => {
    if (event.persisted) { // Si la page est dans le BFCache alors on relance le graphique
        displayOnScreen()
    }
})