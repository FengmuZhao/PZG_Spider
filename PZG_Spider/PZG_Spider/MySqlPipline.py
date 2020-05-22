import pymysql.cursors
import datetime
import time


class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='pzg_spider',  # 数据库名
            user='root',  # 数据库用户名
            passwd='zhaodd',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item and item['company_name']:
            # 判定公司是否已经插入
            company_Count = self.check_company(item['company_name'])
            if company_Count == 0:
                self.cursor.execute(
                    """insert into pzg_company(company_name, company_href, company_profile, company_province, company_city, 
                                               contact, telephone, faxnumber, address, mailbox, 
                                               cellphone)
                                    value (%s, %s, %s, %s, %s, 
                                            %s, %s, %s, %s, %s, 
                                            %s)""",
                    (item['company_name'], item['company_href'], item['company_profile'], item['company_province'], item['company_city'],
                     item['contact'], item['telephone'], item['faxnumber'], item['address'], item['mailbox'],
                     item['cellphone'])
                )
                # 提交sql语句
                self.connect.commit()
        return item

    def check_company(self, company_name):
        # 定义sql
        sql = "select count(*) from pzg_company where company_name = '%s' " % company_name
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]