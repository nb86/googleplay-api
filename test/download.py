from gpapi.googleplay import GooglePlayAPI
import sys
import os
import pickle

misses = 0
def download(server, package):
    global misses
    print("-----------------------------------------")
    print('Downloading...' + package )
    try:
        download = server.download(package, expansion_files=True)
    except:
        print("!!! Package " + package + " does not exist in this Unofficial Play Store!!!!")
        misses += 1
        return
    with open('pull/' + download['docId'] + '.apk', 'wb') as first:
        for chunk in download.get('file').get('data'):
            first.write(chunk)
    print('Success!')


if os.path.isfile('saved_session'):
    with open('saved_session', 'rb') as f:
        server = pickle.load(f)
else:
    server = GooglePlayAPI("it_IT", "Europe/Rome")
    email=input("Enter your Google Play Store email: ")
    password=input("Enter your Google Play Store password: ")
    server.login(email, password)
    with open("saved_session", "wb") as f:
        pickle.dump(server, f)
    

if not os.path.exists('pull'):
    os.makedirs('pull')

with open(sys.argv[1], 'r') as f:
    allpackages = f.readlines()

for line in allpackages:
    package = line[:-5]
    download(server, package)

print("*************************************************************************")
print("Total number of missed packages from Unofficial Play Store is " + str(misses))
print("*************************************************************************")
