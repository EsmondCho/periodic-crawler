from celery import shared_task
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from datetime import datetime, timedelta
from django.utils import timezone
from .models import *
import time
from time import sleep
import json


@shared_task
def crawling_clien(time_to=None, hour=None, time_from=None, start_page=None):

    execute_time = datetime.now()
    start_time = time.time()

    # Celery crontab passing arguments not type of date but string.
    # So change str to datetime object.
    if time_to:
        time_to = str(time_to).replace('T', ' ')
        if type(time_to) == str:
            time_to = datetime.strptime(time_to[:19], '%Y-%m-%d %H:%M:%S')

    if time_from:
        time_from = str(time_from).replace('T', ' ')
        if type(time_from) == str:
            if len(time_from) < 22:
                time_from = datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')
            else:
                time_from = datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S.%f')

    st = StInfoTb.objects.get(st_name='clien')

    site_url = st.st_url
    board_url = site_url + '/service/board/cm_vcoin?po='
    if start_page:
        page_num = start_page
    else:
        page_num = 0

    service_log_path = "/home/esmond/celery_django/djserver/log/chromedriver.log"
    service_args = ['--verbose']

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    driver = webdriver.Chrome("/bin/chromedriver_for_linux", chrome_options=options, service_args=service_args, service_log_path=service_log_path)

    driver.set_page_load_timeout(30)

    if hour:
        time_from = time_to - timedelta(hours=hour)

    new_stored_posts_num = 0
    new_stored_comments_all = 0

    while True:
        print("[page_num: {}]".format(page_num))

        driver.get(board_url + str(page_num))
        posts = driver.find_elements_by_css_selector('div.list_item.symph_row')

        # page + 1 if datetime of last post is later than from_ parameter
        last_post_date_str = posts[-1].find_element_by_css_selector('span.timestamp').get_attribute('textContent')
        last_post_date_obj = datetime.strptime(last_post_date_str, '%Y-%m-%d %H:%M:%S')
        if time_to < last_post_date_obj:
            page_num += 1
            continue

        links = []
        for post in posts:
            post_date_str = post.find_element_by_css_selector('span.timestamp').get_attribute('textContent')
            post_date_obj = datetime.strptime(post_date_str, '%Y-%m-%d %H:%M:%S')
            if time_to > post_date_obj:
                if post.find_elements_by_css_selector('a.list_subject'):
                    links.append(post.find_element_by_css_selector('a.list_subject').get_attribute('href'))

        for index, link in enumerate(links):
            try:
                driver.get(link)
            except TimeoutException as ex:
                print("TimeoutException has been thrown(1). " + str(ex))
                driver.quit()
                print("sleep for 5 seconds and restart chrome driver...")
                for i in range(1, 6):
                    print(i)
                    sleep(1)
                try:
                    driver = webdriver.Chrome("/bin/chromedriver_for_linux", chrome_options=options, service_args=service_args, service_log_path=service_log_path)
                    driver.set_page_load_timeout(30)
                    driver.get(link)
                except TimeoutException as ex2:
                    print("TimeoutException has been thrown(2). " + str(ex2))
                    driver.quit()
                    print("sleep for 5 seconds and restart chrome driver...")
                    for i in range(1, 6):
                        print(i)
                        sleep(1)
                    try:
                        driver = webdriver.Chrome("/bin/chromedriver_for_linux", chrome_options=options, service_args=service_args, service_log_path=service_log_path)
                        driver.set_page_load_timeout(30)
                        driver.get(link)
                    except TimeoutException as ex3:
                        print("TimeoutException has been thrown(3). " + str(ex3))
                        print("page_now: {}".format(page_num))
                        print("index: {}".format(index))
                        driver.quit()
                        print("Stop crawling.")

                        fail_dic = {
                            'current_page': page_num,
                            'new_stored_posts': new_stored_posts_num,
                            'new_stored_comments': new_stored_comments_all,
                            'execute_time': str(execute_time),
                            'taken_time': str(time.time() - start_time),
                            'success': 0
                        }
                        result_json_fail = json.dumps(fail_dic)
                        return result_json_fail

            try:
                title = driver.find_element_by_class_name('post_subject').find_elements_by_tag_name('span')[-1].text
                content = driver.find_element_by_css_selector('div.post_article.fr-view').text
                date_str = driver.find_element_by_css_selector('div.post_author').find_elements_by_tag_name('span')[0].text.strip()[:19]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                symph = driver.find_element_by_css_selector('div.post_symph.view_symph').find_element_by_tag_name('span').text
                view_count = driver.find_element_by_css_selector('span.view_count').find_element_by_tag_name('strong').text
                print(str(index) + ") " + date_str)

            except:
                driver.quit()
                print("Post parsing exception! Continue to next loop after 5 seconds...")
                for i in range(1, 6):
                    print(i)
                    sleep(1)
                driver = webdriver.Chrome('/bin/chromedriver_for_linux', chrome_options=options)
                driver.set_page_load_timeout(30)
                continue

            # Closing infinite loop
            if date_obj < time_from:
                driver.quit()
                result_dic = {
                    'new_stored_posts': new_stored_posts_num,
                    'new_stored_comments': new_stored_comments_all,
                    'execute_time': str(execute_time),
                    'taken_time': str(time.time() - start_time),
                    'success': 1
                }
                result_json = json.dumps(result_dic)
                return result_json
            # elif:
            #     # Add code that raising invalid params error
            #     return False

            existing_post = PsTb.objects.filter(ps_title=title, ps_date=timezone.make_aware(date_obj))
            if existing_post:
                # Get only 1 post if there are multiple posts with same title and date
                post = existing_post[0]
            else:
                # when symph > 99, symph is not 100.. but 99+(string) so change into integer
                if type(symph) == str:
                    symph = int(symph[0:2])
                try:
                    post = PsTb.objects.create(
                        st_id=st, ps_title=title,
                        ps_content=content, ps_date=timezone.make_aware(date_obj),
                        ps_view_count=int(view_count), ps_symph=int(symph)
                    )
                    post.save()
                    new_stored_posts_num += 1
                except:
                    print('Post storing exception! Continue to next loop...')
                    continue

            existing_comments_obj_list = CoTb.objects.filter(ps_id=post)

            existing_comments_list = []
            for co in existing_comments_obj_list:
                existing_comments_list.append(co.co_content)

            comments = driver.find_elements_by_css_selector('div.comment_row')
            new_stored_comments_num = 0
            for co in comments:
                if "blocked" in co.get_attribute("class"):
                    continue
                content = co.find_element_by_css_selector('div.comment_view').text.strip()
                co_date_str = co.find_element_by_css_selector('span.timestamp').get_attribute('textContent')[:19]
                co_date_obj = datetime.strptime(co_date_str, '%Y-%m-%d %H:%M:%S')

                # Storing only new comments
                try:
                    if content not in existing_comments_list:
                        comment = CoTb.objects.create(
                            ps_id=post, co_content=content,
                            co_date=timezone.make_aware(co_date_obj)
                        )
                        comment.save()
                        new_stored_comments_num += 1
                except:
                    print('Comment storing exception! Continue to next loop...')
                    continue
            print('new stored comments: {}'.format(new_stored_comments_num))
            new_stored_comments_all += new_stored_comments_num

        page_num += 1


@shared_task
def say_name(name, gender):
    j = {
        'name': name,
        'gender': gender
    }
    jj = json.dumps(j)
    return jj


