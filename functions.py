import os
import PIL.Image as Image
from CTkMessagebox import CTkMessagebox as CTkM
from customtkinter import filedialog as fd
import zipfile
import shutil
import subprocess
import json

with open("settings/lang.json", "r", encoding="UTF-8") as lJ:
    langJson = json.load(lJ)

language = "EN"


def setLanguage(lang: str) -> None:
    global language
    language = lang


def get_translation(key, **kwargs):
    return langJson[language][key].format(**kwargs)


def checkIntegrityFont(font: str) -> bool:
    if not os.path.exists(f"letters/{font}"):
        return False

    for l in "abcdefghijklmnopqrstuvwxyz":
        if not os.path.exists(f"letters/{font}/{l}.png"):
            return False

    if not os.path.exists(f"letters/{font}/space.png"):
        return False

    height = Image.open(f"letters/{font}/A.png").height

    for file in os.listdir(f"letters/{font}"):
        if Image.open(f"letters/{font}/{file}").height != height:
            return False

    return True


def checkIntegrityColor(color: str) -> bool:
    if not os.path.exists(f"colors/{color}.png"):
        return False

    for file in os.listdir(f"colors"):
        if Image.open(f"colors/{file}").height != 3 and Image.open(f"colors/{file}").width != 1:
            return False

        if file == f"{color}.png":
            return True

    if not os.path.exists("grey.png"):
        return False

    if Image.open("grey.png").height != 3 and Image.open("grey.png").width != 1:
        return False

    return True


def checkIntegrityText(text: str) -> None:
    if not text:
        CTkM(title=get_translation("error"), message=get_translation("error_empty_text"), icon="cancel")
        return

    for letter in text:
        if not letter in "abcdefghijklmnopqrstuvwxyz ":
            CTkM(title=get_translation("error"), message=get_translation("error_invalid_character", letter=letter),
                 icon="cancel")
            return

    CTkM(title=get_translation("success"), message=get_translation("success_valid_text"), icon="info")


def checkIntegrityTextFont(text: str, font: str) -> bool:
    for letter in text:
        if not os.path.exists(f"letters/{font}/{letter}.png"):
            print(letter)
            return False

    return True


def importNewFont() -> None:
    zip_path = fd.askopenfilename(filetypes=[("Zip files", "*.zip")])
    if not zip_path:
        return

    font_name = os.path.splitext(os.path.basename(zip_path))[0]
    temp_dir = f"temp_{font_name}"

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    required_files = [f"{l}.png" for l in "abcdefghijklmnopqrstuvwxyz"] + ["space.png"]
    for file in required_files:
        if not os.path.exists(os.path.join(temp_dir, file)):
            CTkM(title=get_translation("error"), message=get_translation("error_missing_file", file=file))
            shutil.rmtree(temp_dir)
            return

    dest_dir = os.path.join("letters", font_name)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for file in os.listdir(temp_dir):
        shutil.move(os.path.join(temp_dir, file), os.path.join(dest_dir, file))

    shutil.rmtree(temp_dir)
    CTkM(title=get_translation("success"), message=get_translation("success_font_imported"))


def deleteFont(font: str) -> None:
    if not os.path.exists(f"letters/{font}"):
        CTkM(title=get_translation("error"), message=get_translation("error_font_not_found"))
        return
    shutil.rmtree(f"letters/{font}")
    CTkM(title=get_translation("success"), message=get_translation("success_font_deleted"))


def importNewColor() -> None:
    color_path = fd.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not color_path:
        return

    color_name = os.path.splitext(os.path.basename(color_path))[0]
    dest_path = os.path.join("colors", f"{color_name}.png")
    shutil.copy(color_path, dest_path)
    CTkM(title=get_translation("success"), message=get_translation("success_color_imported"))


def deleteColor(color: str) -> None:
    if not os.path.exists(f"colors/{color}.png"):
        CTkM(title=get_translation("error"), message=get_translation("error_color_not_found"))
        return
    os.remove(f"colors/{color}.png")
    CTkM(title=get_translation("success"), message=get_translation("success_color_deleted"))


def createText(text: str, font: str, color: str, openFile: bool, openDir: bool) -> None:
    if not checkIntegrityFont(font):
        CTkM(title=get_translation("error"), message=get_translation("error_invalid_font"))
        return

    if not checkIntegrityColor(color):
        CTkM(title=get_translation("error"), message=get_translation("error_invalid_color"))
        return

    if not checkIntegrityTextFont(text, font):
        CTkM(title=get_translation("error"), message=get_translation("error_invalid_text"))
        return

    line = Image.open(f"letters/{font}/A.png").height

    textList = [[] for _ in range(line)]

    for letter in text:
        letterImage = Image.open(f"letters/{font}/{letter}.png")
        pixels = list(letterImage.getdata())
        for i in range(line):
            textList[i].extend(pixels[i * letterImage.width:(i + 1) * letterImage.width])

    pixelChange = {Image.open("grey.png").getpixel((0, i)): Image.open(f"colors/{color}.png").getpixel((0, i)) for i in
                   range(3)}

    for i in range(len(textList)):
        for j in range(len(textList[i])):
            textList[i][j] = pixelChange[textList[i][j]]

    image = Image.new("RGB", (len(textList[0]), line))
    image.putdata([item for sublist in textList for item in sublist])

    if not os.path.exists("output"):
        os.makedirs("output")

    output_path = os.path.abspath(f"output/{text}.png")
    image.save(output_path)

    if openDir:
        if os.name == 'nt':
            os.system(f'explorer /select,"{output_path}"')
        elif os.name == 'posix':
            folder_path = os.path.dirname(output_path)
            os.system(f'xdg-open "{folder_path}"')

    if openFile:
        if os.name == 'nt':
            subprocess.run(['start', output_path], shell=True)
        elif os.name == 'posix':
            subprocess.run(['xdg-open', output_path])
