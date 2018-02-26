# KNDL-Rando

Kirby: Nightmare in Dream Land Randomizer

Randomization program for Kirby: Nightmare in Dream Land (KNDL) for GBA

https://github.com/Aquova/KNDL-Rando

Written by Austin Bricker (Aquova), 2017-2018

https://twitter.com/Aquova_

## -- Overview --

Contained are programs to randomize the enemy abilities in Kirby: Nightmare in Dream Land. There are three programs contained within this repository which are to be used with a US version of Kirby: Nightmare in Dream Land for GBA.

First is a .lua script intended to be used with BizHawk or similar lua-compatible emulator. The lua script edits the RAM in real time, ensuring a completely random ability each time an enemy is swallowed. Keep in mind this is a work in progress, and some bugs have been known to occur.

Secondly, there are two programs that edit the ROM, allowing it to be distributed and used with any emulator, as detailed below.
However, while the abilites are randomized, they are always constant within that ROM.
Ex. If a fire enemy now gives you the spark ability, ALL fire enemies will always give you the spark ability.

## -- Usage --

In addition to the files included in the repository, you will also need a US copy of the Kirby: Nightmare in Dream Land ROM (which is left to the user to obtain). Follow the instructions in the subcategories below for your operating system/preference.

#### --- Windows ---

Run `KNDL-Randomize-PC.exe`, found on the 'Releases' page. Select the options you desire, and select the location of your .gba KNDL ROM. Finish by clicking the 'Randomize' button. The randomized ROM will be saved into the same folder as the original, with the seed appended onto the end of the file name.

#### --- macOS ---

Run `KNDL-Randomize-PC.app`, found on the 'Releases' page. Select the options you desire, and select the location of your .gba KNDL ROM. Finish by clicking the 'Randomize' button. The randomized ROM will be saved into the same folder as the original, with the seed appended onto the end of the file name.

#### --- Linux/Python ---

Linux users, or users who want to simply run the Python program itself, have two options.

1. If you have Python3, Qt5, and PyQt installed, you can run the following command in Terminal:

`python3 KNDL-Randomize.py`

This will open the same application as the PC and Mac binaries.

2. If you just have Python 3, there is a Command Line version of the program, which can be run via:

`python3 KNDL-Simple.py`

Make sure that your .gba file is located in the same folder as the program, then simply follow the instructions.

#### --- Lua Compatible Emulator ---

If your emulator supports Lua scripts (such as Bizhawk), you are welcome to instead use the `KNDL-Script.lua` script. This script edits the RAM in real time, allowing for complete randomization of Kirby's abilities, meaning that eating enemies of the same type may give different results.

## -- Known Issues / Future Plans --

- Enemies normally without abilities are not randomized
- Mini-bosses are not randomized
- The Star Rod, while available, is very experimental, and has many visual bugs.

## -- Version History --

v1.0.0 - I've added support for changing Kirby's color to those from The Amazing Mirror

v0.1.0 - Initial Release. All enemies with an ability are randomized. Mini-bosses and enemies normally without abilities are not supported. Star Rod is available, but very glitchy.

## -- Special Thanks --

The author of MapDeluxe, which helped me learn how to spawn in different enemies for testing.
