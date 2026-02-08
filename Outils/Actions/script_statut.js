async function Sauvegarde() { // Ajouter datas
    // Recup bouton
    let BoutonLimite1Clic = document.getElementById("button-sauvegarde")

    // Recup valeur champs
    let StatutUser = document.getElementById("statut-user").value
    let RaisonUser = document.getElementById("raison-user").value.trim()

    // Vérification
    if (RaisonUser.length >= 130) {
        alert("Erreur de saisie, le champ raison ne doit pas dépasser 130 caractères.")
        return
    }
    if (!RaisonUser) { // cette vérification doit se faire après celle de length
        RaisonUser = null // ça evite de stocker une data en str = ""
    }

    // Vérification de l'ancien statut pr interdire la sauvegarde du même statut 2 fois d'affiler
    let HistoriqueDB = await db.statut_analyse.toArray()
    let StatutData = HistoriqueDB.map(statutBDD => statutBDD.statut).reverse() // reverse pour inverser la liste pour l'ordre
    
    // Initialisation
    let LastStatutUser = "Actif·ve"
    if (StatutData.length > 0) {
        LastStatutUser = StatutData[0]
    }

    if (LastStatutUser == StatutUser) {
        alert(`Impossible de modifier votre statut : vous êtes déjà en mode : "${StatutUser}".`)
        return    
    }

    BoutonLimite1Clic.disabled = true // Pour empeche que le user clique 2 fois
    // signe d'enregistrement pr le user
    BoutonLimite1Clic.textContent = "Sauvegarde..."

    // Recup de la date
    let DateActuelle = new Date().toISOString() // ça renvoie ça "2026-01-24T13:55:37.171Z"
    // Enlever la partie qui nous interrese pas
    DateActuelle = DateActuelle.split("T") // ['2026-01-24', '13:57:55.505Z']
    DateActuelle = DateActuelle[0] // '2026-01-24'

    // Ajout datas
    await db.statut_analyse.add({
        statut: StatutUser,
        date: DateActuelle,
        raison: RaisonUser
    })

    // Pause
    await new Promise(r => setTimeout(r, 1000))
    // remise etat normal
    BoutonLimite1Clic.textContent = "Sauvegarder"
    BoutonLimite1Clic.disabled = false // Réactivation du bouton

    window.location.href = "historique_statut_analyses.html"

    return
}

async function LastStatut() {
    let HistoriqueDB = await db.statut_analyse.toArray()

    let StatutData = HistoriqueDB.map(statutBDD => statutBDD.statut).reverse() // reverse pour inverser la liste pour l'ordre

    if (StatutData.length > 0) {
        // on prend l'index 0 pour avoir son dernier statut
        const LastStatutUser = StatutData[0]
        document.getElementById("ancien-statut").textContent = "Statut en cours : " + LastStatutUser
    }

    return
}

window.addEventListener("DOMContentLoaded", () => {
    LastStatut()
})
