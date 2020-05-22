# -*- coding: utf-8 -*-

"""
@Authon:zdd
@desc:中国温室网-企业名录
"""
import scrapy
from pyquery import PyQuery as pq
from PZG_Spider.items import AgrowswItem
import requests
import logging
log = logging.getLogger(__name__)

class AgrowswSpider(scrapy.Spider):
    name = 'agrowsw'                                # 爬虫名称
    allowed_domains = ['www.agrowsw.com']      # 允许爬取的域名列表
    start_urls = ['http://www.agrowsw.com/Company?page=104']  # 开始爬取的资源链接列表

    def parse(self, response):
        # with open("Company.html", 'w', encoding='utf-8') as f:
        #     f.write(str(response.body))

        item = AgrowswItem()
        doc = pq(response.body)
        all_company = doc(".n_jiaru .gs_mc")            # 通过 pyqurery 获取所有企业
        for company in all_company.items():             # 循环所有企业
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
                company_name = company("strong").text()     # 获取公司名称
                company_href = company("strong a").attr("href")     # 获取公司网站
                if company_href:
                    res = requests.get(company_href)
                    url_encoding = res.encoding     # 获取编码格式
                    html_text = pq(company_href, encoding=url_encoding)  # 用pyquery解析html文件

                    company_profile = html_text('.company_name span').text()    # 公司简介
                    contact_list = html_text(".contact_l li")
                    if not str(contact_list).strip():
                        contact_list = html_text(".left_tel li")

                    # 循环获取联系人信息
                    for contact_l in contact_list.items():
                        strong_name = str(contact_l("strong").text()).replace(u'\xa0', '').replace(' ', '')
                        if not strong_name:
                            strong_name = str(contact_l("b").text()).replace(u'\xa0', '').replace(' ', '')
                        strong_value = str(contact_l("span").text()).replace(u'\xa0', '').replace(' ', '')
                        if '联系人' in strong_name:
                            contact = strong_value
                        if '电话' in strong_name:
                            telephone = strong_value
                        if '传真' in strong_name:
                            faxnumber = strong_value
                        if '地址' in strong_name:
                            address = strong_value
                        if '邮箱' in strong_name:
                            mailbox = strong_value
                        if '手机' in strong_name:
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
            except Exception as e:
                log.exception(e)

        # css选择器提取下一页链接
        next_page = response.css('div.Pager a:last-child::attr(href)').extract_first()
        print(next_page)
        if next_page is not None:  # 判断是否存在下一页
            next_page = response.urljoin(next_page)

            yield scrapy.Request(next_page, callback=self.parse)


