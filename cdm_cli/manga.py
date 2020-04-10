import requests

from bs4 import BeautifulSoup
from typing import List

from .chapter import Chapter
from .exeptions import ChapterListEmpty, ChapterNotFound


class Manga(object):
    def __init__(self, title: str, link: str) -> None:
        self.__title: str = title
        self.__link: str = f'http://centraldemangas.online{link}'
        self.__chapters: List[Chapter] = []

    @property
    def title(self) -> str:
        return self.__title

    @property
    def link(self) -> str:
        return self.__link

    @property
    def chapters(self) -> List[Chapter]:
        return self.__chapters.copy()

    def __str__(self) -> str:
        return f'{self.__title} - {self.__link}'

    def __repr__(self) -> str:
        return self.__title

    def populate(self):
        """Populate the chapters attribute by make a request in the manga page detail in CDM website
        """
        response = requests.get(self.__link)
        soup = BeautifulSoup(response.content, 'html.parser')
        chapters = soup.select('td a')
        self.__chapters = [
            Chapter(chapter.get_text().strip(), chapter.get('href')) for
            chapter in chapters
        ]
        self.__chapters.reverse()

    def search(self, title: str) -> Chapter:
        """Performs a search in the manga list based in the title passed to the function

        Arguments:
            title {str} -- The title of the chapter you looking for

        Raises:
            ChapterNotFound: If the title is not found in the manga list the ChapterNotFound error is raised
            ChapterListEmpty: If the manga list is empty the ChapterListEmpty error is raised, you probably not run the populate method

        Returns:
            Chapter -- If the title is found the method will return the respective Chapter object
        """
        if self.__chapters:
            for chapter in self.__chapters:
                if chapter.title.lower() == title.lower():
                    return chapter
            raise ChapterNotFound('Capítulo não encontrado')
        else:
            raise ChapterListEmpty('A lista de capítulos está vazia')
