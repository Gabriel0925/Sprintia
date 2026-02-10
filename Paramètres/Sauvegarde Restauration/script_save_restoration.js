// bien faire attention au : "(!!!--- Modifier si ajout de table ---!!!)" c'est partout dans les tables

async function DownloadDatas() {
    let BoutonDownload = document.getElementById("download-button")
    BoutonDownload.textContent = "Téléchargement..."
    BoutonDownload.disabled = true // désactivation du bouton

    // Initialisation
    let ClefLocalStorage = "" // prepa pr la boucle
    let DicoDataLocalStorage = {} // ex structure dico : ColorActuelleUse: "theme_azur",...

    for (let i=0; i < localStorage.length; i++) { // on parcour la longueur du localstorage
        ClefLocalStorage = localStorage.key(i) // on recupere la clé de elt du local storage, ça marche de la meme meniere qu'une liste avec les index par exemple ça renvoie : "ToggleThemeComplet"
        DicoDataLocalStorage[ClefLocalStorage] = localStorage.getItem(ClefLocalStorage) // ajout dans le dico
    }

    // (!!!--- Modifier si ajout de table ---!!!)
    // recup des datas de chaque table de l'indexedDB 
    let WorkoutDB = await db.entrainement.toArray()
    let NiveauCourseDB = await db.niveau_course.toArray()
    let StatutDB = await db.statut_analyse.toArray()
    let JrmCoachDB = await db.JRM_Coach.toArray()

    // (!!!--- Modifier si ajout de table ---!!!)
    // Dictionnaire avec les datas du local storage et les tables de l'indexed DB
    const DataTelecharger = {
        DataLocalStorage: DicoDataLocalStorage,
        DataIndexedDB: {
            entrainement: WorkoutDB,
            niveau_course: NiveauCourseDB,
            statut_analyse: StatutDB,
            JRM_Coach: JrmCoachDB
        }
    }

    // Transformation des objets (le dico avec toutes les datas) en txt JSON
    let TxtDataUser = JSON.stringify(DataTelecharger)

    // création d'un blob
    // l'utilité du blod est de contourner le back-end en gros on créer une URL temporaire
    // juste pour que lors du clic sur le bouton, au moins le navigateur c'est quoi aller chercher ici le fichiers JSON
    const VarBlob = new Blob([TxtDataUser], {type: "application/json"})

    // Création d'un lien pour le blob (c un objet)
    let UrlBlob = URL.createObjectURL(VarBlob)
    let LienURL = document.createElement("a") // on créer la balise a dans le html

    LienURL.href = UrlBlob // on créer le lien a href
    LienURL.download = "Sauvegarde-Sprintia.json" // pour enregistrer le fichier dans l'appareil d'un user
    LienURL.click() // on simmule le click pour lancer le download

    // Légère pause
    await new Promise(r => setTimeout(r, 650))
    // confirmation sauvegarde
    BoutonDownload.textContent = "Téléchargé"
    // Pause
    await new Promise(r => setTimeout(r, 650))
    // remise etat normal
    BoutonDownload.textContent = "Télécharger mes données"
    BoutonDownload.disabled = false // Réactivation du bouton

    return
}

async function ReadFile(event) {
    const File = event.target.files[0]

    if (File) {
        let BoutonRestoration = document.getElementById("restoration-button")
        BoutonRestoration.textContent = "Importation..."
        BoutonRestoration.disabled = true // désactivation du bouton

        try {
            // ne pas utiliser fetch car fetch attend une url vers un serveur
            const TextFile = await File.text() // on liis le contenu du fichier sous format text
            const DataFile = JSON.parse(TextFile) // "conversion" en objet javascript
            const DataFileLocalStorage = DataFile.DataLocalStorage // dico des datas localstorage uniquement

            // on vide le local storage avant d'entrer les datas du fichier user
            localStorage.clear()
            for (var key in DataFileLocalStorage) { // on enregistre les datas du localstorage
                localStorage.setItem(key, DataFileLocalStorage[key])
            }

            const DataFileIndexedDB = DataFile.DataIndexedDB // dico des datas indexedDB uniquement

            // (!!!--- Modifier si ajout de table ---!!!)
            // on isole les datas de chaque table
            const TableEntrainement = DataFileIndexedDB.entrainement
            const TableNiveauCOurse = DataFileIndexedDB.niveau_course
            const TableStatuts = DataFileIndexedDB.statut_analyse
            const TableJRMCoach = DataFileIndexedDB.JRM_Coach

            // (!!!--- Modifier si ajout de table ---!!!)
            // on vide chaque table de l'indexedDB avant d'ajouter les datas
            await db.entrainement.clear()
            await db.niveau_course.clear()
            await db.statut_analyse.clear()
            await db.JRM_Coach.clear()

            // (!!!--- Modifier si ajout de table ---!!!)
            for (let element of TableEntrainement) { // on recupere les datas ligne par ligne de la table correspondante
                await db.entrainement.add(element)
            }
            for (let element of TableNiveauCOurse) { // on recupere les datas ligne par ligne de la table correspondante
                await db.niveau_course.add(element)
            }
            for (let element of TableStatuts) { // on recupere les datas ligne par ligne de la table correspondante
                await db.statut_analyse.add(element)
            }
            for (let element of TableJRMCoach) { // on recupere les datas ligne par ligne de la table correspondante
                await db.JRM_Coach.add(element)
            }
            
            // Légère pause
            await new Promise(r => setTimeout(r, 650))
            // confirmation sauvegarde
            BoutonRestoration.textContent = "Importé"
            // Pause
            await new Promise(r => setTimeout(r, 650))
            // remise etat normal
            BoutonRestoration.textContent = "Restaurer mes données"
            BoutonRestoration.disabled = false // Réactivation du bouton
        
            location.reload()    
        } catch {
            alert("Une erreur est survenue, veuillez réessayer !")
        }
    }

    return
}

async function SupprimerDatas() {
    // Demande de confirmation avant de continuer
    if (confirm("Êtes-vous sur de vouloir supprimer toutes vos données ?")) {
        let ButtonReinitialiser = document.getElementById("reinitialiser-sprintia")
        ButtonReinitialiser.textContent = "Chargement..."
        ButtonReinitialiser.disabled = true // désactivation du bouton
       
        localStorage.clear()
        sessionStorage.clear()

        
        // (!!!--- Modifier si ajout de table ---!!!)
        // on vide chaque table de l'indexedDB avant d'ajouter les datas
        await db.entrainement.clear()
        await db.niveau_course.clear()
        await db.statut_analyse.clear()
        await db.JRM_Coach.clear()

        // Légère pause
        await new Promise(r => setTimeout(r, 650))
        // confirmation sauvegarde
        ButtonReinitialiser.textContent = "Réinitialisé"
        // Pause
        await new Promise(r => setTimeout(r, 650))
        // remise etat normal
        ButtonReinitialiser.textContent = "Réinitialiser Sprintia"
        ButtonReinitialiser.disabled = false // Réactivation du bouton
        
        location.reload()
    }

    return
}