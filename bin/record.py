#!/usr/bin/python

import sys, re, os, subprocess, mimetypes, shlex
from datetime import datetime
from config import config


is_url = True


def main():
	global is_url
	if len(sys.argv) != 2: 
		print "record.py: missing url"
		sys.exit(1)

	urlparam = sys.argv[1]
	if os.path.isfile(urlparam):
		is_url = False;
		urlparam = loadurl(urlparam)

	validate = re.compile(r'^(http|https|rtmp|rtmpe)://.*$')
	if not validate.match(urlparam):
		notify( "record.py: invalid url")
		sys.exit(1)

	if '|' in urlparam:
		notify("record.py: complex url not implemented")
		sys.exit(1)
	else:
		url =  urlparam.strip()

	# # ffmpeg dictionary to hold url and ffmpeg options
	ffmpegDict = {}

	# if 'user-agent' in urlDict:
	#     ua = urlDict['user-agent']
	#     useragent = "-user-agent '{0}'".format(ua)
	#     ffmpegDict['user-agent'] = useragent

	# if 'referer' in urlDict:
	#     rf = urlDict['referer']
	#     referer = "-headers 'Referer: {0}'".format(rf)
	#     ffmpegDict['referer'] = referer

	# if 'cookie' in urlDict:
	#     cd = re.search('(http|https)://[a-zA-Z0-9.-]*[^/]', url) # cookie domain name
	#     cookiedomain = cd.group()
	#     cookieurl = urlDict['cookie']
	#     cookie = "-cookies '{0}; path=/; {1};'".format(cookieurl, cookiedomain)
	#     ffmpegDict['cookie'] = cookie

	# nltid = re.findall('nltid=[a-zA-Z0-9&%_*=]*', url) # nltid cookie in url

	# if nltid:
	#     cd = re.search('(http|https)://[a-zA-Z0-9.-]*[^/]', url) # cookie domain name
	#     cookiedomain = cd.group()
	#     cookieurl = nltid[0]
	#     cookie = "-cookies '{0}; path=/; {1};'".format(cookieurl, cookiedomain)
	#     ffmpegDict['nltid'] = cookie

	# http and rtmp regexes
	http = re.compile(r'^(http|https)://')
	# rtmp = re.compile(r'^(rtmp|rtmpe)://')

	if http.match(url):
		command = ffmpeg(url, **ffmpegDict)
	#         elif options[0] == "-a":
	#             ffrec = audio.ffmpegaudio(**ffmpegDict)
	# elif rtmp.match(url):
	# 	command = rtmp(url,**ffmpegDict)
	#         elif options[0] == "-a":
	#             rtmprec = audio.rtmpaudio(**ffmpegDict)
   
	runprocess(command)
	notify("Download completed")





# def parse_url(urldata):
#     ud_split = urldata.split(r'|')
#     stream_url = ud_split[0] # url before |
#     params = ud_split[1] # url after |
#     ud_decode = unquote(unquote(params))
#     data = splitEquals(master(ud_decode)) # create the url dictionary
#     data['url'] = stream_url # add the url to the dictionary
#     return data
	# # url dictionary keys lowercased for searching
	# urlDict = {k.lower(): v for k, v in theUrl.items()}



def loadurl(path):
	url = ""
	if mimetypes.guess_type(path)[0] == 'text/plain':
		with open(path, 'r') as file:
			url = file.read()
		file.close()        
	return url




def ffmpeg(url, **kwargs):
	''' ffmpeg function
	ffmpeg recording function
	'''
	time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	ext = 'mkv'
	recordingfile = os.path.join(config['save_path'], 'video-{}.{}'.format(time, ext))
	ffmpeg = 'ffmpeg'

	# get the values from the dictionary passed to the function
	# values = list(kwargs.values())

	ffcmd = "{0} -hide_banner -stats -v panic -i {1} -c:v copy -c:a copy {2}".format(ffmpeg, url, recordingfile)

	# if any(word in kwargs for word in ('user-agent', 'referer', 'cookie')):                 
	#     # dict minus first time which is the url
	#     options = values[1:]
	#     remove_bracket = str(options)[1:-1]
	#     options_join = ''.join(remove_bracket).replace('"', '')
	#     ffcmd = "{0} -hide_banner -stats -v panic {2} -i {1} -c:v copy -c:a copy {3}".format(ffmpeg, url, options_join, recordingfile)

	# split the ffmpeg command for subprocess
	ffsplit = shlex.split(ffcmd)

	#print ffcmd
	return ffsplit
 


def runprocess(command):
	print command 
	try:
		process = subprocess.check_call(command)
	except KeyboardInterrupt:
		print("process stopped by user")
	except IOError:
		print("input output error,  maybe missing command?")	


def notify(message):
	global is_url
	print message
	if is_url:
		sendcmd = "kodi-send -a 'Notification(VideoTools,{0})'".format(message)
		command = shlex.split(sendcmd)
		runprocess(command)



if __name__ == "__main__":
	# execute only if run as a script
	main()