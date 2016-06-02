# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import traceback
import datetime
# sys.path.append("../../../")

_GBL_LINKS_FILE_NAME_FORMAT = './output/links_%s_%s.txt'
_GBL_PAGES_FILE_NAME_FORMAT = './output/job_%s_%s.txt'

class NeituiYzPipeline(object):

    """
    def __init__(self):
        self.linkfiles = {}

    def open_spider(self, spider):
        
        print "$$$$$$$$$$$$$$ Neitui Spider Opened!!! $$$$$$$$$$$$$$$$$$$$$\nSpider: ", spider.name

        try:
            linkfile = open(_GBL_LINKS_FILE_NAME_FORMAT % (spider.name, datetime.datetime.now().strftime('%Y%m%d%H%M%S')), 'w')
            self.linkfiles[spider] = linkfile
        except Exception as e:
            print "ERROR GEN FILE!! >>> "
            print traceback.format_exc()

    def close_spider(self, spider):
        print "$$$$$$$$$$$$$$ Neitui Spider Closed!!! $$$$$$$$$$$$$$$$$$$$$\nSpider: ", spider.name

        linkfile = self.linkfiles.pop(spider)
        linkfile.close()
    """
    
    def helper_print_item(self, item):
        for key in item.keys():
            if None != item[key]:
                print key, item[key]

    def process_item(self, item, spider):
        itemnamelist = [
            'source_url',
            'job_title',
            'job_location',
            'job_description',
            'requirement_edu',
            'requirement_gender',
            'requirement_language',
            'requirement_major',
            'requirement_anniversary',
            'job_salary',
            'company_name',
            'company_description',
            'company_address',
            'company_industry',
            'company_scale',
            'company_property',
            'company_portal'
        ]

        """
        try:
            print "Write page file"
            # item file open            
            pagefile = open(_GBL_PAGES_FILE_NAME_FORMAT % (spider.name, item['file_name']), 'wb')
            # file header
            pagefile.write(item['target_web_name'])
            pagefile.write(self.getJobFieldSpt())
            pagefile.write('03')
            pagefile.write(self.getJobFieldSpt())
            # item file body
            for itemname in itemnamelist:
                if item[itemname] is None:
                    pagefile.write(' ')
                else:
                    pagefile.write(item[itemname])
                pagefile.write(self.getJobFieldSpt())
            # item file tail
            pagefile.write(self.getCurrentTimestamp())
            # item file close
            pagefile.close()

            # link file record
            print "Write link file"
            self.linkfiles[spider].write(item['source_url'] + '\n')

        except Exception as e:
            print "ERROR GEN FILE!! >>> "
            print traceback.format_exc()
        """

        self.helper_print_item(item)


        # return item # Without return item, other pipelines will not get the item to process

    def getCurrentTimestamp(self):    
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def getJobFieldSpt(self):
        #得到生成的职位文件字段间的分隔符。使用ascii码1，和hive中默认的分隔符相同
        return chr(1)

