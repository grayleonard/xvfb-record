Xvfb Headless Desktop Recording
===

This program uses Xvfb, a headless Xserver (X virtual framebuffer), to launch GUI programs. Using ffmpeg and x11grab, xvfb-record streams the framebuffer to an RTMP endpoint (tested with [twitch.tv](twitch.tv)). As an example, I have automated streaming netflix and hulu videos using the browser testing software [selenium](http://www.seleniumhq.org/).

Requirements
===

```
packages: Xvfb, ffmpeg, selenium, google-chrome
```

How To Run
===

```
python run.py -s netflix -u username -p password -i 1337

-s or --site : Currently accepts netflix and hulu
-u or --username : Username to use
-p or --password : Password to use
-i or --video_id : Video ID to load
```
