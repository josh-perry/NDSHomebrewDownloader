__author__ = "Josh Perry"

import os
import shutil
import urllib2
import zipfile
import rarfile
from bs4 import BeautifulSoup


dumping_directory = "W:\Plugin repo\dump"


def save_file(url, filename):
    filename = "out/" + filename

    # Check if we already have it
    if os.path.isfile(filename + ".zip") or os.path.isfile(filename + ".rar") or os.path.isfile(filename + ".zip"):
        print "We already have " + filename + ", skipping"
        return

    print("Downloading... " + filename)

    try:
        f = open(filename, 'wb')
        f.write(urllib2.urlopen(url).read())
        f.close()

        if zipfile.is_zipfile(filename):
            print(filename + " is a zip file")
            shutil.move(filename, filename + ".zip")
        elif rarfile.is_rarfile(filename):
            print(filename + " is a rar file")
            shutil.move(filename, filename + ".rar")
        else:
            print(filename + " is an nds file")
            shutil.move(filename, filename + ".nds")
    except urllib2.URLError:
        print "Failed to download: " + filename


def nds_homebrew_hive():
    base_url = "http://www.ndshb.com"

    # Apps #
    page_template = "http://www.ndshb.com/index.php/component/jdownloads/viewcategory/3-apps?start={0}"

    os.mkdir("out")
    os.mkdir("out/ndshb_apps")

    for i in range(0, 7):
        page = page_template.format(i * 10)

        f = urllib2.urlopen(page)
        soup = BeautifulSoup(f.read(), "html.parser")

        for link in soup.find_all(class_="jd_download_url"):
            url = link["href"]
            filename = url.split('/')[-1].split("?")[0]
            save_file(base_url + url, "ndshb_apps/" + filename)

    # Games #
    page_template = "http://www.ndshb.com/index.php/component/jdownloads/viewcategory/4-games?start={0}"

    if not os.path.isdir("out/ndshb_games"):
        os.mkdir("out/ndshb_games")

    for i in range(0, 10):
        page = page_template.format(i * 10)

        f = urllib2.urlopen(page)
        soup = BeautifulSoup(f.read(), "html.parser")

        for link in soup.find_all(class_="jd_download_url"):
            url = link["href"]
            filename = url.split('/')[-1].split("?")[0]
            save_file(base_url + url, "ndshb_games/" + filename)


def process_files(directory):
    for root, directories, files in os.walk(directory):
        for f in files:
            try:
                original = os.path.join(root, f)
                output = os.path.join(dumping_directory, f)

                # Extract zip files
                if f.endswith(".zip"):
                    with zipfile.ZipFile(original, "r") as z:
                        os.mkdir(output[:-3])
                        z.extractall(output[:-3])
                # Extract rar files
                elif f.endswith(".rar"):
                    with rarfile.RarFile(original, "r") as z:
                        os.mkdir(output[:-3])
                        z.extractall(output[:-3])
                # Just copy nds files
                elif f.endswith(".nds"):
                    os.mkdir(output[:-3])
                    shutil.copy(original, os.path.join(output[:-3], f))
            except (zipfile.BadZipfile, rarfile.BadRarFile):
                print "Bad archive: " + f
                continue
            except Exception as e:
                print e
                continue

            print "Processed " + f

        for d in directories:
            process_files(d)


def main():
    nds_homebrew_hive()

    if not os.path.isdir(dumping_directory):
        os.mkdir(dumping_directory)

    process_files("out")

if __name__ == "__main__":
    main()
