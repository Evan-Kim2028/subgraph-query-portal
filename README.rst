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


This library is a collection of public goods Subgraph queriess to obtain cross-chain data for researchers and tool builders. Incorporate subgraph data seamlessly into existing 
web3 on-chain data analytics workflows in Python.


Tools
==========
This project utilizes Subgraph endpoints from `Messari <https://messari.io/report/the-graph-foundation-awards-messari-usd12-5mm-in-first-ever-core-subgraph-developer-grant-to-build-and-standardize-subgraphs>`__ 
and `Subgrounds <https://docs.playgrounds.network/>`__, an open-source Python library built by `Playgrounds <https://playgrounds.network/>`__. 
Data is transformed using `Polars <https://github.com/pola-rs/polars>`__.

Subgraphs
---------
Subgraphs are custom APIs built on indexed blockchain data that can be queried using GraphQL endpoints. For a list of standardized subgraph endpoints by Messari, see `here https://subgraphs.messari.io`__.

Subgrounds
----------
Subgrounds is a Python library that allows seamless Subgraphs into a Python data analytics workflow. 
It provides an open-source solution for interfacing with and querying Subgraphs, streamlining the process of extracting and processing blockchain data. 
With Subgrounds, you can easily incorporate Subgraphs into your Python data pipeline, enabling you to seamlessly integrate blockchain data into your data analytics web3 workflow.

Polars
------
Polars is a blazingly fast DataFrames library implemented in Rust using Apache Arrow Columnar Format as the memory model.

Library Dependencies
============
* Python >= 3.10
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


Examples
========================
Run the following commands from the root directory of the project.

1. Query all of the most recent Univ3 Swap data
    
   .. code:: bash

      python examples/query_univ3_latest.py

2. Query all Univ3 Swap data within a time period:

   .. code:: bash

      python examples/query_univ3_all_swaps.py

1. Query Univ3 WETH/USDC pool data within a time period:

   .. code:: bash

      python examples/query_univ3_weth_usdc.py

2. Query USDC supply going into all Univ3 pools within a time period:

   .. code:: bash

      python examples/query_univ3_usdc_in.py

Cross Chain Query Example
==========================
Load the example notebook `query_univ3_cross_chain.ipyn`_ in the `examples`_ directory. This notebook demonstrates
how a cross chain query workflow would look like if one wanted to query all USDC supply going into Uniswap V3 pools across multiple blockchain subgraphs.


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


