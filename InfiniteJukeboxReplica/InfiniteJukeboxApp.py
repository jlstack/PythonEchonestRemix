__author__ = 'lukestack'

import Tkinter as tk
import InfiniteJukebox

class InfiniteJukeboxApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title = tk.Label(self, text="InfiniteJukeboxReplica", font=("Helvetica", 30), pady=10)
        self.title.pack()
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Get", command=self.on_button)
        self.entry.pack()
        self.button.pack()
        self.thresh = tk.Scale(self, label="Threshold", from_=0, to=80, tickinterval=5, orient='horizontal', length=400)
        self.thresh.set(65)
        self.thresh.pack()

    def on_button(self):
        song = self.entry.get()
        threshold = self.thresh.get()
        print song, threshold
        InfiniteJukebox.main(song, threshold)

app = InfiniteJukeboxApp()
app.mainloop()