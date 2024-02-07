import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class TextEditor(tk.Tk):  # Single inheritance
    def __init__(self):
        super().__init__()

        self.title("Text Editor")
        self.geometry("600x400")

        self.text_area = tk.Text(self, wrap="word")
        self.text_area.pack(fill="both", expand=True)

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Exit", command=self.quit)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                text_content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, text_content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                text_content = self.text_area.get("1.0", tk.END)
                file.write(text_content)

if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
