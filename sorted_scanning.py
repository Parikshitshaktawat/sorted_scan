import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Frame, Label
import logging
import threading

# Configure logging
logging.basicConfig(filename='file_sizes.log', level=logging.INFO, format='%(message)s')

scanning = False

def convert_size(size_bytes):
    """Convert bytes to MB or GB."""
    if size_bytes >= 1_073_741_824:  # Greater than or equal to 1 GB
        return f"{size_bytes / 1_073_741_824:.2f} GB"
    elif size_bytes >= 1_048_576:  # Greater than or equal to 1 MB
        return f"{size_bytes / 1_048_576:.2f} MB"
    else:
        return f"{size_bytes} bytes"

def get_file_sizes(directory):
    """Walk through the directory and return a list of file paths and sizes."""
    file_sizes = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)  # Get file size in bytes
                file_sizes.append((file_path, size))
            except Exception as e:
                logging.error(f"Error getting size for file {file_path}: {e}")
    return file_sizes

def update_listbox(sorted_file_sizes):
    """Update the listbox with sorted file sizes."""
    listbox.delete(0, tk.END)  # Clear the listbox
    for file_path, size in sorted_file_sizes:
        if not scanning:
            break
        readable_size = convert_size(size)
        listbox.insert(tk.END, f"{file_path} - {readable_size}")

def scan_directory():
    """Scan the selected directory and update the listbox."""
    global scanning
    directory = filedialog.askdirectory()
    if directory:
        scanning = True
        scan_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        scanning_label.config(text="Scanning... Please wait.")

        def load_files():
            file_sizes = get_file_sizes(directory)
            sorted_file_sizes = sorted(file_sizes, key=lambda x: x[1], reverse=True)
            update_listbox(sorted_file_sizes)  # Update UI with the sorted file sizes
            stop_scanning()  # Ensure scanning state is reset

        threading.Thread(target=load_files).start()

def stop_scanning():
    """Stop the scanning process."""
    global scanning
    scanning = False
    scan_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    scanning_label.config(text="")

def open_file_in_explorer(event):
    """Open the selected file's directory in Windows Explorer."""
    selection = listbox.curselection()
    if selection:
        file_info = listbox.get(selection[0]).split(" - ")[0]
        os.startfile(os.path.dirname(file_info))

def delete_selected_files():
    """Delete selected files."""
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected files?")
    if confirm:
        for index in reversed(listbox.curselection()):  # Delete from the end to avoid index shift
            file_info = listbox.get(index).split(" - ")[0]
            try:
                os.remove(file_info)
                listbox.delete(index)
                logging.info(f"Deleted file: {file_info}")
            except Exception as e:
                logging.error(f"Error deleting file {file_info}: {e}")
                messagebox.showerror("Error", f"Could not delete file: {file_info}\nError: {e}")

def delete_all_files():
    """Delete all files listed in the listbox."""
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete all files?")
    if confirm:
        for index in reversed(range(listbox.size())):  # Delete from the end
            file_info = listbox.get(index).split(" - ")[0]
            try:
                os.remove(file_info)
                listbox.delete(index)
                logging.info(f"Deleted file: {file_info}")
            except Exception as e:
                logging.error(f"Error deleting file {file_info}: {e}")
                messagebox.showerror("Error", f"Could not delete file: {file_info}\nError: {e}")

def show_info():
    """Show developer info in a message box.""" 
    messagebox.showinfo("Developer Info", "Developed by: Parikshit Shaktawat\nDate: 2024\nContact: parikshitshaktawat.it@gmail.com")

def select_all():
    """Select all items in the listbox."""
    listbox.select_set(0, tk.END)

def deselect_all():
    """Deselect all items in the listbox."""    
    listbox.selection_clear(0, tk.END)

# Set up the main application window
root = tk.Tk()
root.title("File Size Scanner")

# Responsive design
root.geometry("800x600")
root.minsize(800, 600)

# Create and place widgets
frame = Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Frame for Listbox and Scrollbar
list_frame = Frame(frame)
list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

listbox = Listbox(list_frame, selectmode=tk.MULTIPLE, width=80, height=10)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

listbox.bind('<Double-Button-1>', open_file_in_explorer)

# Fixed frame for buttons
button_frame = Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

deselect_all_button = tk.Button(button_frame, text="Deselect All", command=deselect_all, bg="lightcoral")
deselect_all_button.pack(side=tk.LEFT, padx=10, pady=10)

scan_button = tk.Button(button_frame, text="Scan Directory", command=scan_directory, bg="lightgreen")
scan_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop Scanning", command=stop_scanning, bg="lightyellow", state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

delete_selected_button = tk.Button(button_frame, text="Delete Selected", command=delete_selected_files, bg="salmon")
delete_selected_button.pack(side=tk.LEFT, padx=5)

info_button = tk.Button(button_frame, text="Info", command=show_info, bg="lightblue")
info_button.pack(side=tk.RIGHT, padx=5)

# Label to indicate scanning status
scanning_label = Label(root, text="", font=("Helvetica", 12))
scanning_label.pack(pady=10)

# Start the application
root.mainloop()
