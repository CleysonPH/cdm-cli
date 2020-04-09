from cdmdownloader.finder import Finder

if __name__ == "__main__":
    finder = Finder()

    print('Atualizando a lista de mangás disponíveis')
    finder.populate()

    search = input('Qual mangá deseja baixar? ')
    manga = finder.search(search)

    print('Atualizando a lista de cápitulos disponíveis')
    manga.populate()

    for chapter in manga.chapters:
        print(f'Baixando cápitulo {chapter.title}')
        chapter.populate()
        chapter.download(directory=manga.title)
