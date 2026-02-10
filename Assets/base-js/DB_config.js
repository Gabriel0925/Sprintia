// Creation du store d'objet de l'indexed BDD
const db = new Dexie("SprintiaDB")

// Creation de la structure
db.version(3).stores({ // ++ pour autoincrement
    entrainement: "++id, sport, date, nom, duree, rpe, distance, denivele, muscles_travailles, charge_entrainement",
    niveau_course: "++id, niveau_course_user, distance, date",
    statut_analyse: "++id, statut, date, raison",
    JRM_Coach: "id, nom, style, avatar"
})

// Gérer erreur d'ouverture de bdd
db.open().catch(function() {
    alert("Une erreur de base de données s'est produite.")
})