import re
from pathlib import Path
from typing import Dict, List
from playwright.sync_api import Page, expect

def test_homepage_screenshot(page: Page, screenshot_dir: Path):
    page.goto("/")
    page.pause()
    page.screenshot(path=f"{screenshot_dir}/home.png", full_page=True)

def test_homepage_has_logo(page: Page):
    page.goto("/")
    logo = page.locator(".logo")
    expect(logo).to_be_visible()

    logo_subtitle = page.locator('.subtitle')
    expect(logo_subtitle).to_contain_text('Home to the best shows on Linux, Open Source, Security, Privacy, Community, Development, and News')

def test_pagination(page: Page):
    page.goto("/")
    first_card = page.locator('.card').nth(0).text_content
    page_2_button = page.locator('[aria-label="pagination"] >> text=2')
    page_2_button.click()
    page.wait_for_load_state("networkidle")
    assert "/page/2" in page.url
    first_card_second_page = page.locator('.card').nth(0).text_content
    assert first_card != first_card_second_page

def test_rss_feeds(page: Page, expected_rss_feeds: List[Dict[str,str]]):
    page.goto("/")

    for rss_feed in expected_rss_feeds:
        element = page.locator('#rss-feeds-menu > div > a[href^="{}"]'.format(rss_feed['href']))
        expect(element).to_contain_text(rss_feed['title'])


def test_dropdowns(page: Page, expected_dropdown_items):
    page.goto("/")

    for dropdown_item in expected_dropdown_items:
        selector = '.navbar-item > .navbar-dropdown > a[href^="{}"]'.format(dropdown_item['href'])
        element = page.locator(selector)
        expect(element).to_contain_text(dropdown_item['title'])
    


def test_nav(page: Page, expected_dropdowns, expect_nav_items):

    page.goto("/")
    nav = page.locator('#mainnavigation')
    expect(nav).to_be_visible()
    dropdown_nav_items = page.locator('.navbar-start > * > a')
    count = dropdown_nav_items.count()
    for i in range(count):
        expect(dropdown_nav_items.nth(i)).to_contain_text(expected_dropdowns[i]['title'])
        expect(dropdown_nav_items.nth(i)).to_have_attribute('href', expected_dropdowns[i]['href'])


    nav_items = page.locator('.navbar-start > a')
    count = nav_items.count()
    for i in range(count):
        expect(nav_items.nth(i)).to_contain_text(expect_nav_items[i]['title'])
        expect(nav_items.nth(i)).to_have_attribute('href', expect_nav_items[i]['href'])
    
    nav_image = page.locator('.navbar-brand > a > img')

    expect(nav_image.nth(0)).to_be_visible()
    
    
def test_jb_live_indicator(page: Page):
    const simulatedNotLiveResult = '{ total: 0, data: [] }';
    const simulatedLiveResult = '{"total":1,"data":[{"id":50,"uuid":"55b2e9d1-ccf3-4914-9f3f-c5d8a59bd4c1","shortUUID":"bzMpxgG2rDKn9C99GSab92","url":"https://jupiter.tube/videos/watch/55b2e9d1-ccf3-4914-9f3f-c5d8a59bd4c1","name":"LINUX Unplugged 471 - We Broke Our Server","category":{"id":15,"label":"Science & Technology"},"licence":{"id":5,"label":"Attribution - Non Commercial - Share Alike"},"language":{"id":"en","label":"English"},"privacy":{"id":1,"label":"Public"},"nsfw":false,"description":"We broke our server, so lets see if we can fix it live before the show is over!","isLocal":true,"duration":0,"views":0,"viewers":19,"likes":0,"dislikes":0,"thumbnailPath":"/static/thumbnails/b610e5f5-bbb5-4ee1-ac24-421c50f0daf5.jpg","previewPath":"/lazy-static/previews/fcd582d8-68c5-4f00-8a4a-0a8ffde1a4a5.jpg","embedPath":"/videos/embed/55b2e9d1-ccf3-4914-9f3f-c5d8a59bd4c1","createdAt":"2022-08-14T16:26:27.938Z","updatedAt":"2022-08-14T18:53:15.544Z","publishedAt":"2022-08-14T18:53:15.543Z","originallyPublishedAt":null,"isLive":true,"account":{"id":3,"displayName":"JBLive Stream","name":"jblive","url":"https://jupiter.tube/accounts/jblive","host":"jupiter.tube","avatars":[{"width":48,"path":"/lazy-static/avatars/e4d17e7f-a144-4a4a-b5d8-b297b06b727f.png","createdAt":"2022-06-07T23:43:56.565Z","updatedAt":"2022-06-07T23:43:56.565Z"},{"width":120,"path":"/lazy-static/avatars/1340f3e9-d0a7-4bc4-bcbd-a8c865eaf1b8.png","createdAt":"2022-05-30T20:36:19.005Z","updatedAt":"2022-05-30T20:36:19.005Z"}],"avatar":{"width":48,"path":"/lazy-static/avatars/e4d17e7f-a144-4a4a-b5d8-b297b06b727f.png","createdAt":"2022-06-07T23:43:56.565Z","updatedAt":"2022-06-07T23:43:56.565Z"}},"channel":{"id":2,"name":"live","displayName":"live","url":"https://jupiter.tube/video-channels/live","host":"jupiter.tube","avatars":[{"width":48,"path":"/lazy-static/avatars/8acfd2a2-ab4e-48aa-990c-3156a2765d2e.png","createdAt":"2022-06-07T23:43:56.607Z","updatedAt":"2022-06-07T23:43:56.607Z"},{"width":120,"path":"/lazy-static/avatars/e9bcfdb7-90a2-479c-b1da-1ab0e5fc9442.png","createdAt":"2022-05-30T20:38:33.632Z","updatedAt":"2022-05-30T20:38:33.632Z"}],"avatar":{"width":48,"path":"/lazy-static/avatars/8acfd2a2-ab4e-48aa-990c-3156a2765d2e.png","createdAt":"2022-06-07T23:43:56.607Z","updatedAt":"2022-06-07T23:43:56.607Z"}}}]}';
    
    page.goto("/")
    livebutton = page.locator('#livebutton')
    page.evaluate(async () => doLiveHighlight(simulatedLiveResult);)
    expect(livebutton).toHaveCSS('background-color', 'red')
    
    page.evaluate(async () => doLiveHighlight(simulatedNotLiveResult);)
    expect(livebutton).not.toHaveCSS('background-color', 'red')
