import yt_dlp as youtube_dl
from os.path import join
import threading
from time import time 
#######################################################################################################
# from functools import partial
# # import all components from the tkinter library
# from tkinter import *
# # import filedialog module
# from tkinter import filedialog

# # Function for opening the 
# # file explorer window
# def browseFiles(label_file_explorer):
# 	filename = filedialog.askopenfilename(initialdir = "/",
# 										title = "Select a File",
# 										filetypes = (("Text files",
# 														"*.txt*"),
# 													("all files",
# 														"*.*")))
	
# 	# Change label contents
# 	label_file_explorer.configure(text="File Opened: "+filename)
	
	
# def fileExplorerWindow():																					
#     # Create the root window
#     window = Tk()

#     # Set window title
#     window.title('File Explorer')

#     # Set window size
#     window.geometry("500x500")

#     #Set window background color
#     window.config(background = "white")

#     # Create a File Explorer label
#     label_file_explorer = Label(window, 
#                                 text = "Select the text file with the songs URLs",
#                                 width = 100, height = 4, 
#                                 fg = "blue")

        
#     button_explore = Button(window, 
#                             text = "Browse Files",
#                             command = partial(browseFiles, label_file_explorer)) 

#     button_exit = Button(window, 
#                         text = "Exit",
#                         command = exit) 

#     # Grid method is chosen for placing
#     # the widgets at respective positions 
#     # in a table like structure by
#     # specifying rows and columns
#     label_file_explorer.grid(column = 1, row = 1)

#     button_explore.grid(column = 1, row = 2)

#     button_exit.grid(column = 1, row = 3)

#     # Let the window wait for any events
#     window.mainloop()
#######################################################################################################
def get_songs_list(path):
    with open(path, "r") as file:
        songs = file.readlines()
    return songs

def get_video_info(url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = url,download=False
    )
    return video_info

def download_song(video_info, output_folder):
    if video_info.get('creator'):
        filename = f"{video_info['title']} -  {video_info.get('creator')}"
    else:
        filename = f"{video_info['title']}"
    print(f"Downloading {filename}")
    filename = f"{filename}.mp4"
    options={
        'format':'best',#/bestaudio',
        'keepvideo':False,
        'outtmpl':join(output_folder, filename),
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

def get_info_and_download_song(song_url, output_folder):
    video_info = get_video_info(song_url)
    download_song(video_info, output_folder)

if __name__ == '__main__':

    songs_path = input('Archivo con lista de canciones: ')
    dest_path = input('Carpeta donde las queres guardar:')

    t0 = time()

    songs = get_songs_list(songs_path)
    #Separo en grupos de descarga para que no se hagan muchos threads al mismo tiempo
    group_size = 5
    songs_groups = [songs[i:i+group_size] for i in range(0, len(songs), group_size)]
    
    for group in songs_groups:
        threads = list()
        for song in group:
            x = threading.Thread(target=get_info_and_download_song, args=(song,dest_path))
            threads.append(x)
            x.start()

        for thread in threads:
            thread.join()
    t1 = time()
    print(f'Duración: {t1-t0:.2f} seg')

