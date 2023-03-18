.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/usdc_depeg.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/usdc_depeg
    .. image:: https://readthedocs.org/projects/usdc_depeg/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://usdc_depeg.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/usdc_depeg/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/usdc_depeg
    .. image:: https://img.shields.io/pypi/v/usdc_depeg.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/usdc_depeg/
    .. image:: https://img.shields.io/conda/vn/conda-forge/usdc_depeg.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/usdc_depeg
    .. image:: https://pepy.tech/badge/usdc_depeg/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/usdc_depeg
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/usdc_depeg

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

==========
Subgraph Query Portal
==========

This library is a collection of reusable public goods Subgraph queriess to obtain cross-chain data for researchers and tool builders powered by `Messari Subgraph Endpoints <https://subgraphs.messari.io/>`__, 


Tools
==========
This project utilizes Subgraph endpoints from `Messari <https://messari.io/report/the-graph-foundation-awards-messari-usd12-5mm-in-first-ever-core-subgraph-developer-grant-to-build-and-standardize-subgraphs>`__ 
and `Subgrounds <https://docs.playgrounds.network/>`__, an open-source Python library built by `Playgrounds <https://playgrounds.network/>`__. 
Data is transformed using `Polars <https://github.com/pola-rs/polars>`__.

Subgraphs
---------
Subgraphs are custom APIs built on indexed blockchain data that can be queried using GraphQL endpoints. A list of Messari Endpoints can be found `here https://subgraphs.messari.io`__.

Subgrounds
----------
Subgrounds is an open-source Python library for interfacing with and querying Subgraphs. 
It simplifies the process of extracting and processing data from various blockchains.

Polars
------
Polars is a blazingly fast DataFrames library implemented in Rust using Apache Arrow Columnar Format as the memory model.

Library Requirements
============
* Python 3.10 or higher
* Subgrounds
* Polars
* Pyarrow


Installation
============

1. Install virtualenv:

   .. code:: bash

      python -m venv .venv
      source .venv/bin/activate

2. Install from github source:

   .. code:: bash

      pip install git+https://github.com/Evan-Kim2028/subgraph-query-portal.git


Run a dex query test
====================
1. Run the following command from the root directory of the project:

   .. code:: bash

      python -m subgraph_query_portal.tests.test_dex_query


Making Changes to Source Code
=============================
1. Enable editable mode. Instructs pip to install the package in a way that allows you to make changes to the package's source code and have those changes take effect immediately

   .. code:: bash

      pip install -e .
