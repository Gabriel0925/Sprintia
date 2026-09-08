let promptForIA = undefined
const buttonFonction  = {
    "Analyser mes tendances": promptTendances,
    "Analyser ma CE": promptCE,
    "Analyser mon indulgence": promptIndulgence,
    "Analyser ma récupération": promptRecuperation,
    "Approfondir l'analyse": promptAnalyseEntrainement,
    "Demander à Vibe": promptDiscussion
}

async function windowsBriefing(textInButton) {
    document.querySelector("section.background-SPRINTIA-briefing").style.display = "flex"
    document.querySelector("div.windows-SPRINTIA-briefing").classList.add("open")
    document.querySelector("body").classList.add("briefing-open") 
    document.querySelector("main").classList.add("briefing-open")

    promptForIA = await buttonFonction[textInButton]() // on créer le prompt
    if (promptForIA != undefined) { // si le début de prompt a été généré
        promptForIA = await addPromptContrainte(promptForIA) // on ajoute les contraintes
    }
}
function closeWindows() {
    document.querySelector("div.windows-SPRINTIA-briefing").classList.add("close")
    document.querySelector("body").classList.remove("briefing-open")
    document.querySelector("main").classList.remove("briefing-open")

    setTimeout(() => {
        document.querySelector("section.background-SPRINTIA-briefing").style.display = "none"

        document.querySelector("div.windows-SPRINTIA-briefing").classList.remove("close")
        document.querySelector("div.windows-SPRINTIA-briefing").classList.remove("open")
    }, 150);
}

const dicoLienIA = {
    "vibe":"https://chat.mistral.ai/", "gemini":"https://gemini.google.com/", 
    "chat-gpt":"https://chatgpt.com/", "claude":"https://claude.ai/",
    "grok":"https://grok.com/", "meta-ai":"https://www.meta.ai/", 
    "deepseek":"https://chat.deepseek.com/", "copilot":"https://copilot.microsoft.com/",
    "perplexity": "https://www.perplexity.ai/"
}
function openIA(favoriteIA) {
    if (promptForIA != undefined) {
        navigator.clipboard.writeText(promptForIA)
        .then(() => {
            if (favoriteIA == "ia-locale") {
                logoDynamique("📋 Copié !")
            } else {
                window.open(dicoLienIA[favoriteIA], '_blank') // ouverture de l'IA préféré du user
            }
        })
        .catch(error => {
            alert("Une erreur s'est produite lors de la copie du prompt dans votre papier presse.", error)
        })

    } else {
        alert("Aucun prompt n'a été créé car SPRINTIA n'a pas assez de données pour en générer un !")
        return
    }
}

const dicoIA = {
    "vibe":"Vibe", "gemini":"Gemini", "chat-gpt":"ChatGPT", "claude":"Claude",
    "grok":"Grok", "meta-ai":"Meta AI", "deepseek":"DeepSeek", "copilot":"Copilot",
    "perplexity": "Perplexity", 
    "ia-locale": "l'IA locale de votre choix" // on le met quand meme dans le dico pour : ".explanation-briefing"
}
function nameFavoriteIA() {
    let favoriteIA = localStorage.getItem("iaFavorite")

    if (favoriteIA != null) { // si il y a des datas
        if (favoriteIA == "ia-locale") {
            // pas exactement le meme texte pour l'IA locale car les données tournent en local sur l'appareil
            document.querySelector(".explanation-briefing").innerHTML = `
                SPRINTIA a généré un prompt qui contient certaines données que vous avez enregistrées dans l'application. <strong>En cliquant sur le bouton ci-dessous vous acceptez
                le transfert de vos données à ${dicoIA[favoriteIA]}</strong>.
                <a href="/plus/parametres/SPRINTIA-briefing/a-propos.html" class="lien">En savoir plus</a>.
            `
            document.getElementById("button-open-ia").textContent = "Copier"

        } else {
            // changement du nom de l'IA dans le texte explicatif
            document.querySelector(".explanation-briefing").innerHTML = `
                SPRINTIA a généré un prompt qui contient certaines données que vous avez enregistrées dans l'application. <strong>En cliquant sur le bouton ci-dessous vous acceptez
                le transfert de vos données à ${dicoIA[favoriteIA]}</strong>. Vos données quitteront SPRINTIA et seront donc soumises aux conditions de ${dicoIA[favoriteIA]}.
                <a href="/plus/parametres/SPRINTIA-briefing/a-propos.html" class="lien">En savoir plus</a>.
            `
            document.getElementById("button-open-ia").textContent = "Copier & Ouvrir " + dicoIA[favoriteIA]

        }
        document.getElementById("button-open-ia").onclick = () => openIA(favoriteIA)

        // le bouton dans discuter avec le coach
        let buttonEnDessousTextarea = document.getElementById("button-SPRINTIA-briefing-ask")
        if (buttonEnDessousTextarea) {
            buttonEnDessousTextarea.textContent = "Demander à " + dicoIA[favoriteIA]
        }
    }
}

function cleanEntrainementForIA(allWorkout) {
    return allWorkout.map((workout) =>{
        // on sépare les points gps du reste des données de l'entrainement car on n'envoie pas les points GPS à l'IA!
        const {points_gps, ...autreStats} = workout
        return autreStats
    })
}
function cleanRecuperationForIA(allRecuperation) {
    return allRecuperation.map(elt => ({ // on garde que les datas essentielles car les ID par exemple on s'en fou
        "date": elt.date,
        "fc_repos": elt.fc_repos
    }))
}

async function coachUser() {
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

    return JSON.stringify({"nom_coach_user": nameCoach, "avatar_coach_user": avatarCoach, "style_coach_user": styleCoachUser}, null, 2)
}
async function addPromptContrainte(prompt) {
    // --- Recup personnalisation des prompts ---
    let personnaliteCoachBriefingUser = localStorage.getItem("personnaliteCoachBriefing")
    if (personnaliteCoachBriefingUser == null) {personnaliteCoachBriefingUser="true"} // si pas de datas on autorise de base

    // --- Recup niveaux d'analyse ---
    let niveauAnalyseIaUser = localStorage.getItem("niveauAnalyseIA")
    if (niveauAnalyseIaUser == null) {niveauAnalyseIaUser="modere"} // si pas de datas on met sur le niveau modéré

    // --- commencement des contraintes pour l'IA ---
    let promptWithContrainte = prompt
    
    // --- Personnalisation des prompts ---
    if (personnaliteCoachBriefingUser == "true") { // si le user a activé le duplication du style du coach de SPRINTIA à son IA alors
        promptWithContrainte += "\nVoici le coach que l'utilisateur a configuré dans la PWA SPRINTIA :\n"
        promptWithContrainte += await coachUser() // ajout du dico contenant le nom, l'avatar et le style du coach
        
        promptWithContrainte += `

Contraintes :
- Reprend exactement le style du coach que l'utilisateur a configuré dans SPRINTIA
- Tutoie l'utilisateur et répond en français
- N'hésite pas à lui poser une question pour continuer la discussion et renforcer le lien entre
    toi (le coach de SPRINTIA) et l'utilisateur.`

    } else {
        promptWithContrainte += `

Contraintes :
- Adopte une posture de coach sportif neutre, factuelle et objective
- Tutoie l'utilisateur et répond en français
- Pose lui quelques questions à la fin de l'analyse pour continuer la discussion et renforcer ce lien entre
    toi (le coach de SPRINTIA) et l'utilisateur.`
    }

    // --- Niveaux d'analyse ---
    if (niveauAnalyseIaUser == "essentiel") {
        promptWithContrainte += "\n\nExplique les concepts avec des mots simples, évite le jargon technique, privilégie la pédagogie."
    } else if (niveauAnalyseIaUser == "expert") {
        promptWithContrainte += "\n\nUtilise des termes techniques et physiologiques précis. L'utilisateur est un athlète expérimenté qui comprend les métriques de charge avancées."
    }
    // si le user a choisi modéré on ne change rien car les IA sont déjà dans une forme de neutralité

    return promptWithContrainte
}

async function promptTendances() {
    // début du prompt
    let prompt = `Tu es le coach sportif expert de la PWA nommé SPRINTIA. Analyse les données que SPRINTIA te fournit dans ce prompt.\n\nStructure de ta réponse :
    1. 3 insights clés sur sa performance récente.
    2. 1 conseil actionnable pour sa prochaine séance.
    3. Analyse les tendances des statistiques en comparant la semaine actuelle (les 7 derniers jours) aux semaines précédentes.

Information temporelle : nous sommes aujourd'hui le ${createObjetDate(0)}.

Données d'entraînement :\n`

    // récup des données entrainement de l'utilisateur
    let historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(21)).toArray()
    let nbEntrainement = historiqueData.length

    if (nbEntrainement < 5) {
        historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(30)).toArray()
    } else if (nbEntrainement > 10) {
        historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(14)).toArray()
    }
    
    historiqueData = cleanEntrainementForIA(historiqueData) // on nettoie les datas inutile

    if (historiqueData.length <= 0) {
        // on return undefined au moins la var prompt sera égale à undefined car il n'y pas assez de données et ça bloquera l'utilisateur d'ouvrir 
        // une IA alors qu'il n'y a pas de data
        return undefined
    }

    // ajout des données au prompt
    prompt += JSON.stringify(historiqueData, null, 2)

    return prompt
}
async function promptCE() {
    // début du prompt
    let prompt = `Tu es le coach sportif expert de la PWA nommé SPRINTIA. Analyse les données que SPRINTIA te fournit dans ce prompt et apporte une vraie plus-value à l'algorithme de SPRINTIA pour aider l'utilisateur.\n\nStructure de ta réponse :
    1. Interprète ce que SPRINTIA a analysé mais en apportant une plus-value qu'un algorithme ne peut pas comprendre.
    2. Regarde la régularité : la charge vient-elle de séances régulières et stables, ou de gros pics soudains ?
    3. Suggère un conseil actionnable pour la prochaine séance et propose lui une type de séance à privilégier (en précisant un RPE cible cohérent avec l'état actuel de sa charge d'entraînement).

Information temporelle : nous sommes aujourd'hui le ${createObjetDate(0)}.

Données d'entraînement :\n`
    let historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(28)).toArray()
    historiqueData = cleanEntrainementForIA(historiqueData)

    if (historiqueData.length <= 3) {
        // on return undefined au moins la var prompt sera égale à undefined car il n'y pas assez de données et ça bloquera l'utilisateur d'ouvrir 
        // une IA alors qu'il n'y a pas de data
        return undefined
    }

    // ajout des données au prompt
    prompt += JSON.stringify(historiqueData, null, 2)

    // ajout de l'interpretation de SPRINTIA
    prompt += `
        
Voici ce que SPRINTIA a interpreté :
Statut : ${document.getElementById("statut-ce").textContent}
Charge aiguë (7J) : ${Number(document.getElementById("charge-7j").textContent)} CE (=charge entraînement)
Cible pour rester en statut productif : ${document.getElementById("cible-charge-7j").textContent}
Charge chronique (28J) : ${Number(document.getElementById("charge-28j").textContent)} CE
    `

    return prompt
}
async function promptIndulgence() {
    // début du prompt
    let prompt = `Tu es le coach sportif expert de la PWA nommé SPRINTIA. Tu dois analyser plus profondément ce que l'algorithme nommé "Indulgence de course" de SPRINTIA ne peut pas voir ni comprendre. Ton but ? Aider l'utilisateur à gérer sa tolérence mécanique en course à pied et apporte des conseils pertinents.\n\nStructure de ta réponse : 
    1. Interprète ce que SPRINTIA a analysé mais ne te contente pas de valider la distance cible calculée par SPRINTIA, explique lui comment diviser intelligemment ce volume. Bien entendu tu adapteras ton explication en fonction du type de coureur·euse. 
    2. Explique à l'utilisateur comment ses séances influencent la fatigue musculaire globale de ses jambes, même si son kilométrage de course semble faible.
    3. N'hésite pas à prendre en compte les autres sports que l'utilisateur a pratiqué mais reste focus un maximum sur la course à pied.

Information temporelle : nous sommes aujourd'hui le ${createObjetDate(0)}.

Données d'entraînement :\n`
    let historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(28)).toArray()
    historiqueData = cleanEntrainementForIA(historiqueData)

    if (historiqueData.length <= 0) {
        // on return undefined au moins la var prompt sera égale à undefined car il n'y pas assez de données et ça bloquera l'utilisateur d'ouvrir 
        // une IA alors qu'il n'y a pas de data
        return undefined
    }
        
    // si l'algorithme écrit "0,0 - 0,0 km" ça veut dire que le user n'a pas fais d'entrainement de course à pied ses 28 derniers jours
    if (document.getElementById("reponse-algo-indulgence").textContent == "0,0 - 0,0 km") {
        return undefined
    }

    // ajout des données au prompt
    prompt += JSON.stringify(historiqueData, null, 2)

    // ajout de l'interpretation de SPRINTIA
    const dicoTypeCoureur = {
        "occasionnel": "Occasionnel·le",
        "regulier": "Régulier·ère",
        "confirme": "Confirmé·e",
    }
    let typeCoureur = dicoTypeCoureur[localStorage.getItem("typeCoureur")]
    if (typeCoureur == null) {typeCoureur = "Occasionnel·le"}
    prompt += `
        
Voici ce que SPRINTIA a interpreté :
L'analyse du coach de SPRINTIA : ${document.getElementById("reponse-coach-indulgence").textContent}
Distance réel sur 7J : ${document.getElementById("reponse-algo-allure").textContent}
Distance hebdomadaire conseillée : ${document.getElementById("reponse-algo-indulgence").textContent}
Type de coureur·euse (séléctionné par l'utilisateur dans les paramètres) : ${typeCoureur}
    `

    return prompt
}
async function promptRecuperation() {
    // début du prompt
    let prompt = `Tu es le coach sportif expert de la PWA nommé SPRINTIA. Tu dois analyser plus profondément ce que l'algorithme nommé "Récupération" de SPRINTIA ne peut pas voir ni comprendre. Ton but ? Aider l'utilisateur à comprendre s'il est en forme pour faire une séance d'entraînement, l'algorithme de récupération n'as accès qu'à la FC repos de l'utilisateur mais toi tu as accès à la FC repos et à ses entraînements.\n\nStructure de ta réponse :
    1. Interprète ce que SPRINTIA a analysé mais ne te contente pas de valider ce que l'algorithme analyse va chercher plus loin dans l'analyse étant donné que tu as accès à l'historique d'entraînement.
    2. Suggère un entraînement que l'utilisateur pourrais faire en fonction de ses préférences et de sa récupération. N'hésites pas à lui conseiller du repos si il en a besoin.

Information temporelle : nous sommes aujourd'hui le ${createObjetDate(0)}.

Données d'entraînement :\n`
    let historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(7)).toArray()
    let historiqueRecuperationData = await db.recuperation.where("date").aboveOrEqual(createObjetDate(7)).toArray()
    let recuperationUserToday = await db.recuperation.where("date").aboveOrEqual(createObjetDate(0)).toArray()

    // on vérifie d'abord si l'utilisateur a saisi sa FC repos du jour avant de faire le prompt
    if (recuperationUserToday.length <= 0) {return undefined} // pour pas qu'on génère le prompt

    if (historiqueData.length < 2) {
        historiqueData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(14)).toArray()
    }
    if (historiqueRecuperationData.length < 3) {
        historiqueRecuperationData = await db.entrainement.where("date").aboveOrEqual(createObjetDate(14)).toArray()
    }

    if (historiqueData.length <= 0 || historiqueRecuperationData.length <= 0) {
        // on return undefined au moins la var prompt sera égale à undefined car il n'y pas assez de données et ça bloquera l'utilisateur d'ouvrir 
        // une IA alors qu'il n'y a pas de data
        return undefined
    }

    // on enleve les datas des points gps
    historiqueData = cleanEntrainementForIA(historiqueData)

    // ajout des données au prompt
    prompt += JSON.stringify(historiqueData, null, 2)

    // ajout de la recup
    prompt += "\n\nDonnées de récupération :\n"
    historiqueRecuperationData = cleanRecuperationForIA(historiqueRecuperationData)
    prompt += JSON.stringify(historiqueRecuperationData, null, 2)

    // ajout de l'interpretation de SPRINTIA
    prompt += `
        
Voici ce que SPRINTIA a interpreté :
L'analyse du coach de SPRINTIA : ${document.getElementById("reponse-coach").textContent}
FC repos du jour : ${document.getElementById("fc-repos-today").textContent}
Moyenne 30J : ${document.getElementById("fc-repos-moyenne-30j").textContent}
    `

    return prompt
}

async function promptAnalyseEntrainement() {
    // récup de l'id de l'entraînement
    const settingURL = window.location.search // recup des parametres de l'URL de la page 

    if (settingURL) { // on vérifie qu'il y a un setting avant de faire un split
        const tableauSeparation = settingURL.split("=") // ["?workout", "id"]
        
        if (tableauSeparation.length == 2) { // vérification pour éviter d'essayer de prendre l'index 1 alors qu'il y a que l'index 0 ou alors qu'il 5 index
            idWorkout = parseInt(tableauSeparation[1]) // on recup l'id
        } else {
            return undefined // pour stoper le programme dans une autre fonction
        }
    } else {
        return undefined // pour stoper le programme dans une autre fonction
    }

    // début du prompt
    let prompt = `Tu es le coach sportif expert de la PWA nommé SPRINTIA. Ton but ? Encourager et analyser les statistiques de l'entraînement de l'utilisateur tu devrais lui donner :
    1. Une phrase de motivation
    2. 1 insights clés sur son entraînement
    3. Pose lui des questions sur cet entraînement

Information temporelle : nous sommes aujourd'hui le ${createObjetDate(0)}.

Données :\n`

    // récup des données entrainement de l'utilisateur
    let historiqueData = await db.entrainement.get(idWorkout) 
    // ça renvoie un dico et non un tableau donc
    historiqueData = cleanEntrainementForIA([historiqueData]) // on met le dico dans un tableau pour pouvoir utiliser la fonction cleanEntrainementForIA    

    if (historiqueData.length <= 0) {
        // on return undefined au moins la var prompt sera égale à undefined car il n'y pas assez de données et ça bloquera l'utilisateur d'ouvrir 
        // une IA alors qu'il n'y a pas de data
        return undefined
    }

    // ajout des données au prompt
    prompt += JSON.stringify(historiqueData, null, 2)

    return prompt
}

async function promptDiscussion() {
    // début du prompt
    let prompt = "Tu es le coach sportif expert de la PWA nommé SPRINTIA. L'utilisateur ouvre une discussion avec toi. Tu as accès à l'intégralité des données de son profil sur SPRINTIA.\nTon but ? Répondre à ses questions de manière fluide et précise en te basant sur toutes ses données.\nInformation temporelle : Nous sommes aujourd'hui le " + createObjetDate(0) + "."

    // récup des données entrainement de l'utilisateur
    let choiceUserToShareData = localStorage.getItem("shareProfilDataInPrompt") || "true"
    let dataProfil = await db.profil.get(1)
    let historiqueDataWorkout = await db.entrainement.where("date").aboveOrEqual(createObjetDate(21)).toArray()
    let historiqueDataRecuperation = await db.recuperation.where("date").aboveOrEqual(createObjetDate(7)).toArray()
    let historiqueDataRecuperation30J = await db.recuperation.where("date").aboveOrEqual(createObjetDate(30)).toArray() // on s'en sert pr calculer la baseline

    // on adapte le nombre de donnée en fonction de si il y a trop ou pas assez de données
    if (historiqueDataWorkout.length < 5) {
        historiqueDataWorkout = await db.entrainement.where("date").aboveOrEqual(createObjetDate(30)).toArray()
    } else if (historiqueDataWorkout.length > 10) {
        historiqueDataWorkout = await db.entrainement.where("date").aboveOrEqual(createObjetDate(14)).toArray()
    }

    if (historiqueDataRecuperation.length < 3) {
        historiqueDataRecuperation = await db.recuperation.where("date").aboveOrEqual(createObjetDate(14)).toArray()
    }

    // on vérifie que l'historique d'entrainement car les datas de récupération c'est pas obligatoire
    if (historiqueDataWorkout.length <= 0) {
        // on return undefined au moins la var prompt sera égale à undefined car il n'y pas assez de données et ça bloquera l'utilisateur d'ouvrir 
        // une IA alors qu'il n'y a pas de data
        return undefined
    }

    if (dataProfil != undefined && choiceUserToShareData == "true") { // si le user à configurer son profil alors on ajoute ses datas dans le prompt
        // le profil de l'utilisateur
        prompt += "\nLe profil de l'utilisateur :\n"
        prompt += JSON.stringify(dataProfil, null, 2)
    }

    // on enleve les datas des points gps
    historiqueDataWorkout = cleanEntrainementForIA(historiqueDataWorkout)

    // les datas des entrainements des users
    prompt += "\n\nL'historique d'entrainement de l'utilisateur :\n"
    prompt += JSON.stringify(historiqueDataWorkout, null, 2)

    if (historiqueDataRecuperation.length > 0) { // si le user à enregistré des données de récupération on ajoute ses datas dans le prompt
        // le profil de l'utilisateur
        prompt += "\n\nLes données de récupération de l'utilisateur :\n"
        historiqueDataRecuperation = cleanRecuperationForIA(historiqueDataRecuperation)
        prompt += JSON.stringify(historiqueDataRecuperation, null, 2)

        // calcul de la baseline
        let sommeFcRepos = 0
        historiqueDataRecuperation30J.forEach(element => {
            sommeFcRepos += element.fc_repos
        });
        let moyenne30J = Math.round(sommeFcRepos/historiqueDataRecuperation30J.length)

        // ajout de la baseline
        prompt += "\nMoyenne 30J : " + moyenne30J + " bpm"
    }

    // ajout du prompt de l'utilisateur (pr info on a déjà vérifié si le textearea était vide dans le html)
    prompt += `\n\nVoici la question que l'utilisateur a posé à SPRINTIA : '${document.getElementById("promt-user").value}'\n`

    return prompt
}

document.addEventListener("DOMContentLoaded", () => {
    let iconFermer = document.querySelector("div.windows-SPRINTIA-briefing-head i.icon_fermer")
    if (iconFermer) {iconFermer.addEventListener("click", closeWindows)}

    nameFavoriteIA()
})