import re
import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook

cookies = {
    '_CIAN_GK': '68dd4799-93a8-41d0-97cb-decac1f5923e',
    'SLG_G_WPT_TO': 'ru',
    'SLG_GWPT_Show_Hide_tmp': '1',
    'SLG_wptGlobTipTmp': '1',
    'session_region_id': '1',
    'session_main_town_region_id': '1',
    'adb': '1',
    'login_mro_popup': '1',
    'cookie_agreement_accepted': '1',
    'distance_calculating_onboarding_counter': '3',
    'hide_route_tab_onboarding': '1',
    'feedback_banner_hide': '1',
    '_ga': 'GA1.2.1220383993.1661351406',
    'uxs_uid': '3f8731a0-23b9-11ed-b74f-c9ef069edf25',
    'countCallNowPopupShowed': '0%3A1661367807923',
    'cf_clearance': '74c40xFlfNNUOF8LarVjlKFA.ZqWmaJTz.6pjS9z8U0-1661499578-0-250',
    'ism_visited': '1',
    'rrpvid': '823249126290869',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'sopr_session': 'c1955d8a59d7462a',
    '__cf_bm': 'EPE6lGRUn.gw6Ni.alardwR.ykC_Q2sHwpJLSLr69HI-1662883293-0-AZBKounWOg11r7c0yjzy4G0MEKRJVUyqJMcgVNy/xdpatKZ4QoN1a5upVBEntv3qUYjKeVd4s5GkBvHrdc0XopQ=',
    'anti_bot': '2|1:0|10:1662883407|8:anti_bot|40:eyJyZW1vdGVfaXAiOiAiNDYuMTcyLjIyMy42NiJ9|f32870f2956317ff425bdc8949b204753b249b984cb43a86aa37e9e94341f891',
}

headers = {
    'authority': 'www.cian.ru',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en,en-US;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_CIAN_GK=68dd4799-93a8-41d0-97cb-decac1f5923e; SLG_G_WPT_TO=ru; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; session_region_id=1; session_main_town_region_id=1; adb=1; login_mro_popup=1; cookie_agreement_accepted=1; distance_calculating_onboarding_counter=3; hide_route_tab_onboarding=1; feedback_banner_hide=1; _ga=GA1.2.1220383993.1661351406; uxs_uid=3f8731a0-23b9-11ed-b74f-c9ef069edf25; countCallNowPopupShowed=0%3A1661367807923; cf_clearance=74c40xFlfNNUOF8LarVjlKFA.ZqWmaJTz.6pjS9z8U0-1661499578-0-250; ism_visited=1; rrpvid=823249126290869; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; sopr_session=c1955d8a59d7462a; __cf_bm=EPE6lGRUn.gw6Ni.alardwR.ykC_Q2sHwpJLSLr69HI-1662883293-0-AZBKounWOg11r7c0yjzy4G0MEKRJVUyqJMcgVNy/xdpatKZ4QoN1a5upVBEntv3qUYjKeVd4s5GkBvHrdc0XopQ=; anti_bot=2|1:0|10:1662883407|8:anti_bot|40:eyJyZW1vdGVfaXAiOiAiNDYuMTcyLjIyMy42NiJ9|f32870f2956317ff425bdc8949b204753b249b984cb43a86aa37e9e94341f891',
    'if-none-match': 'W/"9d7b4-Oug9zLBKlTg+q1+/BMzTCJZVmxg"',
    'referer': 'https://www.cian.ru/captcha/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera GX";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.78',
}


wb = load_workbook('Data.xlsx')
ws = wb.active


async def gather_data():
    params = {
    'offerType[0]': 'suburban',
    'regionId': '4593',
    'page': '1',
    }
    async with aiohttp.ClientSession() as session:
        r = await session.get('https://www.cian.ru/realtors/', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(await r.text(), 'lxml')
        tasks = []
        for page in range(1, int(soup.find_all(class_='_9400a595a7--content--sGuO7')[-1].text) + 1):
            task = asyncio.create_task(get_data_realtors(page,session))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def get_data_realtors(page,session):
    params = {
    'offerType[0]': 'suburban',
    'regionId': '4593', # 4593
    'page': f'{page}',
    }
    await asyncio.sleep(2)
    r = await session.get('https://www.cian.ru/realtors/', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(await r.text(), 'lxml')
    # Получения javascript.
    js = soup.find_all('script')[-6].text    

    # Users id.
    
    ids = re.findall(r"\"cianUserId\":(\d+)", js)

    for counter, id in enumerate(ids):
        params = {
        'deal_type': 'sale',
        'engine_version': '2',
        'id_user': f'{id}',
        'offer_type': 'suburban',
        'p':'1'
        }
        # Проверка на наличие объектов.
        status = False
        if soup.find_all('div', class_='_9400a595a7--right--EuJ9l')[counter].find('span').text != 'Нет объектов': 
            await asyncio.sleep(5)
            response  = await session.get(f'https://www.cian.ru/agents/{id}/', headers=headers, cookies=cookies)
            
            soup2 = BeautifulSoup(await response.text(),'lxml')
            try:
                js_number = soup2.find_all('script')[-6].text
            except:
                with open('i.html','w',encoding='utf-8')as f:
                    f.write(soup2.prettify())
                time.sleep(10)
                print('ошибка')
                continue
            # Номер риелтора
            try:
                part_number = soup2.find(class_='_3ea6fa5da8--phones_minimized--XieZH').find('span').text.replace(' ', '')[2:].split('-')[0]
            except:
                continue

            number = '+7'+re.search(fr'\"number\":\"({part_number}\d+)\"', js_number)[1]
    
            # Проверка есть ли продажа загородной недвижимости.
            property = soup2.find('div', class_='_3ea6fa5da8--name--xlUVq', text='Продажа загородной недвижимости')
            if property:
                link = property.find_previous().find(class_='realtor-reviews-frontend-link_component-link-6KsidO9E5ia')
                if link:
                    # Ссылка на подробнее в загородной недвижимости
                    url = 'https://www.cian.ru/cat.php'
                    resp = await session.get(url, params=params, headers=headers, cookies=cookies)
                    soup3 = BeautifulSoup(await resp.text(),'lxml')
                    with open('links.txt','a',encoding='utf-8')as f:
                        f.write(soup3.prettify())
                    if soup3.find(class_='_93444fe79c--list-item--FFjMz _93444fe79c--list-item--active--WifA5'):
                        status = await check_price(session,url,id)
                    else:
                        prices = soup3.find_all('span', {'data-mark':'MainPrice'})
                        for price in prices:
                            if int(price.text.replace('₽','').replace(' ','').strip()) > 40_000_000:
                                status = True
                                break
                else:
                    prices = property.find_previous().find_all(class_='_3ea6fa5da8--header--JV__7')
                    for price in prices:
                        # Если цена объекта больше 40 млн, записать номер телефона в таблицу.
                        if int(price.text.replace('₽','').replace(' ','').strip()) > 40_000_000:
                            status = True
                            break
                if status:
                    ws.append([number,f'https://www.cian.ru/agents/{id}/'])

async def check_price(session,url,id):
    page = 1
    params = {
        'deal_type': 'sale',
        'engine_version': '2',
        'id_user': f'{id}',
        'offer_type': 'suburban',
        'p':f'{page}'
    }
    while True:
        response = await session.get(url,params =params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        print('ok')
        if page>1:
            if soup.find(class_='_93444fe79c--list-item--FFjMz _93444fe79c--list-item--active--WifA5').text == '1':
                break
        prices = soup.find_all('span', {'data-mark':'MainPrice'})
        for price in prices:
            if int(price.text.replace('₽','').replace(' ','').strip()) > 40_000_000:
                return True
        page= page+1

    return False


def main():
    asyncio.get_event_loop().run_until_complete(gather_data())
    wb.save('Data.xlsx')
if __name__ =='__main__':
    main()