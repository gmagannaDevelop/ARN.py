# ARN.py

Final Project : Algorithms and Object-Oriented programming. Secodary structure of ARN molecules

## Students 

* Lydie Tran
* Gustavo Magaña López


## Caveats on extra dependencies

The user interface is built using [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/). 
It requires a `tkinter` backend which apparently
is not explicitly required by the package itself, 
so pypoetry does not resolve it automatically.
To be able to run the GUI, the `python3-tk` dependency 
must be met using the system's package manager :
```bash
$ sudo apt install python3-tk
```


## Build System

This project leverages [poetry](https://python-poetry.org/) 
as the main dependency tracking system. 
The code is simultaneously developed and 
tested both on `Pop!_OS 20.04 LTS x86_64` (Ubuntu-based linux system) and
`Windows 10`.
