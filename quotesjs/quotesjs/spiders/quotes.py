import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    script = '''
    function main(splash, args)
        splash.private_mode_enabled = false
        headers = {
            ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        splash:on_request(function(res)
            splash:set_custom_headers(headers)
        end)
        assert(splash:go(args.url))
        assert(splash:wait(1))

        return {
            html = splash:html()
        }
    end
    '''


    def start_requests(self):
        start_url = 'http://quotes.toscrape.com/js/page/1/'
        yield SplashRequest(
            url=start_url,
            callback = self.parse,
            endpoint = "execute",
            args = {"lua_source": self.script}
        )

    def parse(self, response):
        for q in response.css(".quote"):
            yield {
                "text": q.xpath(".//span[@class='text']/text()").get(),
                "author": q.css("small.author::text").get(),
                "tags": q.css(".tags a.tag::text").getall()
            }

        next_page = response.css(".pager .next a")
        print(next_page)
        if next is not None:
            url = next_page.attrib["href"]
            yield SplashRequest(
                url=f'http://quotes.toscrape.com{url}',
                callback = self.parse,
                endpoint = "execute",
                args = {"lua_source": self.script}
        )
