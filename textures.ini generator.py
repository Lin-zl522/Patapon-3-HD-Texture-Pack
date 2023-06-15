# CAUTION: this script skips the 'new' folder for reasons so don't use that folder for anything
# if you encounter any issues with the script please contact me @hozd in discord

import pathlib

root_folder = pathlib.Path(__file__).resolve().parent
ini_filename = "textures.ini"

with open(root_folder / ini_filename, "w") as ini_file:
    ini_file.write("# write your comments here\n\n[options]\n\nversion = 1\nhash = xxh64\nignoreAddress = True\nignoreMipmap = True\nreduceHash = True\n;video = True\n\n[games]\n\nUCES01421 = textures.ini\nUCUS98751 = textures.ini\nUCAS40318 = textures.ini\nNPJG00122 = textures.ini\n\n[hashes]\n\n; TEXTURES: Start\n\n")
    
    seen_paths = set()
    seen_hashes = set()
    undefined_paths = set()

    for png_path in root_folder.glob("**/*.png"):
        rel_path = png_path.relative_to(root_folder).as_posix()
        if "new" in rel_path.split('/'):
            continue

        texture_hash = png_path.stem[:24]
        postfix = png_path.stem[24:]

        if all(c.isdigit() or c.lower() in 'abcdef' for c in texture_hash) and len(texture_hash) == 24:
            if postfix:
                full_texture_hash = f"{texture_hash}{postfix}"
                if full_texture_hash not in seen_hashes:
                    ini_file.write(f"#{full_texture_hash} = {rel_path}\n")
                    undefined_paths.add(rel_path)
                    seen_hashes.add(full_texture_hash)
            else:
                if texture_hash not in seen_hashes:
                    ini_file.write(f"{texture_hash} = {rel_path}\n")
                    seen_hashes.add(texture_hash)
            seen_paths.add(rel_path)
    
    ini_file.write("\n; TEXTURES: End\n")

    if undefined_paths:
        ini_file.write("\n; OTHER: Start\n\n")
        for path in sorted(undefined_paths):
            ini_file.write(f"#{path}\n")
        ini_file.write("\n; OTHER: End\n")
    
    ini_file.write("\n[hashranges]")
