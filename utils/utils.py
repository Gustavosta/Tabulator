#!/usr/bin/env python3
#-*- coding:utf -8-*-

import re


def detect_repeating_text(text: str):
    """
    Function to detect duplicate phrases or words in text, as text AIs 
    often repeat text depending on prompt and token limit.

    :param text: Text to be analyzed
    :return: True if text has duplicate phrases or words, False otherwise
    """

    match = re.search(r'(\w+)(\s+\1)+', text)
    return False if match else True


