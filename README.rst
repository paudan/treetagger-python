treetagger-python
=================

A Python module for interfacing with the TreeTagger by Helmut Schmid.

Copyright (C) 2016 Mirko Otto

For license information, see LICENSE.txt

Dependencies
------------

-  `TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
-  Python 2.7 or Python 3
-  `NLTK <http://nltk.org/>`__

Tested with Treetagger 3.2, Python 2.7/3.5 and NLTK 3.2.4

INSTALLATION
------------

Before you install the ``treetagger-python`` package please ensure you
have downloaded and installed the
`TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
itself.

The
`TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
is a copyrighted software by Helmut Schmid and
`IMS <http://www.ims.uni-stuttgart.de/>`__, please read the license
agreement before you download the TreeTagger package and language
models.

After the installation of the ``TreeTagger`` set the environment
variable ``TREETAGGER_HOME`` to the installation directory of the
``TreeTagger``.

::

    export TREETAGGER_HOME='/path/to/your/TreeTagger/cmd/'

Alternatively you can use ``path_to_home`` parameter in ``TreeTagger`` constructor and set file to the tagger file directly:

.. code:: python

    from treetagger import TreeTagger
    tt = TreeTagger(language='english', path_to_home='~/treetagger/cmd/tree-tagger-english')

Usage
-----

Tagging a sentence from Python:

.. code:: python

    from treetagger import TreeTagger
    tt = TreeTagger(language='english')
    tt.tag('What is the airspeed of an unladen swallow?')

The output is a list of (token, tag):

::

    [(u'What', u'WP'), (u'is', u'VBZ'), (u'the', u'DT'),
     (u'airspeed', u'NN'), (u'of', u'IN'), (u'an', u'DT'),
     (u'unladen', u'JJ'), (u'swallow', u'NN'), (u'?', u'SENT')]

Tagging a german sentence from Python:

.. code:: python

    from treetagger import TreeTagger
    tt = TreeTagger(language='german')
    tt.tag('Das Haus hat einen großen hübschen Garten.')

The output is a list of (token, tag):

::

    [(u'Das', u'ART'), (u'Haus', u'NN'), (u'hat', u'VAFIN'), (u'einen', u'ART'),
     (u'großen', u'ADJA'), (u'hübschen', u'ADJA'), (u'Garten', u'NN'), (u'.', u'$.')]


Chunking the same sentences from Python will produce such parse trees:

.. code:: python

    from treetagger import TreeTagger
    treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')
    tt = TreeTagger(language='english', path_to_home=treetagger_path)
    sentence = tt.tag('What is the airspeed of an unladen swallow?')
    cp = TreeTaggerChunker(language='english', path_to_home=treetagger_path)
    cp.parse(sentence)

The output is a parse tree:

::

    (ROOT
      (NC (What WP))
      (VC (is VBZ))
      (NC (the DT) (airspeed NN))
      (PC (of IN) (NC (an DT) (unladen JJ) (swallow NN))))


Similarly, the following example illustrates chunking for German language:

.. code:: python

    from treetagger import TreeTagger
    treetagger_path = os.path.join('/', 'usr', 'local', 'treetagger', 'cmd')
    tt = TreeTagger(language='german', path_to_home=treetagger_path)
    sentence = tt.tag('Das Haus hat einen großen hübschen Garten.')
    cp = TreeTaggerChunker(language='german', path_to_home=treetagger_path)
    cp.parse(sentence)

The output is a parse tree:

::

    (ROOT
      (NC (What WP))
      (VC (is VBZ))
      (NC (the DT) (airspeed NN))
      (PC (of IN) (NC (an DT) (unladen JJ) (swallow NN))))
    .(ROOT
      (NC (Das ART) (Haus NN))
      (VC (hat VAFIN))
      (NC (einen ART) (grossen ADJA) (hubschen ADJA) (Garten NN))
      (. $.))
