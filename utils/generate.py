#!/usr/bin/env python3
#-*- coding:utf -8-*-

import aiohttp, random, regex

from utils.utils import detect_repeating_text
from config import Config


async def gpt3(
    prompt: str, 
    API_KEY: str = Config.OPENAI_KEY, 
    model: str = 'text-davinci-003', 
    tokens: int = 256, 
    temperature: float = 0.7
    ):
    """
    Generate text using OpenAI GPT-3

    :param prompt: Prompt
    :param API_KEY: OpenAI API key
    :param model: OpenAI model
    :param tokens: Number of tokens
    :param temperature: Temperature
    :return: Generated text
    """

    try:
        retys = 10
        counter = 0
        headers = {
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
            }

        json = {
            "prompt": prompt, 
            "temperature": temperature,
            "max_tokens": tokens
        }
        url = f"https://api.openai.com/v1/engines/{model}/completions"

        while counter <= retys:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=json) as response:
                    r = await response.json()

            result = r['choices'][0]['text']
            if not detect_repeating_text(result):
                return result
            else:
                print('O artigo gerado não é coeso, tentando novamente')
                counter+=1
                continue

        print('\nNão foi possível gerar um texto coeso e sem repetições\n')

    except Exception as e:
        print('Erro ao enviar o prompt para o GPT-3', e)

    return None


async def generate_article(theme = None):
    """
    Generate theme and article using GPT-3

    :param theme: Article theme
    :return: Article title and content
    """
    
    try:
        if theme is None:
            themes = await gpt3(f'Cite {random.randint(2, 5)} ideias de tópicos aleatórios e reais para títulos de artigos relacionados à programação (com um emoji no título), como: dicas, ensinamentos e curiosidades sobre programação e tecnologia\n', tokens=random.randint(256, 512), temperature=0.9)
            themes = regex.sub(r'\d+\.?\s?\d*\s?\-?\s?\d*\s?\:?\s?', '', themes).strip()
            themes = themes.replace('\n\n', '\n').split('\n')
            theme = random.choice(themes).strip()

        content = await gpt3(f'Faça um artigo de caráter técnico, criativo e descontraído, com conteúdo verdadeiro e de valor, com introdução e bem formatado em markdown (sem o título h1) relacionado ao tema: "{theme}". Lembre-se de usar h2 caso haja um subtítulo, emojis e também código, links e exemplos, caso isso seja necessário no artigo. O artigo é voltado para um forum de programação chamado: TabNews, lembre-se de os cumprimentar na introdução do artigo (de forma criativa)!\n', tokens=3800, temperature=0.7)
        if content is not None:
            content = content.replace(theme, '').strip()

        return theme, content

    except Exception as e:
        print('Erro ao gerar artigo', e)

    return None, None

