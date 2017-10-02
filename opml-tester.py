#!/usr/bin/env python
"""
opml-tester - Broken Feed Checker
Copyright (C) 2017  Kazutoshi Noguchi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import listparser
import requests
from pprint import pprint
import colorama
from colorama import Fore, Style
import feedparser
import time
from datetime import datetime
from dateutil import relativedelta

colorama.init()
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; Tablet PC 2.0; rv:11.0) like Gecko"}

def get(_type, title, url):
    print("Checking {} {} ({})... ".format(_type, title, url), end='')
    sys.stdout.flush()

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + Style.BRIGHT + "NG (HTTP)" + Fore.RESET + Style.RESET_ALL)
        return None

    if len(r.history) > 0:
        print(Fore.YELLOW + Style.BRIGHT + "MOVED TO {}".format(r.url) + Fore.RESET + Style.RESET_ALL)
        return None

    return r.text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} OPML...".format(sys.argv[0]))
        sys.exit(1)

    for path in sys.argv[1:]:
        print(Fore.CYAN + Style.BRIGHT + "Checking OPML {}".format(path) + Fore.RESET + Style.RESET_ALL)
        result = listparser.parse(path)

        for feed in result.feeds:
            feed_text = get("feed", feed.title, feed.url)
            if feed_text is None:
                continue

            feed = feedparser.parse(feed_text)
            if feed.bozo:
                print(Fore.RED + Style.BRIGHT + "NG (FEED)" + Fore.RESET + Style.RESET_ALL)
                continue

            #pprint(feed)
            latest = -1
            for entry in feed.entries:
                if 'updated' in entry:
                    e_time = entry.updated_parsed
                elif 'published' in entry:
                    e_time = entry.published_parsed
                else:
                    print("?")
                    continue
                e_time_unix = time.mktime(e_time)
                latest = max(e_time_unix, latest)

            if latest == -1:
                print(Fore.GREEN + Style.BRIGHT + "OK" + Fore.RESET + Style.RESET_ALL)
            else:
                timediff = relativedelta.relativedelta(datetime.now(), datetime.fromtimestamp(latest))
                if timediff.years >= 1:
                    print(Fore.YELLOW + Style.BRIGHT + "OLD ({}yr)".format(timediff.years) + Fore.RESET + Style.RESET_ALL)
                elif timediff.months >= 6:
                    print(Fore.YELLOW + Style.BRIGHT + "OLD ({}mo)".format(timediff.months) + Fore.RESET + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + Style.BRIGHT + "OK" + Fore.RESET + Style.RESET_ALL)


        for page in result.opportunities:
            page_text = get("page", page.title, page.url)
            if not page_text is None:
                print(Fore.GREEN + Style.BRIGHT + "OK" + Fore.RESET + Style.RESET_ALL)
