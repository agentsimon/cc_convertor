import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def choose_conversion_type():
    """Displays a dialog to choose the conversion type using radio buttons."""
    root = tk.Tk()
    root.title("Choose Conversion Type")

    var = tk.StringVar(value="3dgs_to_cc")

    tk.Label(root, text="Select Conversion Type:").pack(pady=10)

    tk.Radiobutton(root, text="3DGS to CloudCompare (with RGB)", variable=var, value="3dgs_to_cc").pack(anchor=tk.W)
    tk.Radiobutton(root, text="CloudCompare to 3DGS", variable=var, value="cc_to_3dgs").pack(anchor=tk.W)

    def get_choice():
        choice = var.get()
        root.destroy()
        return choice

    tk.Button(root, text="OK", command=get_choice).pack(pady=10)
    root.mainloop()
    return var.get()


def browse_ply_file(conversion_type):
    home_dir = os.path.expanduser("~")
    filename = filedialog.askopenfilename(
        initialdir=home_dir,
        title="Select .ply file",
        filetypes=(("PLY files", "*.ply"), ("All files", "*.*"))
    )
    if filename:
        ply_entry.delete(0, tk.END)
        ply_entry.insert(0, filename)


def browse_output_dir(conversion_type):
    home_dir = os.path.expanduser("~")
    output_dir = filedialog.askdirectory(
        initialdir=home_dir,
        title="Select Output Directory"
    )
    if output_dir:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_dir)


def convert_ply(conversion_type):
    try:
        input_file = ply_entry.get()
        output_dir = output_entry.get()

        if not input_file or not output_dir:
            raise ValueError("Please select both input file and output directory.")

        if conversion_type == "3dgs_to_cc":
            if not input_file.lower().endswith(".ply"):
                raise ValueError("Selected file is not a .ply file.")
            basename = os.path.basename(input_file)
            name, _ = os.path.splitext(basename)
            output_file = os.path.join(output_dir, name + "_cc.ply")
            command = [
                "3dgsconverter",
                "-i", input_file,
                "-o", output_file,
                "-f", "cc",
                "--rgb"
            ]

        elif conversion_type == "cc_to_3dgs":
            if not input_file.lower().endswith(".ply"):
                raise ValueError("Selected input file is not a .ply file.")
            basename = os.path.basename(input_file)
            name, _ = os.path.splitext(basename)
            output_file = os.path.join(output_dir, name + "_3dgs.ply")
            command = [
                "3dgsconverter",
                "-i", input_file,
                "-o", output_file,
                "-f", "3dgs"
            ]
        else:
            raise ValueError("Invalid conversion type selected.")

        if os.path.exists(output_file):
            raise FileExistsError(f"Output file already exists: {output_file}")

        process = subprocess.run(command, capture_output=True, text=True, check=False)

        if process.returncode == 0:
            stderr_output = process.stderr if process.stderr else "Standard Error: 0"
            result_label.config(text=f"Conversion successful! Output saved to: {output_file}\n\nStdout: {process.stdout}\n{stderr_output}")
            print(f"Conversion successful! Output saved to: {output_file}")
            print("Standard Output:\n", process.stdout)
            print(stderr_output)
        else:
            result_label.config(text=f"Conversion failed with return code {process.returncode}!\nStdout: {process.stdout}\nStderr: {process.stderr}")
            print(f"Conversion failed with return code {process.returncode}!")
            print("Standard Output:\n", process.stdout)
            print("Standard Error:\n", process.stderr)

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



conversion_type = choose_conversion_type()
if conversion_type:
    root = tk.Tk()
    root.title("PLY File Converter")

    ply_label = tk.Label(root, text="Select .ply file:")
    ply_label.grid(row=0, column=0, sticky="w")
    ply_entry = tk.Entry(root, width=50)
    ply_entry.grid(row=0, column=1)
    ply_button = tk.Button(root, text="Browse", command=lambda: browse_ply_file(conversion_type))
    ply_button.grid(row=0, column=2)

    output_label = tk.Label(root, text="Select output directory:")
    output_label.grid(row=1, column=0, sticky="w")
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1)
    output_button = tk.Button(root, text="Browse", command=lambda: browse_output_dir(conversion_type))
    output_button.grid(row=1, column=2)

    convert_button = tk.Button(root, text="Convert", command=lambda: convert_ply(conversion_type))
    convert_button.grid(row=2, column=1)

    result_label = tk.Label(root, text="")
    result_label.grid(row=3, column=0, columnspan=3)

    center_window(root)
    root.mainloop()
else:
    print("Conversion cancelled by user.")
