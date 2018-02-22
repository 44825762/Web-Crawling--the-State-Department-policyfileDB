import requests
from lxml import etree
import pymysql

def getinner(url):
    page = requests.get(url)
    page.encoding = "utf-8"
    html = etree.HTML(page.text)
    table = html.xpath('//table[@class="bd1" ]')

    # 文件标题
    try:
        if table[0].xpath("normalize-space(string(.))") != '':
            title=table[0].xpath("normalize-space(string(.))")
            title_str=title.split(' ')
            if len(title_str) > 15:
                search_num=title_str[3]#索引号
                theme=title_str[5]#主题分类
                send_office=title_str[7]#发文机关
                achieve_date=title_str[9]#成文日期
                headline=title_str[11]#标题
                send_num=title_str[13]#发文字号
                send_date=title_str[15]#发布日期

                # 文件内容
                content_list = html.xpath('//td[@class="b12c"]/p')
                content_index = 0
                for i in content_list:
                    if i != ' ':
                        content_index += 1
                data_contant = ""
                for i in range(content_index):
                    p = content_list[i]
                    data_contant += str(p.xpath("string(.)") + "\n")

                sql = "insert into policy(search_num,theme,send_office,achieve_date,headline,send_num,send_date,contant) values('" + search_num + "','" + theme + "','" + send_office + "','" + achieve_date + "','" + headline + "','" + send_num + "','" + send_date + "','" + data_contant + "');"
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    connection.commit()
    except Exception as e:
        print(e)
        print(url)

def spyider(url):
    page = requests.get(url)
    html = etree.HTML(page.text)
    urllist = html.xpath('//td[@class="info"]/a/@href')
    index = 0
    for i in urllist:
        if i != '':
            index += 1
    for i in range(index):
        if urllist[i]!="http://172.31.16.4/website-webapp/wcm/initEdit_manuscript.action?websiteId=w1&manuscriptId=5151747&status=1&channelId=gc283&nextManuscriptId=5125001&prevManuscriptId=&viewStatus=3#":
            getinner(urllist[i])

if __name__ == '__main__':
    config = {  # mysql连接配置
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'db': 'gwy',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
    }
    connection = pymysql.connect(**config)   #获取连接
    p=0
    for i in range(101):
        url = "http://sousuo.gov.cn/list.htm?q=&n=200&p="+str(i)+"&t=paper&sort=pubtime"
        spyider(url)

    print("完成")

