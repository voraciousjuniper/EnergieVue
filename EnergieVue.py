import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

def calculer_scenarios():
    try:
        cons_passee = float(entry_cons_passee.get())
        heures = float(entry_heures.get())
        minutes = float(entry_minutes.get())
        reserve = float(entry_reserve.get())
        
        mod_opt = float(scale_opt.get()) / 100.0
        mod_pess = float(scale_pess.get()) / 100.0
        
        duree_totale_heures = heures + (minutes / 60.0)
        if duree_totale_heures <= 0 or reserve <= 0 or cons_passee <= 0:
            raise ValueError
            
        rythme_moyen = cons_passee / duree_totale_heures
        
        rythme_opt = rythme_moyen * mod_opt
        rythme_milieu = rythme_moyen
        rythme_pess = rythme_moyen * mod_pess
        
        scenarios = [
            ("Optimiste 🌟", rythme_opt, lbl_opt_date, lbl_opt_timer),
            ("Juste Milieu 🎯", rythme_milieu, lbl_milieu_date, lbl_milieu_timer),
            ("Pessimiste ⚡", rythme_pess, lbl_pess_date, lbl_pess_timer)
        ]
        
        date_debut = datetime(2026, 11, 2, 18, 22)
        
        for nom, rythme, lbl_date, lbl_timer in scenarios:
            heures_restantes = reserve / rythme
            jours = int(heures_restantes // 24)
            hrs = int(heures_restantes % 24)
            mins = int(round((heures_restantes % 1) * 60))
            if mins == 60:
                hrs += 1
                mins = 0
            if hrs == 24:
                jours += 1
                hrs = 0
                
            date_fin = date_debut + timedelta(hours=heures_restantes)
            
            lbl_date.config(text=f"📅 Fin prévue : {date_fin.strftime('%d/%m/%Y à %H:%M')}")
            
            timer_str = "⏱️ Autonomie : "
            if jours > 0:
                timer_str += f"{jours}j "
            timer_str += f"{hrs}h {mins}m"
            lbl_timer.config(text=timer_str)
            
    except ValueError:
        for lbl in [lbl_opt_date, lbl_opt_timer, lbl_milieu_date, lbl_milieu_timer, lbl_pess_date, lbl_pess_timer]:
            lbl.config(text="⚠️ Valeur invalide")

# --- Fenêtre principale ---
root = tk.Tk()
root.title("⚡ Energievue - Visualiseur d'Autonomie")
root.geometry("540x650")
root.configure(bg="#F0F3F9")

# --- Système de défilement (Scrollbar + Canvas) ---
main_canvas = tk.Canvas(root, bg="#F0F3F9", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg="#F0F3F9")

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Redimensionnement automatique de la largeur interne
def _on_canvas_configure(event):
    main_canvas.itemconfig(canvas_window, width=event.width)

main_canvas.bind("<Configure>", _on_canvas_configure)
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Défilement à la molette de la souris
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# --- Header Attrayant ---
header_frame = tk.Frame(scrollable_frame, bg="#6C5CE7", pady=20)
header_frame.pack(fill="x")

lbl_header = tk.Label(
    header_frame, 
    text="⚡ ENERGIEVUE ⚡", 
    font=("Segoe UI", 18, "bold"), 
    bg="#6C5CE7", 
    fg="white"
)
lbl_header.pack()

lbl_subtitle = tk.Label(
    header_frame, 
    text="Simulez votre recharge de compteur en un clin d'œil", 
    font=("Segoe UI", 9, "italic"), 
    bg="#6C5CE7", 
    fg="#DFE6E9"
)
lbl_subtitle.pack(pady=(2, 0))

# --- Section 1: Formulaire des Données ---
frame_inputs = tk.LabelFrame(
    scrollable_frame, 
    text="  📌 Vos Paramètres Réels  ", 
    font=("Segoe UI", 11, "bold"), 
    bg="white", 
    fg="#2D3436", 
    bd=0, 
    relief="flat",
    padx=15, 
    pady=15
)
frame_inputs.pack(padx=20, pady=15, fill="x")

# Consommation passée
tk.Label(frame_inputs, text="Consommation observée (kWh) :", bg="white", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=6)
entry_cons_passee = ttk.Entry(frame_inputs, width=10, justify="center")
entry_cons_passee.insert(0, "0.52")
entry_cons_passee.grid(row=0, column=1, padx=10, pady=6)

# Durée
tk.Label(frame_inputs, text="Durée d'observation :", bg="white", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=6)
frame_duree = tk.Frame(frame_inputs, bg="white")
frame_duree.grid(row=1, column=1, padx=10, pady=6, sticky="w")

entry_heures = ttk.Entry(frame_duree, width=4, justify="center")
entry_heures.insert(0, "4")
entry_heures.pack(side="left")
tk.Label(frame_duree, text="h", bg="white", font=("Segoe UI", 10, "bold"), fg="#6C5CE7").pack(side="left", padx=(2, 6))

entry_minutes = ttk.Entry(frame_duree, width=4, justify="center")
entry_minutes.insert(0, "2")
entry_minutes.pack(side="left")
tk.Label(frame_duree, text="m", bg="white", font=("Segoe UI", 10, "bold"), fg="#6C5CE7").pack(side="left", padx=2)

# Réserve restante
tk.Label(frame_inputs, text="Énergie restante (kWh) :", bg="white", font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=6)
entry_reserve = ttk.Entry(frame_inputs, width=10, justify="center")
entry_reserve.insert(0, "11.22")
entry_reserve.grid(row=2, column=1, padx=10, pady=6)

# --- Section 2: Curseurs Ajustables ---
frame_sliders = tk.LabelFrame(
    scrollable_frame, 
    text="  🎛️ Modulateurs de Consommation  ", 
    font=("Segoe UI", 11, "bold"), 
    bg="white", 
    fg="#2D3436", 
    bd=0,
    padx=15, 
    pady=15
)
frame_sliders.pack(padx=20, pady=10, fill="x")

tk.Label(frame_sliders, text="Mode Économe (Optimiste % du rythme) :", bg="white", font=("Segoe UI", 9, "bold"), fg="#00B894").pack(anchor="w", pady=(0, 2))
scale_opt = tk.Scale(frame_sliders, from_=30, to=95, orient="horizontal", bg="white", activebackground="#00B894", highlightthickness=0, troughcolor="#EBFEEE", fg="#2D3436")
scale_opt.set(70)
scale_opt.pack(fill="x", pady=(0, 10))

tk.Label(frame_sliders, text="Mode Intensif (Pessimiste % du rythme) :", bg="white", font=("Segoe UI", 9, "bold"), fg="#D63031").pack(anchor="w", pady=(0, 2))
scale_pess = tk.Scale(frame_sliders, from_=105, to=250, orient="horizontal", bg="white", activebackground="#D63031", highlightthickness=0, troughcolor="#FFECEC", fg="#2D3436")
scale_pess.set(150)
scale_pess.pack(fill="x")

# --- Bouton d'action principal avec effet Hover ---
def on_enter(e):
    btn_calculer.config(bg="#5A4BDB")

def on_leave(e):
    btn_calculer.config(bg="#6C5CE7")

btn_calculer = tk.Button(
    scrollable_frame, 
    text="🚀 LANCER LA SIMULATION", 
    font=("Segoe UI", 11, "bold"), 
    bg="#6C5CE7", 
    fg="white", 
    activebackground="#5A4BDB", 
    activeforeground="white", 
    bd=0, 
    padx=20, 
    pady=12, 
    cursor="hand2",
    command=calculer_scenarios
)
btn_calculer.pack(pady=20)
btn_calculer.bind("<Enter>", on_enter)
btn_calculer.bind("<Leave>", on_leave)

# --- Section 3: Cartes de Résultats ---
def créer_carte_scenario(parent, titre, bg_color, border_color, text_color):
    card = tk.Frame(parent, bg=bg_color, highlightbackground=border_color, highlightthickness=2, padx=15, pady=12)
    card.pack(padx=20, pady=8, fill="x")
    
    lbl_title = tk.Label(card, text=titre, font=("Segoe UI", 12, "bold"), bg=bg_color, fg=text_color)
    lbl_title.pack(anchor="w")
    
    lbl_date = tk.Label(card, text="📅 Fin prévue : --/--/---- à --:--", font=("Segoe UI", 10), bg=bg_color, fg="#636E72")
    lbl_date.pack(anchor="w", pady=(4, 2))
    
    lbl_timer = tk.Label(card, text="⏱️ Autonomie : --h --m", font=("Segoe UI", 11, "bold"), bg=bg_color, fg=text_color)
    lbl_timer.pack(anchor="w")
    
    return lbl_date, lbl_timer

lbl_opt_date, lbl_opt_timer = créer_carte_scenario(scrollable_frame, "🌟 Scénario Optimiste (Économe)", "#E8F8F5", "#55E6C1", "#009432")
lbl_milieu_date, lbl_milieu_timer = créer_carte_scenario(scrollable_frame, "🎯 Scénario Nominal (Standard)", "#EBF5FB", "#74B9FF", "#0984E3")
lbl_pess_date, lbl_pess_timer = créer_carte_scenario(scrollable_frame, "⚡ Scénario Pessimiste (Intensif)", "#FDEDEC", "#FF7675", "#D63031")

# Spacer en bas pour faciliter le défilement
tk.Frame(scrollable_frame, height=20, bg="#F0F3F9").pack()

# Calcul initial
calculer_scenarios()

root.mainloop()