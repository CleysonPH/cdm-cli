import os
import re
import requests

from typing import List, Dict
from bs4 import BeautifulSoup

from .page import Page
from .exeptions import PagesListEmpty


class Chapter(object):
    def __init__(self, title: str, link: str) -> None:
        self.__title: str = title
        self.__link: str = f'http://centraldemangas.online{link.replace("ler-online", "ler-online-completo")}'
        self.__pages: List[Page] = []
        self.__headers: Dict[str, str] = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': self.__link,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    @property
    def title(self) -> str:
        return self.__title

    @property
    def link(self) -> str:
        return self.__link

    @property
    def pages(self) -> List[Page]:
        return self.__pages.copy()

    def __str__(self) -> str:
        return f'{self.__title} - {self.__link}'

    def __repr__(self) -> str:
        return f'{self.__title} - {self.__link}'

    def _generate_page_link(self, url_sulfix: str, page_id: str) -> str:
        """Generate the link for one page of the chapter

        Arguments:
            url_sulfix {str} -- The url_sulfix, is get in the page chapter
            page_id {str} -- The id attribute of the page img tag

        Returns:
            str -- Returns the link of the page for make the download
        """
        page_number = page_id.split('_')[-1]
        page_link = f'{url_sulfix}{page_number}.jpg'
        return page_link

    def populate(self) -> None:
        """Populate the pages attribute by make a request in the chapter page detail in CDM website
        """
        response = requests.get(self.__link)
        soup = BeautifulSoup(response.content, 'html.parser')
        url_sulfix = soup.find_all('script')[-1].string.strip().split(
            '\n')[3].strip().split()[-1].replace("'", "").replace(";", "")
        pages = soup.find_all('img', id=re.compile(r'^pag_\d+'))
        self.__pages = [
            Page(page.get('alt'), self._generate_page_link(url_sulfix, page.get('id'))) for
            page in pages
        ]

    def download(self, directory: str) -> None:
        """Download all pages of the chapter in a directory with the title of the chapter

        Keyword Arguments:
            directory {str} -- The name of the directory with will holds the chapter directory

        Raises:
            PagesListEmpty: If the page list is empty the PageListEmpty error is raised, you probably not run the populate method
        """
        if self.__pages:
            dir_path = os.path.join('Mangas', directory, self.__title)
            os.makedirs(dir_path, exist_ok=True)

            for page in self.__pages:
                response = requests.get(page.link, headers=self.__headers)
                file_name = f'{page.title}.jpg'
                file_path = os.path.join(dir_path, file_name)

                with open(file_path, 'wb') as file:
                    file.write(response.content)
        else:
            raise PagesListEmpty('A lista de páginas está vazia')
