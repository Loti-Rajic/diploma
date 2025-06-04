import os

# Funkcija za odstranitev vsega od markerja naprej
def clean_text(text):
    marker = "Opozorilo:297. členu Kazenskega zakonika"
    index = text.find(marker)
    if index != -1:
        return text[:index].strip()
    return text.strip()

def clean_all_txt_in_directory(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                original_text = f.read()

            cleaned_text = clean_text(original_text)

            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            print(f"Obdelano: {filename}")

# Pot do mape
directory = 'D:\\faks\\fri-fu\\diploma\\aplikacija\\24ur_articles'
clean_all_txt_in_directory(directory)
