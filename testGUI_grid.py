import tkinter as tk
import customtkinter as ctk 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title = "Custom Tkinter - test of nested frames"
root.geometry("1024x768+400+100")

root.grid_columnconfigure((0,1,2), minsize=300, weight=1, uniform = 'thirds')
root.grid_rowconfigure((0), weight=1) #, uniform = 'a')
root.grid_rowconfigure((1), minsize=300, weight=6) #, uniform = 'a')
root.grid_rowconfigure((2), minsize=200, weight=4) #, uniform = 'a')

frame_title = ctk.CTkFrame(master=root)
frame_upper = ctk.CTkFrame(master=root)
frame_lower = ctk.CTkFrame(master=root)
frame_1 = ctk.CTkFrame(master=frame_upper, border_width=2)
frame_2 = ctk.CTkFrame(master=frame_upper, border_width=2)
frame_3 = ctk.CTkFrame(master=frame_upper, border_width=2)
label_title = ctk.CTkLabel(master=frame_title, text="Server Admin Tool", height=96, font=("Arial", 36))
label_1 = ctk.CTkLabel(master=frame_1, text="Players", font=("Arial", 16))
label_2 = ctk.CTkLabel(master=frame_2, text="Game Status", font=("Arial", 16))
textbox = ctk.CTkTextbox(master=frame_lower, border_width=2) 

frame_title.grid(row=0, column=0, columnspan=3, sticky="nesw")
label_title.pack(side="left", fill="both", expand=True, padx=10, pady=10)
frame_upper.grid(row=1, column=0, columnspan=3, sticky="nesw")
frame_lower.grid(row=2, column=0, columnspan=3, sticky="nesw")
frame_1.pack(anchor='center', side="left", fill="both", expand=True, padx=10, pady=10)
frame_2.pack(anchor='center', side="left", fill="both", expand=True, padx=10, pady=10)
frame_3.pack(anchor='center', side="left", fill="both", expand=True, padx=10, pady=10)
label_1.pack(side="top", anchor='w', padx=15, pady=12)#, fill="both", expand=True)
label_2.pack(side="left", anchor='ne', padx=15, pady=12)#, fill="both", expand=True)
textbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

player_values=[]
list_players = tk.Listbox(frame_1, listvariable=player_values, height=10, background="#2E2E2F")
list_players.pack(side="top", padx=10, pady=10, fill="both", expand=True)

def populatebox():
    list_players.insert(0, "First Player")

btn = ctk.CTkButton(master=frame_3, text="Load Players", command = lambda: populatebox())
btn.pack()

root.mainloop() 
