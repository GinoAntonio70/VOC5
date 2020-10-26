import pandas as pd
import os
import random
from tkinter import *
import tkinter as tk
import random
import pickle



def load_df():
    global relativerPfad, df
    path = os.getcwd()
    relativerPfad = os.path.join(path, "vokabeln.csv")

    try:
        df = pd.read_csv(relativerPfad, index_col=0)
        df.reset_index(inplace=True, drop=True)
    except:
        df = pd.DataFrame(columns=['deutsch', 'uebersetzung'])
        df.reset_index(inplace=True, drop=True)
        df.to_csv(relativerPfad)
    return df


def vokabeltest(*event):
    dfc = pickle.loads(pickle.dumps(df))

    def frage(*event):

        dfc_laenge = dfc.shape[0]
        if dfc.shape[0] > 0:

            global zufallszahl
            zufallszahl = (random.randint(0, dfc_laenge - 1))
            fragewort_deutsch = dfc.iloc[zufallszahl, 0]
            uebersetze = Label(text="Übersetze:  ", width="31", height="2", bg="grey")
            uebersetze.place(x=200, y=100)
            fragewort_label = Label(text=fragewort_deutsch, font="Helvetica 14 bold italic", width="18", height="2",
                                    bg="grey")
            fragewort_label.place(x=200, y=150)
            eingabe_wort = StringVar

            def check(*vokabel):

                eingabe = str(ueber_entry.get())
                antwort = str(dfc.iloc[zufallszahl, 1])
                if antwort == eingabe:
                    richtig_label = Label(text="Die letze Antwort war richtig!", width="50", height="2", bg="white")
                    richtig_label.place(x=150, y=20)
                    dfc.drop(dfc.index[zufallszahl], inplace=True)
                    dfc.reset_index(drop=True, inplace=True)
                    ueber_entry.delete(0, END)
                    ueber_entry.focus_set()
                    global richtige_abfragen
                    richtige_abfragen += 1
                    frage()
                else:
                    richtige_antwort = antwort + " wäre richtig gewesen!"
                    falsch_label = Label(text=richtige_antwort, width="50", height="2", bg="white")
                    falsch_label.place(x=150, y=20)
                    ueber_entry.delete(0, END)
                    ueber_entry.focus_set()
                    global falsche_abfragen
                    falsche_abfragen += 1
                    frage()

            ueber_entry = Entry(textvariable=eingabe_wort, font="Helvetica 14 bold italic", width="20", bg="grey")
            ueber_entry.place(x=200, y=230)
            ueber_entry.focus_set()
            ueber_entry.bind('<Return>', check)

            check_button = tk.Button(master, text="check", width="25", height="2", bg="grey", command=check)
            check_button.bind('<Return>', check)
            # check_button.place(x=200, y=280)

            next_button = tk.Button(master, text="next", width="25", height="2", bg="grey", command=check)
            next_button.bind('<Return>', vokabeltest)
            # next_button.place(x=200, y=340)

        else:
            for widget in master.winfo_children():
                widget.destroy()

            if (df.shape[0]) >= 50:
                fleiss_label = Label(
                    text="Respekt! Das waren einge Vokabeln - so viel ich konnte die nicht mehr zählen - " + str(
                        df.shape[0]),
                    width="60", height="2", bg="yellow")
                fleiss_label.place(x=100, y=200)
            if (df.shape[0]) <= 5:
                faul_label = Label(text="Du fauler Lappen, das war's schon? Nur " + str(df.shape[0]) + " Vokabeln?",
                                   width="60", height="2", bg="yellow")
                faul_label.place(x=100, y=200)

            else:
                medium_label = Label(
                    text="Komm schon! Ich brauche mehr Vokabeln! " + str(df.shape[0]) + " Vokabeln? Da geht noch was!",
                    width="60", height="2", bg="yellow")
                medium_label.place(x=100, y=200)

            ergebnis = "Für " + str(df.shape[0]) + " Vokabeln, hast Du " \
                       + str(falsche_abfragen + richtige_abfragen) + " Versuche gebraucht!"
            ergebnis_label = Label(text=ergebnis, width="60", height="2", bg="grey")
            ergebnis_label.place(x=100, y=100)

            abfrage_button = Button(master, text="Vokabeln abfragen?", width="25", height="2", bg="grey",
                                    command=vokabeln_abfragen)
            abfrage_button.place(x=10, y=430)
            abfrage_button.bind('<Return>', vokabeln_abfragen)

            eingabe_button = Button(master, text="Vokabeln eingeben?", width="25", height="2", bg="grey",
                                    command=vokabeln_anlegen)
            eingabe_button.place(x=220, y=430)
            eingabe_button.focus_set()
            eingabe_button.bind('<Return>', vokabeln_anlegen)

            button_quit = Button(master, text="kein Bock mehr!", width="25", height="2", bg="grey",
                                 command=master.destroy)
            button_quit.place(x=430, y=430)

    frage()

    button_quit = Button(master, text="kein Bock mehr!", width="30", height="2", bg="grey", command=quit)
    button_quit.place(x=200, y=430)
    button_quit.bind('<Return>', quit)


def vokabeln_abfragen(*event):
    load_df()
    for widget in master.winfo_children():
        widget.destroy()

    if df.shape[0] == 0:

        keine_vokabel_label = Label(text="keine Vokabeln gespeichert!",
                                    width="30", height="2", bg="orange")
        keine_vokabel_label.place(x=200, y=140)
        weiter_button = Button(text="Vokabeln anlegen!",
                               width="30", height="2", bg="grey",
                               command=vokabeln_anlegen)
        weiter_button.place(x=200, y=200)

        button_quit = Button(master, text="kein Bock mehr!", width="30", height="2", bg="grey", command=quit)
        button_quit.place(x=200, y=430)
        button_quit.bind('<Return>', quit)

    else:
        vokabeltest()


def vokabeln_loeschen(*event):
    dfl = pd.DataFrame(columns=['deutsch', 'uebersetzung'])
    dfl.reset_index(inplace=True, drop=True)
    dfl.to_csv(relativerPfad)


def vokabeln_anlegen(*event):
    for widget in master.winfo_children():
        widget.destroy()

    load_df()

    deutsches_wort = Label(text="Deutsch:  ", font='bold', bg="grey")
    uebersetzung = Label(text="Übersetzung:  ", font='bold', bg="grey")
    deutsches_wort.place(x=230, y=150)
    uebersetzung.place(x=230, y=250)

    deutsch = StringVar()
    ueber = StringVar()

    deutsch_entry = Entry(textvariable=deutsch, width="30")
    deutsch_entry.place(x=230, y=180)
    deutsch_entry.focus_set()
    deutsch_entry.bind('<Return>', 'event generate %W <Tab>')

    ueber_entry = Entry(textvariable=ueber, width="30")
    ueber_entry.place(x=230, y=280)
    ueber_entry.bind('<Return>', 'event generate %W <Tab>')

    def save_info(*event):
        # print([deutsch.get(), ueber.get()])
        df.reset_index(inplace=True, drop=True)
        df.loc[len(df.index)] = [deutsch.get(), ueber.get()]
        df.to_csv(relativerPfad)
        deutsch_entry.delete(0, END)
        ueber_entry.delete(0, END)

        deutsch_entry.focus_set()

    def quit(*event):
        master.destroy()




    merken = tk.Button(master, text="merken", width="30", height="2", bg="grey", command=save_info)
    merken.bind('<Return>', save_info)
    merken.place(x=230, y=330)

    zur_abfrage_wechseln = Button(text="Zur Abfrage wechseln?", width="30", height="2", bg="grey",
                                  command=vokabeln_abfragen)
    zur_abfrage_wechseln.bind('<Return>', vokabeln_abfragen)
    zur_abfrage_wechseln.place(x=230, y=380)

    loeschen_button = Button(text="Alle Vokabeln Löschen?", width="30", height="2", bg="grey",
                                  command=vokabeln_loeschen)
    loeschen_button.bind('<Return>', vokabeln_abfragen)
    loeschen_button.place(x=230, y=10)

    button_quit = Button(master, text="kein Bock mehr!", width="30", height="2", bg="grey", command=quit)
    button_quit.place(x=230, y=430)
    button_quit.bind('<Return>', quit)


master = Tk()
master.geometry("640x480")
master['bg'] = '#49A'
master.title("Super Vokabelapp")


gruss_label = Label(master, text="Yang's Vokabel Trainer", font=("Helvetica", 18), width="25", height="2", bg="darkgrey")
gruss_label.place(x=140, y=230)

abfrage_button = Button(master, text="Vokabeln abfragen?", width="25", height="2", bg="grey", command=vokabeln_abfragen)
abfrage_button.place(x=440, y=430)
abfrage_button.bind('<Return>', vokabeln_abfragen)

eingabe_button = Button(master, text="Vokabeln eingeben?", width="25", height="2", bg="grey", command=vokabeln_anlegen)
eingabe_button.place(x=10, y=430)
eingabe_button.focus_set()
eingabe_button.bind('<Return>', vokabeln_anlegen)

richtige_abfragen = 0
falsche_abfragen = 0

mainloop()
