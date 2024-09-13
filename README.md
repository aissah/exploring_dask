# Intro to Dask

This repo contains some products from exploring the use cases for dask. Dask is a flexible parallel computing library for analytic computing. It is designed to scale from single machines to clusters of machines.

## Overview

The repo contains the following:

- notebooks: contains jupyter notebooks that
  - gives an introduction and demonstrates the use of dask - [intro](notebooks/1.intro.ipynb).
  - gives examples of use cases for dask - [examples](notebooks/2.examples.ipynb).
  - makes comparison between dask and OMP and MPI routines - [OMP_MPI_routines](notebooks/3.OMP_MPI_routines.ipynb.ipynb).
  - has the intension of implementing the ising model using dask - [ising_model](notebooks/Incomplete_Ising_model.ipynb).
- game_of_life_app: contains a simple game of life app that uses dask to parallelize the computation of the next generation of cells.
- Everything else is supporting files for the notebooks and the game of life app.

## Game of Life App

The game of life app is intended to be a simple implementation of the game of life using dask. Currently, it there is more focus on developing the webapp than parallelizing. This happened at a point when the write was also exploring the use of streamlit to build webapps. Since then the streamlit project has been separated out and hosted at: <https://funwithstreamlthafiz.streamlit.app/>. The app is a web app that allows users to interact with the game of life.
