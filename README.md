# Find Your Chinese Name

> A program that suggests five Chinese given names after you choose two words about personality, meaning, or style.

## Table of Contents

- [General Information](#general-information)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Project Status](#project-status)
- [Room for Improvement](#room-for-improvement)
- [Acknowledgements and References](#acknowledgements-and-references)
- [Contact](#contact)

## General Information

I made an interactive Chinese name finder using Processing Python Mode for my UTS Creative Coding project.

For people who do not understand the characters or their meanings, choosing a Chinese name can be difficult. With this project, users can explore names by selecting words that matter to them, like Calm, Creative, Nature or Hope.

The interface is English. For each suggested name, the following are given: Chinese characters, pinyin, English explanations and a list of matching words. This book animation reinforces the concept of opening a book and discovering a name.

## Technologies Used

### 1. Processing Python Mode and mouse interaction

The project is running Processing version 4.4.6 using Python Mode, the environment reported to work during development. Buttons and cards are drawn as rectangles. The program checks the mouse position for clicks and highlights buttons when the mouse is over them. 

The `page` variable controls the cover, selection page, and results page.

### 2. Lists, dictionaries, and name matching

Source file has 15 preference words and 30 name records. Every name has tags. The program then compares the two words selected to these tags, and counts the matches: 

```python
matched = [word for word in selected if word in item["tags"]]
```

Names matching both words appear before names matching only one. `shuffle()` changes the order of candidates before sorting, so names with equal scores can appear in different orders.

When changing word batches, the program excludes the previous batch and selected words. It gives priority to words not yet seen in the current cycle.

### 3. Drawing the book and timing the animation

The book consists of rectangles, lines and an ellipse. A four sided shape . The turning page . no downloaded book image, GIF or sprite sheet is used. 

`cos()` moves the page edge from right to left, and `sin()` raises and lowers it. The animation uses elapsed time:

```python
elapsed = millis() - book_started
next_frame = int(elapsed // BOOK_FRAME_MS)
```

There are eight poses, each lasting 90 milliseconds, so one turn lasts about 0.72 seconds. Clicks are ignored while a batch-change animation is playing. On the cover, the book floats gently and turns a page every 2.4 seconds.

## Features

- Animated welcome screen with a Start button.
- Five preference words at a time, each with an English explanation.
- Two-word selection that is kept when browsing another batch.
- Page-turn animation when clicking Show Another Five.
- Five name suggestions with pinyin, meanings, and match counts.
- Clear selection, Back, and Start Again controls.

In this version, Find My Name shows the results immediately. The page-turn animation is used on the cover and when changing word batches.

## Screenshots

### Welcome screen

![Welcome screen](welcome.png)

The welcome screen shows an animated book. Click **Start** to begin choosing words for your Chinese name.

## Setup

1. Install Processing 4.4.6 and a compatible Python Mode. Other versions are not guaranteed to work.

2. Put `Find_Your_Chinese_Name4.pyde` inside a folder called `Find_Your_Chinese_Name4`.

3. Open the sketch in Processing and check that the selected mode is Python.

4. Click Run.

Keep `README.md` at the repository root, alongside the sketch folder. All word and name data are included in the `.pyde` file.

This is a Processing Python Mode sketch not a standalone Python 3 script. Uses the standard-library modules `random`, `sys` and `traceback`. It requires no extra sketch libraries or external assets.

The default font is Microsoft YaHei. If Chinese characters appear as boxes, change `FONT_NAME` to an installed Chinese font. For example, PingFang SC can be used on a Mac where it is available.

If opening the sketch fails, create a blank Python Mode sketch and paste the complete code into it. If running still fails, check the console and try a small Python Mode example first. Startup messages numbered `[1/5]` to `[5/5]` help locate problems.

## Usage

1. Click **Start** to enter the selection page.
2. Click a word card to select it. Click it again to deselect it.
3. Click **Show Another Five** to browse more words. Your existing selections are kept.
4. Click Find My Name, selecting exactly two words.
5. Read the five suggestions and compare their meanings and matching words.
6. Click **Back** to return with your selections, or **Start Again** to clear everything and return to the cover.

To clear all selected words, including words not shown in the current batch, select Clear selection.

## Project Status

The current prototype includes the cover, word selection, name matching, and results screens. It is intended for demonstration and learning.

The suggestions are given names, not full names with surnames. Tags and overall meanings are interpretations for this prototype, rather than definitive cultural explanations. Some suggestions match only one selected word. Selections are not saved after the program closes.

## Room for Improvement

Possible future improvements include:

- Expanding and reviewing the name dataset.
- Adding tone marks and pronunciation audio.
- Letting users save favourite names.
- Improving the layout for different screen sizes.

These features are not included in the current version.

## Acknowledgements and References

The following Processing Python Mode documentation explains the drawing, movement, and timing functions used in this project:

- [Coordinate System and Shapes](https://py.processing.org/tutorials/drawing/)
- [2D Transformations](https://py.processing.org/tutorials/transform2d/)
- [vertex()](https://py.processing.org/reference/vertex)
- [millis()](https://py.processing.org/reference/millis)
- [sin()](https://py.processing.org/reference/sin) and [cos()](https://py.processing.org/reference/cos)

[Anatomy of a page-flip animation by Mark Pospesel](https://mpospese.com/2012/05/23/anatomy-of-a-page-flip-animation/) was found later as a reference for comparing page-turn principles. The existing code was not adapted from that article.

The implementation was written and edited with conversational programming help . The documentation above describes relevant techniques but it is not the source of the full project code.

This README follows the general structure of my earlier [poem_buttem project](https://github.com/kaihangzhang-cmd/kaihang-s-a2git), with guidance from [How to write a good README](https://bulldogjob.com/readme/how-to-write-a-good-readme-for-your-github-project) and the [README cheatsheet](https://github.com/ritaly/README-cheatsheet).

## Contact

Created by Kaihang Zhang for the UTS Creative Coding project.
