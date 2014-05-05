# -*- coding: utf-8 -*-

import urllib2
import re
import xbmc

response = urllib2.urlopen("http://cpbltv.com")
# <div class="context" onClick="top.location.href='http://www.cpbltv.com/vod/content/1223.html';">058&nbsp;義大 VS 兄弟 2014/05/02<br></div>
#print response.read().decode('utf-8')

m = re.findall(r"top.location.href=\'(?P<url>[\w\.\/\:]+)\';\">[0-9]+&nbsp;(?P<combination>[\x01-\xff]{6}\sVS\s[\x01-\xff]{6})\s(?P<date>[\d]{4}\/[\d]{2}\/[\d]{2})", response.read())

t = m[0]

response = urllib2.urlopen(t[0])
main_url = "http://www.cpbltv.com"
#/vod/player.html?&type=vod&width=620&height=348&id=1288&autoPlay=true
m = re.findall(r"iframe src=\"([\/\w\.\?\&\=]+autoPlay=true)", response.read())

url = main_url + m[0]
#print url

response = urllib2.urlopen(url)
#url: "http://cpbl-hichannel.cdn.hinet.net/vod/content/cpbl-0504CPBL02/hd-hls-pc/index.m3u8?token1=mjZXFT-gOAB53C3ihcoVkw&token2=aRdoUN4Qse7L3hK_wl-j3Q&expire1=1399275737&expire2=1399282937",
m = re.findall(r"url\:\s\"([\/\w\d\-\.\:]+index.m3u8\?token1=[\w\-\d]+&token2=[\w\_\-\d]+&expire1=[\d]+&expire2=[\d]+)", response.read())

playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
playlist.clear()
playlist.add(str(m[0]))
xbmc.Player().play( playlist)
