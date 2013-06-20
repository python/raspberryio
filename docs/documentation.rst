.. _documentation:

Write documentation
-------------------

We believe Raspberry IO needs to have documentation as good as our
code. It's what you're reading now and is generally the first point of
contact for new developers. We value great, well-written documentation
and aim to improve it as often as possible. And we're always looking
for help with documentation!

Getting the raw documentation
*****************************

The official documentation is available on `Read the Docs`_. This is
the compiled HTML version. However, we edit it as a collection of text
files for maximum flexibility. These files live in the top-level
``docs/`` directory of a Raspberry IO release. If you'd like to start
contributing to our docs, get the code from our Github repository (see
:ref:`getcode`).

Using Sphinx
************

Before building the documentation, you must have downloaded the
Raspberry IO source code. See the :ref:`getcode` section for
instructions on installing Raspberry IO locally.

We use the Sphinx__ documentation system (based on docutils__). To
build the documentation locally, you'll need to install Sphinx.

.. code-block:: console

    $ pip install Sphinx

Then, building the HTML is easy. Just run make from the ``docs`` directory.

.. code-block:: console

    $ cd raspberryio/docs
    $ make html

(or ``make.bat html`` on Windows)

The compiled HTML code will be in ``raspberryio/docs/_build/``.

To get started contributing, you'll want to read the `reStructuredText
Primer`_. After that, you'll want to read about the `Sphinx-specific markup`_
that's used to manage metadata, indexing, and cross-references.

Documentation starting points
*****************************

Typically, documentation changes come in two forms:

* **General improvements:** typo corrections, error fixes and better
  explanations through clearer writing and more examples.

* **New features:** documentation of features that have been added to the
  framework since the last release.

If you're interested in helping out, a good starting point is with the
`documentation label`_ on the GitHub issue tracker.

__ http://sphinx.pocoo.org/
__ http://docutils.sourceforge.net/

.. _Read the Docs: http://raspberryio.readthedocs.org/
.. _documentation label: https://github.com/caktus/raspberryio/issues?labels=documentation&page=1&state=open
.. _reStructuredText Primer: http://sphinx.pocoo.org/rest.html#rst-primer
.. _Sphinx-specific markup: http://sphinx.pocoo.org/markup/index.html#sphinxmarkup
