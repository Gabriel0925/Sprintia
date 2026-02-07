async function SupprimerDatas() {
    // Demande de confirmation avant de continuer
    if (confirm("Êtes-vous sur de vouloir supprimer toutes vos données ?")) {
        let ButtonReinitialiser = document.getElementById("reinitialiser-sprintia")
        ButtonReinitialiser.textContent = "Chargement..."
        ButtonReinitialiser.disabled = true // désactivation du bouton
        
        localStorage.clear()
        sessionStorage.clear()
        const DataIndexedDB = await indexedDB.databases()
        DataIndexedDB.forEach(db => {
            indexedDB.deleteDatabase(db.name)
        })

        // Légère pause
        await new Promise(r => setTimeout(r, 650))

        // confirmation sauvegarde
        ButtonReinitialiser.textContent = "Réinitialisé"

        // Pause
        await new Promise(r => setTimeout(r, 650))

        // remise etat normal
        ButtonReinitialiser.textContent = "Réinitialiser Sprintia"
        ButtonReinitialiser.disabled = false // Réactivation du bouton
    }

    return
}