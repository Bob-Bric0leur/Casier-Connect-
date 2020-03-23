import tkinter as tk
import database
from functools import partial


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Settings)
        self.geometry("800x400")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill=tk.BOTH)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.setting_icon = tk.PhotoImage(file="icon/icon-setting-50.png")


        top = tk.Frame(self)
        top.grid_columnconfigure(0, weight=10)
        top.grid_columnconfigure(1, weight=1)
        tk.Button(top, text="Parametre", image=self.setting_icon, relief=tk.FLAT, font=("Arial", 10), 
                command=lambda: master.switch_frame(Settings)).grid(row=0, column=1, pady=10)

        top.pack(fill = tk.BOTH)

        tk.Label(self, text="Veuiller scaner votre carte", font=("Arial", 20)).pack(expand=True)

        tk.Button(self, text="simu carte", command=lambda: master.switch_frame(SelectionPage)).pack()

#class PinCode():

#class Inscription():

class Settings(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.List = None
        self.master = master
        self.exit_icon = tk.PhotoImage(file="icon/icon-exit-50.png")
        self.exit_icon_sub = self.exit_icon.subsample(2)

        #Creation Menu gauche
        Menu = tk.Frame(self, background="light grey", relief=tk.RAISED)
        Menu.grid_columnconfigure(0, weight=1)

        #ajout Boutton au Menu gauche
        tk.Button(Menu, text="Utilisateurs", relief=tk.FLAT, font=("Arial", 15, "bold"), background="light grey", command=self.list_users).grid(row=0, pady=10)
        tk.Button(Menu, text="Casiers", relief=tk.FLAT, font=("Arial", 15, "bold"), background="light grey", command=self.list_locker).grid(row=1, pady=10)

        Menu.grid(row=0, column=0, sticky="nsew")
        
        #Ajout Button sortir
        Menu2 = tk.Frame(self, background="light grey")
        tk.Button(Menu2, image=self.exit_icon_sub, compound=tk.LEFT, text=" Sortir", relief=tk.FLAT, font=("Arial", 15, "bold"), background="light grey",
        command= lambda: master.switch_frame(StartPage)).pack()
        Menu2.grid(row=1, column=0, sticky="nsew")
      
        #Config ratio
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=1)


    
    def list_users(self):
        if self.List != None:
            self.List.destroy()

        self.frames = None

        self.List = tk.Frame(self)     
        self.List.grid(rowspan=2, row=0, column=1, sticky="nsew")
        
        self.List.grid_columnconfigure(0, weight=1)
        self.List.grid_rowconfigure(1, weight=1)
        self.user_var = tk.StringVar()
        self.user_var.trace_add("write", self.on_change)

        self.entry = tk.Entry(self.List, textvariable=self.user_var, font=("Arial", 15))
        self.entry.grid(row=0, column=0, sticky="nsew")
        
        self.List2 = VerticalScrolledFrame(self.List)
        self.List2.grid(row=1, column=0, sticky="nsew")
        
        self.List2.interior.grid_columnconfigure(0, weight=1)
       
        self.frames = [tk.Label(self.List2.interior, text="Veuiller entrer un nom ou un numéro d'étudiant", font=("Arial", 15, "bold"))]
        self.frames[0].grid(row=0 , column=0)
        


    def on_change(self, *args):
        if self.frames != None:
            for i in self.frames:
                i.destroy()

        if database.partial_select(self.user_var.get()) == [] and database.partial_select_num(self.user_var.get()) == []:
            self.frames = [tk.Label(self.List2.interior, text="Aucune Correspodance", font=("Arial", 15, "bold"))]
            self.frames[0].grid(row=0 , column=0)
            self.List.update_idletasks()
            print("pas de correspondance")

        elif self.user_var.get() == "":
            self.frames = [tk.Label(self.List2.interior, text="Veuiller entrer un nom ou un numéro d'étudiant", font=("Arial", 15, "bold"))]
            self.frames[0].grid(row=0 , column=0)
            self.List.update_idletasks()
            print("vide")
            
        else:
            try:
                int(self.user_var.get())

                self.frames = [UserFrame(self.List2.interior, i[1][0], background="lightgrey") for i in enumerate(database.partial_select_num(self.user_var.get()))]

            except:
                self.frames = [UserFrame(self.List2.interior, i[1][0], background="lightgrey") for i in enumerate(database.partial_select(self.user_var.get()))]

            for i in enumerate(self.frames):
                i[1].grid(row=i[0], column=0, pady=5)
            self.List.update_idletasks()

    def list_locker(self):
        if self.List != None:
            self.List.destroy()

        self.List = VerticalScrolledFrame(self)
        self.List.grid(rowspan=2, row=0, column=1, sticky="nsew")
        self.List.interior.columnconfigure(0, weight=1)

        self.frames = [LockerFrame(self.List.interior, i[1][0], background="lightgrey") for i in enumerate(database.select_all_casier())]
        for i in enumerate(self.frames):
            i[1].grid(row=i[0], column=0, pady=5)
        self.List.update_idletasks()


class UserFrame(tk.Frame):
    def __init__(self, parent, uid, *args, **kw):
        self.parent = parent
        self.etat_agrandissement = False
        self.uid = uid
        self.max_casier = tk.IntVar()
        self.max_casier.set(database.get_max_locker(uid))
        
        self.button_var = tk.StringVar()
        self.button_var.set("down")


        tk.Frame.__init__(self, self.parent, *args, **kw)
        
        self.user_info = database.select_user_by_uid(self.uid)


        self.nom_label = tk.Label(self, text="Nom: "+str(self.user_info[0]), font=("Arial", 15, "bold"), background="lightgrey")
        self.nom_label.grid(row=0, column=0)

        self.prenom_label = tk.Label(self, text="Prenom: "+str(self.user_info[1]), font=("Arial", 15, "bold"), background="lightgrey")
        self.prenom_label.grid(row=0, column=1, padx=10)

        self.numEtu_label = tk.Label(self, text="Num Etu: "+str(self.user_info[2]), font=("Arial", 15, "bold"), background="lightgrey")
        self.numEtu_label.grid(row=0, column=2, padx=10)

        self.down_button = tk.Button(self, textvariable=self.button_var , width=5, font=("Arial", 15, "bold"), relief=tk.FLAT, background="lightgrey",  command=self.on_click)
        self.down_button.grid(row=0, column=3, padx=20)

        
    def on_click(self):
        if not self.etat_agrandissement:
            self.button_var.set("up")

            self.test = tk.Label(self, textvariable=self.max_casier, font=("Arial", 15, "bold"))
            self.test.grid(row=1, column=0, pady=10)

            self.plus_button = tk.Button(self, text="+", command=self.add_max)
            self.plus_button.grid(row=1, column=1)

            self.moin_button = tk.Button(self, text="-", command=self.remove_max)
            self.moin_button.grid(row=1, column=2)

            self.etat_agrandissement = True

        else:

            l=list(self.grid_slaves(row=int(1)))
            for w in l:
                w.grid_forget()

            self.button_var.set("down")
            self.etat_agrandissement = False

    def add_max(self):
        database.set_max_locker(self.uid, database.get_max_locker(self.uid)+1)

        self.max_casier.set(database.get_max_locker(self.uid))

    def remove_max(self):
        if database.get_max_locker(self.uid)>0:
            database.set_max_locker(self.uid, database.get_max_locker(self.uid)-1)
            self.max_casier.set(database.get_max_locker(self.uid))


class LockerFrame(tk.Frame):
    def __init__(self, parent, casier_id, *args, **kw):
        self.parent = parent
        self.etat_agrandissement = False
        self.casier_id = casier_id

        
        self.button_var = tk.StringVar()
        self.button_var.set("down")


        tk.Frame.__init__(self, self.parent, *args, **kw)
        
        self.casier_info = database.select_casier_by_id(self.casier_id)


        self.num_casier = tk.Label(self, text="Casier "+str(self.casier_info[0]), font=("Arial", 15, "bold"), background="lightgrey")
        self.num_casier.grid(row=0, column=0)


        self.down_button = tk.Button(self, textvariable=self.button_var , width=5, font=("Arial", 15, "bold"), relief=tk.FLAT, background="lightgrey",  command=self.on_click)
        self.down_button.grid(row=0, column=2, padx=20)

        
    def on_click(self):
        if not self.etat_agrandissement:
            self.button_var.set("up")

            self.etat_agrandissement = True

        else:

            l=list(self.grid_slaves(row=int(1)))
            for w in l:
                w.grid_forget()

            self.button_var.set("down")
            self.etat_agrandissement = False


class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        """
        self.offset_y = 0
        self.prevy = 0
        self.scrollposition = 1

        def on_press(event):
            self.offset_y = event.y_root
            if self.scrollposition < 1:
                self.scrollposition = 1
            elif self.scrollposition > interior.winfo_reqheight():
                self.scrollposition = interior.winfo_reqheight()
            canvas.yview_moveto(self.scrollposition / interior.winfo_reqheight())

        def on_touch_scroll(event):
            nowy = event.y_root

            sectionmoved = 15
            if nowy > self.prevy:
                event.delta = -sectionmoved
            elif nowy < self.prevy:
                event.delta = sectionmoved
            else:
                event.delta = 0
            self.prevy= nowy

            self.scrollposition += event.delta
            canvas.yview_moveto(self.scrollposition/ interior.winfo_reqheight())

        self.bind("<Enter>", lambda _: self.bind_all('<Button-1>', on_press), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<Button-1>'), '+')
        self.bind("<Enter>", lambda _: self.bind_all('<B1-Motion>', on_touch_scroll), '+')
        self.bind("<Leave>", lambda _: self.unbind_all('<B1-Motion>'), '+')
        """


class SelectionPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.open_lock = tk.PhotoImage(file="icon/open-lock.png")
        self.open_lock_sub = self.open_lock.subsample(3)

        self.locker_icon = tk.PhotoImage(file="icon/icon-school-locker.png")

        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)
        tk.Label(self, text="test", font=("Arial", 15, "bold")).grid(columnspan=2, row=0, column=0)



        tk.Button(self, background="lightgrey", text="Ouvrir mon Casier", image=self.open_lock_sub, compound=tk.BOTTOM, relief=tk.FLAT, font=("Arial", 15, "bold")).grid(row=1, column=0)

        tk.Button(self, background="lightgrey", text="Attribution Casier", image=self.locker_icon, compound=tk.BOTTOM, relief=tk.FLAT, font=("Arial", 15, "bold")).grid(row=1, column=1)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()