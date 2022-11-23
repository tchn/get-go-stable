#!/bin/env python3
import json
from optparse import OptionParser
import requests

go_dev_url: str = "https://go.dev/dl/"
res_mode: str = "json"
os: str = "linux"
arch: str = "amd64"
url2get_go_stables: str = go_dev_url + "?mode=" + res_mode #"https://go.dev/dl/?mode=json"

# main
def main( options ):
    res_http = requests.get(url2get_go_stables)
    raw_json = json.loads(res_http.text)
    go_stables: list = [ x["version"] for x in raw_json if x["stable"] == True ]
    go_stable_filename: str = f"%s.%s-%s.tar.gz" % (go_stables[0], os, arch)
    go_stable_filepath: str = f"%s/%s" % (options.outdir, go_stable_filename)
    go_dev_dl_url : str = f"%s/%s" % (go_dev_url, go_stable_filename) #https://go.dev/dl/go1.19.3.linux-amd64.tar.gz

    r = requests.get(go_dev_dl_url, stream=True)
    with open(go_stable_filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

if __name__ == '__main__':
    opt_parser = OptionParser()
    opt_parser.add_option("-o", "--outdir", dest="outdir", type="string", 
                  help="directory to save file in", default="./")
    (options, args) = opt_parser.parse_args()
    main( options )