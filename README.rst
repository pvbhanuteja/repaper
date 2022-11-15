=======
repaper
=======


.. image:: https://img.shields.io/pypi/v/repaper.svg
        :target: https://pypi.python.org/pypi/repaper

.. image:: https://img.shields.io/travis/pvbhanuteja/repaper.svg
        :target: https://travis-ci.com/pvbhanuteja/repaper

.. image:: https://readthedocs.org/projects/re-paper/badge/?version=latest
        :target: https://re-paper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pvbhanuteja/repaper/shield.svg
        :target: https://pyup.io/repos/github/pvbhanuteja/repaper/
        :alt: Updates

.. image:: https://pepy.tech/badge/repaper
        :target: https://pepy.tech/badge/repaper
        :alt: Downloads


Convert photo of a form to web based froms or editable pdf forms. 


* Free software: MIT license
* Documentation: https://re-paper.readthedocs.io.

============
Installation
============


Stable release
--------------

To install repaper, run this command in your terminal:

.. code-block:: console

    $ pip install repaper

This is the preferred method to install repaper, as it will always install the most recent stable release.

=====
Usage
=====


To use repaper in a project::

    from repaper import repaper


To generate a google form from the a form image::

    from repaper import repaper

    re_paper = repaper('../samples/test.jpg')

    form_id = re_paper.make_google_from('../secrets/credentials.json')

    print(f'''Form created with form id: {form_id["formId"]} and is accessible at: \n https://docs.google.com/forms/d/{form_id['formId']}/viewform \n
    edit and publish the form to make it accessible to others''')

Command line usage to generate google form from image::

    repaper google-form --img_path ./samples/test.jpg --oauth_json ./secrets/credentials.json


Development Lead
----------------

* Bhanu Pallakonda <pvbhanuteja@gmail.com>
* Gaurav Sood <gsood07@gmail.com>

Contributors
------------

None yet. Why not be the first?


Features
--------

* TODO

Credits
-------
Portions of this research were conducted with the advanced computing resources provided by `Texas A&M High Performance Research Computing`_.

.. _`Texas A&M High Performance Research Computing`: https://hprc.tamu.edu/research/citations.html

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
