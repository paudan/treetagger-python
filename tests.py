# -*- coding: utf-8 -*-
import os
from treetagger import TreeTagger, TreeTaggerChunker

treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')

def test_tagging():
    def test_language(language, phrase):
        tt = TreeTagger(language=language, path_to_home=treetagger_path)
        return tt.tag(phrase)

    en_tags = test_language('english', 'What is the airspeed of an unladen swallow?')
    print(en_tags)
    assert en_tags[1][0] == 'is'
    assert en_tags[1][1] == 'VBZ'
    de_tags = test_language('german', 'Das Haus hat einen großen hübschen Garten.')
    print(de_tags)
    assert de_tags[0][0] == 'Das'
    assert de_tags[0][1] == 'ART'


def test_chunking():
    language='english'
    tt = TreeTagger(language=language, path_to_home=treetagger_path)
    phrase = 'What is the airspeed of an unladen swallow?'
    sentence = tt.tag(phrase)
    cp = TreeTaggerChunker(language=language, path_to_home=treetagger_path)
    print(cp.parse(sentence))


def test_chunking_de():
    language='german'
    tt = TreeTagger(language=language, path_to_home=treetagger_path)
    phrase = 'Das Haus hat einen großen hübschen Garten.'
    sentence = tt.tag(phrase)
    cp = TreeTaggerChunker(language=language, path_to_home=treetagger_path)
    print(cp.parse(sentence))