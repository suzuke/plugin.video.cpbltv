# -*- coding: utf-8 -*-

import urllib2
import re
import xbmc, xbmcgui, xbmcplugin
import sys
import urlparse

plugin_url = sys.argv[0]
handle = int(sys.argv[1])
params = dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))

def index():
    #replay part
    response = urllib2.urlopen("http://cpbltv.com")
    channels = re.findall(r"top.location.href=\'([\w\.\/\:]+)\';\">[0-9]+&nbsp;([\x01-\xff]{6}\sVS\s[\x01-\xff]{6})\s([\d]{4}\/[\d]{2}\/[\d]{2})", response.read())
    for channel in channels:
        url = plugin_url + "?act=play&channel=" + channel[0]
        combination = channel[1]
        date = channel[2]

        li = xbmcgui.ListItem(combination + " " + date)
        li.setProperty('mimetype', 'video/x-msvideo')
        li.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle, url, li, True)

    xbmcplugin.endOfDirectory(handle)


def play():
        response = urllib2.urlopen(params['channel'])
        main_url = "http://www.cpbltv.com"
        m = re.findall(r"iframe src=\"([\/\w\.\?\&\=]+autoPlay=true)", response.read())
        url = main_url + m[0]
        response = urllib2.urlopen(url)
        url = re.findall(r"url\:\s\"([\/\w\d\-\.\:]+index.m3u8\?token1=[\w\-\d]+&token2=[\w\_\-\d]+&expire1=[\d]+&expire2=[\d]+)", response.read())
        url = str(url[0])
        playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        playlist.clear()
        playlist.add(url)
        xbmc.Player().play(playlist)



{
    'index': index,
    'play': play,
}[params.get('act', 'index')]()
