import os
import time
from datetime import datetime
import hashlib
import urllib.parse

import arrow
from selenium import webdriver

months = {
    "fev": "Feb",
    "abr": "Apr",
    "mai": "May",
    "ago": "Aug",
    "set": "Sep",
    "out": "Oct",
    "dez": "Dec",
}


def get_profile():
    browser_profile = webdriver.FirefoxProfile()
    browser_profile.set_preference("dom.webnotifications.enabled", False)
    browser_profile.set_preference("intl.accept_languages", "pt-br")
    return browser_profile


class TwitterTagsClient:
    def __init__(self, np_posts=5):
        self.np_posts = np_posts

    def load(self, hashtag):
        # Using Firefox driver NO WINDOW MODE
        os.environ["MOZ_HEADLESS"] = "1"

        driver = webdriver.Firefox(
            firefox_profile=get_profile(),
            executable_path=f"{os.getcwd()}/src/scraping/driver/geckodriver",
        )
        # f"https://twitter.com/search?q={hashtag}&src=typed_query&f=live"
        # https://twitter.com/hashtag/febre?f=live
        # https://twitter.com/search?q=%22falta%20de%20ar%22%20lang%3Apt&src=typed_query&f=live
        driver.get(
            f"https://twitter.com/search?q=%22{urllib.parse.quote(hashtag)}%22%20lang%3Apt&src=typed_query&f=live"
        )

        not_found = False
        while not_found:
            try:
                login = driver.find_element_by_class_name("dropdown-signin")
                login.click()
                ultimas = driver.find_elements_by_class_name(
                    "AdaptiveFiltersBar-target"
                )
                ultimas[1].click()
                not_found = True
                time.sleep(0.1)
            except Exception as e:
                print(f"ERROR: AdaptiveFiltersBar-target not found : {e}")

        data = {"hashtag": hashtag, "comments": []}
        for _ in range(self.np_posts + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

            tweets = driver.find_elements_by_tag_name("article")
            for tweet in tweets:
                try:
                    username = tweet.find_element_by_xpath(
                        "./div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span"
                    )
                    comment = tweet.find_element_by_xpath(
                        "./div/div[2]/div[2]/div[2]/div[1]"
                    )
                    dt = tweet.find_element_by_xpath(
                        "./div/div[2]/div[2]/div[1]/div/div/div[1]/a"
                    )

                    if username and comment:
                        username = username.text.strip()
                        comment = comment.text.strip()

                        # Tratamento de data
                        tm = (
                            dt.get_attribute("title")
                            .replace(" de ", "/")
                            .replace(" · ", " ")
                        ).lower()
                        for key, value in months.items():
                            if key in tm:
                                tm = tm.replace(key, value.title())
                                break
                        dt = arrow.get(tm, "h:mm A D/MMM/YYYY")

                        data["comments"].append(
                            {
                                "hash": hashlib.sha256(
                                    (username + "|" + comment).encode("ascii", "ignore")
                                ).hexdigest(),
                                "username": username,
                                "data": dt.format("DD/MM/YYYY HH:mm"),
                                "timestamp": dt.timestamp,
                                "comment": comment,
                            }
                        )
                except Exception as e:
                    pass
                    # print(f"ERROR: username or comment not found : {e}")
        driver.close()
        return data
