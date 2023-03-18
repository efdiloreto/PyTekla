
## Installing PyTekla

PyTekla is available on PyPI:

```bash
pip install pytekla
```

Optionally you can install PyTekla along the libraries for data management (for example, pandas):
```bash
pip install pytekla[data]
```
or the "dev" version:
```bash
pip install pytekla[dev]
```

PyTekla officially supports Python 3.11+.


## Other requeriments

Keep in mind that you'll need a Tekla Structures installed in your machine.

!!! note

    It is recommended to work with virtual environments.


## Total beginners guide

### Installing Python

Go to [Python.org](https://www.python.org/downloads/) and download the last Python version.

![Python Download](images/Python%20download.png){ width="800" }

Run the installer and make sure you have checked the "ADD python.exe to PATH" checkbox during the installation.

![Python Installation](images/Python%20checkbox.png){ width="800" }


### Installing the IDE (Integrated Development Environment)

We are gonna use PyCharm, because we think PyCharm is good for beginners because it offers an intuitive and supportive environment for learning and practicing Python programming.

Got to [Jetbrains](https://www.jetbrains.com/pycharm/download/#section=windows) and download PyCharm Community

![PyCharm Download](images/PyCharm%20download.png){ width="800" }

Install it and run it. Select "New Project".

![PyCharm New project](images/Pycharm%20Start.png){ width="800" }

Configure the new project and make sure you are creating a "virtual environment" for this project [Steps 2 and 3].

![PyCharm Config](images/PyCharm%20New%20Project.png){ width="800" }

Open the terminal.

![PyCharm Terminal](images/PyCharm%20First%20Window.png){ width="800" }


Open the CMD.

![PyCharm CMD](images/Pycharm%20cmd.png){ width="800" }

Install PyTekla

```bash
pip install pytekla
```

![Install PyTekla](images/Install%20Pytekla.png){ width="800" }


After this you are all set! Follow the [First Steps section](first_steps.md) to start coding with PyTekla.


## What next?

In order to use PyTekla you'll need some basic Python knowledge. Check out the following resources for beginners:

- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)
- [Corey Schafer - Youtube Channel](https://www.youtube.com/watch?v=YYXdXT2l-Gg&list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7)
