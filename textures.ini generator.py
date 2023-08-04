import pathlib

root_folder = pathlib.Path(__file__).resolve().parent
ini_filename = "textures.ini"

def write_textures_section(ini_file, textures, header):
    ini_file.write(f"\n; {header}: START\n")
    for texture_hash, rel_path in sorted(textures.items(), key=lambda item: item[1]):
        ini_file.write(f"{texture_hash} = {rel_path}\n")
    ini_file.write(f"; {header}: END\n")

def get_texture_hash(png_path):
    texture_hash = png_path.stem[:24]
    postfix = png_path.stem[24:]
    if all(c.isdigit() or c.lower() in 'abcdef' for c in texture_hash) and len(texture_hash) == 24:
        if postfix:
            return f"{texture_hash}{postfix}"
        else:
            return texture_hash
    return None

def main():
    custom_textures = {}
    other_textures = {}
    seen_paths = set()

    custom_textures_folder = root_folder / "_custom_textures"
    for png_path in custom_textures_folder.glob("**/*.png"):
        rel_path = png_path.relative_to(root_folder).as_posix()
        texture_hash = get_texture_hash(png_path)
        if texture_hash:
            custom_textures[texture_hash] = rel_path

    for png_path in root_folder.glob("**/*.png"):
        rel_path = png_path.relative_to(root_folder).as_posix()
        if "new" in rel_path.split('/'):
            continue

        texture_hash = get_texture_hash(png_path)
        if texture_hash and rel_path not in seen_paths:
            if texture_hash in custom_textures:
                continue
            other_textures[texture_hash] = rel_path
            seen_paths.add(rel_path)

    with open(root_folder / ini_filename, "w") as ini_file:
        ini_file.write("# write your comments here\n\n[options]\n\nversion = 1\nhash = xxh64\nignoreAddress = True\nignoreMipmap = True\nreduceHash = True\n;video = True\n\n[games]\n\nUCES01421 = textures.ini\nUCUS98751 = textures.ini\nUCAS40318 = textures.ini\nNPJG00122 = textures.ini\n\n[hashes]\n\n")

        write_textures_section(ini_file, other_textures, "TEXTURES")
        
        write_textures_section(ini_file, custom_textures, "CUSTOM TEXTURES")

        if other_textures:
            ini_file.write("\n; OTHER: Start\n\n")
            for rel_path in sorted(seen_paths - set(other_textures.values())):
                ini_file.write(f"#{rel_path}\n")
            ini_file.write("\n; OTHER: End\n")

        ini_file.write("\n[hashranges]")

if __name__ == "__main__":
    main()
