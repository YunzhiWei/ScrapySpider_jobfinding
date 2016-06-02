# -*- coding: utf-8 -*-
import scrapy

import datetime
from neitui_yz.items import JobInfoItem


_GLB_SPIDER_NAME     = "zhaopin000"
_GLB_ALLOWED_DOMAIN  = ["zhaopin.com"]
_GLB_START_POINT_URL = "http://sou.zhaopin.com"
_GLB_SEARCH_KEYWORDS = ["hadoop"] #, "Python", "大数据", "技术总监"]
_GLB_START_URL_LIST  = [_GLB_START_POINT_URL + _keyword for _keyword in _GLB_SEARCH_KEYWORDS]


class NeituiSpider(scrapy.Spider):

    name = _GLB_SPIDER_NAME
    allowed_domains = _GLB_ALLOWED_DOMAIN

    start_urls = _GLB_START_URL_LIST

    todayflag  = "10-" # datetime.datetime.now().strftime('%m-%d')

    def parse(self, response):
        """
        Function:   This function is to parse the search result list

        IN:         response - crawl response
        Out:        NA

        Special:    
        """

        # iterate each search result to see if there is any new for today
        # if yes, try to get the link and invoke parse_result_detail for details
        for result in response.xpath('//div[@id="joblist"]/div[@class="content commentjobs brjobs topjobs"]/ul/li'):
            # print result
            resulthref = result.xpath('div[@class="cont"]/div[@class="jobnote clearfix"]/div[@class="jobnote-l"]/a/@href').extract()
            resultdate = result.xpath('div[@class="cont"]/div[@class="jobmore display"]/span[@class="createtime"]/text()').extract()
            if (len(resulthref) > 0) and (len(resultdate) > 0):
                detailurl  = "http://www." + _GLB_ALLOWED_DOMAIN[0] + resulthref[0].encode('utf-8')
                if resultdate[0].find(self.todayflag) == -1:
                    print resultdate[0], self.todayflag
                    # continue # the record is old, go on for next one
                    break

                # print detailurl
                yield scrapy.Request(detailurl, callback = self.parse_result_detail)

        # try to find if there is the next page link in the current search result
        # if yes, try to get the link and invoke this parse to process
        pagelinks = response.xpath('//div[@class="t_pagelink"]/p[@class="page"]/a[@class="next"]/@href').extract()
        if len(pagelinks) > 0:
                nextpageurl = "http://www." + _GLB_ALLOWED_DOMAIN[0] + pagelinks[0].encode('utf-8')
                print "Next @ ", nextpageurl
                yield scrapy.Request(nextpageurl, callback = self.parse)

    def parse_result_detail(self, response):
        """
        Function:   This function is to parse the detail page for more information for the job position

        IN:         response - crawl response
        Out:        NA

        Special:    
        """
        
        itemfieldlist = ['job_title', 'job_salary', 'job_location', 'company_name']
        keystringdict = {
            'job_title':    '//div[@id="neituiDetail"]/div[@class="maincontent"]/div[@id="detail"]/div/ul[@class="clearfix"]/li/div[@class="cont"]/div[@class="jobnote"]/strong/text()',
            'job_salary':   '//div[@id="neituiDetail"]/div[@class="maincontent"]/div[@id="detail"]/div/ul[@class="clearfix"]/li/div[@class="cont"]/div[@class="jobnote"]/span[@class="padding-r10 pay"]/text()',
            'job_location': '//div[@id="neituiDetail"]/div[@class="maincontent"]/div[@id="detail"]/div/ul[@class="clearfix"]/li/div[@class="cont"]/div[@class="jobtitle"]/span[@class="jobtitle-r"]/text()',
            'company_name': '//div[@id="neituiDetail"]/div[@class="maincontent"]/div[@id="detail"]/div/ul[@class="clearfix"]/li/div[@class="cont"]/div[@class="jobtitle"]/span[@class="jobtitle-l"]/text()' }
        tditemfieldlist = [
            'job_description',
            'requirement_edu', 'requirement_gender', 'requirement_language', 'requirement_major', 'requirement_anniversary',
            'company_description', 'company_address', 'company_industry', 'company_scale', 'company_property', 'company_portal' ]

        item = JobInfoItem()
        item['target_web_name'] = 'neitui'
        item['source_url']      = response.url
        item['file_name']       = response.url.split("/")[-1]
        item['job_datetime']    = datetime.datetime.now().strftime('%Y%m%d')
        for itemfield in itemfieldlist:
            item[itemfield]     = self.helper_abstract_key_info(response, keystringdict[itemfield])
        for itemfield in tditemfieldlist:
            item[itemfield]     = "To do"
        yield item

    def helper_abstract_key_info(self, response, keystr, idx = 0):
        """
        Function:   This helper function for the routain job of xpath process

        IN:         response - crawl response
                    keystr - string to locate the key information in the xpath
        Out:        NA

        Special:    
        """

        strlist = response.xpath(keystr).extract()
        if len(strlist) > idx:
            return strlist[idx].encode('utf-8')
        else:
            return None

