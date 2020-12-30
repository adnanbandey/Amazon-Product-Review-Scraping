import time
import math, requests, json
from scrapy.http import HtmlResponse
import pandas as pd
raw_dataframe = [ ]
req=['https://www.amazon.in/Fitkit-Classic-Shaker-Bottle-700ml/product-reviews/B081DT98TF/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews',
    'https://www.amazon.in/Mi-Smart-Band-Waterproof-up/product-reviews/B07WLL998K/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews',
    'https://www.amazon.in/Lifebuoy-Laundry-Sanitizer-500-ml/product-reviews/B0874ZBZWV/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'] #ENTER HERE ALL THE URLS HERE LIKE I HAVE ADDED THREE URLS RANDOMLY

head = {'accept': 'text/html, */*',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 'origin': 'https://www.amazon.in',
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KWH, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'x- requested-with': 'XMLHttpRequest'
        }

for r in req:
    time.sleep(5)
    res = requests.get(r,headers=head)
    time.sleep(5)
    response = HtmlResponse( url=res.url,body=res.content )
    product_name = response.xpath( '//h1/a/text()').extract_first(default=' ' ).strip()
    total_reviews = response.xpath('//*[@id="filter-info-section"]/div/span/text()').extract_first(default='').strip().split('|')[-1].split()[0]
    total_pages = math.ceil(int(total_reviews)/10)
    for i in range(1,total_pages+1):
        url = f"{r}&pageNumber={i}"
        head = {'accept': 'text/html, */*',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8', 'origin': 'https://www.amazon.in',
        'referer':response.url,
        'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KWH, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'x- requested-with': 'XMLHttpRequest'
        }
        res = requests.post(url,headers=head)
        response = HtmlResponse(url=res.url, body=res.content)
        loop = response.xpath('//div[contains(@class,"a-section review")]')
        for part in loop:
            review_title = part.xpath('.//a[contains(@class,"review-title-content")]/span/text()').extract_first(default=' ').strip()
            rating =part.xpath('.//a[contains(@title,"out of 5 stars")]/@title').extract_first(default=' ').strip().split()[0].strip()
            description =''.join(part. xpath('.//span[contains(@class,"review-text-content")]/span/text()') .extract()).strip()
            try:
                helpful_count =part.xpath('.//span[contains(@class,"cr-vote-text")]/ text()').extract_first(default ='').strip().split()[0].strip()
            except:
                helpful_count = 0
            date=part.xpath('.//span[@data-hook="review-date"]/text()').extract()[0].strip()  
            try:
                badge=part.xpath('.//span[@data-hook="avp-badge"]/text()').extract()[0].strip()
            except:
                badge='Not verified'
                
            raw_dataframe.append([product_name,review_title,rating, description,helpful_count,date,badge])
            
df =pd.DataFrame(raw_dataframe,columns = ['Product Name','Review Title','Review Rating','Description','Helpful Count','Date','Badge'])    
