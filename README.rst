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

======================
Subgraph Query Portal
======================

:literal:`queryportal` is a Subgraph query management library and makes it easy to query cross-chain, cross-subgraph data on the decentralized Graph Network.


Tools
==========
This project utilizes Subgraph endpoints from `Messari <https://messari.io/report/the-graph-foundation-awards-messari-usd12-5mm-in-first-ever-core-subgraph-developer-grant-to-build-and-standardize-subgraphs>`__ 
and `Subgrounds <https://github.com/0xPlaygrounds/subgrounds>`_, an open-source Python library built by `Playgrounds <https://playgrounds.network/>`_. 
Data is transformed using `Polars <https://github.com/pola-rs/polars>`_.

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
====================
* Python >= 3.10
* Subgrounds = 1.5.2
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

For a list of examples, please see `<https://github.com/Evan-Kim2028/queryportal_notebooks>`_ which is a repository of queryportal notebook examples.



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
===============
Queryinterface is an abstract class that defines the interface for all subgraph queries via the :literal:`query()` method.

Some reasons why a developer would want to contribute their subgraph queries to this project:
- Provides a common interface for querying subgraphs
- Provides polars dataframe output by default
- Use existing subgraph queries as building blocks for other queries


Query the Decentralized Graph Network 
=====================================
Create a :literal:`.env` file in the directory and enter the playgrounds api key PG_KEY =api-key

Since decentralized endpoints are defined by hashes, there is no easy default for naming decentralized subgraphs. 
Thus the main difference for querying the Graph Network compared to the hosted network is that the endpoint will 
look different and be submitted as a dictionary. 

The decentralized endpoint formatting is :literal:`https://api.playgrounds.network/v1/proxy/subgraphs/id/subgraph_id` 
where subgraph_id is the ID of the subgraph. These can be found by searching `<https://thegraph.com/explorer>`_.
For example the subgraph key for uniswap is found here `<https://thegraph.com/explorer/subgraphs/2szAn45skWZFLPUbxFEtjiEzT1FMW8Ff5ReUPbZbQxtt?view=Overview&chain=mainnet>`_ 
and is :literal:`2szAn45skWZFLPUbxFEtjiEzT1FMW8Ff5ReUPbZbQxtt`.