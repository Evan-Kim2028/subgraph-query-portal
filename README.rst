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
usdc_depeg
==========


Cross-Chain USDC Supply Data Insights using Subgraphs, Subgrounds and DataStreams

Overview
==========
A comprehensive analysis of USDC supply in LPs across Ethereum, Polygon,
Arbitrum, and Optimism, revealing a **668m USDC** increase between
**March 9th-13th**.

Tools
==========
This project utilizes Subgraphs from `The Graph <https://thegraph.com/explorer>`__ and `DataStreams <https://github.com/Evan-Kim2028/DataStreams>`__, 
a subgraph query library built on top of `Subgrounds <https://docs.playgrounds.network/>`__, 
an open-source Python library built by `Playgrounds <https://playgrounds.network/>`__. Data is transformed using `Polars <https://github.com/pola-rs/polars>`__.

Subgraphs
---------
Subgraphs are custom APIs built on indexed blockchain data that can be queried using GraphQL. 

Subgrounds
----------
Subgrounds is an open-source Python library for interfacing with and querying Subgraphs. 
It simplifies the process of extracting and processing data from various blockchains.

DataStreams
-----------
DataStreams is a subgraph query library built that extends the functionality of Subgrounds.

Polars
------
Polars is a blazingly fast DataFrames library implemented in Rust using Apache Arrow Columnar Format as the memory model.

Requirements
============
* Python 3.10 or higher
* DataStreams
* Subgrounds
* Polars


Installation
============
1. Install Python (if not already installed): https://www.python.org/downloads/
2. Install DataStreams:

   .. code:: bash

      pip install git+https://github.com/Evan-Kim2028/DataStreams.git

DataStreams uses Subgrounds as a dependency so once you install DataStreams, there is no need to install Subgrounds.
3. Install Polars

    .. code:: bash
    
        pip install polars