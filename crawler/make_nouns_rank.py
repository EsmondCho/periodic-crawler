from crawler.models import *
from datetime import datetime, timedelta
from konlpy.tag import Twitter
import operator
import json, time
import re


def make_rank(period_minute):

    start_time = time.time()

    twitter = Twitter()
    start = datetime(2018, 2, 20)
    end = start - timedelta(minutes=period_minute)
    list = []

    while True:
        print(str(period_minute) + ") " + str(start))

        posts = PsTb.objects.filter(ps_date__lte=start, ps_date__gte=end)

        post_title_list = []
        post_content_list = []
        for post in posts:
            post_title_list.append(post.ps_title)
            post_content_list.append(post.ps_content)

        title_nouns = []
        for title in post_title_list:
            title_nouns += twitter.nouns(title)
            title_nouns += re.findall("[A-Za-z]+", title)

        content_nouns = []
        for content in post_content_list:
            content_nouns += twitter.nouns(content)
            content_nouns += re.findall("[A-Za-z]+", content)

        title_content_nouns = title_nouns + content_nouns

        title_nouns_count = {}
        for n in title_nouns:
            try: title_nouns_count[n] += 1
            except: title_nouns_count[n] = 1

        content_nouns_count = {}
        for n in content_nouns:
            try: content_nouns_count[n] += 1
            except: content_nouns_count[n] = 1

        title_content_nouns_count = {}
        for n in title_content_nouns:
            try: title_content_nouns_count[n] += 1
            except: title_content_nouns_count[n] = 1

        sorted_title_rank = sorted(title_nouns_count.items(), key=operator.itemgetter(1))
        sorted_title_rank.reverse()
        sorted_title_rank_list = []
        if len(sorted_title_rank) >= 30:
            length = 30
        else:
            length = len(sorted_title_rank)
        for i in range(0, length):
            key = sorted_title_rank[i][0]
            value = sorted_title_rank[i][1]
            dic = {key: value}
            sorted_title_rank_list.append(dic)

        sorted_content_rank = sorted(content_nouns_count.items(), key=operator.itemgetter(1))
        sorted_content_rank.reverse()
        sorted_content_rank_list = []
        if len(sorted_content_rank) >= 30:
            length = 30
        else:
            length = len(sorted_content_rank)
        for i in range(0, length):
            key = sorted_content_rank[i][0]
            value = sorted_content_rank[i][1]
            dic = {key: value}
            sorted_content_rank_list.append(dic)

        sorted_title_content_rank = sorted(title_content_nouns_count.items(), key=operator.itemgetter(1))
        sorted_title_content_rank.reverse()
        sorted_title_content_rank_list = []
        if len(sorted_title_content_rank) >= 30:
            length = 30
        else:
            length = len(sorted_title_content_rank)
        for i in range(0, length):
            key = sorted_title_content_rank[i][0]
            value = sorted_title_content_rank[i][1]
            dic = {key: value}
            sorted_title_content_rank_list.append(dic)

        period_dic = {
            'to': str(start),
            'from': str(end),
            'title': sorted_title_rank_list,
            'content': sorted_content_rank_list,
            'title_content': sorted_title_content_rank_list
        }

        list.append(period_dic)

        start = end
        end = end - timedelta(minutes=period_minute)

        if end < datetime(2018, 2, 1):
            break
        # if end < datetime(2017, 11, 28):
        #     break

    f = open('post_word_rank_per_' + str(period_minute) + 'minutes.txt', 'w')
    f.write(str(list))
    f.close()

    json_data = json.dumps(list)
    f = open('post_word_rank_per_' + str(period_minute) + 'minutes.json', 'w')
    f.write(json_data)
    f.close()

    taken_time = time.time() - start_time
    return taken_time


def do_make_rank():

    # minutes = [15, 30, 60, 120, 180, 360, 720, 1440, 10080]
    minutes = [60]

    for m in minutes:
        make_rank(m)

    return True

