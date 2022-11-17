from datetime import datetime
import json
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CharlottetownSpider(CrawlSpider):
    name = 'charlottetown'
    allowed_domains = ['www.kijiji.ca']

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

    estates_seen = set()
    authors_seen = set()

    def start_requests(self):
        yield scrapy.Request(url='https://www.kijiji.ca/b-apartments-condos/charlottetown-pei/c37l1700119', headers={
            'User-Agent': self.user_agent
        })
        for i in range(2, 9):
            yield scrapy.Request(
                url=f"https://www.kijiji.ca/b-apartments-condos/charlottetown-pei/page-{i}/c37l1700119",
                headers={
                    'User-Agent': self.user_agent
                }, dont_filter=True)

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='info-container']/div[@class='title']/a"),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        # Rule(LinkExtractor(restrict_xpaths="//div[@class='pagination']/a[@title='Next']")),
    )

    def set_user_agent(self, request, spider):
        # Filtering real estates by id ... return None
        estate_id = request.url.split('/')[-1]
        if estate_id in self.estates_seen:
            return None
        self.estates_seen.add(estate_id)
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_p(self, response):
        items = response.xpath("//div[@class='info-container']/div[@class='title']/a/@href").getall()
        for i in items:
            yield response.follow(url=i, callback=self.parse_item, headers={'User-Agent': self.user_agent})

    def parse_item(self, response):
        real_estate_info = {}

        # Getting real_estate info
        real_estate_info['id'] = response.url.split('/')[-1]
        real_estate_info['title'] = response.xpath("//h1/text()").get()
        if not real_estate_info['title']:
            yield {
                'type': 'real_estate',
                'id': real_estate_info['id']
            }
        else:
            real_estate_info['price'] = response.xpath("//div[@class='priceWrapper-1165431705']/span/text()").get()
            if real_estate_info['price'] != "Please Contact":
                real_estate_info['price'] = int(real_estate_info['price'].replace('$', '').replace(',', ''))
            real_estate_info['address'] = response.xpath("//span[@class='address-3617944557']/text()").get()
            real_estate_info['posted'] = response.xpath("//time/@datetime").get()

            real_estate_info['posted'] = datetime.strptime(real_estate_info['posted'], '%Y-%m-%dT%H:%M:%S.%fZ')
            real_estate_info['utilities_included'] = response.xpath(
                "//span[@class='utilities-3542420827']/text()").get()

            additional = response.xpath(
                "//div[contains(@class, 'root-2377010271 light-3420168793 attributeCard-1535740193')]")

            for section_id in range(2):
                section_body = additional[section_id].xpath(".//ul[@class='list-1757374920 disablePadding-1318173106']")
                data = {}
                for item in section_body.xpath(".//li"):
                    div = item.xpath('.//div')
                    if div:
                        div_header = div.xpath('.//h4/text()').get()
                        div_body = div.xpath('.//ul/li/text()').getall()
                        if not div_body:
                            div_body = div.xpath('.//ul/text()').get()
                    else:
                        div_header = item.xpath('.//dl/dt/text()').get()
                        div_body = item.xpath('.//dl/dd/text()').get()
                        if not div_body:
                            div_body = item.xpath('.//dl/dd/span/text()').get()
                        if div_header == "Move-In Date":
                            div_body = datetime.strptime(div_body, '%B %d, %Y')
                    if div_header:
                        data[div_header] = div_body
                real_estate_info['The Unit' if section_id else 'Overview'] = data

            description_body = response.xpath(".//div[@class='descriptionContainer-231909819']/div")
            description_text = description_body.xpath(".//text()").getall()

            description = ""
            for tag in description_body.xpath(".//*"):
                temp = tag.xpath(".//text()").get()
                if not temp:
                    temp = tag.xpath(".//*/text()")
                if temp:
                    description += "\n" + temp + "\n"
            if description_text:
                description += "\n" + "".join(description_text)
            real_estate_info['description'] = description

            # Filtering author by id.
            author_a = response.xpath('//a[@class="link-2686609741"]')
            author_link = author_a.xpath('.//@href').get()
            author_id = author_link.split('/')[2]
            real_estate_info['author_id'] = author_id
            # if author_link and author_link.split('/')[2]:
            #     author_id = response.xpath(author_link.split('/')[2])
            #     # Could be optimized
            #     author_type = response.xpath("//div[@class='line-2791721720']/text()").get()
            #     if not author_type == "Owner":
            #         yield scrapy.Request(url=author_link, callback=self.process_author)

            # author_name = author_a.xpath('.//@text()').get()
            yield {
                'type': 'real_estate',
                'data': real_estate_info
            }
            request_author_body = [
                {
                    "operationName": "GetProfile",
                    "variables": {
                        "userId": author_id
                    },
                    "query": "query GetProfile($userId: Long) {\n  findProfile(id: $userId) {\n    ...CoreProfile\n    numberOfOrganicAds\n    responsiveness\n    replyRate\n    __typename\n  }\n}\n\nfragment CoreProfile on Profile {\n  companyName\n  displayName\n  id\n  isAdmarkt\n  isReadIndicatorEnabled\n  isSfidEnabled\n  memberSince\n  photoUrl\n  profileName\n  profileType\n  __typename\n}\n"
                }
            ]
            yield scrapy.Request(url="https://www.kijiji.ca/anvil/api", callback=self.process_author, method='POST',
                                 headers={'User-Agent': self.user_agent, 'apollo-require-preflight': 'true',
                                          'Content-Type': 'application/json'},
                                 body=json.dumps(request_author_body),
                                 meta={
                                     'author_id': author_id,
                                     'url': response.url,
                                     'adId': real_estate_info['id']
                                 })

    def process_author(self, response):
        try:
            resp = json.loads(response.body)[0]['data']['findProfile']
        except KeyError:
            resp = None
        if not resp:
            yield {
                'type': 'author',
                'data': {"author_id": response.meta['author_id']}
            }
        else:
            author_info = {
                "author_id": response.meta['author_id'],
                "name": resp.get('companyName') or resp.get('profileName'),
                "profileType": resp.get('profileType'),
                "numberOfOrganicAds": resp.get('numberOfOrganicAds'),
                "responsiveness": resp.get('responsiveness'),
                "replyRate": resp.get('replyRate'),
                "memberSince": resp.get('memberSince')
            }
            request_body = [
                {
                    "operationName": "GetDynamicPhoneNumber",
                    "variables": {
                        "adId": response.meta['adId'],
                        "sellerId": response.meta['author_id'],
                        "vipUrl": response.meta['url'] + "?siteLocale=en_CA",
                        "listingType": "rent",
                        "sellerName": author_info['name']
                    },
                    "query": "query GetDynamicPhoneNumber($sellerId: String!, $adId: String!, $userId: String, $vipUrl: String!, $listingType: String!, $sellerName: String!) {\n  getDynamicPhoneNumber(sellerId: $sellerId, adId: $adId, userId: $userId, vipUrl: $vipUrl, listingType: $listingType, sellerName: $sellerName) {\n    local\n    e164\n    __typename\n  }\n}\n"
                }
            ]
            yield scrapy.Request(url="https://www.kijiji.ca/anvil/api", callback=self.get_phone_number,
                                 method='POST',
                                 headers={'User-Agent': self.user_agent,
                                          'apollo-require-preflight': 'true', 'Content-Type': 'application/json'},
                                 body=json.dumps(request_body), meta={'data': author_info})

    def get_phone_number(self, response):
        try:
            resp = json.loads(response.body)[0]['data']['getDynamicPhoneNumber']
        except KeyError:
            resp = None

        if resp:
            response.meta['data']['phone_number'] = resp['e164']

        return {
            'type': 'author',
            'data': response.meta['data']
        }
