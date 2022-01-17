from tkinter import *
from tkinter import filedialog as opens
import pygame
import os
import time
from tkinter import ttk
from ttkthemes import themed_tk as tk
import threading
from mutagen.mp3 import MP3

pygame.mixer.init()

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.minsize(780, 400)
root.title("DOMDOM")
root.iconbitmap("image/icon.ico")
root.resizable(0, 0)

menubar = Menu(root)
root.config(menu=menubar)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open")
submenu.add_command(label="Exit", command=root.quit)

playImage = PhotoImage(file="image/play.png")
pauseImage = PhotoImage(file="image/pause.png")
stopImage = PhotoImage(file="image/stop-button.png")
nextImage = PhotoImage(file="image/sext.png")
previousImage = PhotoImage(file="image/previous.png")
muteImage = PhotoImage(file="image/mute.png")
volumeImage = PhotoImage(file="image/olume.png")
musicImage = PhotoImage(file="image/headphones.png")
rewindImage = PhotoImage(file="image/ewind.png")

list_song = []
index = 0
addd = 0
listed = FALSE
muted = FALSE
stopped = FALSE
paused = FALSE


def add_music():
    global listed
    global stopped
    global addd
    global paused

    file_path = opens.askopenfilenames(initialdir="", filetypes=(("All Files", "*.*"), ("Mp3 files", "*.mp3")),
                                       title="Select Files")

    if not listed:
        for files in file_path:
            if files.endswith(".mp3") or files.endswith(".MP3"):
                list_song.append(files)
                name = os.path.basename(files)
                listbox.insert(addd, name)
                addd += 1

        current_song = list_song[index]
        pygame.mixer_music.load(current_song)
        pygame.mixer_music.play()
        playImage.configure(file="image/pause.png")

        playing = os.path.basename(current_song)

        currentplaying = ttk.Label(root, text=playing,
                                   justify="center", relief=SUNKEN,
                                   font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

        file_data = os.path.splitext(current_song)

        if file_data[1] == ".mp3":
            audio = MP3(current_song)
            total_length = audio.info.length

            mins, sec = divmod(total_length, 60)
            mins = round(mins)
            sec = round(sec)

            timeformat = "{:02d}:{:02d}".format(mins, sec)

            totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
            t1 = threading.Thread(target=start_counting, args=(total_length,))
            t1.start()
        else:
            a = pygame.mixer.Sound(current_song)
            total_length = a.get_length()

            totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

            t1 = threading.Thread(target=start_counting, args=(total_length,))
            t1.start()
        listed = TRUE
        stopped = FALSE
        paused = FALSE

    else:
        for files in file_path:
            if files.endswith(".mp3") or files.endswith(".MP3"):
                list_song.append(files)
                name = os.path.basename(files)
                listbox.insert(addd, name)
                addd += 1

                listed = TRUE
                stopped = FALSE
                paused = FALSE




def play():
    global index
    global paused
    global stopped
    global listed

    if stopped:
        try:
            selected_song = listbox.curselection()
            selected_song = int(selected_song[0])
            index = selected_song
            time.sleep(1)
            current_song = list_song[index]
            pygame.mixer_music.load(current_song)
            pygame.mixer_music.play()
            playImage.configure(file="image/pause.png")

            playing = os.path.basename(current_song)

            currentplaying = ttk.Label(root, text=playing,
                                       justify="center", relief=SUNKEN,
                                       font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

            file_data = os.path.splitext(current_song)

            if file_data[1] == ".mp3":
                audio = MP3(current_song)
                total_length = audio.info.length

                mins, sec = divmod(total_length, 60)
                mins = round(mins)
                sec = round(sec)

                timeformat = "{:02d}:{:02d}".format(mins, sec)

                totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                      justify="center", relief=GROOVE,
                                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
                t1 = threading.Thread(target=start_counting, args=(total_length,))
                t1.start()
            else:
                a = pygame.mixer.Sound(current_song)
                total_length = a.get_length()

                totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                      justify="center", relief=GROOVE,
                                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

                t1 = threading.Thread(target=start_counting, args=(total_length,))
                t1.start()

            stopped = FALSE
            paused = FALSE
        except:
            if not listed:
                add_music()
                listed = TRUE
            else:
                pass

    elif not stopped:
        if paused:
            pygame.mixer_music.unpause()
            playImage.configure(file="image/pause.png")
            paused = FALSE

        else:
            pygame.mixer_music.pause()
            playImage.configure(file="image/play.png")
            paused = TRUE
    #
    # else:
    #     pygame.mixer_music.pause()
    #     playImage.configure(file="image/play.png")
    #     paused = TRUE


def start_counting(t):
    while t and pygame.mixer_music.get_busy():
        if paused:
            continue
        else:
            mins, sec = divmod(t, 60)
            mins = round(mins)
            sec = round(sec)

            timeformat = "{:02d}:{:02d}".format(mins, sec)

            currenttime = ttk.Label(root, text=f"Current Time: -{timeformat}",
                                    justify="center", relief=GROOVE,
                                    font="verdana 10 bold", width=24, anchor=W).place(x=540, y=42)
            time.sleep(1)
            t -= 1
            print(t)

        if t < 3:
            finished()
            break


def stop():
    global stopped
    global paused
    pygame.mixer.music.stop()
    stopped = TRUE
    paused = TRUE
    playImage.configure(file="image/play.png")


def pause():
    global paused
    pygame.mixer.music.pause()
    paused = TRUE


def next():
    try:
        global currenttime
        global index
        global stopped
        global paused

        stop()
        time.sleep(1)

        index += 1

        next = list_song[index]

        pygame.mixer_music.load(next)
        pygame.mixer_music.play()

        playing = os.path.basename(next)
        playImage.configure(file="image/pause.png")

        currentplaying = ttk.Label(root, text=playing,
                                   justify="center", relief=SUNKEN,
                                   font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

        file_data = os.path.splitext(next)

        if file_data[1] == ".mp3":
            audio = MP3(next)
            total_length = audio.info.length

            mins, sec = divmod(total_length, 60)
            mins = round(mins)
            sec = round(sec)

            timeformat = "{:02d}:{:02d}".format(mins, sec)

            totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
        else:
            a = pygame.mixer.Sound(next)
            total_length = a.get_length()

            totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

        t1 = threading.Thread(target=start_counting, args=(total_length,))
        t1.start()
        stopped = FALSE
        paused = FALSE
    except:
        try:
            index = 0

            next = list_song[index]

            pygame.mixer_music.load(next)
            pygame.mixer_music.play()

            playing = os.path.basename(next)
            playImage.configure(file="image/pause.png")

            currentplaying = ttk.Label(root, text=playing,
                                       justify="center", relief=SUNKEN,
                                       font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

            file_data = os.path.splitext(next)

            if file_data[1] == ".mp3":
                audio = MP3(next)
                total_length = audio.info.length

                mins, sec = divmod(total_length, 60)
                mins = round(mins)
                sec = round(sec)

                timeformat = "{:02d}:{:02d}".format(mins, sec)

                totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                      justify="center", relief=GROOVE,
                                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
            else:
                a = pygame.mixer.Sound(next)
                total_length = a.get_length()

                totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                      justify="center", relief=GROOVE,
                                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

            t1 = threading.Thread(target=start_counting, args=(total_length,))
            t1.start()
            stopped = FALSE
            paused = FALSE
        except:
            pass


def finished():
    try:
        global currenttime
        global index
        index += 1

        next = list_song[index]

        pygame.mixer_music.load(next)
        pygame.mixer_music.play()

        playing = os.path.basename(next)

        currentplaying = ttk.Label(root, text=playing,
                                   justify="center", relief=SUNKEN,
                                   font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

        file_data = os.path.splitext(next)

        if file_data[1] == ".mp3":
            audio = MP3(next)
            total_length = audio.info.length

            mins, sec = divmod(total_length, 60)
            mins = round(mins)
            sec = round(sec)

            timeformat = "{:02d}:{:02d}".format(mins, sec)

            totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
        else:
            a = pygame.mixer.Sound(next)
            total_length = a.get_length()

            totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

        t1 = threading.Thread(target=start_counting, args=(total_length,))
        t1.start()
    except:
        index = 0


def previous():
    try:
        global index
        global stopped
        global paused

        stop()
        time.sleep(1)

        index -= 1

        previous = list_song[index]

        pygame.mixer_music.load(previous)
        pygame.mixer_music.play()
        playImage.configure(file="image/pause.png")

        playing = os.path.basename(previous)

        currentplaying = ttk.Label(root, text=playing,
                                   justify="center", relief=SUNKEN,
                                   font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

        file_data = os.path.splitext(previous)

        if file_data[1] == ".mp3":
            audio = MP3(previous)
            total_length = audio.info.length

            mins, sec = divmod(total_length, 60)
            mins = round(mins)
            sec = round(sec)

            timeformat = "{:02d}:{:02d}".format(mins, sec)

            totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
        else:
            a = pygame.mixer.Sound(previous)
            total_length = a.get_length()

            totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                  justify="center", relief=GROOVE,
                                  font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

        t1 = threading.Thread(target=start_counting, args=(total_length,))
        t1.start()
        stopped = FALSE
        paused = FALSE
    except:
        try:
            index = 0

            previous = list_song[index]

            pygame.mixer_music.load(previous)
            pygame.mixer_music.play()
            playImage.configure(file="image/pause.png")

            playing = os.path.basename(previous)

            currentplaying = ttk.Label(root, text=playing,
                                       justify="center", relief=SUNKEN,
                                       font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

            file_data = os.path.splitext(previous)

            if file_data[1] == ".mp3":
                audio = MP3(previous)
                total_length = audio.info.length

                mins, sec = divmod(total_length, 60)
                mins = round(mins)
                sec = round(sec)

                timeformat = "{:02d}:{:02d}".format(mins, sec)

                totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                                      justify="center", relief=GROOVE,
                                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
            else:
                a = pygame.mixer.Sound(previous)
                total_length = a.get_length()

                totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                                      justify="center", relief=GROOVE,
                                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

            t1 = threading.Thread(target=start_counting, args=(total_length,))
            t1.start()
            stopped = FALSE
            paused = FALSE
        except:
            pass


def mute():
    global muted
    global scale
    global curren_value
    if muted:
        scale.set(curren_value)
        volumeImage.configure(file="image/olume.png")
        muted = FALSE
    else:
        done = pygame.mixer.music.get_volume()
        curren_value = done * 100
        scale.set(0)
        volumeImage.configure(file="image/mute.png")
        muted = TRUE


def volume(val):
    global muted
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)
    volumeImage.configure(file="image/olume.png")
    muted = FALSE


def rewind():
    global index
    global stopped
    global paused

    stop()
    time.sleep(1)

    current_song = list_song[index]
    pygame.mixer_music.load(current_song)
    pygame.mixer_music.play()
    playImage.configure(file="image/pause.png")

    file_data = os.path.splitext(current_song)

    if file_data[1] == ".mp3":
        audio = MP3(current_song)
        total_length = audio.info.length

        mins, sec = divmod(total_length, 60)
        mins = round(mins)
        sec = round(sec)

        timeformat = "{:02d}:{:02d}".format(mins, sec)

        totaltime = ttk.Label(root, text=f"Total Time: {timeformat}",
                              justify="center", relief=GROOVE,
                              font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
    else:
        a = pygame.mixer.Sound(current_song)
        total_length = a.get_length()

        totaltime = ttk.Label(root, text=f"Total Time: {total_length}",
                              justify="center", relief=GROOVE,
                              font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)

    t1 = threading.Thread(target=start_counting, args=(total_length,))
    t1.start()
    stopped = FALSE
    paused = FALSE


def delete():
    global stopped, paused, listed
    selected_song = listbox.curselection()
    selected_song = int(selected_song[0])
    listbox.delete(selected_song)
    list_song.pop(selected_song)
    stopped = FALSE
    paused = FALSE
    listed = FALSE
    # print(list_song)


musiclabel = ttk.Label(root, image=musicImage).place(x=450, y=70)

playbutton = ttk.Button(root, image=playImage, command=play).place(x=390, y=200)

stopbutton = ttk.Button(root, image=stopImage, command=stop).place(x=570, y=200)

# pausebutton = ttk.Button(root, image=pauseImage, command=pause).place(x=650, y=200)

previousbutton = ttk.Button(root, image=previousImage, command=previous).place(x=390, y=280)

rewindbutton = ttk.Button(root, image=rewindImage, command=rewind).place(x=480, y=280)

nextbutton = ttk.Button(root, image=nextImage, command=next).place(x=570, y=280)

volumebutton = ttk.Button(root, image=volumeImage, command=mute).place(x=390, y=320)

# playlist codes
playlistname = ttk.Label(root, text="PLAY LIST",
                         justify="center", relief=SUNKEN,
                         font="tahoma 15 bold", width=15, anchor=S).place(x=80, y=12)

listbox = Listbox(root, height=15, width=35)
listbox.place(x=30, y=40)

add = ttk.Button(root, text="+ Add", width=5, command=add_music).place(x=55, y=320)
remvoe = ttk.Button(root, text="- Del", width=5, command=delete).place(x=155, y=320)

currentplaying = ttk.Label(root, text="Current Music Playing",
                           justify="center", relief=SUNKEN,
                           font="verdana 10 bold", width=45, anchor=W).place(x=350, y=12)

totaltime = ttk.Label(root, text="Total Time: ",
                      justify="center", relief=GROOVE,
                      font="verdana 10 bold", width=20, anchor=W).place(x=350, y=42)
currenttime = ttk.Label(root, text="Current Time: ",
                        justify="center", relief=GROOVE,
                        font="verdana 10 bold", width=24, anchor=W).place(x=540, y=42)

scale = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, length=280, command=volume)
scale.place(x=470, y=340)
scale.set(20)


def close():
    stop()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)

stop()

root.mainloop()









# import pygame
# from tkinter import *
# from mutagen.mp3 import MP3
# import threading as th
# import time
# import os
# from tkinter import filedialog as file
# from tinytag import TinyTag, TinyTagException
#
# pygame.init()
#
# root = Tk()
# root.minsize(300, 150)
# root.resizable(0, 0)
# songs = []
# index = 0
#
#
# def file_select():
#     global index
#     global song_name
#     # file.askdirectory()
#     names = file.askopenfilenames(initialdir="",
#                                   filetypes=(("All Files", "*.*"),
#                                              ("Music Files", "*.mp3")),
#                                   title="Select File")
#     for files in names:
#         if files.endswith(".mp3"):
#             songs.append(files)
#
#     current_name = os.path.basename(songs[index])
#
#     current = songs[index]
#     # tag = TinyTag.get(current)
#     # print(str(tag.duration()))
#
#     file_date = os.path.splitext(current)
#
#     # if fil
#
#     song_name = Label(root, text=current_name)
#     song_name.configure(text=current_name)
#     song_name.place(x=30, y=100)
#
#     pygame.mixer.init()
#     pygame.mixer_music.load(current)
#     pygame.mixer_music.play()
#
#     name = os.path.basename(current)
#
#     playing = Label(root, text=name, )
#
#     file_data = os.path.splitext(current)
#
#     if file_data[1] == ".mp3":
#         audio = MP3(current)
#
#         total_lenght = audio.info.length
#
#     t = th.Thread(target=start_counting, args=(total_lenght,))
#     t.start()
#
#
# def start_counting(t):
#     while t:
#         mins, sec = divmod(t, 60)
#
#         mins = round(mins)
#         sec = round(sec)
#
#         time_fomat = "%02i:%02i" % (mins, sec)
#
#         cur_time = Label(root,
#                          text="Current time: -" + time_fomat).place(x=50, y=70)
#         time.sleep(1)
#         t -= 1
#
#         if t <= 3:
#             next_music()
#             break
#
#
# def next_music():
#     pygame.mixer_music.stop()
#     time.sleep(1)
#
#     try:
#         global index
#         global song_name
#         index += 1
#
#         current_name = os.path.basename(songs[index])
#
#         current = songs[index]
#         # tag = TinyTag.get(current)
#         # print(str(tag.duration()))
#
#         current_name = os.path.basename(current)
#         song_name.configure(text=current_name)
#
#         pygame.mixer.init()
#         pygame.mixer.music.load(current)
#         pygame.mixer_music.play()
#
#         file_data = os.path.splitext(current)
#
#         if file_data[1] == ".mp3":
#             audio = MP3(current)
#
#             total_lenght = audio.info.length
#
#         t = th.Thread(target=start_counting, args=(total_lenght,))
#         t.start()
#
#     except:
#         # global index
#         # global song_name
#
#         pygame.mixer_music.stop()
#         time.sleep(1)
#
#         index = 0
#
#         current_name = os.path.basename(songs[index])
#
#         current = songs[index]
#         # tag = TinyTag.get(current)
#         # print(str(tag.duration()))
#
#         current_name = os.path.basename(current)
#         song_name.configure(text=current_name)
#
#         pygame.mixer.init()
#         pygame.mixer.music.load(current)
#         pygame.mixer_music.play()
#
#         file_data = os.path.splitext(current)
#
#         if file_data[1] == ".mp3":
#             audio = MP3(current)
#
#             total_lenght = audio.info.length
#
#         t = th.Thread(target=start_counting, args=(total_lenght,))
#         t.start()
#
#
# def set_volume(val):
#     volume = int(val) / 100
#
#     pygame.mixer_music.set_volume(volume)
#
#
# next = Button(root, text="Next", command=next_music)
# next.pack()
#
# scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
# scale.pack()
# scale.set(40)
#
# file_select()
#
# root.mainloop()
