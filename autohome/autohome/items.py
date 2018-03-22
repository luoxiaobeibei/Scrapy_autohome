# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # brand = scrapy.Field()#品牌
    car_line = scrapy.Field()#车系1
    firm = scrapy.Field()#厂商1
    level = scrapy.Field()#级别
    # energy = scrapy.Field()#能源类型
    # ttm = scrapy.Field()#上市时间
    # max_power = scrapy.Field()#最大功率
    # max_torque = scrapy.Field()#最大扭矩
    name = scrapy.Field()#1
    year = scrapy.Field()#1
    engine = scrapy.Field()#发动机1
    gas = scrapy.Field()#排气量1
    air_out = scrapy.Field()#排气方式1
    engine_power = scrapy.Field()#发动机最大功率1
    place = scrapy.Field()#排列方式1
    cylinder = scrapy.Field()#气缸数1
    gear_box = scrapy.Field()#变速箱1
    longth = scrapy.Field()#长1
    width = scrapy.Field()#宽1
    height = scrapy.Field()#高1
    structure = scrapy.Field()#车身结构
    # max_speed = scrapy.Field()#最高车速
    # lingbai = scrapy.Field()#零百加速
    oil_wear = scrapy.Field()#车主油耗1
    warranty = scrapy.Field()#整车质保1
    sale = scrapy.Field()#是否在售1
    link = scrapy.Field()#所在链接1
    dgp = scrapy.Field()#经销商指导价 Distributor guide price1
    msrp = scrapy.Field()#厂商指导价 Manufacturer's suggested retail price1
    # first_price = scrapy.Field()#全款购车价格
    second_price = scrapy.Field()#二手指导价格1
    drive_mode = scrapy.Field()#驱动方式1
    pingfen = scrapy.Field()#1评分
