import click
import time

from typing import List

from .finder import Finder, Manga
from .exeptions import ChapterNotFound, MangaNotFound


@click.group()
def cli():
    pass


@click.argument('manga')
@click.option('--chapter', help='Title of the chapter you want to download')
@click.option('--all', is_flag=True, help='Download all the chapters')
@click.option('--last', is_flag=True, help='Download the last chapter')
@cli.command()
def download(manga: str, chapter: str, all: bool, last: bool):
    finder = Finder()

    click.echo('Getting the available mangas')
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


@cli.command()
def update():
    finder = Finder()
    finder.populate()
    before_update = len(finder.mangas)

    click.echo('Updating the manga list by the CDM website')
    finder.update()

    after_update = len(finder.mangas)

    click.echo(
        f'Update complete, found {after_update - before_update} new manga(s)'
    )


@cli.command()
def show():
    finder = Finder()

    click.echo('Getting the available mangas')
    finder.populate()

    click.echo(f'List of available mangas, total: {len(finder.mangas)}')
    time.sleep(1)
    for manga in finder.mangas:
        click.echo(manga)


@cli.command()
@click.argument('manga')
def search(manga):
    finder = Finder()
    finder.populate()

    results: List[Manga] = []

    for m in finder.mangas:
        if manga.lower() in m.title.lower():
            results.append(m)

    click.echo(f'Found {len(results)} result(s)')
    for m in results:
        click.echo(m)


if __name__ == "__main__":
    cli()
