# -*- coding: utf-8 -*-
import scrapy

class GischemSpider(scrapy.Spider):
    name = "gischem"
    allowed_domains = ["www.gischem.de"]
    start_urls = (
        'http://www.gischem.de/suche/liste.htm',
    )

    def parse(self, response):

        list_urls = response.xpath('//a[contains(@href, "liste.htm?client_request")]/@href').extract()
        for url in list_urls:
            yield scrapy.Request('http://www.gischem.de/suche/%s' % url, callback=self.parse)

        overview_urls = response.xpath('//a[contains(@href, "uebersicht.htm?client_session_Dokument")]/@href').extract()
        for overview_url in overview_urls:
            yield scrapy.Request('http://www.gischem.de/suche/%s' % overview_url, callback=self.parse)

        document_urls = response.xpath('//a[contains(@href, "dokument.htm?client_session_Dokument=")]/@href').extract()
        for url in document_urls:
            yield scrapy.Request('http://www.gischem.de/suche/%s' % url, callback=self.parse_document)

    def parse_document(self, response):
        betriebsanweisung_xpath = '//div[contains(@class, "ueberschrift") and contains(text(), "Betriebsanweisungsentwurf")]'
        is_betriebsanweisung = len(response.xpath(betriebsanweisung_xpath)) > 0

        name = response.css('h1.Hsuche::text').extract_first()
        ghs_doc = response.xpath('//*[contains(*/text(), "GHS") and contains(@href, "DOC")]/@href').extract_first()

        if is_betriebsanweisung and ghs_doc:

            ghs_doc = ghs_doc.replace('../', '')

            self.logger.info('Response URL: %s' % response.url)
            self.logger.info('GHS Doc: %s/%s' % ('http://www.gischem.de', ghs_doc))

            yield {
                 'substance': name,
                 'file_urls': ['%s/%s' % ('http://www.gischem.de', ghs_doc)]
            }
