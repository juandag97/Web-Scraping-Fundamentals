"""
    Author: @juandag97
    Date: 06-Dec-2020, Sunday
    Description: scraper used for obtain data
    from page https://www.larepublica.co/
"""

"""
Some required libraries.
"""

import requests
import lxml.html as html 
import os 
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_MAIN_ARTICLE = '//text-fill[not(@class)]/a/@href'

XPATH_TITLE = '//h2[not(@class)]/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_CONTENT = '//div[@class="html-content"]/p[not(@class)]/text()'

"""
    Some xpaths that don't work as we expected
"""

#XPATH_LINK_TO_MAIN_ARTICLE = '//h2[@style="font-size: 36px; line-height: 40px;"]/a/@href'
# XPATH_LINK_TO_SECONDARY_ARTICLE = '//h2[@style="font-size: 17px; line-height: 21px;"]/a/@href'

# XPATH_BIG_TITLE = '//h2[@style="font-size: 36px; line-height: 40px;"]/a/text()'
# XPATH_SMALL_TITLE = '//h2[@style="font-size: 17px; line-height: 21px;"]/a/text()'

"""
For generate the files that contains the title, summary
and content of the news
"""

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            #For generate a html document from the string notice
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                content = parsed.xpath(XPATH_CONTENT)
            #Because we are not interested in the news that don't have summary
            except IndexError:
                return

            #With is a python contextual manager 
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in content:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')

    #Catch error when http response is diferent to 200
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_MAIN_ARTICLE)
            #print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()