class Page(object):
    def __init__(self, title: str, link: str) -> None:
        self.__title: str = title
        self.__link: str = link

    @property
    def title(self) -> str:
        return self.__title

    @property
    def link(self) -> str:
        return self.__link

    def __str__(self) -> str:
        return f'{self.__title} - {self.__link}'

    def __repr__(self) -> str:
        return f'{self.__title} - {self.__link}'
