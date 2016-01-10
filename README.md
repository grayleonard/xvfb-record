Xvfb Headless Desktop Recording
===

This program uses Xvfb, a headless Xserver (X virtual framebuffer), to launch GUI programs. It then records the desktop with `x11grab` and ffmpeg - either to a file or streaming. It can automate browser actions using the browser testing software [selenium](http://www.seleniumhq.org/).

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
