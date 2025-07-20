import os
import zipfile

version = ""
modrinthFile = open("modrinth-changelog.md", "w")
githubFile = open("github-changelog.md", "w")
envFile = open(os.getenv("GITHUB_ENV"), "a")


with open("CHANGELOG.md", "r") as inFile:
    for line in inFile.readlines():
        if line.startswith("\n"):
            break
        elif line.startswith("## "):
            version = line.split("[")[1].split("]")[0]
            envFile.write(f"\nNAME=Version {version} - {line.split(' ')[-1].strip()}")
            envFile.write(f"\nVERSION={version}")
        elif line.startswith("### "):
            modrinthFile.write(line)
            githubFile.write(line)
        else:
            modrinthFile.write(line)
            githubFile.write(line)

with open("CHANGELOG.md", "r") as inFile:
    for line in inFile.readlines():
        if line.startswith("- Support Minecraft version "):
            githubFile.write(f"\nFor Minecraft version `{line.split('`')[1]}`.")
            minecraftVersions = line.split('`')[1].split("-")
            envFile.write(f"\nMINECRAFT_VERSION=>={minecraftVersions[0]} <={minecraftVersions[-1]}")
            break

zf = zipfile.ZipFile(f"muffintime-data-pack-{version}.zip", "w")
for dirname, subdirs, files in os.walk("."):
    if dirname.startswith(os.path.join(".", ".")):
        continue
    if not dirname == ".":
        zf.write(dirname)
    for filename in files:
        if not filename.startswith(".") and not filename.startswith("modrinth") and not filename.startswith("github") and not filename.startswith("muffintime"):
            zf.write(os.path.join(dirname, filename))
zf.close()