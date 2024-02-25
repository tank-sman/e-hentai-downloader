from bs4 import BeautifulSoup
from time import sleep, ctime
from os import get_terminal_size
from settings import readSetting
from colorama import Back, Fore, Style
import requests, json, os, re

invalid_chars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]

imglimit = 0


def replaceName(text):
    export = ""
    for i in text:
        if i in invalid_chars:
            export += "-"
        else:
            export += i
    return export


# datas = dict(json.load(open("./data.json")))
def get_header():
    datas = readSetting()
    userdata = [
        "ipb_memeber_id=" + datas["ipb_member_id"],
        "ipb_pass_hash=" + datas["ipb_pass_hash"],
        "ipb_session_id=" + datas["ipb_session_id"],
        "sk=" + datas["sk"],
    ]
    cookies = ""
    for i in userdata:
        cookies += i + "; "

    head = {
        "Cookie": cookies,
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
    }

    return head


def download(link: str):
    # req = requests.get(link,cookies=cockies)
    downloaded = False
    while not downloaded:
        try:
            req = requests.get(link, headers=get_header())
            downloaded = True
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt\n")
            exit()
        except Exception as err:
            print("Connection Error: ", err)
            sleep(0.2)
    return req.text


def image_download_request(link, filename):
    response = requests.get(link, stream=True, headers=get_header())
    response.raise_for_status()  # Raise error if download fails
    with open(filename, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


def download_image(url: str):
    # data = requests.get(url, headers=head)
    downloaded = False
    while not downloaded:
        try:
            data = requests.get(url, headers=get_header())
            downloaded = True
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt\n")
            exit()
        except Exception as err:
            print("Error: ", err)
            sleep(0.2)
    bs = BeautifulSoup(data.text, "html.parser")
    try:
        link = bs.find("div", {"id": "i6"}).find_all("a")[-1].attrs["href"]
        GN = bs.find("h1").contents[0]

        GN = replaceName(GN)

        filename = GN + "/" + url.split("/")[-1] + ".png"

    except:
        exit(data.text)

    if len(link) == 1:
        print("\nNo High quality image Found\n donwloading lower quality.")
        link = bs.find("img", {"id": "img"}).attrs["src"]
    # sleep(1)

    # Create the folder
    if os.path.isdir(GN) == False:
        os.mkdir(GN)
    downloaded = False
    while not downloaded:
        try:
            image_download_request(link, filename)
            downloaded = True
        except KeyboardInterrupt:
            break
        except:
            print("\n connection error")
            sleep(0.2)
            pass


def get_downloadeds(name: str, GN: str):
    if os.path.isfile(GN + "/" + name + ".png"):
        return False
    else:
        return True


def complete_list(link, pages):
    page_numbers = set()
    for url in pages:
        match = re.search(r"p=(\d+)", url)
        if match:
            page_numbers.add(int(match.group(1)))

    complete_urls = [link]
    for page_number in range(1, max(page_numbers) + 1):
        complete_urls.append(f"{link}?p={page_number}")

    return complete_urls


def create_download_info(url, pageData, imageslink):
    bs = BeautifulSoup(pageData, "html.parser")
    box = bs.find("div", {"class": "gm"})
    mainGN = str(box.find("h1", {"id": "gn"}).contents[0])
    GN = replaceName(mainGN)

    # Create the folder
    if os.path.isdir(GN) == False:
        os.mkdir(GN)

    clas = bs.find("div", {"class": "cs"}).contents[0]
    Uploader = bs.find("div", {"id": "gdn"}).find("a").attrs["href"]

    Posted, Parent, Visible, Language, File_Size, pagesNumber, Favorited = bs.find_all(
        "td", {"class": "gdt2"}
    )

    tagnames = {}
    tgbox = bs.find("div", {"id": "gd4"})

    # for i in tgbox.find_all("td",{"class":"tc"}):
    #     tagnames[i]=

    for i in tgbox.find_all("tr"):
        m = i
        tagdata = m.find_all("a")
        tagstr = ""
        for d in tagdata:
            tagstr += str(d.contents).replace("\\t", "").replace("\\n", "")
        tagnames[str(i.find("td", {"class": "tc"}).contents[0])] = tagstr
    tags = ""

    for i in tagnames:
        tags += i + tagnames[i]
        tags += "\n"

    imagelist = ""
    for i in imageslink:
        imagelist += i + "\n"

    fulltext = f"""    {url}

{mainGN}

Category: {clas}
Date: {Posted.contents[0]}
Language: {Language.contents[0]}
File Size: {File_Size.contents[0]}
Pages: {pagesNumber.contents[0]}
Favorited: {Favorited.contents[0]}

Rating:{bs.find("td",{"id":"rating_label"}).contents[0]}

Uploader: {Uploader}

{tags}

images links:

{imagelist}

download started on {ctime()}
Created by github.com/tank-sman/e-hentai-downloader.
"""
    try:
        file = open(GN + "/info.txt", "x", encoding="utf-8")
        file.write(fulltext)
        file.close()
    except:
        print("info file exist.")
        rewrite = readSetting()["rewriteInfo"]
        if rewrite:
            print("Rewriting...")
            file = open(GN + "/info.txt", "w", encoding="utf-8")
            file.write(fulltext)
            file.close()


def checkIMGlimit():
    home = download("https://e-hentai.org/home.php")
    bs = BeautifulSoup(home, "html.parser")
    # open("site-datas/tempdata.html","w",encoding="utf-8").write(home)
    limit = bs.find("strong").contents[0]
    as_str = limit + f"/5000"
    while int(limit) >= 4950:
        bs = BeautifulSoup(home, "html.parser")
        limit = bs.find("strong").contents[0]
        as_str = limit + f"/5000"
        limittext = as_str + f" image limit. you {Fore.RED}can't{Fore.WHITE} download more images "
        print()
        print(
            limittext
            + (get_terminal_size().columns - len(limittext) - 8) * " "
            + ctime()[11:-5],
            end="\r",
        )
        sleep(20)
        home = download("https://e-hentai.org/home.php")
        bs = BeautifulSoup(home, "html.parser")
        limit = bs.find("strong").contents[0]

    return str(as_str)


def parse_ranges(ranges: str, pages_links: list = []):
    """
    Download ranges of pages, split each range with comma ()
    Ranges prefixed with ! means negative range, pages in these range will be excluded

    Example:

    -10: Download from page 1 to 10
    !8: Exclude page 8
    12: Download page 12
    14-20: Download from page 14 to 20
    !15-17: Exclude page 15 to 17
    !!! NOT YET !!! 30-40/2: Download each 2 pages in 30-40 (30, 32, 34, 36, 38, 40)
    !!! NOT YET !!! 50-60/3: Download each 3 pages in 50-60 (50, 53, 56, 59)
    70-: Download from page 70 to the last page

    Pages range follows your order, a negative range can drop previous selected pages, the
    latter positive range can add it back

    Example:

    !10-20: Download every page except page 10 to 20

    1-10, !1-8/2, 14, 5: Download page 1 to 10 but remove 1, 3, 5, 7 and 4, then add 5 back (2,
    5, 6, 8, 9, 10)"""
    text = ranges
    numbers = pages_links
    export = []

    for range_str in text.split(","):
        if not range_str.startswith("!"):
            toLast = re.match(r"^\d+-+$", range_str)
            fromFirst = re.match(r"-[0-9]+", range_str)

            if toLast != None:
                for i in numbers:
                    if i >= int(range_str[:-1:]):
                        export.append(i)

            elif fromFirst != None:
                for i in numbers:
                    if i <= int(range_str[1::]):
                        export.append(i)

            elif "-" in range_str and "/" not in range_str:
                start, end = map(int, range_str.split("-"))
                for i in range(start - 1, end):
                    export.append(i)

            elif "/" in range_str:
                range_numbers, page_multiple = range_str.split("/")
                start, end = map(int, range_numbers.split("-"))
                for i in range(start - 1, end, int(page_multiple)):  # each page
                    export.append(i)

            else:
                export.append(int(range_str))

        else:  # range_str.startswith("!"):
            toLast = re.match(r"^!\d+-+$", range_str)
            fromFirst = re.match(r"!+-[0-9]+", range_str)
            if toLast != None:
                for i in export.copy():
                    if int(i) >= int(range_str[1:-1]):
                        export.remove(i)

            elif fromFirst != None:
                for i in export.copy():
                    if int(i) <= int(range_str[2::]):
                        export.remove(i)

            elif "-" in range_str and "/" not in range_str:
                listsplit = range_str[1::]
                start, end = map(int, listsplit.split("-"))
                for i in range(start - 1, end):
                    export.remove(i)

            elif "/" in range_str:
                range_numbers, page_multiple = range_str.split("/")
                start, end = map(int, range_numbers.split("-"))
                for i in range(start - 1, end, int(page_multiple)):  # each page
                    export.remove(i)

            else:
                export.remove(int(range_str[1:]))

    export.sort()
    return export


if __name__ == "__main__":
    # print(checkIMGlimit())
    pass
