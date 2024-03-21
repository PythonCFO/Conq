import tkinter
import customtkinter as ctk 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title = "Custom Tkinter - test of nested frames"
root.geometry("1024x768+400+100")

label_title = ctk.CTkLabel(master=root, text="Server Admin Tool", height=96, font=("Arial", 36))
frame_detail = ctk.CTkFrame(master=root,height=350)
frame_ops = ctk.CTkFrame(master=root, height=300)

frame_players = ctk.CTkFrame(master=frame_detail,border_width=2, height=330)
frame_game = ctk.CTkFrame(master=frame_detail, border_width=2, height=330)
frame_controls = ctk.CTkFrame(master=frame_detail, border_width=2, height=330)

label_players = ctk.CTkLabel(master=frame_players, text="Players")
label_game = ctk.CTkLabel(master=frame_game, text="Game")
button = ctk.CTkButton(master=frame_controls, text="TestBtn")
textbox = ctk.CTkTextbox(master=frame_ops, width=668, corner_radius=0)

#Top level layout structure
label_title.pack(side="top", padx=50)
frame_detail.pack(side="top", fill="both", expand=True, padx=10, pady=10) 
frame_ops.pack(side="top", fill="both", expand=True, padx=10, pady=10) 
textbox.pack(side="bottom", padx=10, pady=10)

#Level 2 layout
frame_players.pack(side="left", fill="both", expand=True, padx=10, pady=10)
frame_game.pack(side="left", fill="both", expand=True, padx=10, pady=10)
frame_controls.pack(side="left", fill="both", expand=True, padx=10, pady=10)

#Level 3 layout
label_players.pack(side="top", pady=10)
label_game.pack(side="top", pady=10)
button.pack(side="top", pady=10)

root.mainloop() 
