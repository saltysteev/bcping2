# bcping2
A self-hosted ping monitoring script to check status of remote hosts/ip with a status page. Built using Flask & Python

## overview
I was looking for just a simple up/down monitor that tells me if a host has a heartbeat and some timestamps. Either they were too expensive, or too loaded with unnecessary features. I couldn't believe some companies are charging $50-$100 **a month** to just check the uptime of a handfull of hosts. So I started writing this, and now my company uses it as our daily ping monitor.

Simply put, it pings (ICMP) a host IP or domain and displays the results in a simple status page. It tells you how long it's been either online, or offline, and also reports how long a host was down in a separate event page. You can add or remove hosts directly from the app.

## installation
Install the dependencies with `pip install -e .`

Run the app with `python app.py`