import pprint
import time

from bs4 import BeautifulSoup as bs
import json
from info import set_webtoon_info
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
