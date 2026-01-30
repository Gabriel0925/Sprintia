async function SupprimerDatas() {
    let ButtonReinitialiser = document.getElementById("reinitialiser-sprintia")
    ButtonReinitialiser.textContent = "Chargement..."
    
    localStorage.clear()
    sessionStorage.clear()
    const DataIndexedDB = await indexedDB.databases()
    DataIndexedDB.forEach(db => {
        indexedDB.deleteDatabase(db.name)
    })

    await new Promise(r => setTimeout(r, 1000))// Pause
    alert("Sprintia a bien été réinitialiser.") // Message au user

    // remise etat normal
    ButtonReinitialiser.textContent = "Réinitialiser Sprintia"
    return
}