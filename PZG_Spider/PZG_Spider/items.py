# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PzgSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AgrowswItem(scrapy.Item):
    """
    公司信息
    """
    company_name = scrapy.Field()
    company_href = scrapy.Field()
    company_profile = scrapy.Field()
    company_province = scrapy.Field()
    company_city = scrapy.Field()
    contact = scrapy.Field()
    telephone = scrapy.Field()
    faxnumber = scrapy.Field()
    address = scrapy.Field()
    mailbox = scrapy.Field()
    cellphone = scrapy.Field()


class AgronetItem(scrapy.Item):
    """
    公司信息
    """
    company_name = scrapy.Field()
    company_href = scrapy.Field()
    company_profile = scrapy.Field()
    company_province = scrapy.Field()
    company_city = scrapy.Field()
    contact = scrapy.Field()
    telephone = scrapy.Field()
    faxnumber = scrapy.Field()
    address = scrapy.Field()
    mailbox = scrapy.Field()
    cellphone = scrapy.Field()


class ChinagreenhouseItem(scrapy.Item):
    company_name = scrapy.Field()
    company_href = scrapy.Field()
    company_profile = scrapy.Field()
    company_province = scrapy.Field()
    company_city = scrapy.Field()
    contact = scrapy.Field()
    telephone = scrapy.Field()
    faxnumber = scrapy.Field()
    address = scrapy.Field()
    mailbox = scrapy.Field()
    cellphone = scrapy.Field()