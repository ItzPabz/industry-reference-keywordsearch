import tkinter
from tkinter import ttk
import sv_ttk 
from ctypes import windll
from functions import keyword_search, convertMDtoWord
import tkinter.messagebox as messagebox
import tkinter.filedialog
import pywinstyles, sys
from docx import Document

def apply_theme_to_titlebar(root):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)

root = tkinter.Tk()
sv_ttk.set_theme("dark")
windll.shcore.SetProcessDpiAwareness(1)
root.title("Industry Reference Keyword Search Tool")
root.resizable(False, False)
root.geometry("1000x700")
root.iconbitmap("./icon.ico")

frameLeft = ttk.Frame(root)
frameLeft.pack(side="left", fill="both", expand=True, padx=10, pady=10)
frameRight = ttk.Frame(root)
frameRight.pack(side="right", fill="both", expand=True, padx=10, pady=10)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=7)

# LEFT FRAME COMPONENTS
labelTitle = ttk.Label(frameLeft, text="Industry Keyword Search", font=("Helvetica", 25, 'bold'))
labelTitle.pack(pady=10)

labelInstructions = ttk.Label(frameLeft, foreground="gray", text="Enter keywords below with a new line after each.", font=("Helvetica", 14))
labelInstructions.pack(pady=4)

textareaKeywordDisplay = tkinter.Text(frameLeft, width=31, height=18)
textareaKeywordDisplay.pack(pady=10)
textareaKeywordDisplay.configure(state='normal', bg='#2f2f2f', font=("Helvetica", 18))

def getKeywordValues():
    keyword_values = textareaKeywordDisplay.get("1.0", "end").split("\n")
    keyword_array = [value.strip() for value in keyword_values if value.strip()]
    return keyword_array

def analyzeKeywords():
    keyword_array = getKeywordValues()
    results = keyword_search("./references", keyword_array)

    if results is None:
        processed_results = "No matches found."
    elif isinstance(results, list):
        processed_results = ""
        current_name = ""
        for name, control in results:
            if name != current_name:
                processed_results += f"\n# {name}\n\n"
                current_name = name
            processed_results += f"## {control['id']}: {control['name']}\n- {control['url']}\n- {control['control']}\n\n"
    else:
        processed_results = str(results)
    
    textareaResults.configure(state='normal')
    textareaResults.delete("1.0", "end")
    textareaResults.insert("1.0", processed_results)
    textareaResults.configure(state='disabled')
    textareaResults.configure(wrap='word')

    return processed_results

buttonAnalyze = ttk.Button(frameLeft, text="ANALYZE", style="Accent.TButton", width=48, command=analyzeKeywords)
buttonAnalyze.pack(pady=10)

# RIGHT FRAME COMPONENTS
textareaResults = tkinter.Text(frameRight, width=100, height=36)
textareaResults.pack(pady=10)
textareaResults.configure(state='disabled', bg='#2f2f2f', font=("Helvetica", 10))

subframe = ttk.Frame(frameRight)
subframe.pack(fill="x", padx=10, pady=10)

def copyReultstoClipboard():
    root.clipboard_clear()
    root.clipboard_append(textareaResults.get("1.0", "end"))
    root.update()
    messagebox.showinfo("Copy Successful", "Results copied to clipboard!")

buttonCopy = ttk.Button(subframe, text="Copy", style="Accent.TButton", width=18, command=copyReultstoClipboard)
buttonCopy.pack(side="right", padx=5)

def exportResults():
    doc = convertMDtoWord(textareaResults.get("1.0", "end"))
    filename = tkinter.filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
    if filename:
        doc.save(filename)
        messagebox.showinfo("Export Successful", "Results exported to {}".format(filename))

buttonExport = ttk.Button(subframe, text="Export", style="Primary.TButton", width=18,command=exportResults)
buttonExport.pack(side="right", padx=5)
buttonExport.configure(state='normal')

def showBuildInfo():
    messagebox.showinfo("Build Information", "Version: 1.0.0\nAuthor: Pablo David\nLast Revision: 06 AUG 2024")

buttonBuildInfo = ttk.Button(subframe, text="Build Info", style="Primary.TButton", width=18, command=showBuildInfo)
buttonBuildInfo.pack(side="right", padx=5)

if __name__ == "__main__":
    apply_theme_to_titlebar(root)
    root.mainloop()