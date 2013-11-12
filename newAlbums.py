#! /usr/bin/python3
# -*- coding: utf-8 -*-

#    Launch alerts with new upcoming albums from a rateyourmusic profile page.
#    Copyright (C) 2012  Juan "Nito" Pou  juanpou@ono.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from re import findall, compile
from urllib.request import urlopen, Request
from datetime import date, timedelta
from gi.repository import Notify

RYMUSER = "killa119"
DAYSTOWATCH = 15
#Time showing the alert in seconds
SHOWTIME = 20

RYMMONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def transform(stringdate):
    """ transforms a date like 'Oct 20' into a date type object
    """
    splitteddate = stringdate.split(" ")
    month = int(RYMMONTHS.index(splitteddate[0]) + 1)
    day = int(splitteddate[1])

    transformeddate = date(today.year, month, day)
    diffdays = abs((transformeddate - today).days)
    if diffdays > 180:
        #the year is not right
        if month > 6:
            transformeddate = date(today.year + 1, month, day)
        else:
            transformeddate = date(today.year - 1, month, day)
    return transformeddate


url = "http://rateyourmusic.com/~" + RYMUSER

req = Request(url, headers={'User-Agent': "Magic Browser"})
con = urlopen(req)
html = con.read()
dayRegex = compile(b'<div style="text-align:right;color:#bbb">(.*)<div style="text-align:right;color:#bbb">')
upcomingText = findall(dayRegex, html)
upcomingText = upcomingText[0].decode("utf-8").split("<div style=\"text-align:right;color:#bbb\">")

today = date.today()

for daytext in upcomingText:
    dayRegex = compile(b'<b>(.{6})</b>')
    artistRegex = compile(b'class="artist">(.{1,50})</a>')
    albumRegex = compile(b'class="album">(.{1,50})</a>')
    launchDayText = findall(dayRegex, daytext.encode(encoding='UTF-8'))
    launchDay = transform(launchDayText[0].decode("utf-8"))
    if today <= launchDay <= today + timedelta(days=DAYSTOWATCH):
        if launchDay > today + timedelta(days=DAYSTOWATCH):
            break
        artistText = findall(artistRegex, daytext.encode(encoding='UTF-8'))
        albumText = findall(albumRegex, daytext.encode(encoding='UTF-8'))
        resultText = ""
        for i in range(len(artistText)):
            resultText = resultText + artistText[i].decode("utf-8") + "\n" + albumText[i].decode("utf-8") + "\n\n"
        Notify.init("newAlbums")
        notification = Notify.Notification.new(str(launchDay), resultText, None)
        notification.set_urgency(urgency=Notify.Urgency.NORMAL)
        notification.set_timeout(SHOWTIME * 1000)
        notification.show()