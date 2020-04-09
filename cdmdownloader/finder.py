import requests
import requests_cache

from bs4 import BeautifulSoup
from typing import List

from cdmdownloader.manga import Manga
from cdmdownloader.exeptions import MangaListEmpty, MangaNotFound

requests_cache.install_cache('cache')


class Finder(object):
    def __init__(self) -> None:
        self.__mangas: List[Manga] = []
        self.__base_url = 'http://centraldemangas.online/titulos/filtro/*/p/'
        self.__total_pages: int = 0

    @property
    def mangas(self) -> List[Manga]:
        return self.__mangas.copy()

    def _get_number_of_pages(self) -> None:
        """Make a request to CDM website and get the total pages in the pagination manga list"""
        response = requests.get(f'{self.__base_url}1')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.__total_pages = int(
            soup.find_all(
                'a', class_='ui circular mini icon basic button')[-1].text
        )

    def populate(self) -> None:
        """Populate the mangas attribute by make requests in each page of the manga list CDM website
        """
        self._get_number_of_pages()
        manga_list: List[Manga] = []
        for current_page in range(1, self.__total_pages + 1):
            response = requests.get(f'{self.__base_url}{current_page}')
            soup = BeautifulSoup(response.content, 'html.parser')
            mangas = soup.select('.content .header a')
            manga_list += [
                Manga(manga.text.strip(), manga.get('href')) for
                manga in mangas
            ]
        self.__mangas = manga_list

    def search(self, title: str) -> Manga:
        """Performs a search in the manga list based in the title passed to the function

        Arguments:
            title {str} -- The title of the manga you looking for

        Raises:
            MangaNotFound: If the title is not found in the manga list the MangaNotFound error is raised
            MangaListEmpty: If the manga list is empty the MangaListEmpty error is raised, you probably not run the populate method

        Returns:
            Manga -- If the title is found the method will return the respective Manga object
        """
        if self.__mangas:
            for manga in self.__mangas:
                if manga.title.lower() == title.lower():
                    return manga
            raise MangaNotFound('Mangá não encontrado')
        else:
            raise MangaListEmpty('A lista de mangás está vazia')
