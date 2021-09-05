import scrapy

class Autoscout24Spider(scrapy.Spider):
    name = 'autoscout24'
    allowed_domains = ['www.autoscout24.com']
    start_urls = ['https://www.autoscout24.com/lst/?sort=standard&desc=0&ustate=N%2CU&size=20&page=1&cy=D&atype=C&']
    #list_of_makes = ["Audi", "BMW", "Ford", "Mercedes-Benz", "Opel", "Volkswagen", "Renault", "Abarth", "Chevrolet", "Dodge", "Fiat", "Honda", "Jaguar", "Jeep", "Land Rover", "Lexus", "Maserati", "Mitsubishi", "Nissan", "Peugeot", "Porsche", "Subaru", "Suzuki", "Toyota", "Volvo"]
    list_of_makes = ["Mercedes-Benz"]
    def parse(self, response):
        base_url = 'https://www.autoscout24.com/lst/'
        middle_url = '?sort=standard&desc=0&offer=J%2CS%2CU&gear=A&fuel=B&ustate=N%2CU&size=20&page='
        last_url = '&cy=D&priceto=100000&pricefrom=12500&kmto=150000&kmfrom=10000&fregto=2015&fregfrom=2000&atype=C&'

        posts = response.xpath("//div[@class='cl-list-element cl-list-element-gap']")
        for post in posts:
            makemodel = post.xpath(".//h2[@class='cldt-summary-makemodel sc-font-bold sc-ellipsis']/text()").get()
            version = post.xpath(".//h2[@class='cldt-summary-version sc-ellipsis']/text()").get()
            price = post.xpath(".//span[@class='cldt-price sc-font-xl sc-font-bold']/text()").get()
            mileage = post.xpath(".//li[@data-type='mileage']/text()").get()
            firstreg = post.xpath(".//li[@data-type='first-registration']/text()").get()
            power = post.xpath(".//ul[@data-item-name='vehicle-details']/li[3]/text()").get()
            offertype = post.xpath(".//li[@data-type='offer-type']/text()").get()
            previousowners = post.xpath(".//li[@data-type='previous-owners']/text()").get()
            transmission = post.xpath(".//li[@data-type='transmission-type']/text()").get()
            fuel = post.xpath(".//li[@class='summary_item_no_bottom_line']/text()").get()
            consumption = post.xpath(".//li[@data-type='combined-consumption']/text()").get()
            co2 = post.xpath(".//li[@data-type='co2-emission']/text()").get()
            address = post.xpath(".//span[@class='cldf-summary-seller-contact-zip-city']/text()").get()
            url = 'https://www.autoscout24.com'+post.xpath(".//a[@data-item-name='detail-page-link']/@href").get()
            
            yield{
                'makemodel' : makemodel, 
                'version' : version,  
                'price' : price,
                'mileage' : mileage,
                'firstreg' : firstreg,
                'power' : power,
                'offertype' : offertype,
                'previousowners' : previousowners,
                'transmission' : transmission,
                'fuel' : fuel,
                'consumption' : consumption,
                'co2' : co2,
                'address' : address,
                'url' : url
            }
        
        for make in Autoscout24Spider.list_of_makes: 
            page = 1   
            while page <= 20:
                yield scrapy.Request(url=base_url+make+middle_url+str(page)+last_url, callback=self.parse)
                page += 1