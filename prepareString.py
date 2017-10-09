# -*- coding: utf-8 -*-
import nltk

def PrepareString (message):
    """Prepares a concatenated string of lower case characters from a custom text"""
    raw = message
    Words = nltk.word_tokenize(raw)
    Words = [word.lower() for word in Words if word.isalpha()]
    return "".join(Words)