from cdmdownloader.finder import Finder

if __name__ == "__main__":
    finder = Finder()

    print('Atualizando a lista de mangás disponíveis')
    finder.populate()

    manga_title = input('Qual mangá deseja baixar? ')
    manga = finder.search(manga_title)

    print('Atualizando a lista de cápitulos disponíveis')
    manga.populate()

    chapter_title = input('Qual capítulo deseja baixar? ')
    chapter = manga.search(chapter_title)

    print(f'Baixando o capítulo {chapter.title} de {manga.title}')
    chapter.populate()
    chapter.download(manga.title)
