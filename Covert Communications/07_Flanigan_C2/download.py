import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

#

def download_image(url, pathname):

    print("\n-------------------- DOWNLOADING FILES --------------------\n")

    # Destination path for download

    file_name = os.path.basename(url)
    print("File Name: "+ file_name + "\n")
    dest_path = os.path.join(pathname, file_name)
    print("Destination Path: "+ dest_path + "\n")

    try:
        """
        Downloads a file given an URL and puts it in the folder `pathname`
        """
        # if path doesn't exist, make that path dir
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        # download the body of response by chunk, not immediately
        response = requests.get(url, stream=True)

        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))

        # get the file name
        filename = os.path.join(pathname, url.split("/")[-1])

        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1), "Downloading...", total=file_size, unit="B", unit_scale=True, unit_divisor=1)
        with open(filename, "wb") as f:
            for data in progress.iterable:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))
        return
    except Exception as e:
        print("downloading bytes didnt work")
        pass

def download_text(link, dest):
    res = requests.get(link)
    html_page = res.content
    soup = bs(html_page, 'html.parser')
    text = soup.find_all(string=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
    ]

    # for t in text:
    #     if t.parent.name not in blacklist:
    #         output += '{} '.format(t)

    filename = 'imgTitle.txt'
    print("Downloading text data...\n")
    print(text)
    with open(filename, 'w') as f:
        print(text[23])
        f.write(text[23])



def main():
    dest = "/home/ace/Desktop/c6"
    image_link = input("Enter the image URL: ")
    text_link = input("Enter the text link: ")

    download_image(image_link, dest)
    download_text(text_link, dest)


if __name__ == "__main__":
    main()
