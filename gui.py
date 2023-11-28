import tkinter as tk
from tkinter import scrolledtext
import subprocess

class GUIApp:
    def __init__(self, master):
        self.master = master
        master.title("Security Camera")

        self.laptop_button = tk.Button(master, text="Laptop", command=self.run_laptop)
        self.laptop_button.pack()

        self.pi_button = tk.Button(master, text="Raspberry Pi", command=self.run_pi)
        self.pi_button.pack()

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20)
        self.output_text.pack()

    def run_laptop(self):
        self.run_program("laptop")

    def run_pi(self):
        self.run_program("pi")

    def run_program(self, machine):
        command = ['python', 'laptop.py'] if machine == 'laptop' else ['python', 'pi.py']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.output_text.insert(tk.END, output)
                self.output_text.see(tk.END)
                self.master.update_idletasks()

def main():
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()