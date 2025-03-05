# the script completely skips the "new" folders and subfolders
# remove lines 33-35 if you want to parse them

# it also WILL parse your entire machine's images given the opportunity so please don't run it outside your texture folders

import pathlib

texture_folder = pathlib.Path(__file__).resolve().parent
ini_filename = "textures.ini"
custom_textures_folder = texture_folder / "_custom_textures"

seen_hashes = set()
custom_hashes = []
texture_hashes = []
other_entries = []

def valid_hash(filename):
    return len(filename) == 24 and all(c.lower() in '0123456789abcdef' for c in filename)

def sort_key(entry):
    _, rel_path = entry
    return rel_path.split('/') 

# parse the custom textures first
for png_path in custom_textures_folder.glob("*.png"):
    rel_path = png_path.relative_to(texture_folder).as_posix()
    filename = png_path.stem  

    if valid_hash(filename):
        custom_hashes.append((filename, rel_path))
        seen_hashes.add(filename)
    else:
        custom_hashes.append((f";{filename} (invalid hash)", rel_path))

# parse everything else
for png_path in texture_folder.glob("**/*.png"):
    if custom_textures_folder in png_path.parents or "new" in png_path.parts:
        continue 

    rel_path = png_path.relative_to(texture_folder).as_posix()
    filename = png_path.stem 

    if valid_hash(filename):
        if filename in seen_hashes:
            other_entries.append((f"{filename} (dupe)", rel_path))
        else:
            texture_hashes.append((filename, rel_path))
            seen_hashes.add(filename)
    else:
        other_entries.append((f"{filename} (invalid hash)", rel_path))

# sorting paths so that the ini is more readable
custom_hashes.sort(key=sort_key)
texture_hashes.sort(key=sort_key)
other_entries.sort(key=sort_key)

# write the ini file
with open(texture_folder / ini_filename, "w") as ini_file:
    # write custom comments in this line if you want them to appear automatically
    ini_file.write("# write your comments here\n\n[options]\n\nversion = 1\nhash = xxh64\nignoreAddress = True\nignoreMipmap = True\nreduceHash = True\n;video = True\n\n[games]\n\nUCES01421 = textures.ini\nUCUS98751 = textures.ini\nUCAS40318 = textures.ini\nNPJG00122 = textures.ini\n\n[hashes]\n")
    # don't touch the options unless you're working with something other than patapon 3 and you know what you're doing
    
    # write custom texture hashes
    ini_file.write("\n; CUSTOM_TEXTURES: Start\n\n")
    for hash_value, rel_path in custom_hashes:
        ini_file.write(f"{hash_value} = {rel_path}\n")
    ini_file.write("\n; CUSTOM_TEXTURES: End\n")

    # write good texture hashes
    ini_file.write("\n; TEXTURES: Start\n\n")
    for hash_value, rel_path in texture_hashes:
        ini_file.write(f"{hash_value} = {rel_path}\n")
    ini_file.write("\n; TEXTURES: End\n")

    # write duplicates and invalid hashes
    if other_entries:
        ini_file.write("\n; OTHER: Start\n\n")
        for hash_value, rel_path in other_entries:
            ini_file.write(f"#{hash_value} = {rel_path}\n")
        ini_file.write("\n; OTHER: End\n")

    ini_file.write("\n[hashranges]")