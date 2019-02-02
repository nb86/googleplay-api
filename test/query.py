from gpapi.googleplay import GooglePlayAPI
import time

from config import *
import argparse
import pickle
from helpers import sizeof_fmt, print_header_line, print_result_line

def download(api, package):
    print('Downloading...' + package )
    download = api.download(package, expansion_files=True)
    with open(download['docId'] + '.apk', 'wb') as first:
        for chunk in download.get('file').get('data'):
            first.write(chunk)
    print('Success!')

ap = argparse.ArgumentParser(description='Query and Download Apks from Google Play Store')
ap.add_argument('-e', '--email', dest='email', help='google username')
ap.add_argument('-p', '--password', dest='password', help='google password')
ap.add_argument('-c', '--cookie', dest='cookie', help='cookie file')
ap.add_argument('-k', '--package', dest='package', help='apk package name')
ap.add_argument('-t', '--category', dest='category', help='category')
ap.add_argument('-s', '--subcategory', dest='subcategory', help='apps_topselling_free | apps_topgrossing | apps_movers_shakers | apps_topselling_paid')
ap.add_argument('-l', '--limit', dest='limit', help='limit number of listed apps')
ap.add_argument('-o', '--offset', dest='offset', help='list apps from offset')
ap.add_argument('-f', '--field', dest='field', help='field of the apk list interested for printing, e.g: docid')
ap.add_argument('-ba', '--batch', dest='batch', help='batch download randomly top #n free in each category')

args = ap.parse_args()
api = GooglePlayAPI('it_IT', 'Europe/Rome')

######## LOGIN ############
if args.cookie is not None:
    try:
        with open(args.cookie, "rb") as f:
            api = pickle.load(f)
    except: 
        print("Can't login by cookie")
        exit(1)
else:
    try:
        api.login(args.email, args.password, None, None)
    except Exception as e:
        print("Can't login by email/password")
        exit(1)
    with open("login_cookie", "wb") as f:
        pickle.dump(api, f)
        

####### DOWNLOAD 1 APK ######
if args.package is not None:
    download(api, args.package)
    exit(0)


###### DOWNLOAD IN BATCH TOP N FREE IN EACH CATEGORY #####
if args.batch is not None:
    cat = ["Business", "Dating", "Education"]
    pkg = []
    print("Packages mining...") 
    for c in cat:
        mess = api.list(c.upper(), "apps_topselling_free", args.batch, args.offset)    
        time.sleep(2)
        for m in mess:
            pkg.append(m["docid"])
    print(pkg)
    input("Press Enter to start downloading...")
    for i in pkg:
        download(api, i)
        time.sleep(2)
    exit(0)
    


####### LIST APKS ###########
try:
    message = api.list(args.category.upper(), args.subcategory, args.limit, args.offset)
except:
    print("Error: HTTP 500 - one of the provided parameters is invalid")
    exit(1)

if (args.subcategory is None):
    print(SEPARATOR.join(["Subcategory ID", "Name"]))
    for doc in message:
        print(SEPARATOR.join([doc['docid'], doc['title']]))
else:
    if args.field is None:
        print_header_line()
        for c in message:
            print_result_line(c)
    else:
        for c in message:
            print(c[args.field])

