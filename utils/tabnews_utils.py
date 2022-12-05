#!/usr/bin/env python3
#-*- coding:utf -8-*-

import aiohttp
from config import Config


HOST = Config.TABNEWS_HOST


async def get_tabnews_access_token(email = Config.TABNEWS_EMAIL, password = Config.TABNEWS_PASSWORD):
    """
    Get TabNews access token

    :param email: TabNews email
    :param password: TabNews password
    :return: TabNews access token
    """

    try:
        headers = {
            "Content-Type": "application/json"
            }

        json = {
            "email": email, 
            "password": password
        }
        url = f"{HOST}/api/v1/sessions"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as response:
                r = await response.json()
        return r['token']

    except Exception as e:
        print('Erro ao obter token de acesso do TabNews', e)

    return None


async def post_tabnews_article(title: str, content: str, reference = None):
    """
    Post TabNews article

    :param title: Article title
    :param content: Article content
    :param reference: Article reference
    :return: Article ID
    """

    try:
        session_id = await get_tabnews_access_token()
        url = f'{HOST}/api/v1/contents'
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"session_id={session_id}"
            }

        json = {
            "title": title,
            'body': content,
            'status': 'published'
        }

        if reference:
            json['source_url'] = reference

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as response:
                r = await response.json()
        return r['id']

    except Exception as e:
        print('Erro ao postar artigo no TabNews', e)

    return None


