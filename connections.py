import os

import requests,time

class WaybackArchive:
    def __init__(self):
        self.links = []
        self.parse_links()
        self.save_all()
        os.remove('connection_errors.txt')

    # This will parse all the links with connection errors
    def parse_links(self)->None:
        with open('connection_errors.txt') as f:
            self.links = f.readlines()
            self.links = [link.replace("\n","") for link in self.links]

    # This method will save all the links on the wayback machine
    def save_all(self)->None:
        for link in self.links:
            print(f'saving {link}')
            self.save(link)
            time.sleep(30)

    # This method will save a given website link on the wayback machine
    def save(self, site: str) -> None:
        count = 1
        try:
            requests.get("https://web.archive.org/save/" + site)
        except requests.exceptions.ConnectionError:
            print('connection error')

            # initiates a longer break
            time.sleep(120)
            while True:
                if count == 3:
                    break
                try:
                    requests.get("https://web.archive.org/save/" + site)
                    break
                except ConnectionError:
                    time.sleep(120)
                    count += 1




if __name__ == "__main__":
    wa = WaybackArchive()