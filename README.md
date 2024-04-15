# E-Hentai Downloader

A relatively simple downloader for e-hentai galleries

Obviously, there is a much better program [https://github.com/ccloli/E-Hentai-Downloader] for this task, and it requires more RAM, but this program saves files directly, so it needs much less RAM.

And it is not necessary that the browser is open at the same time. If the browser consumes a lot of resources or you want to continue browsing you can close your browser or gallery browser tab .

## installing

**Running a virtual environment is recommended.**

### installing using git

``` ps1
git clone https://github.com/tank-sman/e-hentai-downloader

cd e-hentai-downloader

pip install -r requirements.txt

python main.py
```

### installing with zip

Unpack zip file and open terminal in extracted folder.

``` ps1
pip install -r requirements.txt

python main.py
```

In the first run, you need to enter site cookies manually

### In Chrome (or _mayby_ other browser with chromium core like edge and ...)

``` Inspect (F12) > Application > Cookies ```

### In Firefox

``` Inspect (Q) (F12) > Storage > Cookies ```

Copy and paste the values as the program prompts

## ***in the future:***

- [x] Download single images

- [x] Download multiple files with parallel execution

- [ ] Automatic login or automatic cookies copy

- [ ] Handling downloads on peak hours

- [x] Fix single page galleries downloading issue

- [ ] Torrent Download

- [x] Fix for MPdownlaod

***That's it for now----***

## Contributions

All types of contributions are highly appreciated whatever it would be adding new features, fixing bugs, writing tests or docs, improving the current docs' grammars, or even fixing the typos!

### Please Leave a review

At this moment, I need your reviews and suggestions. Send them in [discussions](https://github.com/tank-sman/e-hentai-downloader/discussions). Thank you.💖
