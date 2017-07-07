# -*- coding: utf-8 -*-
# Natural Language Toolkit: Interface to the TreeTagger POS-tagger
#
# Copyright (C) Paulius Danenas
# Author: Paulius Danenas <danpaulius@gmail.com>, based on code by Mirko Otto

"""
A Python module for NLTK interfacing with the Treetagger by Helmut Schmid.
"""

import os
import sys
import re
from subprocess import Popen, PIPE

from nltk.internals import find_binary
from nltk.tag.api import TaggerI
from nltk.chunk.api import ChunkParserI
from nltk.tree import Tree, ParentedTree

_treetagger_url = 'http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/'

_treetagger_languages = ['bulgarian', 'dutch', 'english', 'estonian', 'finnish', 'french', 'galician', 'german',
                         'italian', 'polish', 'russian', 'slovak', 'slovak2', 'spanish']

class TreeTagger(TaggerI):
    r"""
    A class for POS tagging with TreeTagger. The inputs are the paths to:
     - language (the source language used for training on training data)
     - (optionally) the path to the TreeTagger binary
     - (optionally) path to the TreeTagger file with abbreviations of tags for particular language

    This class communicates with the TreeTagger binary via pipes.

    Example:

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')
        >>> tt = TreeTagger(language='english', path_to_home=treetagger_path)
        >>> tt.tag('What is the airspeed of an unladen swallow ?')
        [(u'What', u'WP'), (u'is', u'VBZ'), (u'the', u'DT'),
         (u'airspeed', u'NN'), (u'of', u'IN'), (u'an', u'DT'),
         (u'unladen', u'JJ'), (u'swallow', u'NN'), (u'?', u'SENT')]


    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')
        >>> tt = TreeTagger(language='german', path_to_home=treetagger_path)
        >>> tt.tag('Das Haus hat einen großen hübschen Garten.')
        [(u'Das', u'ART'), (u'Haus', u'NN'), (u'hat', u'VAFIN'), (u'einen', u'ART'),
         (u'großen', u'ADJA'), (u'hübschen', u'ADJA'), (u'Garten', u'NN'), (u'.', u'$.')]

    """

    def __init__(self, path_to_home=None, language='english',
                 verbose=False, abbreviation_list=None):
        """
        Initialize the TreeTagger POS tagger.

        :param path_to_home: The directory of the TreeTagger binary (cmd subdirectory).
        :param language: Default language is german.
        :param abbreviation_list: Path to abbreviation list file

        """
        treetagger_paths = ['.', '/usr/bin', '/usr/local/bin', '/opt/local/bin',
                            '/usr/local/treetagger/cmd', '~/treetagger/cmd']
        treetagger_paths = list(map(os.path.expanduser, treetagger_paths))
        self._abbr_list = abbreviation_list

        if language in _treetagger_languages:
            if sys.platform.startswith("win"):
                treetagger_bin_name = 'tag-' + language
            else:
                treetagger_bin_name = 'tree-tagger-' + language
        else:
            raise LookupError('Language not in language list!')

        try:
            self._treetagger_bin = find_binary(
                treetagger_bin_name, os.path.join(path_to_home, treetagger_bin_name),
                env_vars=('TREETAGGER', 'TREETAGGER_HOME'),
                searchpath=treetagger_paths,
                url=_treetagger_url,
                verbose=verbose)
        except LookupError:
            print('NLTK was unable to find the TreeTagger bin!')
        if abbreviation_list is not None and \
                not (os.path.exists(abbreviation_list) and os.path.isfile(abbreviation_list)):
            self._abbr_list = None


    def tag(self, sentences):
        """Tags a single sentence: a list of words.
        The tokens should not contain any newline characters.
        """

        # Write the actual sentences to the temporary input file
        if isinstance(sentences, list):
            _input = '\n'.join((x for x in sentences))
        else:
            _input = sentences

        # Run the tagger and get the output
        if(self._abbr_list is None):
            p = Popen([self._treetagger_bin], 
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        elif(self._abbr_list is not None):
            p = Popen([self._treetagger_bin,"-a",self._abbr_list], 
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        if sys.version_info >= (3,):
            (stdout, stderr) = p.communicate(bytes(_input, 'UTF-8'))
            treetagger_output = stdout.decode('utf-8')
        else:
            (stdout, stderr) = p.communicate(_input)
            treetagger_output = stdout

        # Check the return code.
        if p.returncode != 0:
            print(stderr)
            raise OSError('TreeTagger command failed!')

        # Output the tagged sentences
        tagged_sentences = []
        for tagged_word in treetagger_output.strip().split('\n'):
            words = tagged_word.split('\t')
            tagged_sentences.append(('_'.join(words[:-2]), words[-2]))
        return tagged_sentences



class TreeTaggerChunker(ChunkParserI):
    r"""
     A class for text chunking with TreeTagger. The inputs are the paths to:
     - language (the source language used for training on training data)
     - (optionally) the path to the TreeTagger binary
     - (optionally) path to the TreeTagger file with abbreviations of tags for particular language

    This class communicates with the TreeTagger binary via pipes.

    Example:

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')
        >>> tt = TreeTagger(language='english', path_to_home=treetagger_path)
        >>> sentence = tt.tag('What is the airspeed of an unladen swallow ?')
        >>> cp = TreeTaggerChunker(language='english', path_to_home=treetagger_path)
        >>> cp.parse(sentence)
        (ROOT
          (NC (What WP))
          (VC (is VBZ))
          (NC (the DT) (airspeed NN))
          (PC (of IN) (NC (an DT) (unladen JJ) (swallow NN))))
        .

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')
        >>> tt = TreeTagger(language='german', path_to_home=treetagger_path)
        >>> tt.tag('Das Haus hat einen großen hübschen Garten.')
        >>> cp = TreeTaggerChunker(language='german', path_to_home=treetagger_path)
        >>> cp.parse(sentence)
        [(u'Das', u'ART'), (u'Haus', u'NN'), (u'hat', u'VAFIN'), (u'einen', u'ART'),
         (u'großen', u'ADJA'), (u'hübschen', u'ADJA'), (u'Garten', u'NN'), (u'.', u'$.')]

    """

    def __init__(self, path_to_home=None, language='english',
                 verbose=False, abbreviation_list=None):

        treetagger_paths = ['.', '/usr/bin', '/usr/local/bin', '/opt/local/bin',
                            '/usr/local/treetagger/cmd', '~/treetagger/cmd']
        treetagger_paths = list(map(os.path.expanduser, treetagger_paths))
        self._abbr_list = abbreviation_list

        if language in _treetagger_languages:
            if sys.platform.startswith("win"):
                treetagger_bin_name = 'chunk-' + language
            else:
                treetagger_bin_name = 'tagger-chunker-' + language
        else:
            raise LookupError('Language not in language list!')

        try:
            self._treetagger_bin = find_binary(
                treetagger_bin_name, os.path.join(path_to_home, treetagger_bin_name),
                env_vars=('TREETAGGER', 'TREETAGGER_HOME'),
                searchpath=treetagger_paths,
                url=_treetagger_url,
                verbose=verbose)
        except LookupError:
            print('NLTK was unable to find the TreeTagger bin!')
        if abbreviation_list is not None and \
                not (os.path.exists(abbreviation_list) and os.path.isfile(abbreviation_list)):
            self._abbr_list = None


    def parse(self, tokens):
        # TreeTagger takes only text for input, therefore, tokens must be combined to source text again
        _input = ' '.join([token[0] for token in tokens])

        if(self._abbr_list is None):
            p = Popen([self._treetagger_bin],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        elif(self._abbr_list is not None):
            p = Popen([self._treetagger_bin,"-a",self._abbr_list],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        if sys.version_info >= (3,):
            (stdout, stderr) = p.communicate(bytes(_input, 'UTF-8'))
            treetagger_output = stdout.decode('utf-8')
        else:
            (stdout, stderr) = p.communicate(_input)
            treetagger_output = stdout

        # Check the return code.
        if p.returncode != 0:
            raise OSError('TreeTagger chunker command failed!')

        parse_tree = ''
        for tagged_word in treetagger_output.strip().split('\n'):
            pattern = re.compile(r'<\s*[A-Z]+\s*>')
            match = re.match(pattern, tagged_word)
            if match:
                parse_tree += "(" + match.group(0).lstrip('< ').rstrip('> ')
            elif re.match(r'<\s*/*\s*[A-Z]+\s*>', tagged_word):
                parse_tree += ")"
            elif re.match(r'\?\s*SENT\s*\?', tagged_word):
                continue
            else:
                words = tagged_word.split('\t')
                _str = '_'.join(words[:-2])
                parse_tree += ' ({} {}) '.format(_str, words[-2])
        parse_tree = "(S {} )".format(parse_tree)
        # Transform into compatible parse tree string
        try:
            if sys.version_info < (3,):
                parse_tree = parse_tree.decode('utf-8')
            parse = Tree.fromstring(parse_tree)
            parse = self.__get_nltk_parse_tree__(parse)
        except Exception:
            parse = None
        finally:
            return parse


    def __get_nltk_parse_tree__(self, tree):

        def create_tree(tree):
            nodes = []
            for n in tree:
                subtrees = [subtree for subtree in n.subtrees(filter=lambda k: k != n)]
                if len(subtrees) > 0:
                    subnodes = create_tree(n)
                    nodes.append(ParentedTree(n.label(), subnodes))
                else:
                    parent_label = n.parent().label() if n.parent() is not None \
                                                         and n.parent().label() not in ['S', 'ROOT'] else None
                    nodes.append(ParentedTree(parent_label, [(n[0], n.label())]))
            return nodes

        def move_up(tree):
            for n in tree:
                if isinstance(n, Tree):
                    subtrees = [subtree for subtree in n.subtrees(filter=lambda k: k != n)]
                    for subtree in subtrees:
                        if subtree.label() == n.label():
                            tmp = subtree
                            parent = subtree.parent()
                            parent.remove(tmp)
                            subsub = [s for s in subtree.subtrees(filter=lambda k: k != subtree)]
                            if len(subsub) == 0:
                                n.extend(tmp.leaves())
                            else:
                                move_up(subtree)
            return tree

        tree = ParentedTree.convert(tree)
        new_tree = ParentedTree('S', create_tree(tree))
        return move_up(new_tree)



if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
