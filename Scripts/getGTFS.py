import os
import requests
import zipfile
from transitfeeds import TransitFeeds

API_KEY = os.environ.get("GTFSFeed")
tf = TransitFeeds(API_KEY)
i = 0
# os.chdir("..")
print("WD: "+os.getcwd())
feedid = 'sptrans/1049'

for c in range(30):
    versions = tf.feed_versions(feedid, page=c)

    for v in versions:
        print("############## FEED "+str(i)+" ##############")
        print("ID: "+v.id)
        date = v.id[13:]
        dirName = 'DATA/SPTRANS/'+date
        try:
            os.makedirs(dirName)
            print("DIRETORIO ", dirName,  " CRIADO ")
        except FileExistsError:
            print("DIRETORIO ", dirName,  " JÁ EXISTE")
        print("LINK: "+v.url)
        url = v.url
        myfile = requests.get(url)
        open(os.getcwd()+"/"+dirName+"/GTFS.zip", 'wb').write(myfile.content)
        print("DOWNLOAD FEITO")
        with zipfile.ZipFile(os.getcwd()+"/"+dirName+"/GTFS.zip", 'r')\
                as zip_ref:
            zip_ref.extractall(os.getcwd()+"/"+dirName)
        i = 1+i

print("FIM DO PROCESSO")
