from utils.tabnews_utils import post_tabnews_article
from utils.generate import generate_article
import asyncio


async def main():
    """
    Main funcion to generate and post articles

    Note: This project is not finished yet and is still under construction!
    """

    article = await generate_article()
    if article[0] is not None and article[1] is not None:
        print('Título do artigo:', article[0])
        print('\nConteúdo do artigo:\n\n', article[1])
        await post_tabnews_article(article[0], article[1])
        print('\nArtigo postado com sucesso no TabNews!')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
