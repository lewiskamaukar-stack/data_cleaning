import os 
import shutil

folders = ["images","music","documents"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("folders created!")

source = "images"
items = os.listdir(source)
files = [f for f in items if os.path.isfile(os.path.join(source, f))]
print (f"Found {len(files)} files in {source}")

ext_map = {
    ".jpg": "images",
    ".jpeg": "images",
    ".png":"images",

    ".mp3":"music",
    ".wav":"music",

    ".doc":"documents",
    ".pdf":"documents",
    ".txt":"documents",
}

default_folder = "others"

def safe_move(src_path, dest_folder):
    basename = os.path.basename(src_path)
    name, ext = os.path.splitext(basename)
    dest_path = os.path.join(dest_folder, basename)

    counter = 1
    while os.path.exists(dest_path):
        new_name = f"{name} ({counter}){ext}"
        dest_path = os.path.join(dest_folder, new_name)
        counter += 1

    shutil.move(src_path, dest_path)
    return dest_path

# DRY RUN mode
DRY_RUN = True

for f in files:
    name, ext = os.path.splitext(f)
    ext = ext.lower()
    target_folder = ext_map.get(ext, default_folder)
    source_path = os.path.join(source, f)

    if DRY_RUN:
        print(f"[DRY RUN] Would move: {source_path} -> {target_folder}")
    else:
        os.makedirs(target_folder, exist_ok=True)
        moved_to = safe_move(source_path, target_folder)
        print(f"Moved: {source_path} -> {moved_to}")

print("Done.")
