#!/usr/local/bin/python3
import argparse
from lal_modules.webui import DEFAULT_PORT, run

####################################
#### Main program goes here
####################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'台灣郵局存證信函產生器 Web UI')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=u'伺服器埠號')
    parser.add_argument('--no-browser', action='store_true', help=u'啟動後不自動開啟瀏覽器')
    args = parser.parse_args()
    run(port=args.port, open_browser=not args.no_browser)
