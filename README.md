=======================
Core Craft REST API 
=======================
:Info: See `Core Craft site <https://github.com/Core-Craft/backend/>`_ for the latest source.
:Documentation: Available at `ChatGPT <https://github.com/Core-Craft/backend/README.md>`_
:Author: Amit Das


About
=====
This code provides an API endpoint that generates text based on prompts given by users, using the pre-trained GPT2 language model from the transformers library.


Getting started
===============
* Fork this repository (Click the Fork button in the top right of this page, click your Profile Image)
* Clone your fork down to your local machine

```markdown
git clone https://github.com/Core-Craft/backend.git
```

* Create a branch

```markdown
git checkout -b branch-name
```

* Make your changes (choose from any task below)
* Commit and push

```markdown
git add .
git commit -m 'Commit message'
git push origin branch-name
```

* Create a new pull request from your forked repository (Click the `New Pull Request` button located at the top of your repo)
* Wait for your PR review and merge approval!
* __Star this repository__ if you had fun!


Installation
============
You can install the dependencies using the following command:

.. code-block:: bash

    pip install -r requirements/dev.txt

.. end-code-block


Usage
=====
To start the server, simply run the following command:

.. code-block:: bash

    uvicorn app.main:app --reload

.. end-code-block

This will start the server on http://localhost:8000.


Endpoint
========
http://localhost:8000/docs


Example Request
===============
.. code-block:: http

    POST /generate HTTP/1.1
    Host: localhost:8000
    Content-Type: application/json

    {
        "prompt": "The quick brown fox"
    }


Example Response
================
.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: text/plain

    jumps over the lazy dog.


References
==========
- `FastAPI <https://fastapi.tiangolo.com/>`_
- `Uvicorn <https://www.uvicorn.org/>`_
- `Pydantic <https://pydantic-docs.helpmanual.io/>`_
- `Transformers <https://huggingface.co/transformers/>`_
