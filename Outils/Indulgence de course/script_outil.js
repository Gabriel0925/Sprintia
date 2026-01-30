async function CalculIndulgence() {
    // Recup valeur des champs
    let Distance28JUser = parseFloat(document.getElementById("distance28j-user").value.trim().replace(",", "."))
    let Distance7JUser = parseFloat(document.getElementById("distance7j-user").value.trim().replace(",", "."))

    // Vérif
    if (isNaN(Distance28JUser) || isNaN(Distance7JUser)) {
        alert("Erreur de saisie : tous les champs doivent être remplis.")
        return
    }
    if (Distance28JUser <= 0) {
        alert("Valeur non valide, le champs distance 28j doit être supérieur à 0.")
        return
    }
    if (Distance28JUser >= 1500) {
        alert("Valeur non valide, la distance (28j) doit être inférieur à 1500.")
        return
    }
    if (Distance7JUser >= 375) {
        alert("Valeur non valide, la distance (7j) doit être inférieur à 375.")
        return
    }

    // Initialisation coefficient
    const CoefFourchetteDebut = [1.18, 1.15, 1.12, 1.09, 1.06]
    const CoefFourchetteFin = [1.25, 1.2, 1.15, 1.12, 1.1]

    let IndulgenceDeCourseDebut = 0
    let IndulgenceDeCourseFin = 0

    // Calibration par semaine
    let Distance28J = Distance28JUser/4

    if (Distance28J <= 10) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[0]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[0]
    } else if (Distance28J <= 20) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[1]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[1]
    } else if (Distance28J <= 40) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[2]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[2]
    } else if (Distance28J <= 60) {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[3]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[3]
    } else {
        IndulgenceDeCourseDebut = Distance28J*CoefFourchetteDebut[4]
        IndulgenceDeCourseFin = Distance28J*CoefFourchetteFin[4]
    }

    let ResultIndulgenceCourse = IndulgenceDeCourseDebut.toFixed(1).replace(".", ",") + " - " + IndulgenceDeCourseFin.toFixed(1).replace(".", ",") + " km"

    document.getElementById("reponse-algo-indulgence").innerHTML = ResultIndulgenceCourse

    // direction sauvegarde
    SauvegardeRestauration("Sauvegarde", Distance7JUser, Distance28JUser, ResultIndulgenceCourse, "", "")

    // Go interpretation
    await InterpretationIDC(Distance7JUser, Distance28J, IndulgenceDeCourseFin, "Fonction")
    return
}

function SauvegardeRestauration(ChoseFaire, Distance7JUser, Distance28JUser, ResultIndulgenceCourse, Interpretation, InterpretationParagraphe) {
    // Vérification si l'utilisateur a desactiver la fonction
    let SauvegardeIDC = localStorage.getItem("SauvegardeIDC")

    // On ne sauvegarde rien ou restaure rien si le user a desactiver l'option sauvegarde mais on cache le message d'aide du debut
    if (SauvegardeIDC == "False") {
        document.getElementById("text-info-sauvegarde").style.display = 'none'
        return
    }

    // On cache le message d'aide si il y a qqch dans le local storage 
    if (SauvegardeIDC != null) {
        document.getElementById("text-info-sauvegarde").style.display = 'none'
    }

    if (ChoseFaire == "Restauration") {
        // Remplir les 2 champs distance
        let RecentDistance7J = localStorage.getItem("RecentDistance7J")
        let RecentDistance28J = localStorage.getItem("RecentDistance28J")

        if (RecentDistance7J) {
            document.getElementById("distance7j-user").value = RecentDistance7J
        }
        if (RecentDistance28J) {
            document.getElementById("distance28j-user").value = RecentDistance28J
        }

        // Remplir la fourchette
        let RecentFourchette = localStorage.getItem("FourchetteDistance")
        if (RecentFourchette) {
            document.getElementById("reponse-algo-indulgence").innerHTML = RecentFourchette
        }

        // Remplir l'analyse du coach 
        let CoachAnalyse = localStorage.getItem("CoachInterpretation")
        if (CoachAnalyse) {
            InterpretationParagraphe.innerHTML = Interpretation[CoachAnalyse]
        }

        // Activation du text info sur sauvegarde
        let TextSauvegarde = document.querySelector(".text-info")
        TextSauvegarde.classList.add("visible") 

        // Restauration de la dernière sauvegarde de date
        let SauvegardeDate = localStorage.getItem("DateSauvegardeIDC") // true or false

        if (SauvegardeDate != "False"){ // Si le user n'a pas refusé alors on reaffiche la date de sauvegarde
            // Recup de la date
            let DateSauvegardee = localStorage.getItem("DateValueSauvegardeIDC") // value de la date

            // Affichage
            if (DateSauvegardee == null) {
                document.querySelector(".text-info").innerHTML = "Aucune sauvegarde"
            } else {
                document.querySelector(".text-info").innerHTML = "Sauvegardé le : " + DateSauvegardee
            }
            
        } else if (SauvegardeDate == "False") {
            // Si l'utilisateur a desactiver alors on affiche pas le txt info
            document.querySelector(".text-info").style.display = "none"
        }
    } else {
        // Enregistrement des datas
        localStorage.setItem("RecentDistance7J", Distance7JUser)
        localStorage.setItem("RecentDistance28J", Distance28JUser)
        localStorage.setItem("FourchetteDistance", ResultIndulgenceCourse)

        // Enregistrement de la date
        let SauvegardeDate = localStorage.getItem("DateSauvegardeIDC") // value true or false
        if (SauvegardeDate != "False"){ // Si le user n'a pas refusé alors on enregistre
            // Recup de la date
            let DateNow = new Date()

            // Formatage de la date
            const DateFormatee = DateNow.toLocaleDateString("fr-FR",
                {
                    day: "numeric",
                    month: "short",
                    year: "numeric"
                }
            )

            // Sauvegarde
            localStorage.setItem("DateValueSauvegardeIDC", DateFormatee)

            // Affichage
            document.querySelector(".text-info").innerHTML = "Sauvegardé le : " + DateFormatee
        }
    }

    return
}

async function InterpretationIDC(Distance7JUser, Distance28J, IndulgenceDeCourseFin, Lieu) {
    // Recup du champs JRM
    let InterpretationParagraphe = document.getElementById("reponse-coach-indulgence")
    // si utilisateur a desctiver l'option de sauvegarde alors on ne sauvegarde rien
    let SauvegardeIDC = localStorage.getItem("SauvegardeIDC")


    // Interpretation initialisation
    const Interpretation = {
        "1": "Sprintia n'a pas encore assez de données pour analyser votre indulgence de course. Pas de panique vous avez juste besoin de compléter les champs pour que Sprintia vous donne des conseils pour progresser.", 
        "2": "Vous courez moins depuis 7 jours, c'est dommage ! Si c'est un choix profitez-en pour vous reposer ou travailler d'autre aspect de la course comme du renforcement ou de la mobilité.", 
        "3": "Parfait ! Vous progressez grâce à votre régularité ainsi qu'à votre discipline, continuez comme ça pour booster vos performances. Pour maximiser votre progression, pensez toujours à varier vos allures.", 
        "4": "Attention vous courez bien plus que d'habitude ! Si vous continuez sur ce rythme vous risquez de vous blesser. P'tit conseil, réduisez votre volume d'entraînement.", 
        // Pour les statut
        "5": "Statut : <strong>Vacances</strong><br>Profitez de cette pause pour vous ressourcer, apprécier en famille, de repos, et revenez encore plus motivé·e pour battre tous vos records !", 
        "6": "Statut : <strong>Blessure</strong><br>Prenez vraiment le temps de laisser votre corps se régénérer complètement, afin de revenir encore plus fort·e que jamais.", 
        "7": "Statut : <strong>Malade</strong><br>N'allez pas vous entraîner votre organisme a besoin de récupérer pour le moment, mais dès que cette maladie sera partie vous pourrez reprendre vos entraînements.", 
        "8": "Statut : <strong>Suspension</strong><br>Profitez-en pour vous reposer, Sprintia analysera vos entraînements seulement quand vous serez prêt·e·s !", 
    }

    if (Lieu == "Initialisation") {
        // Initialisation du paragraphe
        InterpretationParagraphe.innerHTML = Interpretation["1"]

        // Remplissage des champs
        SauvegardeRestauration("Restauration", 0, 0, 0, Interpretation, InterpretationParagraphe)
    } else {
        // Check du statut du user
        let HistoriqueDB = await db.statut_analyse.toArray()

        let StatutData = HistoriqueDB.map(statutBDD => statutBDD.statut).reverse() // reverse pour inverser la liste pour l'ordre

        // Unit 
        let LastStatutUser = ""
        if (StatutData.length > 0) {
            // on prend l'index 0 pour avoir son dernier statut
            LastStatutUser = StatutData[0]
        } else {
            // si il n'y a pas de statut on le met sur actif
            LastStatutUser = "Actif·ve"
        }

        if (LastStatutUser == "Vacances") {
            InterpretationParagraphe.innerHTML = Interpretation["5"]

            // Regarder si l'utilisateur a autorisé la sauvegarde
            if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                localStorage.setItem("CoachInterpretation", "5")
            }

        } else if (LastStatutUser == "Blessure") {
            InterpretationParagraphe.innerHTML = Interpretation["6"]

            // Regarder si l'utilisateur a autorisé la sauvegarde
            if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                localStorage.setItem("CoachInterpretation", "6")
            }
            
        } else if (LastStatutUser == "Malade") {
            InterpretationParagraphe.innerHTML = Interpretation["7"]

            // Regarder si l'utilisateur a autorisé la sauvegarde
            if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                localStorage.setItem("CoachInterpretation", "7")
            }
            
        } else if (LastStatutUser == "Suspendre") {
            InterpretationParagraphe.innerHTML = Interpretation["8"]

            // Regarder si l'utilisateur a autorisé la sauvegarde
            if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                localStorage.setItem("CoachInterpretation", "8")
            }
            
        } else if (LastStatutUser == "Actif·ve") {
            if (Distance28J <= Distance7JUser && Distance7JUser <= IndulgenceDeCourseFin) {
                InterpretationParagraphe.innerHTML = Interpretation["3"]

                // Regarder si l'utilisateur a autorisé la sauvegarde
                if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                    localStorage.setItem("CoachInterpretation", "3")
                }
            } else if (Distance7JUser > IndulgenceDeCourseFin) {
                InterpretationParagraphe.innerHTML = Interpretation["4"]

                // Regarder si l'utilisateur a autorisé la sauvegarde
                if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                    localStorage.setItem("CoachInterpretation", "4")
                }
            } else {
                InterpretationParagraphe.innerHTML = Interpretation["2"]

                // Regarder si l'utilisateur a autorisé la sauvegarde
                if (SauvegardeIDC == "True" || SauvegardeIDC == null) {
                    localStorage.setItem("CoachInterpretation", "2")
                }
            }
        }
    }

    return
}

// Il faut attendre que la page soit chargé avant de modifier les sauvegarde,...
window.addEventListener("DOMContentLoaded", () => {
    InterpretationIDC(0, 0, 0, "Initialisation")
}) 