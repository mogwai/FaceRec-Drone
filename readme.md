# Tello Follow Face

### Introduction 

This program will feed video from tello drone and move based on the location of the
largest face in the view. 


### Running

1. Connect to Trello with Wifi
2. Run `python tello_ui.py`

### Features

- Will search for nearby faces if none are present

### Attributions

[Face Detection - dlib](http://dlib.net/face_detector.py.html)


### TODO

- [ ] Subroutine for sending RC Commands
- [ ] Store recently seen faces and use to move drone in search mode
- [ ] Basic search mode
- [ ] Make sure the height is reasonable
- [ ] Reconnection Timeout
- [ ] Depth Perception Model