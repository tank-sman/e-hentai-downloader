from multiprocessing import Pool
from functions import *
from colorama import Back, Fore, Style

def Download():
    link = input("gallery link: ")

    link = link[0 : link.find("?")]
    link += "/" if not link.endswith("/") else link +""
    
    get_header()

    data = downloadPage(link)
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
        data = downloadPage(link + "?nw=always")

    if data.startswith("Your IP"):
        while retry < 3:
            data = downloadPage(link)
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
    os.environ["DownloadGalleryName"] =GN
    print("\n\n\n\n"+"="*32+"\n"+ mainGN)
    print("LETS GO!"+"\n"+"="*32+"\n\n\n\n")

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
        print("Page", pagenumberCount,end="\r")
        pagenumberCount += 1
        sleep(0.5)
        # print(i)
        data = downloadPage(i)
        if not data.startswith("Your IP"):
            bs = BeautifulSoup(markup=data, features="html.parser")
            imagebox = bs.find_all("div", {"class": "gdtm"})
        else:
            while data.startswith("Your IP"):
                data = downloadPage(i)
                print(i)
                print(data)
            bs = BeautifulSoup(markup=data, features="html.parser")
            imagebox = bs.find_all("div", {"class": "gdtm"})

        for pic in imagebox:
            # print(pic.find("a")["href"])
            pages_links.append(pic.find("a")["href"])

    print(
        "\n===============================\n"
        + str(len(pages_links))
        + " pages\n==============================="
    )
    pageRange = input("Page range(leave empty to download all gallry):")
    if pageRange != "":
        pageRange = parse_ranges(pageRange)
        FinalPageLinks = []
        for i in pageRange:
            FinalPageLinks.append(pages_links[i])
        create_download_info(link, data, pages_links)
    else:
        FinalPageLinks = pages_links.copy()
        create_download_info(link, data, pages_links)

    try:
        with Pool(4) as p:
            p.map(MProdownload,FinalPageLinks)
    except KeyboardInterrupt:
        exit("closeing")
    print()

def MProdownload(link):
    GN = os.environ["DownloadGalleryName"]
    if get_downloadeds(link.split("/")[-1],GN):
        imglimit = checkIMGlimit()
        sleep(1)
        terminalx = get_terminal_size().columns
        strprint = (
                link
                + " " * (terminalx - len(link) - len(imglimit) - 11)
                + f"|{imglimit}| "
                + ctime()[11:-5]
            )
        print(strprint)
        print(link.split("/")[-1])
        download_image(link)

    else:
        terminalx = get_terminal_size().columns
        print(
                link.split("/")[-1]
                + " already downloaded"
                + " " * (terminalx - len(link.split("/")[-1]) - 21),
                end="\r",
            )
        sleep(0.02)



# if __name__ == "__main__":
#     Download()

# // todo: add https://e-hentai.org/home.php to check for image limit ---- DONE
# todo: handling: Downloading original files of this gallery during peak hours requires GP, and you do not have enough
#// todo: fix: Error on downloading one page gallerys
