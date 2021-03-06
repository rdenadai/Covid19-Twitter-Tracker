import os
import time
import re
from datetime import datetime
import hashlib
import urllib.parse

import arrow
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..processing.utils import is_number, normalizar


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


def chrome_options():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")  # linux only
    options.add_argument("--headless")
    options.add_argument("--lang=pt-br")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    return options


class TwitterTagsClient:
    def __init__(self, n_posts_2_extract=5):
        self.n_posts_2_extract = n_posts_2_extract

    def treat_comment(self, comment):
        comment = comment.replace("\n", " ").strip()
        strip_pos = 0
        for pos in range(1, len(comment)):
            if is_number(comment[-pos]) or comment[-pos] == " ":
                strip_pos = pos
            else:
                break
        if strip_pos > 0:
            comment = comment[:-strip_pos]
        return comment

    def treat_data(self, dt):
        # Old way
        # Tratamento de data
        # tm = (
        #     dt.get_attribute("title")
        #     .replace(" de ", "/")
        #     .replace(" · ", " ")
        # ).lower()
        # for key, value in months.items():
        #     if key in tm:
        #         tm = tm.replace(key, value.title())
        #         break
        # Chrome
        # dt = arrow.get(tm, "h:mm A MMM D, YYYY")
        # Firefox
        # dt = arrow.get(tm, "h:mm A D/MMM/YYYY")

        # <time datetime="2020-06-02T06:25:18.000Z">8 h</time>
        tm = dt.get_attribute("datetime")
        dt = arrow.get(tm)
        return dt

    def load_tags(self, hashtag):
        # Using Firefox driver NO WINDOW MODE
        # os.environ["MOZ_HEADLESS"] = "1"
        # driver = webdriver.Firefox(
        #     firefox_profile=get_profile(),
        #     executable_path=f"{os.getcwd()}/src/scraping/driver/geckodriver",
        # )

        driver = webdriver.Chrome(
            options=chrome_options(),
            executable_path=f"{os.getcwd()}/src/data/scraping/driver/chromedriver",
        )

        # f"https://twitter.com/search?q={urllib.parse.quote(hashtag)}%20lang%3Apt%20until%3A2020-03-15%20since%3A2020-03-10&src=typed_query&f=live"
        driver.get(
            f"https://twitter.com/search?q={urllib.parse.quote(hashtag)}%20lang%3Apt&src=typed_query&f=live"
        )

        not_found = True
        while not_found:
            try:
                tweets = driver.find_elements_by_tag_name("article")
                if len(tweets) > 0:
                    not_found = False
                time.sleep(0.1)
            except Exception as e:
                # print(f"ERROR: AdaptiveFiltersBar-target not found : {e}")
                pass

        data = {"hashtag": hashtag, "comments": []}
        for _ in range(self.n_posts_2_extract + 1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            tweets = driver.find_elements_by_tag_name("article")
            for tweet in tweets:
                try:
                    username = tweet.find_element_by_xpath(
                        "./div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span"
                    )
                    comment = tweet.find_element_by_xpath(
                        "./div/div/div/div[2]/div[2]/div[2]"
                    )
                    dt = tweet.find_element_by_xpath(
                        "./div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a/time"
                    )

                    # Old way
                    # dt = tweet.find_element_by_xpath(
                    #     "./div/div[2]/div[2]/div[1]/div/div/div[1]/a"
                    # ).strip()

                    if username and comment:
                        username = username.text.strip()
                        comment = self.treat_comment(comment.text.strip())
                        dt = self.treat_data(dt)

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


class TwitterGeoClient:
    def load_user_geo(self, username):
        # Using Firefox driver NO WINDOW MODE
        # os.environ["MOZ_HEADLESS"] = "1"
        # driver = webdriver.Firefox(
        #     firefox_profile=get_profile(),
        #     executable_path=f"{os.getcwd()}/src/scraping/driver/geckodriver",
        # )

        driver = webdriver.Chrome(
            options=chrome_options(),
            executable_path=f"{os.getcwd()}/src/data/scraping/driver/chromedriver",
        )

        driver.get(f"https://twitter.com/{username}")
        counter, not_found = 15, False
        while not not_found:
            try:
                nome = driver.find_element_by_xpath(
                    "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/span[1]/span"
                )
                not_found = True
            except:
                pass
            time.sleep(0.5)
            counter -= 1
            if counter <= 0:
                not_found = True

        retorno = None
        for xpath in [
            "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[1]/div/div[4]/div/span[1]",
            "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[1]/div/div[3]/div/span[1]",
        ]:
            try:
                cidade = driver.find_element_by_xpath(xpath)
                cidade = cidade.text
                if "," in cidade:
                    cidade = normalizar(cidade.split(",")[0], sort=False)
                else:
                    cidade = normalizar(cidade.split("-")[0], sort=False)
                retorno = [username, cidade]
                break
            except Exception as e:
                # print(username, str(e))
                pass
        driver.close()
        return retorno
