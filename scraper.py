import requests
import bs4
from pprint import pprint
url = "http://www.prisontalk.com/forums/"
topics = {'GENERAL PRISON TALK': "forumdisplay.php?f=39",
          'HUSBANDS AND BOYFRIENDS': "forumdisplay.php?f=44",
          'WIVES & GIRLFRIEND IN PRISON': "forumdisplay.php?f=110",
          'GAY, LESBIAN, BISEXUAL AND TRANSGENDERED PEOPLE IN PRISON': "forumdisplay.php?f=192",
          'REMEMBERING THOSE THAT PASSED WHILE IN PRISON': "forumdisplay.php?f=1035",
          'WHEN THE RELATIONSHIP IS OVER': "forumdisplay.php?f=412",
          'MET WHILE INCARCERATED': "forumdisplay.php?f=645",
          'PARENTS WITH CHILDREN IN PRISON': "forumdisplay.php?f=75",
          'RAISING CHILDREN WITH PARENTS IN PRISON ': "forumdisplay.php?f=94",
          'ADULT CHILDREN AND SIBLINGS OF INMATES': "forumdisplay.php?f=240",
          'EXTENDED FAMILY': "forumdisplay.php?f=241",
          'JUVENILE': "forumdisplay.php?f=65"}


def create_topic_url(topic):
    url_list = []
    for key, value in topics.items():
        url_list.append(url+value)
    return url_list

def get_threads(topic_url='http://www.prisontalk.com/forums/forumdisplay.php?f=192'):
    topic_page = requests.get(topic_url)
    soup = bs4.BeautifulSoup(topic_page.text, 'html.parser')
    number = topic_url.split('=')[1]
    thread_list = soup.find('tbody', id=f'threadbits_forum_{number}')
    threads_html = []
    threads = {}
    for item in thread_list:
        thread = item.find('a')
        threads_html.append(thread)
    for item in threads_html:
        if type(item) is not int or None:
            try:
               threads[item.text] = item['href']
            except AttributeError and TypeError:
                pass
    pprint(threads)

    print(threads)
if __name__ == '__main__':
    topic_urls = create_topic_url(topics)
    get_threads()