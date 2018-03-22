# -*- coding: utf-8 -*-
import scrapy
import json
import re
from urllib import parse
from scrapy.http import Request
from autohome.items import AutohomeItem

class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['www.autohome.com.cn',]
    chars = ['A','B','C','D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y','Z']
    # chars = ['Y']
    start = 'https://www.autohome.com.cn/grade/carhtml/'
    a = []
    for i in chars:
        a.append(start+str(i)+'.html')
    start_urls = a

    def parse(self, response):
        # brands = response.xpath('//dl[@id]/dt/div/a/text()').extract()
        # car_lines = response.xpath('//dl[@id]//dd//ul//li/h4/a').extract()
        urls = response.xpath('//dl[@id]//dd//ul//li/h4/a/@href').extract()
        for i in urls:
            # i = 'https:'+i
            i = parse.urljoin(response.url, i)
            # print(i)
            yield Request(url=parse.urljoin(response.url, i),callback=self.parse_carlines)
        # print(brands,car_lines,urls)

    def parse_carlines(self,response):
        firmy = response.xpath('//div[@class="subnav-title-name"]/a/text()').extract_first('')
        try:
            firm = firmy.split('-')[0]
        except:
            firm = ''
        if 'title-nav' in response.text:
            urls = response.xpath('//div[@class="tabwrap"]//tr/td/div/a[@title]/@href').extract()
            for i in urls:
                uri = 'https://www.autohome.com.cn/'
                yield Request(url=parse.urljoin(uri, i), callback=self.parse_detail,meta={"sale":2,"firm":firm})
        else:
            urls = response.xpath('//div[@class="interval01 interval-new"]//p/a/@href').extract()
            for i in urls:
                yield Request(url=parse.urljoin(response.url, i), callback=self.parse_detail,meta={"sale":1,"firm":firm})
            # / spec / 25901 /  # pvareaid=101605
            s = response.url.split('/')[3]
            # print(s)
            years = response.xpath('//div[@id="drop2"]//li/a/text()').extract()
            ys = response.xpath('//div[@id="drop2"]//li/a/@data').extract()
            # t_urls = []
            for i in range(len(years)):
                url = 'https://www.autohome.com.cn/ashx/series_allspec.ashx?s=' + s + '&y=' + ys[i]
                yield Request(url=parse.urljoin(response.url, url), callback=self.parse_sale,meta={"sale":2,"year":years[i],"firm":firm})

    def parse_sale(self,response):
        a = json.loads(response.text)
        year = response.meta.get("year", "")
        firm = response.meta.get("firm","")
        for i in a['Spec']:
            i = 'https://www.autohome.com.cn/spec/'+str(i['Id'])+'/'
            yield Request(url= i,callback=self.parse_detail,meta={"sale":2,"year":year,"firm":firm})

    def parse_detail(self,response):
        # url = response.xpath('//li[@class="nav-item"][1]/a/@href').extract_first('')
        # yield Request(url=parse.urljoin(response.url,url),callback=self.parse_peizhi)
        name = response.xpath('//div[@class="subnav-title-name"]/a/h1/text()').extract_first('')
        try:
            year = re.search(r'\d{2,4}',name).group()
        except:
            year = ''
        if not year:
            try:
                year = response.meta.get("year", "")
                year = re.search(r'\d{2,4}', year).group()
            except:
                year = ''
        title_return = response.xpath('//div[@class="subnav-title-return"]/a/text()').extract_first('')
        try :
            car_line = re.search(r"返回 (.*)频道",title_return).group(1)
            print(car_line)
            # car_line = title_return.split(' ')[1]
        except Exception as e:
            print(e)
            # car_line = ''
        dgp = response.xpath('//ul/li[@id="cityDealerPrice"]/span/span/text()').extract_first('')
        msrp = response.xpath('//li[@class="li-price fn-clear"]/span/@data-price').extract_first('')
        second_price =response.xpath('//div[@class="fn-left ml10"]/a/text()').extract_first('')
        sale = response.meta.get("sale", "")
        firm = response.meta.get("firm", "")

        # 配置
        # peizhi = response.xpath('//div[@class="cardetail-infor-car"]/ul/li').extract()
        # print(peizhi)

        pingfen = response.xpath('//ul/li[1]/a[2]/text()').extract_first('')
        oil_wear = response.xpath('//ul/li[@class="cardetail-right"][1]/a/text()').extract_first('')
        structure = response.xpath('//div[@class="cardetail-infor-car"]//ul[@class="fn-clear"]/li[3]/text()').extract_first('')
        stru = structure.split('*')
        longth = stru[0]
        width = stru[1]
        height = stru[2]
        warranty = response.xpath('//ul/li[6]/text()').extract_first('')
        engine = response.xpath('//div[@class="cardetail-infor-car"]/ul/li[7]/text()').extract_first('')
        enginel = engine.split(' ')
        try:
            gas = re.search(r'\d+\.{0,1}\d*',enginel[0]).group()
            air_out = re.search(r'[A-Z]+',enginel[0]).group()
            engine_power = enginel[1]
            place = re.search(r'[A-Z]+',enginel[2]).group()
            cylinder = re.search(r'\d+',enginel[2]).group()
        except:
            gas = ''
            air_out = ''
            engine_power = ''
            place = ''
            cylinder = ''
        gear_box = response.xpath('//div[@class="cardetail-infor-car"]/ul/li[8]/text()').extract_first('')
        drive_mode = response.xpath('//ul/li[9]/text()').extract_first('')
        link = response.url
        level = response.xpath('//div[@class="breadnav fn-left"]//a[2]/text()').extract_first('')

        auto_item = AutohomeItem()

        auto_item["car_line"] = car_line
        auto_item["firm"] = firm
        auto_item["level"] = level
        auto_item["name"] = name
        auto_item["year"] = year
        auto_item["engine"] = engine
        auto_item["gas"] = gas
        auto_item["air_out"] = air_out
        auto_item["engine_power"] = engine_power
        auto_item["place"] = place
        auto_item["cylinder"] = cylinder
        auto_item["gear_box"] = gear_box
        auto_item["longth"] = longth
        auto_item["width"] = width
        auto_item["height"] = height
        auto_item["structure"] = structure
        auto_item["oil_wear"] = oil_wear
        auto_item["warranty"] = warranty
        auto_item["sale"] = sale
        auto_item["link"] = link
        auto_item["dgp"] = dgp
        auto_item["msrp"] = msrp
        auto_item["second_price"] = second_price
        auto_item["drive_mode"] = drive_mode
        auto_item["pingfen"] = pingfen

        yield auto_item









    # def parse_peizhi(self,response):
    #     # yield Request(url=parse.urljoin(response.url,), callback=self.parse_peizhi)
    # 用户评分：暂无
    # 车主油耗：暂无
    #
    # 车身尺寸：4925 * 1860 * 1470
    # 综合油耗：6.8
    # L / 100
    # km(工信部)
    # 车身结构：4
    # 门5座三厢车
    # 整车质保：三年不限公里
    # 发 动 机：2.0
    # T
    # 184
    # 马力
    # L4
    # 变 速 箱：9
    # 挡手自一体
    # 驱动方式：前置后驱
    # 查看详细参数配置 >>
