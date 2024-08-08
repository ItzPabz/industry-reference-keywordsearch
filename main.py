import tkinter
from tkinter import ttk
import sv_ttk
from ctypes import windll
from functions import keyword_search, convertMDtoWord
import tkinter.messagebox as messagebox
import tkinter.filedialog
import pywinstyles, sys
from docx import Document
import requests

FONT_TITLE = ("Helvetica", 25, 'bold')
FONT_INSTRUCTIONS = ("Helvetica", 14)
FONT_TEXTAREA = ("Helvetica", 18)
FONT_RESULTS = ("Helvetica", 10)
BG_COLOR = '#2f2f2f'
WINDOW_TITLE = "Industry Reference Keyword Search Tool"
WINDOW_SIZE = "1000x700"
ICON_PATH = "./icon.ico"

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()
    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

def get_keyword_values(text_widget):
    keyword_values = text_widget.get("1.0", "end").split("\n")
    return [value.strip() for value in keyword_values if value.strip()]

def analyze_keywords(text_widget, result_widget):
    keyword_array = get_keyword_values(text_widget)
    results = keyword_search("./references", keyword_array)
    processed_results = process_results(results)
    update_text_widget(result_widget, processed_results)
    return processed_results

def process_results(results):
    if results is None:
        return "No matches found."
    elif isinstance(results, list):
        processed_results = ""
        current_name = ""
        for name, control in results:
            if name != current_name:
                processed_results += f"\n# {name}\n\n"
                current_name = name
            processed_results += f"## {control['id']}: {control['name']}\n- {control['url']}\n- {control['control']}\n\n"
        return processed_results
    else:
        return str(results)

def update_text_widget(widget, text):
    widget.configure(state='normal')
    widget.delete("1.0", "end")
    widget.insert("1.0", text)
    widget.configure(state='disabled', wrap='word')

def copy_results_to_clipboard(root, text_widget):
    root.clipboard_clear()
    root.clipboard_append(text_widget.get("1.0", "end"))
    root.update()
    messagebox.showinfo("Copy Successful", "Results copied to clipboard!")

def export_results(text_widget):
    doc = convertMDtoWord(text_widget.get("1.0", "end"))
    filename = tkinter.filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
    if filename:
        doc.save(filename)
        messagebox.showinfo("Export Successful", f"Results exported to {filename}")

def show_build_info():
    messagebox.showinfo("Build Information", "Version: 1.0.0\nAuthor: Pablo David\nLast Revision: 06 AUG 2024")

def check_for_updates():
    repo_url = "https://github.com/ItzPabz/industry-reference-keywordsearch"
    response = requests.get(repo_url)
    if response.status_code == 200:
        repo_content = response.text
        if "main.py" in repo_content and "functions.py" in repo_content:
            messagebox.showinfo("Update Available", "An update is available. Please visit the repository to download the latest version.")
        else:
            return True
    else:
        messagebox.showerror("Error", "Failed to fetch repository content.")


def create_main_window():
    root = tkinter.Tk()
    sv_ttk.set_theme("dark")
    windll.shcore.SetProcessDpiAwareness(1)
    root.title(WINDOW_TITLE)
    root.resizable(False, False)
    root.geometry(WINDOW_SIZE)
    root.iconbitmap(ICON_PATH)
    return root

def create_frames(root):
    frame_left = ttk.Frame(root)
    frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    frame_right = ttk.Frame(root)
    frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    root.grid_columnconfigure(0, weight=3)
    root.grid_columnconfigure(1, weight=7)
    return frame_left, frame_right

def create_left_frame_components(frame_left):
    ttk.Label(frame_left, text="Industry Keyword Search", font=FONT_TITLE).pack(pady=10)
    ttk.Label(frame_left, foreground="gray", text="Enter keywords below with a new line after each.", font=FONT_INSTRUCTIONS).pack(pady=4)
    textarea_keyword_display = tkinter.Text(frame_left, width=31, height=18, bg=BG_COLOR, font=FONT_TEXTAREA)
    textarea_keyword_display.pack(pady=10)
    return textarea_keyword_display

def create_right_frame_components(frame_right, root, textarea_keyword_display):
    textarea_results = tkinter.Text(frame_right, width=100, height=36, bg=BG_COLOR, font=FONT_RESULTS, state='disabled')
    textarea_results.pack(pady=10)
    subframe = ttk.Frame(frame_right)
    subframe.pack(fill="x", padx=10, pady=10)
    ttk.Button(subframe, text="Copy", style="Accent.TButton", width=18, command=lambda: copy_results_to_clipboard(root, textarea_results)).pack(side="right", padx=5)
    ttk.Button(subframe, text="Export", style="Primary.TButton", width=18, command=lambda: export_results(textarea_results)).pack(side="right", padx=5)
    ttk.Button(subframe, text="Build Info", style="Primary.TButton", width=18, command=show_build_info).pack(side="right", padx=5)
    return textarea_results

def main():
    root = create_main_window()
    frame_left, frame_right = create_frames(root)
    textarea_keyword_display = create_left_frame_components(frame_left)
    textarea_results = create_right_frame_components(frame_right, root, textarea_keyword_display)
    ttk.Button(frame_left, text="ANALYZE", style="Accent.TButton", width=48, command=lambda: analyze_keywords(textarea_keyword_display, textarea_results)).pack(pady=10)
    apply_theme_to_titlebar(root)
    check_for_updates()
    root.mainloop()


if __name__ == "__main__":
    main()
