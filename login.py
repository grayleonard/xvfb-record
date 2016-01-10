import sys, getopt, time, subprocess, shlex

from selenium import webdriver
from xvfbwrapper import Xvfb

info = dict()
platforms = {
    'hulu' : { 'login': 'https://secure.hulu.com/account/signin', 'watch': 'http://www.hulu.com/watch/'},
    'netflix' : { 'login': 'https://www.netflix.com/Login', 'watch': 'http://www.netflix.com/watch/' }
}
browser = None
xvfb = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 's:u:p:i:d:t', ['site=', 'username=', 'pass=', 'video_id=', 'destination=', 'test'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

if len(opts) < 3:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-s', '--site'):
        info['platform'] = arg
    elif opt in ('-u', '--username'):
        info['username'] = arg
        print arg
    elif opt in ('-p', '--pass'):
        info['pass'] = arg
    elif opt in ('-i', '--video_id'):
        info['video_id'] = arg
    elif opt in ('-d', '--destination'):
        info['destination'] = arg
    elif opt in ('-t', '--test'):
        print info['video_id']
        print platforms[info['platform']]['watch'] + '' + info['video_id']
        sys.exit(2)

def set_up():
    global browser
    global xvfb
    xvfb = Xvfb(width=1280, height=720, colordepth=24)
    xvfb.start()
    browser = webdriver.Chrome()
    print browser.title
    print ':%d' % xvfb.vdisplay_num

def netflix_login():
    global info
    global browser
    global xvfb
    global platforms
    browser.get(platforms[info['platform']]['login'])
    email_input = browser.find_element_by_name('email')
    pass_input = browser.find_element_by_name('password')
    email_input.send_keys(info['username'])
    pass_input.send_keys(info['pass'])
    pass_input.submit()
    print browser.get_cookies()

def hulu_login():
    global info
    global browser
    global xvfb
    global platforms
    browser.get(platforms[info['platform']]['login'])
    email_input = browser.find_element_by_name('login')
    pass_input = browser.find_element_by_name('password')
    email_input.send_keys(info['username'])
    pass_input.send_keys(info['pass'])
    browser.find_element_by_class_name('login-submit').click()
    print browser.get_cookies()

def netflix_fullscreen():
    global browser
    action = webdriver.common.action_chains.ActionChains(browser)
    action.send_keys('f').perform()

def watch():
    global info
    global browser
    global platforms
    watch_url = platforms[info['platform']]['watch'] + '' + info['video_id']
    print platforms[info['platform']]['watch'] + '' + info['video_id']
    browser.get(watch_url)
    video_player = browser.find_element_by_id('flash-player-container')
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(video_player, 330, 437)
    time.sleep(2)
    action.click()
    time.sleep(2)
    action.perform()
    while True:
        time.sleep(60)

def stream():
    global xvfb
    global info
    ffmpeg_stream = '/root/bin/ffmpeg -f x11grab -s 1280x720 -r 24 -i :%d+nomouse -c:v libx264 -preset superfast -pix_fmt yuv420p -s 1280x720 -threads 0 -f flv "%s"' % (xvfb.vdisplay_num, info['destination'])
    args = shlex.split(ffmpeg_stream)
    p = subprocess.Popen(args)
    print p

set_up()
if info['platform'] == 'netflix':
    netflix_login()
elif info['platform'] == 'hulu':
    hulu_login()
stream()
if info['platform'] == 'netflix':
    netflix_fullscreen()
watch()
browser.quit()
xvfb.stop()
