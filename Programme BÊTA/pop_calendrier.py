import customtkinter as ctk
import tkcalendar # Il faut pip installer tkcalendar !!! 

def fermer_app(app):
    app.quit()

ctk.set_appearance_mode("System")

app = ctk.CTk(fg_color="#F0F8FF")
app.geometry("500x500")
app.bind("<Control-w>", lambda event: fermer_app(app))

def pop_up_calendrier():
    calendrier = ctk.CTkToplevel(app)
    calendrier.grab_set()
    calendrier.title("Calendrier")
    calendrier.geometry("300x300")

    affichage_calendrier = tkcalendar.Calendar(calendrier, selectmode="day", date_pattern="dd/MM/yyyy")
    affichage_calendrier.pack(expand=True, fill="both")

    def valider_date():
        date_selectionnee = affichage_calendrier.get_date()
        print(f"Date choisie : {date_selectionnee}")
        calendrier.destroy()

    bouton_valider = ctk.CTkButton(calendrier, text="Valider", command=valider_date)
    bouton_valider.pack(pady=10)

button = ctk.CTkButton(app, text="Pop-up calendrier", fg_color="#1E90FF", hover_color="#104E8B",
                       command=pop_up_calendrier)
button.pack(pady=20)

app.mainloop()