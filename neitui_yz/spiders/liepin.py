# -*- coding: utf-8 -*-
import scrapy

import datetime
from neitui_yz.items import JobInfoItem

_GLB_SPIDER_NAME     = "liepin"
_GLB_ALLOWED_DOMAIN  = ["liepin.com"]
# _GLB_START_POINT_URL = "http://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key="
# the following is for Shanghai ONLY
# just to simplify the debugging
_GLB_START_POINT_URL = "http://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&dqs=020&key="
_GLB_SEARCH_KEYWORDS = ["hadoop"] #, "Python", "大数据", "技术总监"]
_GLB_START_URL_LIST  = [_GLB_START_POINT_URL + _keyword for _keyword in _GLB_SEARCH_KEYWORDS]


class LiepinSpider(scrapy.Spider):

    name = _GLB_SPIDER_NAME
    allowed_domains = _GLB_ALLOWED_DOMAIN

    start_urls = _GLB_START_URL_LIST

    nextpageflag = "下一页"
    todayflag    = datetime.datetime.now().strftime('%Y-%m-%d')

    def parse(self, response):
        """
        Function:   This function is to parse the search result list

        IN:         response - crawl response
        Out:        NA

        Special:    
        """

        # iterate each search result
        for result in response.xpath('//ul[@class="sojob-result-list"]/li'):
            # print result
            resulthref = result.xpath('.//a/@href').extract()
            resultdate = result.xpath('.//a/dl[@class="clearfix"]/dt[@class="date"]/span/text()').extract()
            if (len(resulthref) > 0) and (len(resultdate) > 0):
                detailurl  = resulthref[0]
                if resultdate[0].find(self.todayflag) == -1:
                    print resultdate[0]
                    # continue # the record is old, go on for next one
                    break

                # print detailurl
                # print detailurl.encode('utf-8')
                if detailurl.find("a.liepin.com") > -1:
                    yield scrapy.Request(detailurl, callback = self.parse_result_detail_job_hunter)
                elif detailurl.find("job.liepin.com") > -1:
                    yield scrapy.Request(detailurl, callback = self.parse_result_detail_job_view)
                else:
                    print "Unknown job info patten!"

        # iterate each page link
        for pagelink in response.xpath('//div[@class="pager"]/div[@class="pagerbar"]/a'):
            pagenumlist = pagelink.xpath('text()').extract()
            if len(pagenumlist) > 0:
                pagenum = pagenumlist[0].encode('utf-8')
                if pagenum == self.nextpageflag:
                    nextpageurl = pagelink.xpath('@href').extract()[0]
                    print "Next @ ", pagenum, nextpageurl
                    yield scrapy.Request(nextpageurl, callback = self.parse)

    def parse_result_detail_job_hunter(self, response):
        """
        Function:   This function is to parse the detail page for more information for the job position

        IN:         response - crawl response
        Out:        NA

        Special:    
        """
        
        itemfieldlist = ['job_title', 'job_salary', 'job_location', 'company_name']
        keystringdict = {
            'job_title':    '//div[@class="wrap clearfix"]/div[@class="main"]/div[@class="title"]/div[@class="title-info "]/h1/text()',
            'job_salary':   '//div[@class="wrap clearfix"]/div[@class="main"]/div[@class="title"]/div[@class="job-main "]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-main-title"]/text()',
            'job_location': '//div[@class="wrap clearfix"]/div[@class="main"]/div[@class="title"]/div[@class="job-main "]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span/text()',
            'company_name': '//div[@class="wrap clearfix"]/div[@class="main"]/div[@class="title"]/div[@class="title-info "]/h3/text()' }
        keysindexdict = {
            'job_title':    0,
            'job_salary':   0,
            'job_location': 1,
            'company_name': 0 }        
        tditemfieldlist = [
            'job_description',
            'requirement_edu', 'requirement_gender', 'requirement_language', 'requirement_major', 'requirement_anniversary',
            'company_description', 'company_address', 'company_industry', 'company_scale', 'company_property', 'company_portal' ]

        print "job_hunter"
        
        item = JobInfoItem()
        item['target_web_name'] = 'liepin'
        item['source_url']      = response.url
        item['file_name']       = response.url.split("/")[-1]
        item['job_datetime']    = datetime.datetime.now().strftime('%Y%m%d')
        for itemfield in itemfieldlist:
            item[itemfield]     = self.helper_abstract_key_info(response, keystringdict[itemfield], keysindexdict[itemfield])
        for itemfield in tditemfieldlist:
            item[itemfield]     = "To do"
        yield item

    def parse_result_detail_job_view(self, response):
        """
        Function:   This function is to parse the detail page for more information for the job position

        IN:         response - crawl response
        Out:        NA

        Special:    
        """
        
        itemfieldlist = ['job_title', 'job_salary', 'job_location', 'company_name']
        keystringdict = {
            'job_title':    '//div[@class="wrap clearfix"]/div[@class="main "]/div[@class="title"]/div[@class="title-info "]/h1/text()',
            'job_salary':   '//div[@class="wrap clearfix"]/div[@class="main "]/div[@class="title"]/div[@class="job-main "]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-main-title"]/text()',
            'job_location': '//div[@class="wrap clearfix"]/div[@class="main "]/div[@class="title"]/div[@class="job-main "]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span/text()',
            'company_name': '//div[@class="wrap clearfix"]/div[@class="main "]/div[@class="title"]/div[@class="title-info "]/h3/a/text()'}
        keysindexdict = {
            'job_title':    0,
            'job_salary':   0,
            'job_location': 1,
            'company_name': 0 }
        tditemfieldlist = [
            'job_description',
            'requirement_edu', 'requirement_gender', 'requirement_language', 'requirement_major', 'requirement_anniversary',
            'company_description', 'company_address', 'company_industry', 'company_scale', 'company_property', 'company_portal' ]

        print "job_view_enterprise"

        item = JobInfoItem()
        item['target_web_name'] = 'liepin'
        item['source_url']      = response.url
        item['file_name']       = response.url.split("/")[-1]
        item['job_datetime']    = datetime.datetime.now().strftime('%Y%m%d')
        for itemfield in itemfieldlist:
            item[itemfield]     = self.helper_abstract_key_info(response, keystringdict[itemfield], keysindexdict[itemfield])
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


