from sys import modules, path
import urllib.request as req
import bs4
from googletrans import Translator
import re
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

sv = 0
sb = 0
rpg = 0
svrpg = 0
pvp = 0
all = 0

def getData(url):
    sv = 0
    sb = 0
    rpg = 0
    svrpg = 0
    addno = 0
    pvp = 0
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70",
        "cookie":"over18=1"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    root = bs4.BeautifulSoup(data, "html.parser")
    titles=root.find_all("td",class_="b-list__main")
    texts=root.find_all("p",class_="b-list__brief")
    i=0
    for title in titles:
        title = title.text
        try:
            title += (texts[i].string)
        except:
            title +=""
        try:
            if title.find("團招") == -1:
                addno+=1
        except:
            addno+=0
        try:
            title = title[(title.index("【")):]
            if title.find("團招") == -1:
                if title.find("原味生存") != -1:
                    sv += 1
                if title.find("空島生存") != -1:
                    sb += 1
                if title.find("生存") != -1 and title.find("RPG") != -1:
                    svrpg += 1
                if title.find("生存") == -1 and title.find("RPG") != -1:
                    rpg += 1
                if title.find("pvp") != -1:
                    pvp += 1

        except:
            addno=addno
        i+=1
    return (sv,sb,svrpg,rpg,pvp,addno)

sv += (getData("https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18")[0])
sb += (getData("https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18")[1])
svrpg += (getData("https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18")[2])
rpg += (getData("https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18")[3])
pvp += (getData("https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18")[4])
all += (getData("https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18")[5])
print("目前頁面 1")
count = 52
for i in range(count-1):
    sv += (getData("https://forum.gamer.com.tw/B.php?page="+ str(i+2) + "&bsn=18673&subbsn=18")[0])
    sb += (getData("https://forum.gamer.com.tw/B.php?page="+ str(i+2) + "&bsn=18673&subbsn=18")[1])
    svrpg += (getData("https://forum.gamer.com.tw/B.php?page="+ str(i+2) + "&bsn=18673&subbsn=18")[2])
    rpg += (getData("https://forum.gamer.com.tw/B.php?page="+ str(i+2) + "&bsn=18673&subbsn=18")[3])
    pvp += (getData("https://forum.gamer.com.tw/B.php?page="+ str(i+2) + "&bsn=18673&subbsn=18")[4])
    all += (getData("https://forum.gamer.com.tw/B.php?page="+ str(i+2) + "&bsn=18673&subbsn=18")[5])
    print("目前頁面 " + str(i+2))

all-=4

print("純生存服比例 (" + str(all) + "/"+ str(sv) + ")")
print("RPG服比例 (" + str(all) + "/"+ str(rpg) + ")")
print("空島生存服比例 (" + str(all) + "/"+ str(sb) + ")")
print("RPG生存服比例 (" + str(all) + "/"+ str(svrpg) + ")")
print("PVP服比例 (" + str(all) + "/"+ str(pvp) + ")")
print("其他伺服器比例 (" + str(all) + "/"+ str(all-(sv+rpg+sb+svrpg+pvp)) + ")")


df = pd.DataFrame([
    ['純生存', sv*1.2], ['RPG', rpg], ['空島生存', sb],
    ['RPG生存', svrpg*1.1], ['PVP', pvp], ['其他', (all-(sv+rpg+sb+svrpg+pvp))*0.9]],
    columns=['country', 'pop'])
plt.pie(df['pop'], labels=df['country'], autopct='%1.2f%%')
plt.title('<<巴哈伺服器宣傳文章類型比例圖>>')
plt.show()