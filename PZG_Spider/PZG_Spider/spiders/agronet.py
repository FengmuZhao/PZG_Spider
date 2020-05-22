# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq
from PZG_Spider.items import AgronetItem

class AgronetSpider(scrapy.Spider):
    name = 'agronet'
    allowed_domains = ['www.agronet.com.cn']
    start_urls = ['http://www.agronet.com.cn/Company/List_oc193.html']

    def parse(self, response):
        # with open("Company.html", 'w', encoding='utf-8') as f:
        #     f.write(str(response.body))
        print('3333333333333333333333333')
        item = AgronetItem()
        doc = pq(response.body)
        all_company = doc(".main dd ul li")  # 通过 pyqurery 获取所有企业
        for company in all_company.items():  # 循环所有企业
            company_name = company("h3 strong a").text()  # 获取公司名称
            company_href = company("h3 strong a").attr("href")  # 获取公司网站
            company_profile = ""    # 公司简介
            company_province = ""   # 公司所在省份
            company_city = ""       # 公司所在城市
            contact = ""            # 联系人
            telephone = ""          # 电话
            faxnumber = ""          # 传真
            address = ""            # 地址
            mailbox = ""            # 邮箱
            cellphone = ""          # 手机号
            contact_list = []
            if company_href:
                html_text = pq(company_href, encoding='utf-8')  # 用pyquery解析html文件
                contact_list = html_text(".contact_l li")
            if contact_list and len(contact_list) > 0:
                # 循环获取联系人信息
                for contact_l in contact_list.items():
                    li_con = contact_l("li")
                    strong_name = str(li_con("strong").text()).strip()
                    strong_value = li_con("span").text().strip()
                    if '联系人：' in strong_name:
                        contact = strong_value
                    if '电   话：' in strong_name:
                        telephone = strong_value
                    if '传   真：' in strong_name:
                        faxnumber = strong_value
                    if '地   址：' in strong_name:
                        address = strong_value
                    if '邮   箱：' in strong_name:
                        mailbox = strong_value
                    if '手   机：' in strong_name:
                        cellphone = strong_value

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

        # css选择器提取下一页链接
        # next_page = response.css('div.Pager a:last-child::attr(href)').extract_first()
        # if next_page is not None:  # 判断是否存在下一页
        #     next_page = response.urljoin(next_page)
        #
        #     yield scrapy.Request(next_page, callback=self.parse)

