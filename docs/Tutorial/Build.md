# Build Manual

This manual can be built locally using [`mkdocs`](https://www.mkdocs.org/). To do so, a python environment must be
created.

## Tools

`git` shall be available to clone the repository. Otherwise, you may want to manually download the archive.

`python` shall be available to build the documentation.

If `doxygen` generated documentation is required, [`doxygen`](https://www.doxygen.nl/) shall be available. It also
uses `graphviz` to generate the graph, install it according to the [instructions](https://graphviz.org/download/).

## Steps

Please follow the instructions below to create a local editing environment.

### Clone the Repository

Clone the repository using the following command:

```bash
git clone https://github.com/TLCFEM/suanPan-manual.git
cd suanPan-manual
```

### Create a Python Environment

Within the `suanPan-manual` directory, create a new virtual environment using whatever tools you have available. Here
the plain python virtual environment is used.

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Requirements

Now that the virtual environment is created, install the requirements using the following command:

```bash
python -m pip install -r requirements.txt
```

Alternatively, if the `doxygen` documentation is required, the following command can be used:

```bash
python -m pip install -e .
```

Note `doxygen` and `git` are required to be available.

### Build and Run

The following command builds and runs the server on `localhost:8000`.

```bash
mkdocs serve
```

## Make Changes

The server monitors changes in real time. Now you can make changes to the manual and check the changes in the browser.