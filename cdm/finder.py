import os
import requests

from bs4 import BeautifulSoup
from typing import List

from .manga import Manga
from .exeptions import MangaListEmpty, MangaNotFound


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Finder(object):
    def __init__(self) -> None:
        self.__mangas: List[Manga] = []
        self.__base_url = 'http://centraldemangas.online/titulos/filtro/*/p/'
        self.__total_pages: int = 0

    @property
    def mangas(self) -> List[Manga]:
        return self.__mangas.copy()

    def _get_manga_list_from_file(self) -> List[Manga]:
        """Get the mangas list of the file manga_list.txt

        Returns:
            List[Manga] -- The list with the mangas available in the file
        """
        manga_list: List[Manga] = []

        with open(os.path.join(BASE_DIR, 'manga_list.txt'), 'r') as file:
            for line in file.readlines():
                title, link = line.strip().split('|')
                manga = Manga(title, link)
                manga_list.append(manga)
        return manga_list

    def _get_number_of_pages(self) -> None:
        """Make a request to CDM website and get the total pages in the pagination manga list"""
        response = requests.get(f'{self.__base_url}1')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.__total_pages = int(
            soup.find_all(
                'a', class_='ui circular mini icon basic button')[-1].text
        )

    def _get_manga_list_from_cdm(self) -> List[Manga]:
        """Get all the mangas by make requests in each page of the manga list CDM website

        Returns:
            List[Manga] -- The list with the mangas available in the CDM website
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
        return manga_list

    def populate(self) -> None:
        """Populate the mangas attribute with de mangas available in the file manga_list.txt if the file exists, otherwise call the update method
        """
        try:
            self.__mangas = self._get_manga_list_from_file()
        except:
            self.update()

    def update(self) -> None:
        """Create the file manga_list.txt with the mangas available in the CDM website and update the mangas attribute
        """
        manga_list = self._get_manga_list_from_cdm()

        with open(os.path.join(BASE_DIR, 'manga_list.txt'), 'w') as file:
            for manga in manga_list:
                file.write(
                    f'{manga.title}|{manga.link[29:]}\n'
                )
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
