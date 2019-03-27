import requests
import bs4
from pprint import pprint
import csv
base_url = "http://www.prisontalk.com/forums/"
topics_url = "forumdisplay.php?f="
topic_pages_url = "&order=desc&page="
#each topic with the first value being the number of the topic and the second being the number of pages in that topic
# topics = {'GENERAL PRISON TALK': ["39", 407],
#           'HUSBANDS AND BOYFRIENDS': ["44", 1312],
#           'WIVES & GIRLFRIEND IN PRISON': ["110", 42],
#           'GAY, LESBIAN, BISEXUAL AND TRANSGENDERED PEOPLE IN PRISON': ["192", 30],
#           'REMEMBERING THOSE THAT PASSED WHILE IN PRISON': ["1035", 12],
#           'WHEN THE RELATIONSHIP IS OVER': ["412", 146],
#           'MET WHILE INCARCERATED': ["645", 290],
#           'PARENTS WITH CHILDREN IN PRISON': ["75", 259],
#           'RAISING CHILDREN WITH PARENTS IN PRISON ': ["94", 79],
#           'ADULT CHILDREN AND SIBLINGS OF INMATES': ["240", 43],
#           'EXTENDED FAMILY': ["241", 11],
#           'JUVENILE': ["65", 20]}

topics = {'GENERAL PRISON TALK': ["39", 407]}
file = 'GENERAL PRISON TALK'

def create_topic_url(topics):
    url_list = {}
    for key, value in topics.items():
        url_list[f'{key}'] = []
        url_list[f'{key}'].append(value[0])
        url_list[f'{key}'].append(base_url+topics_url+value[0])
        for i in range(2,value[1]):
            url_list[f'{key}'].append(base_url+topics_url+value[0]+topic_pages_url+str(i))
    return url_list


def get_threads(topics):
    thread_titles_and_url = {}
    for key, value in topics.items():
        for item in value:
            try:
                topic_page = requests.get(item)
                soup = bs4.BeautifulSoup(topic_page.text, 'html.parser')
                all_thread_info = soup.find('tbody', id=f'threadbits_forum_{value[0]}')
                threads_html = extract_html_for_each_page(all_thread_info)
                threads = extract_thread_title_and_url(threads_html)
                thread_titles_and_url.update(threads)
            except requests.exceptions.MissingSchema:
                pass

    return thread_titles_and_url


def extract_html_for_each_page(html):
    threads_html = []
    for item in html:
        thread = item.find('a')
        threads_html.append(thread)
    return threads_html


def extract_thread_title_and_url(threads_html):
    threads = {}
    for item in threads_html:
        try:
            threads[item.text] = item['href']
        except AttributeError and TypeError:
            pass
    return threads


def extract_first_comment(threads):
    posts_dict = {}
    for key, value in threads.items():
        try:
            post_url = base_url + value
            post_request = requests.get(post_url)
            soup = bs4.BeautifulSoup(post_request.text, 'html.parser')
            posts_html = soup.find('div', id='posts')
            first_post_table = posts_html.find('table')
            first_post = first_post_table('tr')[3]('div')[1].text.encode("utf-8", 'surrogateescape')
            username_block = first_post_table('tr')[2].find('a')
            username = username_block.text.encode("utf-8")
            posts_dict[base_url+value] = [key.encode("utf-8"), username, first_post]
        except AttributeError:
            pass
    return posts_dict


def write_to_csv(posts_dict):
    with open(f'{file}.csv', 'w') as f:
        csv_output = csv.writer(f)
        csv_output.writerow(['Thread URL', 'Title', 'Username', 'First Post'])

        for key in sorted(posts_dict):
            csv_output.writerow([key] + posts_dict[key])


if __name__ == '__main__':
    topic_urls = create_topic_url(topics)
    threads = get_threads(topic_urls)
    posts = extract_first_comment(threads)
    write_to_csv(posts)