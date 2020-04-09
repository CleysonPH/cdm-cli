import click

from cdmdownloader.finder import Finder
from cdmdownloader.exeptions import ChapterNotFound, MangaNotFound


@click.command()
@click.option('--manga', required=True, prompt='Manga title', help='Title of the manga you want to download')
@click.option('--chapter', help='Title of the chapter you want to download')
@click.option('--all', is_flag=True, help='Download all the chapters')
@click.option('--last', is_flag=True, help='Download the last chapter')
def cli(manga: str, chapter: str, all: bool, last: bool):
    finder = Finder()

    click.echo('Updating the available mangas')
    finder.populate()

    try:
        manga_obj = finder.search(title=manga)
        manga_obj.populate()

        if all:
            for chapter_obj in manga_obj.chapters:
                click.echo(
                    f'Downloading the chapter {chapter_obj.title} of {manga_obj.title}'
                )
                chapter_obj.populate()
                chapter_obj.download(manga_obj.title)
        elif last:
            chapter_obj = manga_obj.chapters[-1]
            chapter_obj.populate()
            click.echo(
                f'Downloading the chapter {chapter_obj.title} of {manga_obj.title}'
            )
            chapter_obj.download(manga_obj.title)
        else:
            if not chapter:
                click.echo('Available chapters')
                for chapter_obj in manga_obj.chapters:
                    click.echo(chapter_obj.title, nl=True)

                chapter = click.prompt('Chapter title: ')

            chapter_obj = manga_obj.search(chapter)
            click.echo(
                f'Downloading the chapter {chapter_obj.title} of {manga_obj.title}'
            )
            chapter_obj.populate()
            chapter_obj.download(manga_obj.title)
    except MangaNotFound:
        click.echo('Manga not found')
    except ChapterNotFound:
        click.echo('Chapter not found')


if __name__ == "__main__":
    cli()
