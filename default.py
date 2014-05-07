# -*- coding: utf-8 -*-

import urllib2
import re
import xbmc, xbmcgui, xbmcplugin
import sys
import urlparse
from F4mProxy import f4mProxyHelper

plugin_url = sys.argv[0]
handle = int(sys.argv[1])
params = dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))

def index():
    # Live
    url = plugin_url + "?act=live"
    li = xbmcgui.ListItem("直播")
    xbmcplugin.addDirectoryItem(handle, url, li, True)
    
    # Replay
    
    url = plugin_url + "?act=replay&offset=1"
    li = xbmcgui.ListItem("重播")
    xbmcplugin.addDirectoryItem(handle, url, li, True)

    xbmcplugin.endOfDirectory(handle)

def live():
    response = urllib2.urlopen("http://cpbltv.com")

    m = re.findall(r"live_channel_1", response.read())
    if m:
        url = plugin_url + "?act=livePlay&id=1"
        li = xbmcgui.ListItem("live_channel_1")
        xbmcplugin.addDirectoryItem(handle, url, li, True)

    m = re.findall(r"live_channel_2", response.read())
    if m:
        url = plugin_url + "?act=livePlay&id=2"
        li = xbmcgui.ListItem("live_channel_2")
        xbmcplugin.addDirectoryItem(handle, url, li, True)
    
    xbmcplugin.endOfDirectory(handle)

def replay():
    response = urllib2.urlopen("http://cpbltv.com/lists.php?&offset="+ params['offset'])
    channels = re.findall(r"top.location.href=\'([\w\.\/\:\=\?]+)\';\">[0-9]+&nbsp;([\x01-\xff]{6}\sVS\s[\x01-\xff]{6})\s([\d]{4}\/[\d]{2}\/[\d]{2})", response.read())
    #channels = re.findall(r"<a href=\"([\w\.\/\:\=\?]+)\">\d+&nbsp;([\x01-\xff]{6}\sVS\s[\x01-\xff]{6})\s([\d]{4}\/[\d]{2}\/[\d]{2})", response.read())
    for channel in channels:
        gameInfo = " ".join(channel[1:])
        url = plugin_url + "?act=replayPlay&channel=" + channel[0] + "&gameInfo=" + gameInfo

        li = xbmcgui.ListItem(gameInfo)
        li.setProperty('mimetype', 'video/x-msvideo')
        #li.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle, url, li, True)
    
    offset = str(int(params['offset'])+1)
    li = xbmcgui.ListItem("more...page(" + offset + ")")
    url = plugin_url + "?act=replay&offset=" + offset
    xbmcplugin.addDirectoryItem(handle, url, li, True)

    xbmcplugin.endOfDirectory(handle)


def replayPlay():
    response = urllib2.urlopen(params['channel'])
    main_url = "http://www.cpbltv.com"
    m = re.findall(r"iframe src=\"([\/\w\.\?\&\=]+autoPlay=true)", response.read())
    url = main_url + m[0]
    response = urllib2.urlopen(url)
    url = re.findall(r"url\:\s\"([\/\w\d\-\.\:]+index.m3u8\?token1=[\w\-\d]+&token2=[\w\_\-\d]+&expire1=[\d]+&expire2=[\d]+)", response.read())
    url = str(url[0])
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    li = xbmcgui.ListItem(params['gameInfo'])
    playlist.clear()
    playlist.add(url=url, listitem=li)
    xbmc.Player().play(playlist)

def livePlay():
    response = urllib2.urlopen("http://www.cpbltv.com/vod/player.html?&type=live&width=620&height=348&id="+params['id']+"&0.9397849941728333")
    #url = "http://cpbl-hichannel.cdn.hinet.net/live/pool/cpbl-livestream03/hd-hds-pc/cpbl-livestream03.f4m?token1=lJ8EJPNtvlR5hh6kmuB1Hg&token2=tBVVO7VGJqzuDPHomlY3dA&expire1=1399396006&expire2=1399403206"    
    m = re.findall(r"var play_url = '([\?\w\d\_\&\-\=]+)", response.read())
    url = "http://cpbl-hichannel.cdn.hinet.net/live/pool/cpbl-livestream03/hd-hds-pc/cpbl-livestream03.f4m" + str(m[0])
    player = f4mProxyHelper()
    player.playF4mLink(url, "直播")


{
    'index': index,
    'replay': replay,
    'live': live,
    'replayPlay': replayPlay,
    'livePlay': livePlay,
}[params.get('act', 'index')]()
