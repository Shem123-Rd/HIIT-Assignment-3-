import tkinter as tkinter
from tkinter import ttk
from tkinter import filedialog
class TextEditorbyteam118(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor by Team 118")
        self.geometry("1000x600")
        self.text_area = tkinter.Text(self, wrap="word")
        self.text_area.pack(fill="both", expand=True)
        self.create_menu()
    def create_menu(self):
        menubar = tkinter.Menu(self)
        self.config(menu=menubar)
        file_menu = tkinter.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Exit", command=self.quit)
        background_colour= ("green")
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                text_content = file.read()
                self.text_area.delete("1.0", text_content)
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                text_content = self.text_area.get("1.0", tkinter.END)
                file.write(text_content)

if __name__ == "__main__":
    app = TextEditorbyteam118()
    app.mainloop()
    app.mainloop()
