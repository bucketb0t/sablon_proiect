## Setup

### Install the dependencies:

```commandline
pip install -r requirements.txt
```

### Config file

- I have setup a config.json file to be able to configure the hosting address of the API

<b>config.json</b>

```
{
    host="0.0.0.0",
    port=8000
}
```

### How to run it

1. Open a command prompt or terminal window.
2. Navigate to the directory containing your Python script (`sablon_api.py` in this case) using the cd command.
3. Once you're in the directory containing your Python script, run the following command:
    ```commandline
    uvicorn sablon_api:app --reload
    ```
4. After running the command, you should see output indicating that the FastAPI server is running. By default, it will
   listen on http://127.0.0.1:8000.

### Extras

Here are some useful commands to use installed development tools.

#### Documentation generator: Sphinx

I used Sphinx to generate code documentation. In order to use this tool, you have to install it using pip:

```commandline
pip install Sphinx sphinx_rtd_theme
```

(Optional) If the project doesn't have it configured, then you can do it using this command (you will be prompted with
some questions):

```commandline
python -m sphinx.cmd.quickstart
```

This will generate a few files and directories:

- build/ - here you will find the generated html pages
- source/ - here you will find the .rst templates and configuration file
- Makefile - makefile that can be run using **make** tool (you can install it from
  here: https://gnuwin32.sourceforge.net/packages/make.htm)
- make.bat - Windows batch script that behaves like the Makefile

In order to register a directory with code for automatic documentation, you need to run this command:

```commandline
cd docs/
python -m sphinx.ext.apidoc -o .\source\path_to_directory
```

- this will generate one rst template file for each Python module, under source/ directory

(Optional) If you perform this setup for the first time, then you need to go to **index.rst** and add **modules.rst** as
a
reference, like this:

```commandline
Welcome to Management Web Service's documentation!
==================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
```

Then you need to (re)generate the HTML documentation files:

```commandline
cd docs/
make clean
make html
```

- after doing this, you can view the documentation by opening **docs/build/html/index.html**

**NOTE**: if you get errors when executing this command, that *sphinx-build cannot be found*, then replace it in the
Makefile
with:

```commandline
SPHINXBUILD   ?= python -m sphinx.cmd.build
```

#### Code testing and coverage

- I used pytest for writing unit and integration tests

```commandline
pip install pytest
pytest .\tests\
```

- for code coverage, I used the **coverage** library:

```commandline
pip install coverage
```

that can be used as follows:

```commandline
coverage run -m pytest .\tests\
coverage report  # to generate a CLI code coverage report
coverage html  # to generate a html report
```

#### Code quality checks

1. Pylint

- it's used to verify if the code is respecting some standards

```commandline
pip install pylint
```

- usage:

```commandline
 pylint *
```


