from multiprocessing import Pool
from functions import *
from colorama import Back, Fore, Style


def Download():
    link = input("gallery link: ")

    link = link[0 : link.find("?")]
    link += "/" if not link.endswith("/") else link + ""

    terminalSize = get_terminal_size().columns

    get_header()

    data = downloadPage(link)
    retry = 0
    # open("site-datas/tempdata.html","w",encoding="utf-8").write(data)
    # exit()

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
    if data == "Key missing, or incorrect key provided.":
        print("Please update cookies.   You can do it in Settings")
        return
    
    bs = BeautifulSoup(markup=data, features="html.parser")
    tags = bs.find("div", {"class": "gm"})
    pagelist = bs.find_all("div", {"class": "gtb"})

    pages = []
    ###
    # print(pagelist)
    mainGN = str(bs.find("h1", {"id": "gn"}).contents[0])
    GN = replaceName(mainGN)
    os.environ["DownloadGalleryName"] = GN
    tempMain = mainGN

    if len(mainGN) < 8:
        mainGN = mainGN.center(8)

    if len(mainGN) > (terminalSize - 6) and terminalSize > 0 :
        mainGN = "((Gallry name is too long. i'm not gonig to show it.))"
    else:
        tempMain = mainGN

    # this line print gallery name
    print("\n\n\n\n")
    print(padLeft(f"┌──{'─'*(len(mainGN))}──┐"))
    print(padLeft(f"│  {mainGN}  │"))
    print(padLeft(f"│  {''.center(len(mainGN))}  │"))
    print(padLeft(f"│  {'LETS GO!'.center(len(mainGN))}  │"))
    print(padLeft(f"└──{'─'*(len(mainGN))}──┘"))
    print("\n\n\n\n")
    mainGN = tempMain

    pages_links = []
    try:
        infofile = open(GN + "/info.txt", "r",encoding="utf-8")
        print("Reading Data from INFO file")
        # print("continuing from ")
        for line in infofile.readlines():
            if line.startswith("Page"):
                print(
                    "\n===============================\n"
                    + line
                    + "==============================="
                )
            elif line.startswith("https://e-hentai.org"):
                pages_links.append(line.strip("\n"))
            else:pass
    except Exception as error :
        # print(error)
        try:os.mkdir(GN)
        except:pass
        for i in pagelist[0].find_all("a"):
            if i not in pages:
                pages.append(i.attrs["href"])
        if len(pages) == 1:
            pass
        else:
            pages.pop()  # if didn't work so I remove it manualiy. so this line do -> removes next page button
            pages = complete_list(link, pages)
        #############
        # print(pages)

        print("Downloading pages contents")
        pagenumberCount = 1
        for i in pages:
            print("Page", pagenumberCount, "/", len(pages), end="\r")
            pagenumberCount += 1
            # sleep(0.5)

            data = downloadPage(i)
            if data.startswith("Your IP"):
                while data.startswith("Your IP"):
                    data = downloadPage(i)
                    print(i)
                    print(data)

            htmlpage = BeautifulSoup(markup=data, features="html.parser")
            imagebox = htmlpage.find_all("div", {"class": "gdtm"})
              
            for pic in imagebox:
                pages_links.append(pic.find("a")["href"])

        print(
            "\n===============================\nPages: "
            + str(len(pages_links))
            + " pages\n==============================="
        )

    pageRange = input("Page range(leave empty to download all gallry):")
    if pageRange != "":
        pageRange = parse_ranges(pageRange,pages_links)
        FinalPageLinks = []
        for i in pageRange:
            FinalPageLinks.append(pages_links[i])
        create_download_info(link, data, pages_links)
    else:
        FinalPageLinks = pages_links.copy()
        create_download_info(link, data, pages_links)

    try:
        core = int(loads(environ["userdata"])["core"])
        # FinalPageLinks = split_list(FinalPageLinks,core)

        ### Multiprocess if core > 1  
        if core > 1:
            with Pool(core) as p:
                p.map(MPdownload, FinalPageLinks)
        else:
            for i in FinalPageLinks:
                link = i
                if get_downloadeds(link.split("/")[-1],GN):
                    imglimit = checkIMGlimit()
                    sleep(1)
                    logger(link, imglimit)
                    download_image(link)
                else:pass

    except KeyboardInterrupt:
        if p:
            p.terminate()
        exit("closeing")

    except Exception as e:
        p.terminate()
        print(e)
        exit("closeing")

    print("Recheck...                           ")

    for i in FinalPageLinks:
        link = i
        if get_downloadeds(link.split("/")[-1],GN):
            imglimit = checkIMGlimit()
            sleep(1)
            logger(link,imglimit)
            download_image(link)
        else:pass
    print("ALL IMAGES DOWNLOADED.")


def MPdownload(links:list):
    # workerNumber = f"Worker {links.keys()[0]} |"
    workerNumber = ""
    # linklist = links.values()[0]
    linklist = links
    link = linklist
    # for link in linklist: 
    GN = os.environ["DownloadGalleryName"]
    try:
        if get_downloadeds(link.split("/")[-1], GN):
            imglimit = checkIMGlimit()
            sleep(1)
            logger(link,imglimit)
            download_image(link)

        else:
            terminalx = get_terminal_size().columns
            print(
                workerNumber
                +link.split("/")[-1]
                + " already downloaded"
                + " " * (terminalx - len(link.split("/")[-1]) - 21)
            )
            # sleep(0.02)
    except KeyboardInterrupt:
        exit("closeing")
    except Exception as e:
        print(e)
        exit()


def Normaldownloader(links:list):
    linklist = links
    for link in linklist: 
        GN = os.environ["DownloadGalleryName"]
        try:
            if get_downloadeds(link.split("/")[-1], GN):
                imglimit = checkIMGlimit()
                sleep(1)
                logger(link,imglimit)
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
        except KeyboardInterrupt:
            exit("closeing")


if __name__ == "__main__":
    # if len(sys.argv)>2:
    #   os.environ["justPV"]="true"
    # else:
    Download()
os.environ["justPV"]="false"

# // todo: add https://e-hentai.org/home.php to check for image limit ---- DONE
# todo: handle: Downloading original files of this gallery during peak hours requires GP, and you do not have enough
# // todo: fix: Error on downloading one page gallerys
