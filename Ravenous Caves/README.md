# Ravenous Caves: the game

This project is the remake of an indie game,
initially built with by pygame and initially authored by Dan Allen.

We now use the `pyved-engine` lib, codebase has been tested and works fine along with the version `23.6a1`

Python+pygame compatibility: tested with py `3.9.13`
(you may need `pip install pygame==2.5.0` so that it runs fine).

## About

The project consists in a remake of old indie games (roguelike genre).
Our inspiration comes from a software
initially built with by pygame and authored by *Dan Allen*,
and also from a game name
"The enchanted cave" by *Dustin Auxier*.

Now we are using the `pyved-engine` + Python3.
The new project maintainer is [moonb3ndr](https://github.com/wkta).


## How to run the game?

**Important**: Firstly you need python3. Secondly, our game depends on the `pyved_engine`:
a work-in-progress [game engine](https://github.com/gaudiatech/pyved-engine)

It also depends on libraries that are listen in the `requirements.txt` file.

To install all these dependencies takes some time, but you need to do this only once!

It is recommended to proceed as follows:
1. download both ravenous caves, and *the custom game engine* on your computer.
The best option is to use git:
```shell
git clone https://github.com/wkta/ravenous-caves.git
```
And then
```shell
git clone https://github.com/gaudiatech/pyved-engine.git
```
2. using the command line, navigate to the folder that **contains ravenous caves**.
3. setup a new virtual environment by typing `python -m venv venv` and activate that virtual environment, for example on windows: `venv\Scripts\activate.bat`
4. install all basic requirements by typing ...
```shell
pip install -r requirements.txt
```
5. using the command line, navigate to the folder that contains the game engine.
6. install the engine within the current (still active) virtual environment. You can do that
by typing ... (see pip documentation and "editable mode" installation if you wish to learn more)
```shell
pip install -e .
```
7. go back to the folder **that contains ravenous caves** and type...
```shell
python main.py
```
## Copyright notice

The artwork and visual assets, which includes the contents of the assets/IMG/ folder, are covered by the CC Attribution 4.0 license in the root file CC.

Please note that this project include TrueType fonts under the internal/FONTS/ folder which are NOT covered by the CC License. These are:

Spinal Tap (http://www.rockbandfonts.com/), 
Devinne Swash, by Dieter Steffmann.
http://www.fontspace.com/dieter-steffmann/devinne-swash
Chancery Gothic and Courier.

Todo: either obtain permission to use these files or remove them from the current (derivative) repo.
