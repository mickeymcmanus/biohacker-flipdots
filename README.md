# Flip Dot Display Library #

This is a python library to power MAYA's flip dot display. It includes the ability to display basic text, video,
textual transitions, display text from Twitter, and run a Twitter based scavenger hunt game.

## Installation ##

There are several requirements that must be installed for this package to be fully functional.

*   pySerial -- Used for communication to the flip dots.
*   PIL -- Used by the video module to convert images to bitmaps to be displayed.
*   Twython -- Used for communicating to Twitter.
*   Requests -- Used by Twython, needed to catch connection errors being thrown by Twython.
*   FFMPEG -- To convert videos into frames to display.

Once the requirements are fulfilled, installation is as simple as:

```
git clone git@git.eng.maya.com:flipdots.git
```

or

```
svn checkout https://YOURUSERNAMEHERE@svn.maya.com/maya_design/trunk/projects/NAMII/Rapid/FlipDots
```

## Usage ##

### Text ###

The following will simply display "Hello World" on the flip dots. getbytes() is usually called before sending to any
basic text function. getbytes() will take a string and convert it into a hex string that is the raw data needed to be
sent to the display.

```python
from core import core

core.fill(core.getbytes("Hello World"))
```

### Video ###

To display a video either put the frames directly into the video/frames directory or place the video into the
video/videos directory. Supported video types, are those supported by your FFMPEG install and supported frame formats
are those supported by your local PIL install.

```python
from video import video

video.convert_video_to_frames("VIDEONAMEHERE.mov")
video.display_video("VIDEONAMEHERE.mov")
```

In the above example convert_video_to_frames the VIDEONAMEHERE.mov video from the video/videos directory and creates
a directory ("video/frames/VIDEONAMEHERE.mov") where it stores the videos frames. display_video uses its parameter to
find a directory in video/frames that matches it. It then will go through each frame at 12 FPS and display each frame
on the flip dots. 12 FPS is about the quickest the flip dot display can turn.

### Twitter ###

The example below will take any direct messages sent to [@flipdots](https://twitter.com/flipdots) and display them
on the flip dot display.

```python
from twitter import twitter

twitter.display_direct_messages()
```

display_direct_messages uses a hashtag system to change the transitions used to display the message. For example, you
send the tweet:

```
@flipdots Mickey McManus #upnext
```

The above will use the upnext transition, defined in the transition/transition.py file to display the text
"Mickey McManus".

You can also specify several transitions and it will choose a random one to use. If no hashtags are used, it will just
use the randomgeneral transition.

### Scavenger Hunt ###

Scavenger hunt has quite a bit of bugs, and was never fully tested, but it is a base first pass example of how it could
be done. The premise of the game is that clues/riddles would be displayed on the board and people would mention
@[@flipdots](https://twitter.com/flipdots) in a tweet with the key/answer as a hashtag, along with a hashtag identifier
for the clue/riddle.

scavengerhuntbackend.py should be run constantly in the background to make updates to the puzzle and data file. This
script checks Twitter every minute and grabs all mentions of @[@flipdots](https://twitter.com/flipdots). It then parses
them looking for hashtags for the puzzle name and key, if one or both are not found or incorrect, it will send a tweet
to the user with a negative response. If the key and puzzle match, it will update the user's data and remove a key from
the puzzle's JSON file.

Example usage:

```
python scavengerhuntbackend.py
```

```python
from games.scavengerhunt import scavengerhunt

scavengerhunt.display_leader_board()    #Displays the current standings

scavengerhunt.display_riddle()          #Displays the next riddle in line
```

## Flip Dot Display Notes ##

### Last Used ###
Flip Dot Display Notes Each unit/module/panel of flip dots is 5 dots wide and 7 high.

Last Used The flip dot display was used by Mickey and Zen at Burning Man 2018 for the airstream "Benderbot" costume for Mick's 1950 Flying Cloud. It was reconfigured into a curved panel of 2 flip dot units high by 6 flip dot units long to fit within the rear window of the airpstream and the playlist was a set of eyes that had different expressions.

Before that, the flip dot display was used for NAMII's booth Jun 10-12th 2013, the booth was composed of a 12ft, 21 panel, 105 column vertical display and a 4ft, 6 panel, 30 column vertical display. The codebase was adapted to this setup. Most of the movies/transitions/etc take advantage of this vertical display setup. Furthermore, it was coded to work with two separate controllers and two separate USB to serial devices. Further adaption of the lower level core commands would need to be changed to be used in a different setup. Probably even wiring harness adaptions as well.

Before that, the display was originally used as a 16ft, 29 panel, 145 column horizontal display at SXSW for the Pepsico display. The original wiring harness, is wired for this one long single row display. Flip Dot Display Library This is a python library to power MAYA's flip dot display. It includes the ability to display basic text, video, textual transitions, display text from Twitter, and run a Twitter based scavenger hunt game.


### USB to Serial ###

When using the blue USB serial adapters on a Mac, you must install the
[FTDI driver](http://www.ftdichip.com/Drivers/VCP.htm). One of them is labelled "main"
(was used on the large 12ft display, used by most commands), the other "secondary"
(was used on the small 4ft display, used only by the clockcore commands).

### Controller Specifics ###

Each controller has two "rows". The first row has 75 addressable columns and the second has 70 addressable columns. The
first panel is at the bottom right, the second is bottom left, the third is next row up on the right. It goes in this
pattern up the board. For the large harness, there is a Sharpied number on the connector and on the board that indicate
positioning.


### Serial ###

#### Fill Messages ####

Each panel is 5 dots wide and 7 high. They are drawn using hex between 0x00 and 0x7f (0xff being if
it was 8 high). The columns are addressed from the bottom up. For example, 0x01 would produce:

```
. . . . .
. . . . .
. . . . .
. . . . .
. . . . .
. . . . .
0 . . . .
```

0x02 would produce:

```
. . . . .
. . . . .
. . . . .
. . . . .
. . . . .
0 . . . .
. . . . .
```

Every time a message is sent to the controller, it increments the column automatically. So if the column counter started
at 0, the first message would fill the first column, the next would fill the second and so forth.

#### Column Set ####

A control message is considered 0x81 or greater. The first control message is always considered a column setter. To move
the column cursor to the first column of the current row, you would send 0x81. If you wanted the column cursor to point
to the second column of the current row, you would send it 0x82.

#### Row Set ####

The second control message, if sent at all, is a row set. For our controller, that only has two rows, the first row is
0x81 and the second is 0x82. Remember, to set a row you must always send a column control message as well. To set the
cursor to the first row and column, you would send 0x81 followed by 0x81. To set it to the second row first column, you
would send 0x81 followed by 0x82.

#### Caveat ####

The column does indeed auto increment, so if you want to fill the first 5 rows completely with all white dots you would
just send 5 messages, all of them being 0x7f. However, once you ge21t to the end of the first row, in our particular
controllers case that is column 75 or 0xcc, you need to move onto the next row. If you look at the fill function,
it shows how this is done.

```python
def fill(m,fillmask=127):
    ser_main.write(reset+row1)
    for i in range(len(m)):
        if i == ROW_BREAK:
            ser_main.write(reset+row2)
        ser_main.write(chr(ord(m[i])&fillmask))
    return m
```

Where ROW_BREAK is 75, reset is 0x81, and row1 is 0x82.


