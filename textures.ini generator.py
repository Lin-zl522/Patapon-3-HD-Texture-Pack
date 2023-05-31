import os

# set the root folder and the name of the ini file
root_folder = os.path.dirname(os.path.abspath(__file__))
ini_filename = "textures.ini"


# loop through all subfolders in the root folder
with open(os.path.join(root_folder, ini_filename), "w") as ini_file:
    # add a start marker to the TEXTURES group, options, comments, games and allthat
    ini_file.write(
    "# https://github.com/Lin-zl522/Patapon-3-HD-Texture-Pack\n\n[options]\n\nversion = 1\nhash = xxh64\nignoreAddress = True\nignoreMipmap = True\nreduceHash = True\n;video = True\n\n[games]\nUCES01421 =textures.ini\nUCUS98751 = textures.ini\nUCAS40318 = textures.ini\nNPJG00122 = textures.ini\n\n[hashes]\n\n; TEXTURES: Start\n\n")
    for folder, _, files in os.walk(root_folder):
        for file in files:
            # only include png files
            if file.endswith(".png"):
                # get the relative path to the png file
                png_path = os.path.join(folder, file)
                rel_path = os.path.relpath(png_path, root_folder).replace("\\", "/")
                # get the texture hash from the png filename
                texture_hash = file[:-4]
                # check if the length is 26 (like [<hash>-1], it will delete the last two symbols)
                if len(texture_hash) == 26:
                    texture_hash = file[:-6]
                    ini_file.write(f"#{texture_hash} = {rel_path}\n")
                # otherwise check if the texture hash is valid and just add it
                elif all(c in "0123456789ABCDEFabcdef" for c in texture_hash):
                    ini_file.write(f"{texture_hash} = {rel_path}\n")
    # add an end marker to the TEXTURES group
    ini_file.write("\n; TEXTURES: End\n\n")
    # add a start marker to the OTHER group
    ini_file.write("; OTHER: Start\n\n")
    for folder, _, files in os.walk(root_folder):
        for file in files:
            # only include files that are png and not already included in the TEXTURES group
            if file.endswith(".png"):
                png_path = os.path.join(folder, file)
                rel_path = os.path.relpath(png_path, root_folder).replace("\\", "/")
                texture_hash = file[:-4]
                if not all(c in "0123456789ABCDEFabcdef" for c in texture_hash):
                    # add the file to the OTHER group
                    ini_file.write(f"#{rel_path}\n")
    # add an end marker to the OTHER group and [hashranges]
    ini_file.write("\n; OTHER: End\n\n[hashranges]")

