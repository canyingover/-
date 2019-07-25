# -*- coding: utf-8 -*-
# @Author: n4663
# @Date:   2019-07-25 19:41:45
# @Last Modified by:   n4663
# @Last Modified time: 2019-07-25 19:42:11


import requests
from lxml import etree
import json
import codecs

html = etree.HTML(r.text,etree.HTMLParser())
r = requests.get("https://pvp.qq.com/web201605/herolist.shtml")
r.encoding = 'GB2312'
urls = html.xpath('//ul[@class="herolist clearfix"]/li/a/@href')



result = codecs.open(u"C:/Users/n4663/Desktop/王者荣耀爬虫/result.json",'w',encoding="utf-8")

zhaohuan_json = json.load(open(u'C:/Users/n4663/Desktop/王者荣耀爬虫/summoner.json'))
zhaohuan_dict = {}
for i in zhaohuan_json:

    zhaohuan_dict.setdefault(i["summoner_id"],[])
    zhaohuan_dict[i["summoner_id"]].append(i["summoner_name"])



mingwen_json = json.load(open(u'C:/Users/n4663/Desktop/王者荣耀爬虫/ming.json'))
mingwen_dict = {}
for i in mingwen_json:
    mingwen_dict.setdefault(i["ming_id"],[])
    mingwen_dict[i["ming_id"]].append(i["ming_name"])
    mingwen_dict[i["ming_id"]].append(i["ming_des"])


def id_map_name(x,d):
    return d[x]



for i in urls:
    url = "https://pvp.qq.com/web201605/" + i
    print url
    r = requests.get(url)

    r.encoding = 'GB2312'
    html = etree.HTML(r.text,etree.HTMLParser())
    # 英雄名称
    name = html.xpath("//h2[contains(@class,'cover-name')]/text()")

    # 英雄定位
    ty=html.xpath('/html/body/div[@class="wrapper"]/div[1]/div/div/div[1]/span/i/attribute::*')

    # 技能简介
    jns=html.xpath('//p[@class="skill-desc"]/text()')
    jinengjianjie = "@^".join(jns)

    # 技能升级建议
    jn_sugg=html.xpath('//p[@class="icon sugg-skill"]/img/@alt')

    zhusheng =  jn_sugg[0]
    fusheng =  jn_sugg[1]

    # 召唤师技能
    zhaohuan_sugg = html.xpath('//div[@class="sugg-info2 info"]/p[@id="skill3"]/@data-skill')[0].split("|")
    zhanhuan_suggs = map(lambda x:zhaohuan_dict[int(x.split("/")[-1].split(".")[0])],zhaohuan_sugg)
    zhanhuan_sugg_1 = zhanhuan_suggs[0][0]
    zhanhuan_sugg_2 = zhanhuan_suggs[1][0]




    # 铭文
    mingwen_sugg = html.xpath('//div[@class="sugg-info info"]/ul/@data-ming')[0].split("|")
    mingwentuijian1 =  ":".join(map(lambda x:mingwen_dict[x],mingwen_sugg)[0]).replace("<p>","").replace("</p>",",")[0:-1]
    mingwentuijian2 =  ":".join(map(lambda x:mingwen_dict[x],mingwen_sugg)[1]).replace("<p>","").replace("</p>",",")[0:-1]
    mingwentuijian3 =  ":".join(map(lambda x:mingwen_dict[x],mingwen_sugg)[2]).replace("<p>","").replace("</p>",",")[0:-1]

    # 英雄关系
    data = html.xpath('//div[@class="hero-list hero-relate-list fl"]/ul/li/a/img/@src')
    zuijiadada = data[0:2]
    yazhiyingxiong = data[2:4]
    beiyazhiyingxiong = data[4:6]

    # 英雄故事
    yingxionggushi = ''.join(html.xpath('//div[@class="pop-bd"]/p/text()'))
    log = "\t".join([name[0],ty[0],
                     jinengjianjie,
                     yingxionggushi,
                     zuijiadada[0],
                     zuijiadada[1],
                     yazhiyingxiong[0],
                     yazhiyingxiong[1],
                     beiyazhiyingxiong[0],
                     beiyazhiyingxiong[1],
                     zhusheng,fusheng,
                     zhanhuan_sugg_1,zhanhuan_sugg_2,
                     mingwentuijian1,mingwentuijian2,mingwentuijian3])
    result.write(log+"\n")

