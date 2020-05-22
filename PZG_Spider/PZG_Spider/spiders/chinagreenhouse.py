# -*- coding: utf-8 -*-
"""
@Authon:zdd
@desc:中国温室网-公司库
"""

import scrapy
from pyquery import PyQuery as pq
from PZG_Spider.items import ChinagreenhouseItem
import logging
log = logging.getLogger(__name__)

class ChinagreenhouseSpider(scrapy.Spider):
    name = 'chinagreenhouse'
    allowed_domains = ['www.chinagreenhouse.com']
    start_urls = ['http://www.chinagreenhouse.com/company/?page=1']

    def parse(self, response):
        item = ChinagreenhouseItem()
        doc = pq(response.body)
        all_company = doc(".b_list li")   # 通过 pyqurery 获取所有企业
        for company in all_company.items():   # 循环所有企业
            company_name = ""
            company_href = ""  # 获取公司网站
            company_profile = ""  # 公司简介
            company_province = ""  # 公司所在省份
            company_city = ""  # 公司所在城市
            contact = ""  # 联系人
            telephone = ""  # 电话
            faxnumber = ""  # 传真
            address = ""  # 地址
            mailbox = ""  # 邮箱
            cellphone = ""  # 手机号
            try:
                # 解析公司信息
                split_com = company("a strong").text().split('所在地：')
                company_name = split_com[0]
                company_province = split_com[1]
                company_href = company("a").attr("href")
                company_profile = company("span").text().split('[已核实]')[0].strip()

                # 解析公司联系方式
                if company_href:
                    html_text = pq(company_href, encoding='utf-8')  # 用pyquery解析html文件
                    contact = html_text(".spb .r .r .t").text()

                    contact_list = html_text(".spb .r .r .b li")
                    if contact_list and len(contact_list) > 0:
                        for contact_l in contact_list.items():
                            li_con = str(contact_l("li"))
                            split_cellphone = li_con.split('手机：')
                            split_telephone = li_con.split('电话：')
                            split_faxnumber = li_con.split('传真：')
                            split_address = li_con.split('地址：')
                            split_mailbox = li_con.split('邮箱：')

                            if split_cellphone and len(split_cellphone) > 1:
                                cellphone = split_cellphone[1].split('</li>')[0]
                            if split_telephone and len(split_telephone) > 1:
                                telephone = split_telephone[1].split('</li>')[0]
                            if split_faxnumber and len(split_faxnumber) > 1:
                                faxnumber = split_faxnumber[1].split('</li>')[0]
                            if split_address and len(split_address) > 1:
                                address = split_address[1].split('</li>')[0]
                            if split_mailbox and len(split_mailbox) > 1:
                                mailbox = split_mailbox[1].split('</li>')[0]

                    item["company_name"] = company_name
                    item["company_href"] = company_href
                    item["company_profile"] = company_profile
                    item["company_province"] = company_province
                    item["company_city"] = company_city
                    item["contact"] = contact
                    item["telephone"] = telephone
                    item["faxnumber"] = faxnumber
                    item["address"] = address
                    item["mailbox"] = mailbox
                    item["cellphone"] = cellphone

                    yield item  # 把取到的数据提交给pipline处理
            except Exception as e:
                log.exception(e)

        # css选择器提取下一页链接
        # next_page = response.css('div.page a:last-child::attr(href)').extract_first()
        # next_page = doc('.page a:last-child').attr("href")
        next_page = doc('#destoon_next').attr("value")
        print(next_page)
        if next_page is not None:  # 判断是否存在下一页
            next_page = response.urljoin(next_page)

            yield scrapy.Request(next_page, callback=self.parse)