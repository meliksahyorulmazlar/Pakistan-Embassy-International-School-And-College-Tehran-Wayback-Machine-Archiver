import requests,lxml,re,time
from bs4 import BeautifulSoup

from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)



class WaybackArchive:
    def __init__(self):
        self.found_links = []
        self.find()
        self.save_all()

    def find(self):
        soup = BeautifulSoup(requests.get('https://peisctehran.com').text,'lxml')
        soup = str(soup)
        links = re.findall(r'"(.*?)"', soup)
        links = [link for link in links if link.startswith('https://peisctehran')]
        self.found_links.append('https://peisctehran.com/')
        self.found_links.append("https://peisctehran.com")

        while links:
            print(len(links))
            if links[0] in self.found_links:
                # This link has already been explored
                links.pop(0)
            else:
                if 'wp-content' in links[0]:
                    # These are photos,pdfs that have no links
                    self.found_links.append(links[0])
                    links.pop(0)
                else:
                    # The link has not been explored-so it finds new links
                    soup = BeautifulSoup(requests.get(links[0]).text, 'lxml')
                    soup = str(soup)
                    new_links = re.findall(r'"(.*?)"', soup)
                    new_links = [link for link in new_links if link.startswith('https://peisctehran')]
                    for new_link in new_links:
                        if new_link not in self.found_links:
                            if new_link not in links:
                                print(new_link)
                                links.append(new_link)
                    self.found_links.append(links[0])
                    links.pop(0)

    # This method will save all the links on the wayback machine
    def save_all(self)->None:
        for link in self.found_links:
            print(f'saving {link}')
            self.save(link)
            time.sleep(2)

    # This method will save a given website link on the wayback machine
    def save(self, site: str) -> None:
        try:
            requests.get("https://web.archive.org/save/" + site)
        except requests.exceptions.ConnectionError:
            print('connection error')
            pass


if __name__ == "__main__":
    wa = WaybackArchive()
