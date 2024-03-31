# 因为selenium的更新异常频繁，原本外面套壳类browser.py已经无法满足需求，所以直接继承webdriver.Chrome类，以便后续更新
# 暂时挂起
import copy
from typing import List
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class webDriver(webdriver.Chrome):
    run_state = 0

    def __init__(
        self,
        proxy=None,
        options: List[str] = None,
        options_dict=None,
        page_load_strategy="normal",
        id=None,
    ):
        self.id = id
        t_options = Options()
        if proxy is not None:
            t_options.add_argument(f"--proxy-server={proxy}")
        if options is not None:
            for _ in options:
                t_options.add_argument(_)
        t_options.add_argument("--enable-javascript")
        t_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        t_options.add_experimental_option("useAutomationExtension", False)
        t_options.page_load_strategy = page_load_strategy
        if options_dict is not None:
            for k, v in options_dict.items():
                t_options.add_experimental_option(k, v)
        super().__init__(options=t_options)

        # js注入
        with open("./stealth.min.js") as f:
            js = f.read()
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

    def page_source_selector(self) -> Selector:
        _ = copy.deepcopy(self.page_source)
        _ = Selector(text=_)
        return _

    def find_element_by_xpath(self, xpath) -> WebElement:
        try:
            element = self.find_element(by=By.XPATH, value=xpath)
            return element
        except Exception as e:
            return None

    def find_elements_by_xpath(self, xpath) -> List[WebElement]:
        try:
            element = self.find_elements(by=By.XPATH, value=xpath)
            return element
        except Exception as e:
            return []

    def wait_element_by_xpath(self, xpath: str, wait_time: int = 5) -> WebElement:
        try:
            Wait(self, wait_time).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element = self.find_element(by=By.XPATH, value=xpath)
            return element
        except Exception as e:
            return None

    def find_element_in_shadow_root_by_xpath_id(
        self, host_element_xpath: str, id: str
    ) -> WebElement:
        try:
            shadow_root_script = " return arguments[0].shadowRoot;"
            host_element = self.find_element_by_xpath(host_element_xpath)
            shadow_root = self.execute_script(shadow_root_script, host_element)
            if (element := shadow_root.find_element(By.ID, id)) is not None:
                return element
        except:
            return None

    def move_to_element(self, element):
        ActionChains(self).move_to_element(element).perform()

    def down_space(self):
        ActionChains(self).key_down(Keys.SPACE)

    def up_space(self):
        ActionChains(self).key_up(Keys.SPACE)

    def get_video_length(self):
        video_list = self.page_source_selector().xpath(
            '//ytd-rich-item-renderer[@class="style-scope ytd-rich-grid-row"]/div/ytd-rich-grid-media/div/div/ytd-thumbnail[1]//a[@id="thumbnail"]'
        )
        return len(video_list)
