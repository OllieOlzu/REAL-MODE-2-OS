import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import tempfile
import shutil
import os
import sys

def compile_asm(code, file_type):
    extension = f".{file_type}"

    save_path = filedialog.asksaveasfilename(
        defaultextension=extension,
        filetypes=[(f"{file_type.upper()} files", f"*{extension}")]
    )
    if not save_path:
        return

    temp_dir = tempfile.mkdtemp()
    temp_asm_path = os.path.join(temp_dir, "temp.asm")
    output_path = os.path.join(temp_dir, f"output{extension}")

    with open(temp_asm_path, "w") as f:
        f.write(code)

    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath("."))
    embedded_nasm = os.path.join(bundle_dir, "nasm.exe")
    temp_nasm_path = os.path.join(temp_dir, "nasm.exe")

    try:
        shutil.copyfile(embedded_nasm, temp_nasm_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not find or copy nasm.exe:\n{e}")
        shutil.rmtree(temp_dir)
        return

    try:
        subprocess.run([temp_nasm_path, "-f", "bin", temp_asm_path, "-o", output_path], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Compilation failed:\n{e}")
        shutil.rmtree(temp_dir)
        return

    try:
        with open(output_path, "rb") as f:
            compiled_data = f.read()
        with open(save_path, "wb") as f:
            f.write(compiled_data)
        messagebox.showinfo("Success", f"Saved to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file:\n{e}")

    shutil.rmtree(temp_dir)

def create_desktop_shortcut():
    try:
        import winshell
        from win32com.client import Dispatch

        desktop = winshell.desktop()
        target = sys.executable  # Path to the EXE (works even when bundled)
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath("."))
        icon_path = os.path.join(bundle_dir, "icon.ico")
        shortcut_path = os.path.join(desktop, "REAL MODE 2 OS.lnk")

        # Only create shortcut if it doesn't already exist
        if not os.path.exists(shortcut_path):
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = icon_path
            shortcut.save()
            print("Shortcut created on desktop.")
    except Exception as e:
        print(f"Could not create shortcut: {e}")

def start_gui():
    root = tk.Tk()
    root.title("REAL MODE 2 OS")
    root.geometry("600x700")

    # Set window icon
    try:
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath("."))
        icon_path = os.path.join(bundle_dir, "icon.ico")
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Warning: Could not set icon.ico: {e}")

    tk.Label(root, text="Enter your ASM code:").pack(anchor='w', padx=10, pady=(10, 0))
    code_text = tk.Text(root, wrap="word", height=20)
    code_text.pack(fill="both", expand=True, padx=10, pady=5)

    output_var = tk.StringVar(value="bin")
    output_menu = tk.OptionMenu(root, output_var, "bin", "img", "iso")
    output_menu.pack(pady=5)

    def on_download():
        code = code_text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("No Code", "Please enter some ASM code first.")
            return
        compile_asm(code, output_var.get())

    tk.Button(root, text="Download", command=on_download).pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_desktop_shortcut()
    start_gui()
