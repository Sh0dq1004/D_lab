import os
import json
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup as bs

def get_obj_id(filePath):
    with open(f"json_files\{filePath}", "r", encoding="utf-8", errors="ignore") as f:
        return [i["objectID"] for i in json.load(f) if "objectID" in list(i)]

def get_text(objIdLst):
    with sync_playwright() as playwriht:
        browser=playwriht.firefox.launch(headless=False)
        context=browser.new_context()
        page=context.new_page()
        page.goto("https://daigovideolab.jp/landing")

        page.click('//*[@id="root"]/header/div[1]/div/div[2]/button[1]')
        page.fill('div.MuiFormControl-root:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)', "kanokaiki@gmail.com")
        page.fill(".MuiInputBase-inputAdornedEnd", "iRr5ipi94LF4Qn")
        page.click('button.MuiButtonBase-root:nth-child(5)')
        page.wait_for_url("https://daigovideolab.jp/")

        #multiprocessing を使えば早くなります
        for i in objIdLst:
            subpage=context.new_page()
            subpage.goto(f"https://daigovideolab.jp/blog/{i}")
            time.sleep(10)# page.wait_for_selector("CSS SELECTOR")でやれば最適だと思います。Fireboxインストールするの面倒だったのでこうしました。
            html=subpage.content()
            page.close()
            
            with open(f"article_folder\{i}.txt","w",encoding="utf-8",errors="ignore") as f:
                f.writelines(html2str(html))
        subpage.close()

def html2str(html):
    soup=bs(html, "html.parser")
    textlst=[]
    for i in soup.find_all("div"):
        text=i.get_text()
        if text != "":
            textlst.append(text)
            break
    return textlst

if __name__=="__main__":
    objIdLst=[]
    for i in os.listdir("json_files"):
        objIdLst.extend(get_obj_id(i))
    get_text(objIdLst)
    