from CTkMessagebox import CTkMessagebox as CTkM
from CTkMenuBar import CTkMenuBar as CTkMB
from CTkMenuBar import CustomDropdownMenu as CDM
import customtkinter as ctk
from PIL import Image
import webbrowser
import functions as f
import json
import os

baseColor = ("#ebebeb", "#242424")
cardContent = ("#dbdbdb", "#2b2b2b")
boxContent = ("#f9f9fa", "#1d1e1e")

with open("settings/setting.json", "r") as sJ:
    settJson = json.load(sJ)
    sJ.close()

theme = settJson["theme"]

with open("settings/lang.json", "r", encoding="UTF-8") as lJ:
    langJson = json.load(lJ)

language = settJson["language"]
f.setLanguage(language)

def get_translation(key, **kwargs):
    return langJson[language][key].format(**kwargs)

def changeThemeJson():
    with open("settings/setting.json", "w") as sJ:
        settJson["theme"] = theme
        json.dump(settJson, sJ, indent=4)
        sJ.close()

def open_repo():
    webbrowser.open_new("https://github.com/aSamu3l/FileOrder")

def open_profile():
    webbrowser.open_new("https://github.com/aSamu3l/")

def f5(event):
    on_f5()

def on_f5():
    colorCombobox.set(get_translation("select_something"))
    colorCombobox.configure(
        values=[os.path.splitext(f)[0] for f in os.listdir("colors") if os.path.isfile(os.path.join("colors", f))])

    fontCombobox.set(get_translation("select_something"))
    fontCombobox.configure(values=[f for f in os.listdir("letters") if os.path.isdir(os.path.join("letters", f))])

    for widget in ft.winfo_children():
        widget.destroy()
    for letter in os.listdir("letters"):
        if os.path.isdir(os.path.join("letters", letter)):
            ft.add_option(letter, command=lambda l=letter: deleteFont(l))
    if len(ft.children) > 0:
        ft.add_separator()
    ft.add_option(get_translation("import_new_font"), command=importFont)

    for widget in cl.winfo_children():
        widget.destroy()
    for color in os.listdir("colors"):
        if os.path.isfile(os.path.join("colors", color)):
            cl.add_option(os.path.splitext(color)[0], command=lambda c=os.path.splitext(color)[0]: deleteColor(c))
    if len(cl.children) > 0:
        cl.add_separator()
    cl.add_option(get_translation("import_new_color"), command=importColor)

    for widget in lang.winfo_children():
        widget.destroy()
    for l in langJson.keys():
        lang.add_option(l, command=lambda lang=l: changeLanguage(lang))

    for widget in ap.winfo_children():
        widget.destroy()
    ap.add_option(get_translation("appearance_system") + (" ✓" if theme == "System" else ""), command=lambda: setAppearance(0))
    ap.add_option(get_translation("appearance_light") + (" ✓" if theme == "Light" else ""), command=lambda: setAppearance(1))
    ap.add_option(get_translation("appearance_dark") + (" ✓" if theme == "Dark" else ""), command=lambda: setAppearance(2))

def importFont():
    f.importNewFont()
    on_f5()

def importColor():
    f.importNewColor()
    on_f5()

def deleteFont(font: str):
    r = CTkM(title=get_translation("delete_font"), message=get_translation("delete_font_confirmation", font=font), icon="warning",
             option_1=get_translation("yes"), option_2=get_translation("no"))
    if r.get() == get_translation("yes"):
        f.deleteFont(font)
        on_f5()

def deleteColor(color: str):
    r = CTkM(title=get_translation("delete_color"), message=get_translation("delete_color_confirmation", color=color), icon="warning",
             option_1=get_translation("yes"), option_2=get_translation("no"))
    if r.get() == get_translation("yes"):
        os.remove(f"colors/{color}.png")
        on_f5()

def changeLanguage(lang):
    global language
    language = lang
    f.setLanguage(lang)
    settJson["language"] = lang
    with open("settings/setting.json", "w") as sJ:
        json.dump(settJson, sJ, indent=4)
    updateTexts()

def updateTexts():
    textText.configure(text=get_translation("textT"))
    entryText.configure(placeholder_text=get_translation("text"))
    textColor.configure(text=get_translation("colorT"))
    colorCombobox.set(get_translation("select_something"))
    textFont.configure(text=get_translation("fontT"))
    fontCombobox.set(get_translation("select_something"))
    optionFile.configure(text=get_translation("open_file"))
    optionFolder.configure(text=get_translation("open_folder"))
    runButton.configure(text=get_translation("save_file"))
    settMB.configure(text=get_translation("settings"))
    helpMB.configure(text=get_translation("help"))
    ap.configure(text=get_translation("appearance"))
    ft.configure(text=get_translation("font"))
    cl.configure(text=get_translation("color"))
    lang.configure(text=get_translation("language"))
    helpMBDropdown.configure(text=get_translation("help"))
    menuBar.update()
    on_f5()

def setAppearance(tipo: int):
    global theme
    for widget in ap.winfo_children():
        widget.destroy()

    if tipo == 1:
        ctk.set_appearance_mode("Light")
        theme = "Light"
    elif tipo == 2:
        ctk.set_appearance_mode("Dark")
        theme = "Dark"
    else:
        ctk.set_appearance_mode("System")
        theme = "System"

    ap.add_option(get_translation("appearance_system") + (" ✓" if theme == "System" else ""), command=lambda: setAppearance(0))
    ap.add_option(get_translation("appearance_light") + (" ✓" if theme == "Light" else ""), command=lambda: setAppearance(1))
    ap.add_option(get_translation("appearance_dark") + (" ✓" if theme == "Dark" else ""), command=lambda: setAppearance(2))

    if os.name == "nt":
        root.iconbitmap("img/iconl.ico" if ctk.get_appearance_mode() == "Light" else "img/icond.ico")

    changeThemeJson()

def save():
    sText = entryText.get()
    sColor = colorCombobox.get()
    sFont = fontCombobox.get()
    sFile = bool(optionFile.get())
    sFolder = bool(optionFolder.get())

    if sText == "" or sColor == get_translation("select_something") or sColor not in colorCombobox.cget("values") or sFont == get_translation("select_something") or sFont not in fontCombobox.cget("values"):
        CTkM(title=get_translation("error"), message=get_translation("error_fill_all_fields"), icon="cancel")
        return

    f.createText(sText, sFont, sColor, sFile, sFolder)

ctk.set_appearance_mode(theme)
root = ctk.CTk()
root.geometry("350x390")
root.title("Text Maker")
if os.name == "nt":
    root.iconbitmap("img/iconl.ico" if ctk.get_appearance_mode() == "Light" else "img/icond.ico")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Bind
root.bind("<F5>", f5)

# Menu Bar
menuBar = CTkMB(root, height=20)

settMB = menuBar.add_cascade(get_translation("settings"))
helpMB = menuBar.add_cascade(get_translation("help"))

# Settings Menu
settMBDropdown = CDM(settMB)

## Appearance
ap = settMBDropdown.add_submenu(get_translation("appearance"))
ap.add_option(get_translation("appearance_system") + (" ✓" if theme == "System" else ""), command=lambda: setAppearance(0))
ap.add_option(get_translation("appearance_light") + (" ✓" if theme == "Light" else ""), command=lambda: setAppearance(1))
ap.add_option(get_translation("appearance_dark") + (" ✓" if theme == "Dark" else ""), command=lambda: setAppearance(2))

## Language
lang = settMBDropdown.add_submenu(get_translation("language"))
for l in langJson.keys():
    lang.add_option(l, command=lambda lang=l: changeLanguage(lang))

settMBDropdown.add_separator()

## Font
ft = settMBDropdown.add_submenu(get_translation("font"))
for letter in os.listdir("letters"):
    if os.path.isdir(os.path.join("letters", letter)):
        ft.add_option(letter, command=lambda l=letter: deleteFont(l))
if len(ft.children) > 0:
    ft.add_separator()
ft.add_option(get_translation("import_new_font"), command=importFont)

## Color
cl = settMBDropdown.add_submenu(get_translation("color"))
for color in os.listdir("colors"):
    if os.path.isfile(os.path.join("colors", color)):
        cl.add_option(os.path.splitext(color)[0], command=lambda c=os.path.splitext(color)[0]: deleteColor(c))
if len(cl.children) > 0:
    cl.add_separator()
cl.add_option(get_translation("import_new_color"), command=importColor)

# Help Menu
helpMBDropdown = CDM(helpMB)
helpMBDropdown.add_option(get_translation("repository"), command=open_repo)
helpMBDropdown.add_separator()
helpMBDropdown.add_option(get_translation("profile"), command=open_profile)

menuBar.pack()

# Entry Frame
entryFrame = ctk.CTkFrame(root, fg_color=cardContent, width=330, height=80)
entryFrame.pack()
entryFrame.place(x=10, y=30)

# Entry Frame Widgets
# Text
textText = ctk.CTkLabel(entryFrame, text=get_translation("textT"), fg_color=cardContent, width=310, height=21, font=("Arial", 21))
textText.pack()
textText.place(x=10, y=10)

# Entry
entryText = ctk.CTkEntry(entryFrame, placeholder_text=get_translation("text"), width=250, height=29)
entryText.pack()
entryText.place(x=10, y=41)

# Button
buttonText = ctk.CTkButton(entryFrame, text="➢", width=50, height=29,
                           command=lambda: f.checkIntegrityText(entryText.get()))
buttonText.pack()
buttonText.place(x=270, y=41)

# Color Frame
colorFrame = ctk.CTkFrame(root, fg_color=cardContent, width=330, height=80)
colorFrame.pack()
colorFrame.place(x=10, y=120)

# Color Frame Widgets
# Text
textColor = ctk.CTkLabel(colorFrame, text=get_translation("colorT"), fg_color=cardContent, width=310, height=21, font=("Arial", 21))
textColor.pack()
textColor.place(x=10, y=10)

# Color ComboBox
colorCombobox = ctk.CTkComboBox(colorFrame, values=[os.path.splitext(f)[0] for f in os.listdir("colors") if
                                                    os.path.isfile(os.path.join("colors", f))], width=310, height=29)
colorCombobox.set(get_translation("select_something"))
colorCombobox.pack()
colorCombobox.place(x=10, y=41)

# Font Frame
fontFrame = ctk.CTkFrame(root, fg_color=cardContent, width=330, height=80)
fontFrame.pack()
fontFrame.place(x=10, y=210)

# Font Frame Widgets
# Text
textFont = ctk.CTkLabel(fontFrame, text=get_translation("fontT"), fg_color=cardContent, width=310, height=21, font=("Arial", 21))
textFont.pack()
textFont.place(x=10, y=10)

# Font ComboBox
fontCombobox = ctk.CTkComboBox(fontFrame,
                               values=[f for f in os.listdir("letters") if os.path.isdir(os.path.join("letters", f))],
                               width=310, height=29)
fontCombobox.set(get_translation("select_something"))
fontCombobox.pack()
fontCombobox.place(x=10, y=41)

# Run Frame
runFrame = ctk.CTkFrame(root, fg_color=cardContent, width=330, height=80)
runFrame.pack()
runFrame.place(x=10, y=300)

# Run Frame Widgets
# Option open file
optionFile = ctk.CTkCheckBox(runFrame, text=get_translation("open_file"), fg_color=cardContent)
optionFile.pack()
optionFile.place(x=10, y=10)

# Option open folder
optionFolder = ctk.CTkCheckBox(runFrame, text=get_translation("open_folder"), fg_color=cardContent)
optionFolder.pack()
optionFolder.place(x=170, y=10)

# Option save file
runButton = ctk.CTkButton(runFrame, text=get_translation("save_file"), width=310, height=29, command=save)
runButton.pack()
runButton.place(x=10, y=41)

root.mainloop()