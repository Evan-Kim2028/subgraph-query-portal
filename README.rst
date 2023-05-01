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

=====================
Subgraph Query Portal
=====================

:literal:`queryportal` a curated collection of Subgraph query public goods and tools to obtain cross-chain data for both analysts and subgraph developers. 
Similar to SQL views, :literal:`queryportal` queries are curated snapshots of data that can be composed with other queries.


Tools
==========
This project utilizes Subgraph endpoints from `Messari <https://messari.io/report/the-graph-foundation-awards-messari-usd12-5mm-in-first-ever-core-subgraph-developer-grant-to-build-and-standardize-subgraphs>`__ 
and `Subgrounds <https://github.com/0xPlaygrounds/subgrounds>`__, an open-source Python library built by `Playgrounds <https://playgrounds.network/>`__. 
Data is transformed using `Polars <https://github.com/pola-rs/polars>`__.

Subgraphs
---------
Subgraphs are custom APIs built on indexed blockchain data that can be queried using GraphQL endpoints. For a list of standardized subgraph endpoints by Messari, see `here <https://subgraphs.messari.io>`__.

Subgrounds
----------
Subgrounds is a Pythonic data access library that represents Subgraph schemas as Python objects, allowing Subgraph GraphQL queries to be written exclusively in Python. Subgrounds leverages functional programming design patterns to express 
subgraphs as. This allows users to integrate Subgraphs into functional programming python data pipelines in Python. 

Polars
------
Polars is a blazingly fast DataFrames library implemented in Rust using Apache Arrow Columnar Format as the memory model.

Library Dependencies
============
* Python >= 3.10
* Subgrounds = 1.2.0
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


Examples
========================
Run the following commands from the root directory of the project.

1. Query all CoW Trades data
    
   .. code:: bash

      python tests/test_cow.py

2. Query all Univ3 Swap data:

   .. code:: bash

      python examples/test_dex_swaps_and_tokens.py



Import Package
========================
If you want to use this package in your own project, you can import as follows:

   .. code:: bash

      import queryportal


Local Development
=============================
To enable editable mode, use the pip install -e . command. 
This installs the package in a way that allows you to modify the source code and have the changes take effect immediately. 
However, be cautious when editing the source files, especially if you have also installed the package from GitHub. 
This may result in conflicting versions of the package.

   .. code:: bash

      pip install -e .


For Developers
========================
Queryinterface is an abstract class that defines the interface for all subgraph queries via the :literal:`query()` method.

Some reasons why a developer would want to contribute their subgraph queries to this project:
- Provides a common interface for querying subgraphs
- Provides polars dataframe output by default
- Use existing subgraph queries as building blocks for other queries


Query the Decentralized Network (In Progress)
========================
Create a .env file in the directory and enter the playgrounds api key PG_KEY =api-key

Then load a header into subgrounds object...this will be a slightly different input in queryportal