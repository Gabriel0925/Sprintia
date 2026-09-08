// le dico localStorage contient toujours une clé qui est nommé : "VersionLocalStorage" et "versionDB" donc on vérif si il y a plus d'une clé
const nbClefInutileLocalStorage = 2

async function createFileJSON() {
    let dicoDataLocalStorage = {} // ex structure dico : 'personnaliteCoachBriefing': 'true',...
    // boucle qui parcout tous ce qu'il y a d'enregistrer dans le local storage
    for (let i=0; i < localStorage.length; i++) {
        // on récup la clé de l'element du local storage et on l'ajoute au dico en recherchant la valeur de cette clé
        dicoDataLocalStorage[localStorage.key(i)] = localStorage.getItem(localStorage.key(i))
    }

    // (!!!--- Modifier si ajout de table ---!!!)
    // recup des datas de chaque table de l'indexedDB 
    let workoutDB = await db.entrainement.toArray()
    let niveauCourseDB = await db.niveau_course.toArray()
    let jrmCoachDB = await db.JRM_Coach.toArray()
    let profilDB = await db.profil.toArray()
    let recupDB = await db.recuperation.toArray()

    // (!!!--- Modifier si ajout de table ---!!!)
    const dataTelecharger = {
        DataLocalStorage: dicoDataLocalStorage,

        DataIndexedDB: {
            entrainement: workoutDB,
            niveau_course: niveauCourseDB,
            JRM_Coach: jrmCoachDB,
            profil: profilDB,
            recuperation:recupDB
        }
    }

    // si il n'y a pas de données on return false
    // le dico localStorage contient toujours une clé qui est nommé : "VersionLocalStorage" et "versionDB" donc on vérif si il y a plus d'une clé
    if (Object.keys(dicoDataLocalStorage).length <= nbClefInutileLocalStorage && workoutDB.length === 0 && niveauCourseDB.length === 0 && 
        jrmCoachDB.length === 0 && profilDB.length === 0 && recupDB.length === 0) {
        return false
    } else {
        // transformation du dico en txt JSON, avec 2 tab comme identation et null pr appliquer aucun filtre
        return JSON.stringify(dataTelecharger, null, 2)
    }
}

async function shareData(button) {
    button.textContent = "Partage en cours..."
    button.disabled = true

    try {
        let txtDataUser = await createFileJSON()

        // si txtDataUser vaut false c'est que ya pas de données à partager
        if (txtDataUser == false) {
            button.textContent = "Aucune donnée à partager"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } else {
            let fileUserData = new File([txtDataUser], "Sauvegarde-SPRINTIA.text", {type: "text/plain"}) // on crée le fichier (txt) car le navigateur bloque les fichiers JSON

            // on vérifie si le navigateur est compatible avec navigator.share et on vérifie aussi si il sait partager un fichier
            if (navigator.canShare && navigator.canShare({files: [fileUserData]})) {
                await navigator.share({files:[fileUserData], // on met dans un tableau car navigator.share peut permettre d'envoyer plusieurs fichier [fichier1, fichier2,...]
                    title:"Sauvegarde SPRINTIA"})            
                
                button.textContent = "Partagé"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
            } else {
                button.textContent = "Navigateur incompatible !"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
            }
        }

    } catch(error) {
        if (error.name== "AbortError") { // ça veut dire que le user à fermer le menu de partage sans envoyer le fichier
            button.textContent = "Partage annulé"
        } else {
            console.log(error) // affichage de l'erreur en console
            button.textContent = "Une erreur s'est produite"
        }
        await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
    } finally {
        button.textContent = "Partager vos données"
        button.disabled = false 
    }
}
async function downloadDatas(button) {
    button.textContent = "Téléchargement..."
    button.disabled = true 

    try {
        let txtDataUser = await createFileJSON()

        // si txtDataUser vaut false c'est que ya pas de données à télécharger
        if (txtDataUser == false) {
            button.textContent = "Aucune donnée enregistrée"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } else {
            // création d'un objet nommé blob (=en gros on créer une URL temporaire)
            // au moins la navigateur c'est ou télécharger le "fichier"
            let urlBlob = URL.createObjectURL(new Blob([txtDataUser], {type: "application/json"})) // par ex : 'blob:http://127.0.0.1:5500/414b2c61-e902-4b86-84fb-61ad6afea08c'
            let baliseHTML = document.createElement("a")

            baliseHTML.href = urlBlob // on attribue l'URL du blob à la balise a
            baliseHTML.download = "Sauvegarde-SPRINTIA.json" // nom du "fichier"
            baliseHTML.click() // on simule un click pour download

            button.textContent = "Téléchargé"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
        }

    } catch(error) {
        console.log(error) // affichage de l'erreur en console
        button.textContent = "Une erreur s'est produite"
        await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
    } finally {
        button.textContent = "Télécharger le fichier"
        button.disabled = false 
    }
}

async function restaurationDatas(event) {
    const file = event.target.files[0] // récup du fichier

    if (file) { // si ya un fichier on change l'état du bouton
        let buttonRestoration = document.getElementById("restoration-button")
        buttonRestoration.textContent = "Restauration..."
        buttonRestoration.disabled = true

        try {
            const textFile = await file.text() // on lis le contenu du fichier sous la forme d'un texte
            const dataFile = JSON.parse(textFile) // conversion en objet js
            const dataFileLocalStorage = dataFile.DataLocalStorage // recup du dico des datas du localstorage
            const dataFileIndexedDB = dataFile.DataIndexedDB // recup du dico des datas de l'indexedDB

            // si le fichier ne contient aucune donnée on affiche un message ds le btn
            // le dico localStorage contient toujours une clé qui est nommé : "VersionLocalStorage" donc on vérif si il y a plus d'une clé
            if (Object.keys(dataFileLocalStorage).length <= nbClefInutileLocalStorage && dataFileIndexedDB.entrainement.length === 0 && 
                dataFileIndexedDB.niveau_course.length === 0 && dataFileIndexedDB.JRM_Coach.length === 0 && 
                dataFileIndexedDB.profil.length === 0 && dataFileIndexedDB.recuperation.length === 0) {
                buttonRestoration.textContent = "Aucune donnée à restaurer"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))

            } else {
                localStorage.clear() // réinitialisation du localStorage
                for (var key in dataFileLocalStorage) {
                    localStorage.setItem(key, dataFileLocalStorage[key]) // enregistrement
                }
                sessionStorage.clear() // on clear le sessionStorage au passage

                for (const table of db.tables) { // on parcourt chaque table de la bdd et on supprime
                    await table.clear()

                    const tableFileJSON = dataFileIndexedDB[table.name] // on récupère les datas de la table actuelle de la boucle for dans le fichier JSON

                    if (tableFileJSON && tableFileJSON.length > 0) {  // on verifie qu'il y a des datas dans la table du JSON
                        for (let elt of tableFileJSON) { // on recupere les datas ligne par ligne de la table correspondante
                            if (table.name == "profil") {
                                // on le met à l'id 1 car il y a que cette ligne dans cette table
                                await table.put(elt, 1) // on utilise direct la var table qui est déjà co à db

                            } else {
                                await table.add(elt) // on utilise direct la var table qui est déjà co à db
                            }
                        }
                    }
                }

                buttonRestoration.textContent = "Restauré"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
                window.location.href = "../../../index.html?accountrestore"
            }

        } catch(error) {
            console.log(error)
            buttonRestoration.textContent = "Une erreur s'est produite"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            buttonRestoration.textContent = "Restaurer vos données"
            buttonRestoration.disabled = false
        }
    }
}

async function nettoyerDatas(conserverDatas) { // conserverDatas vaut soit 30J/90J/365J
    if (confirm(`Êtes-vous sur de vouloir supprimer vos données qui sont plus vieilles que ${conserverDatas} jours ?`)) {
        let buttonNettoyer = document.getElementById("button-nettoyer")
        buttonNettoyer.textContent = "Nettoyage..."
        buttonNettoyer.disabled = true
        
        try {
            let dateMoinsJours = createObjetDate(conserverDatas)

            let nbOperation = 0
            for (const tableElt of db.tables) { // on parcourt chaque table de la bdd et on supprime
                if (tableElt.name != "JRM_Coach" && tableElt.name != "profil") {
                    // .delete() renvoie le nombre d'opération
                    const nbSupprimer = await tableElt.where('date').below(dateMoinsJours).delete()
                    nbOperation+=nbSupprimer
                }
            }
            
            if (nbOperation < 1) {
                buttonNettoyer.textContent = "Rien à nettoyer"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
            } else {
                buttonNettoyer.textContent = "Nettoyé"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
                logoDynamique("🧹 Grand ménage !")
            }
        } catch(error) {
            console.log(error)
            buttonNettoyer.textContent = "Une erreur s'est produite"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            buttonNettoyer.textContent = "Nettoyer"
            buttonNettoyer.disabled = false
        }
    }
}

async function suppressionDonnees() {
    if (confirm("Êtes-vous sur de vouloir supprimer toutes vos données ?")) {
        let buttonReinitialiser = document.getElementById("reinitialiser-SPRINTIA")
        buttonReinitialiser.textContent = "Suppression..."
        buttonReinitialiser.disabled = true
        
        try {
            let dicoDataLocalStorage = {} // ex structure dico : 'personnaliteCoachBriefing': 'true',...
            // boucle qui parcout tous ce qu'il y a d'enregistrer dans le local storage
            for (let i=0; i < localStorage.length; i++) {
                // on récup la clé de l'element du local storage et on l'ajoute au dico en recherchant la valeur de cette clé
                dicoDataLocalStorage[localStorage.key(i)] = localStorage.getItem(localStorage.key(i))
            }

            let nbOperation = 0
            for (const tableElt of db.tables) { // on parcourt chaque table de la bdd
                const dataTable = await tableElt.toArray()
                if (dataTable.length < 1) {
                    nbOperation+=dataTable
                }
            }

            if (nbOperation<1 && Object.keys(dicoDataLocalStorage).length <=nbClefInutileLocalStorage) {
                buttonReinitialiser.textContent = "Aucune donnée à supprimer"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
                
            } else {
                localStorage.clear()
                sessionStorage.clear()
                for (const elt of db.tables) { // on parcourt chaque table de la bdd et on supprime
                    await elt.clear()
                }
                
                buttonReinitialiser.textContent = "Supprimé"
                await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 500))
                window.location.href = "../../../index.html"
            }
        } catch(error) {
            console.log(error)
            buttonReinitialiser.textContent = "Une erreur s'est produite"
            await new Promise(transmissionInfoUser => setTimeout(transmissionInfoUser, 650))
        } finally {
            buttonReinitialiser.textContent = "Supprimer vos données"
            buttonReinitialiser.disabled = false
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const buttonExporterEvent = document.getElementById("partager-button")
    if (buttonExporterEvent) {buttonExporterEvent.addEventListener("click", function() {shareData(buttonExporterEvent)})}

    const buttonDownloadEvent = document.getElementById("download-button")
    if (buttonDownloadEvent) {buttonDownloadEvent.addEventListener("click", function() {downloadDatas(buttonDownloadEvent)})}

    const buttonReinitialisationEvent = document.getElementById("reinitialiser-SPRINTIA")
    if (buttonReinitialisationEvent) {buttonReinitialisationEvent.addEventListener("click", suppressionDonnees)}
    
    const buttonRestaurationEvent = document.getElementById("restoration-button") 
    if (buttonRestaurationEvent) {buttonRestaurationEvent.addEventListener("click", () => {document.getElementById('file-input').click()})}

    const inputFileRestoration = document.getElementById("file-input")
    if (inputFileRestoration) {inputFileRestoration.addEventListener("change", (event) => {restaurationDatas(event)})}
    
    const buttonNettoyageEvent = document.getElementById("button-nettoyer")
    if (buttonNettoyageEvent) {buttonNettoyageEvent.addEventListener("click", () => {nettoyerDatas(Number(document.getElementById('conserver-datas').value))})}

    const selectConserverDatas = document.getElementById("conserver-datas")
    if (selectConserverDatas) {selectConserverDatas.value="90"}
})