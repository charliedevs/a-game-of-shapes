# A Game of Shapes

![Game of Shapes](https://i.ibb.co/xq8Vs34/Game-Of-Shapes.png)

<table>
<tr>
<td>
    
    A simple online two-player strategy game created with pygame. Developed by Charlie Davis and Fernando Rodriguez for the Computer Science Department at Stephen F. Austin State University.
</td>
</tr>
</table>

## Description

The object of the game is to destroy all of your enemy's shapes before they destroy yours. The game is played online between two players. Take turns moving your shapes across the gameboard, and once you're in range of an enemy, attack! 

To successfully land an attack, you must best your opponent in a game of rock, paper, scissors (or at least tie). If your opponent beats you at rock, paper, scissors, they effectively block your attack. Chip away at each other, and see who's left standing in the end. Because in A Game of Shapes, you either win, or you die.

Uses FFF Forward Font, a free font available from [this website.](https://www.1001fonts.com/fff-forward-font.html)

## Usage

Start game by running `main.py`, then enter the IP address and port of the server, which handles the connections between clients.

To start the server, run the `server.py` file, including the IP address and port you wish to run it on as commandline arguments.

**Requires** [Python 3](https://www.python.org/downloads/). 

**The following external modules are required:** 
* [pygame](https://pypi.org/project/pygame/)
* [tkinter](https://pypi.org/user/Tkinter/)
* [cryptography](https://pypi.org/project/cryptography/)

### Contribution
Contribute changes to this project by following these steps:

#### Clone the project to your machine
Before you can contribute, you need to have a local copy of the code on your machine. Cloning is the first step, but in order to have any changes reflected on this repository, you must **fork** this repository.

1. First, you'll need to set up Git on your machine. For Windows, I recommend installing [Git BASH](https://gitforwindows.org/).

2. You also need to create a new GitHub account if you don't already have one.

3. Follow the instructions [on this GitHub Help page](https://help.github.com/en/articles/fork-a-repo) to create a copy of this repository on your account AND clone your repository to your local machine.

#### Use git to track your changes

1. Use the `git status` command to see what files are tracked. This will show you any tracked files that have changes.

2. Use `git add <filename>` for each file you've made changes to that you want git to track.

3. **Commit** your changes each time you add a new feature using `git commit -m 'Short description of change'`.

#### Keep up to date with this repository
Your fork will not automatically be updated when others make changs to this main repo. You need to pull changes from this main repository before you begin making changes to your local copy.

1. Add original repository as remote: `git remote add upstream git://github.com/charliethomasdavis/sfasu-strategy-game.git`

2. Fetch and merge the changes from upstream into your branch: `git pull upstream master`

#### Merge your changes with this repository

1. Push your changes to your fork using `git push origin <branchname>`. \<branchname\> is **master** if you haven't created any branches.
    
2. On github, navigate to [my repository](https://github.com/charliethomasdavis/sfasu-strategy-game/).

3. Create a pull request by [following the instructions here.](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork)

### Style Guide

Keep commenting short and simple; only comment if code is unclear, but prefer to make code more clear. (Comments have been added judiciously throughout the code since we turned this in as a school project)

Use default [pylint](https://www.pylint.org/) configuration for pip8 style guidelines.

Name variables and function names using snake_case, all lowercase with underscores between words. Example: `variable_name`

Name classes using CamelCase, start with uppercase and use uppercase for each word. Example: `ClassName`

Name constant values using ALL_CAPS, with underscores between words. Example:  `CONSTANT_NAME`

## Copyright Information

Copyright (C) 2019  Charles Davis, Fernando Rodriguez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
