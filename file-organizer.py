from pathlib import Path


class Files:
    def __init__(self, file_name, file_suffix, original_name):
          self.file_name = file_name
          self.file_suffix = file_suffix
          self.original_name = original_name

    def decide_folder(self, folder_names):
        for folder, suffixes in folder_names.items():
            if self.file_suffix.lower() in suffixes:
                return folder
        return "Sonstiges"
            

curr_path = Path.cwd()

# Dictionary for file types and folder names
folder_names = {
    "Images" : [".png", ".jpg", ".gif", ".svg", ".psd", ".webp"],
    "Videos" : [".mp4", ".avi", ".mkv", ".mov"],
    "Documents" : [".txt", ".docx", ".doc", ".pdf", ".odt", ".rtf"],
    "Spreadsheets" : [".xlsx", ".xls", ".csv", ".pptx", ".ppt"],
    "Audio" : [".mp3", ".wav", ".flac"],
    "Compressed" : [".zip", ".rar"],
    "System" : [".exe", ".bat"]

}

# User input
def yes_or_no():
    user_input = input().capitalize()
    while user_input not in ("N", "Y"):
        print("Y or N?")
        user_input = input().capitalize()
    if user_input == "N":
        return False
    return True

def find_files(file_path):
    files = []
    for child in file_path.iterdir():
        if child.is_file() and child.name != Path(__file__).name:
            # Seperate file name, suffix and original name
            files.append(Files(child.stem, child.suffix, child.name)) 
    return files

def confirm_files(files):
    # Confirm files by user input
    for file in files:
        print("Ordner: " + file.decide_folder(folder_names) + "\n Datei: " + file.original_name)
    print("Bestätigen? Y or N")
    if not yes_or_no(): 
        print("Programm wird beendet.")
        exit()

def sort_files(path, files):
    # Rename file and move them into a new folder with the correct name
    for file in files:
        folder_path = path / file.decide_folder(folder_names)
        folder_path.mkdir(exist_ok = True)
        file_path = path / file.original_name
        counter = 0
        while True:
            if counter == 0:
                new_name = file.original_name
            else:
                new_name = file.file_name + " (" + str(counter) + ")" + file.file_suffix
            if not (folder_path / new_name).exists():
                break

            counter += 1
        file_path.rename(folder_path / new_name)

files = find_files(curr_path)
confirm_files(files)
sort_files(curr_path, files)