import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def browse_ply_file():
    home_dir = os.path.expanduser("~")  # Get the user's home directory
    filename = filedialog.askopenfilename(
        initialdir=home_dir,  # Start in the user's home directory
        title="Select .ply file",
        filetypes=(("PLY files", "*.ply"), ("All files", "*.*"))
    )
    if filename:
        ply_entry.delete(0, tk.END)
        ply_entry.insert(0, filename)

def browse_output_dir():
    home_dir = os.path.expanduser("~")  # Get the user's home directory
    output_dir = filedialog.askdirectory(
        initialdir=home_dir,  # Start in the user's home directory
        title="Select Output Directory"
    )
    if output_dir:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_dir)

def convert_ply():
    try:
        input_file = ply_entry.get()
        output_dir = output_entry.get()

        if not input_file or not output_dir:
            raise ValueError("Please select both input file and output directory.")

        if not input_file.lower().endswith(".ply"):
            raise ValueError("Selected file is not a .ply file.")

        basename = os.path.basename(input_file)
        name, _ = os.path.splitext(basename)
        output_file = os.path.join(output_dir, name + "_cc.ply")

        if os.path.exists(output_file):
            raise FileExistsError(f"Output file already exists: {output_file}")

        command = [
            "3dgsconverter",
            "-i", input_file,
            "-o", output_file,
            "-f", "cc",
            "--rgb"
        ]

        process = subprocess.run(command, capture_output=True, text=True, check=True)

        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Output file not created: {output_file}")

        result_label.config(text=f"Conversion successful! Output saved to: {output_file}")

    except FileExistsError as e:
        result_label.config(text=f"Error: {e}")
    except FileNotFoundError as e:
        result_label.config(text=f"Error: {e}")
    except ValueError as e:
        result_label.config(text=f"Error: {e}")
    except subprocess.CalledProcessError as e:
        result_label.config(text=f"Error during conversion: Return code {e.returncode}\nStdout: {e.stdout}\nStderr: {e.stderr}")
    except Exception as e:
        result_label.config(text=f"An unexpected error occurred: {e}")


def center_window(root):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")


root = tk.Tk()
root.title("PLY File Converter")

ply_label = tk.Label(root, text="Select .ply file:")
ply_label.grid(row=0, column=0, sticky="w")
ply_entry = tk.Entry(root, width=50)
ply_entry.grid(row=0, column=1)
ply_button = tk.Button(root, text="Browse", command=browse_ply_file)
ply_button.grid(row=0, column=2)

output_label = tk.Label(root, text="Select output directory:")
output_label.grid(row=1, column=0, sticky="w")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1)
output_button = tk.Button(root, text="Browse", command=browse_output_dir)
output_button.grid(row=1, column=2)

convert_button = tk.Button(root, text="Convert", command=convert_ply)
convert_button.grid(row=2, column=1)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3)

center_window(root)

root.mainloop()