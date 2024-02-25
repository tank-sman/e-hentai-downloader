from functions import *
from random import randint
from colorama import Back, Fore, Style

def Download():
    link = input("gallery link: ")

    link = link[0 : link.find("?")]

    data = download(link)
    retry = 0
    # open("site-datas/tempdata.html","w",encoding="utf-8").write(data)
    # exit()
    if data.find("Due to its content, it should not be viewed by anyone") == "-1":
        print(
            f"""
{Back.WHITE}{Fore.BLACK}Offensive For Everyone!{Back.BLACK}{Fore.WHITE}
    Due to its content, it should not be viewed by anyone
but still downloading ;)"""
        )
        sleep(3)
        data = download(link + "?nw=always")

    if data.startswith("Your IP"):
        while retry < 3:
            data = download(link)
            if data.startswith("Your IP "):
                retry += 1
            else:
                break
            print("this IP is blocked")
            print(data[182::])

    if data.startswith("Your IP"):
        exit()

    bs = BeautifulSoup(markup=data, features="html.parser")
    tags = bs.find("div", {"class": "gm"})
    pagelist = bs.find_all("div", {"class": "gtb"})
    pages = []

    mainGN = str(bs.find("h1", {"id": "gn"}).contents[0])
    GN = replaceName(mainGN)
    print("\n\n\n\n" + mainGN)
    print("LETS GO!\n\n\n\n")

    for i in pagelist[0].find_all("a"):
        if i not in pages:
            pages.append(i.attrs["href"])
    if len(pages) == 1:
        pass
    else:
        pages.pop()  # if loop didn't work so I remove it manualiy. so this line do -> removes next page button
        pages = complete_list(link, pages)

    # print(pages)
    pages_links = []

    print("Downloading pages contents")
    pagenumberCount = 1
    for i in pages:
        print("Page", pagenumberCount)
        pagenumberCount += 1
        sleep(0.5)
        # print(i)
        data = download(i)
        if not data.startswith("Your IP"):
            bs = BeautifulSoup(markup=data, features="html.parser")
            imagebox = bs.find_all("div", {"class": "gdtm"})
        else:
            while data.startswith("Your IP"):
                data = download(i)
                print(i)
                print(data)
            bs = BeautifulSoup(markup=data, features="html.parser")
            imagebox = bs.find_all("div", {"class": "gdtm"})

        for pic in imagebox:
            # print(pic.find("a")["href"])
            pages_links.append(pic.find("a")["href"])

    print(
        "===============================\n"
        + str(len(pages_links))
        + " pages\n==============================="
    )
    pageRange = input("Page range(leave empty to download all gallry):")
    if pageRange != "":
        pageRange = parse_ranges(pageRange)
        FinalPageLinks = []
        for i in pageRange:
            FinalPageLinks.append(pages_links[i])
        create_download_info(link, data, FinalPageLinks)
    else:
        FinalPageLinks = pages_links.copy()
        create_download_info(link, data, FinalPageLinks)

    for i in FinalPageLinks:
        if get_downloadeds(i.split("/")[-1],GN):
            imglimit = checkIMGlimit()
            sleep(1)
            terminalx = get_terminal_size().columns
            strprint = (
                i
                + " " * (terminalx - len(i) - len(imglimit) - 11)
                + f"|{imglimit}| "
                + ctime()[11:-5]
            )
            print(strprint, end="\r")
            download_image(i)
        else:
            terminalx = get_terminal_size().columns
            print(
                i.split("/")[-1]
                + " already downloaded"
                + " " * (terminalx - len(i.split("/")[-1]) - 21),
                end="\r",
            )
            sleep(0.02)
    print()


if __name__ == "__main__":
    Download()

# // todo: add https://e-hentai.org/home.php to check for image limit ---- DONE
# todo: handling: Downloading original files of this gallery during peak hours requires GP, and you do not have enough
#// todo: fix: Error on downloading one page gallerys
