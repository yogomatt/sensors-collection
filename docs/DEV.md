# Development Setup

The development environment for this project has to be in a Raspberry PI because the GPIO libraries are needed.

The setup described below is based on terminal interface only for optimizing the Raspberry PI resources.

## Git Setup

It is recommended to clone the project using the SSH protocol because Git relies on the SSH secure comunication, otherwise a credentials manager is required to store a Personal Access Token when using the HTTPS protocol (if not credentials manager is used then the user and access token should be used when executing a git action which so cumbersome when working with terminal interface only).

For setting up SSH private and public keys, follow the link [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

For adding the SSH public key to the GitHub account, follow the link [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?tool=webui)

For testing the connection to the GitHub repository, follow the link [Testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)

Once the SSH is set correctly, it's time to clone the project.

Start creating a new directory to host the repository.

> mkdir /home/my_user/workspace

Now clone the project using the SSH protocol.

> git clone git@github.com:yogomatt/sensors-collection.git

In addition, a few global configurations are needed to facilitate the git actions.

> git config --global user.name "John Doe"

> git config --global user.email "john@doe.org"

With the "global" flag, all repositories will use the same configuration.

To check the status and validate the connection to git use the following command.

> git remote show origin

To be able to work with the python sources it is important to follow the instructions from the next sections.


## Configuring Python 3

Python 3 is usually installed in a Raspberry PI OS, however if it is not installed then follow the instructions from [Installing Python](https://docs.python-guide.org/starting/installation/#installation)

To check the python version use the following command.

> python3 --version

Also make sure that pip is installed with the following command.

> python3 -m pip --version

If not installed then execute the following command.

> python3 -m ensurepip --default-pip

Also make sure that setuptools and wheel are installed because they are needed for building.

> python3 -m pip install --upgrade pip setuptools wheel

For more details see [Installing Packages](https://packaging.python.org/en/latest/tutorials/installing-packages)

## Python 3 Virtual Environment

A virtual environment is recommended in order to isolate the python packages that the application depends on, so more than one project can be develop in the same device.

To create the virtual environment, start creating a directory.

> mkdir /home/my_user/workspace/venv

Execute the following command to create the virtual environment in the new directory.

> python3 -m venv /home/my_user/workspace/venv

The virtual environment has to be activated so the following command must be executed before managing any dependency.

> source /home/my_user/workspace/venv/bin/activate

For more details see [Creating Virtual Environments](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments)

## Managing dependencies

The application has been configured according to the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects) Guide, thus pip was selected as build frontend and setuptools was configured as build backend.

Don't forget that including a new dependency must be performed in the virtual environment, so don't forget to activate to run something like the following command.

> pip3 install requests

Currently the following dependencies are needed for the project.

- RPi.GPIO
- adafruit_dht
- adafruit-circuitpython-dht
- requests

To check if a dependency is already installed use the following command.

> pip freeze | grep RPi

## Packaging

To facilitate the distribution of the project to any device running Raspberry PI OS, the project is built and published to PyPi (Python Package Index).

### Building

To build the project make sure to be within the virtual environment (don't forget to activate it).

Next, run a simple command.

> python3 -m build

Two files should be generated in the dist directory of the project. "The tar.gz file is a source distribution whereas the .whl file is a built distribution".

**Troubleshooting**
If the build process is reporting an error related to encoding then export the following environment variable.

> export PYTHONIOENCODING=utf-8

### Publishing

The project is published in TestPyPi initially and since the account from this repository could be erased randomly, then a new account should be created again.

A few important considerations for the PyPi account.

- Don forget to verify the account
- Enable 2 factor authentication
- Create an API token
- Follow the instructions when the token is created, it will request to create or update the file ~/.pypirc

For publishing from the Raspberry PI environment, follow the next steps.

1. If not installed, proceed to install twine within the context of the virtual environment.

> python3 -m pip install --upgrade twine

2. Go to the project directory and execute the following command.

> python3 -m twine upload --repository testpypi dist/*

**Note: Don forget to activate the virtual environment to execute any command for publishing.**