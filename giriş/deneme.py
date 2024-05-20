import tkinter as tk
from tkinter import filedialog
 
def import_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Images", "*.png,*.jpg"), ("All files", "*.*")])
    if file_path:
        #  'Images (*.png *.jpg)'       ("Text files", "*.txt")
        print("Selected file:", file_path)
 
# Create the main Tkinter window
root = tk.Tk()
root.title("Import Fileded Example")
 
# Create an "Import File" button
import_button = tk.Button(root, text="Import File", command=import_file)
import_button.pack(pady=100)
 
# Run the Tkinter event loop
root.mainloop()