

## Building the documentation 

You can use the `make` command and `make html` to build web pages. 

You need a Python environment with `sphinx` and other
dependencies, you can create it with `uv` by running `scripts/initenv.sh`
from the repository root.

To develop/change documentation, you can then do:

    uv run --group docs make -C doc auto

A page will open at https://127.0.0.1:8000/ serving the docs and it will 
react to changes to source files pretty fast. 

