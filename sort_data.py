import pprint
import requests
import time
from bs4 import BeautifulSoup as bs
import json
from info import set_webtoon_info

max_retries = 3

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
def sort_data(response, webtoon_list):
    res = response.json()

    for section in res["data"]["staticLandingGenreLayout"]["sections"]:
        groups = section["groups"]
        for group in groups:
            items = group["items"]
            for i in items:
                #pprint.pprint(i, sort_dicts=False)
                meta = i['eventLog']['eventMeta']

                title = i['title']
                ageGrade = i['ageGrade']
                category = meta['subcategory']
                view = i['subtitleList'][0]
                id = meta['id']
                content_type = meta['category']
                if not i['badgeList']:
                    free_type = "Free_None"
                else:
                    free_type = i['badgeList'][0]
                new_status = i['statusBadge']
                thumbnail = i['thumbnail']

                webtoon_info = set_webtoon_info("KaKaoPage",
                                                title,
                                                "not ready_info",
                                                "not_ready_author",
                                                ageGrade,
                                                category,
                                                "not_ready_tag",
                                                view,
                                                id,
                                                content_type,
                                                free_type,
                                                new_status,
                                                thumbnail)
                webtoon_list.append(webtoon_info)


def info_supplement(webtoon_list):
    count = 1
    for webtoon in webtoon_list:
        id = webtoon["id"]
        url = f"https://page.kakao.com/_next/data/2.12.2/ko/content/{id}.json"
        response = make_request(url, headers)
        if response is not None:
            try:
                soup = bs(response.text, "lxml")
                element = soup.select("p")[0].text
                page = json.loads(element)
            except json.decoder.JSONDecodeError:
                print("JSONDecodeError. Retrying...")
                time.sleep(3)
                response = make_request(url, headers)
                continue

        description = page["pageProps"]["metaInfo"]["description"]
        author = page["pageProps"]["metaInfo"]["author"]
        tmp = page["pageProps"]["dehydratedState"]["queries"]

        for i in tmp:
            contentHomeAbout = i["state"]["data"]["contentHomeAbout"]
            keyword_list = contentHomeAbout["themeKeywordList"]
            keyword = [item["title"] for item in keyword_list]
            keywords_combined = ', '.join(keyword)
            screenshot = contentHomeAbout["screenshotList"]
            tmp_screenshot = ""
            for i, url in enumerate(screenshot):
                if i > 0:
                    tmp_screenshot += ", "
                tmp_screenshot += url

        webtoon["author"] = author
        webtoon["info"] = description
        if not keywords_combined:
            webtoon["tag"] = "Tag_None"
        else:
            webtoon["tag"] = keywords_combined

        if not tmp_screenshot:
            webtoon["screenshot"] = "Screenshot_None"
        else:
            webtoon["screenshot"] = tmp_screenshot

        pprint.pprint(webtoon, sort_dicts=False)
        print(f"{count}번째 데이터가 추가되었습니다.")
        count += 1

def make_request(url, headers):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP 에러가 발생하면 예외가 발생합니다.
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Retrying...")
            retries += 1
            time.sleep(3)  # 재시도 전에 잠시 기다립니다.

    print("Max retries reached. Unable to make request.")
    return None



