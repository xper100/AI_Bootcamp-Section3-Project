#%%
from os import times
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def get_first_page(search_word):
  naver_first_url = "https://search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=" + str(search_word)

  page = requests.get(naver_first_url)  
  soup = BeautifulSoup(page.content, 'html.parser')
  return page, soup


###################################################################
def get_hospital_naverid(soup):
    # 병원 Naver ID
    hospital_id_step1 = soup.find_all('li', class_='_3YLiU')
    id_list = []
    for id in range(len(hospital_id_step1)):
        id_element = hospital_id_step1[id].attrs['data-loc_plc-doc-id'].split('=')[0]
        id_list.append(id_element)
    return id_list


###################################################################

# 진료종목, 병원이름, 병원주소
def get_info(tag, class_name, soup):
  soup_find_all = soup.find_all(tag, class_= class_name)
  list_items = []
  for i in range(len(soup_find_all)):
    element = soup_find_all[i].text
    list_items.append(element)
  return list_items




# 주와 도시만 뽑기
def get_state_city(address_list):
    state_list = []
    city_list = []
    for i in range(len(address_list)):
      state_id, city_id = address_list[i].split(' ')[:2]
      state_list.append(state_id)
      city_list.append(city_id)

    return state_list, city_list


######################################
######### re로 숫자만 필터링해보기 #########
# 병원 전화번호
def get_contact_info(soup):
  hospital_contact_all = soup.find_all('span', class_='_2ZvRd')
  contact_list = []
  for contact in range(len(hospital_contact_all)):
    contact_element = hospital_contact_all[contact].text
    
    # all contact numbers must have less than 12 digits including '-' between (eg. 031-333-666, 0507-1414-1515, 02-1415-1515, 02-142-4242)
    if len(contact_element) <= 14:
      contact_list.append(contact_element)
    elif len(contact_element) > 14:
      contact_element = contact_element[:14]
      contact_list.append(contact_element)

  return contact_list



###################################################################

# Review 탭 URL
def get_review_page(hospital_id):
  hospital_review_url = "https://pcmap.place.naver.com/hospital/" + hospital_id + "/review/visitor"

  return hospital_review_url


# Home 탭 URl
def get_home_page(hospital_id):
  home_url = "https://pcmap.place.naver.com/hospital/" + hospital_id + "/home"

  return home_url

def get_blog_address(hospital_id):
    home_url = get_home_page(hospital_id)
    page = requests.get(home_url)  
    soup = BeautifulSoup(page.content, 'html.parser')
    blog_address = soup.find('a', attrs = {'class': '_1RUzg'}).text
    return blog_address

def get_avg_stars(hospital_id):
  hospital_review_url = get_review_page(hospital_id)
  
  #------------- 평균평점 가져오기 --------------#
  # 페이지 소스 가져오기
    
  # 객체 생성
  page = requests.get(hospital_review_url)
  soup = BeautifulSoup(page.content, 'html.parser')
  
  # Average Star
  avg_star_zone = soup.find('div', attrs={'class': 'hRJcF'})
  
  avg_star = float(avg_star_zone.find('em').text)

  return avg_star

#%%
def clicking_more_reviews(url, driver):
    try:
        while True:
            driver.find_element_by_class_name('_3iTUo').click()
            print('[댓글 더보기]', end="")
            time.sleep(1)
    except:
        pass


def get_reviews(soup):
    review_list = []
    total_num_review = len(soup.find_all('span', attrs={'class':'_2tObC'}))
    for i in range(total_num_review):
        # Star
        star = soup.find_all('span', attrs={'class':'_2tObC'})[i].text

        # Review comment
        comment = soup.find_all('span', attrs = {'class':'WoYOw'})[i].text

        review_list.append({
            'review_star': star,
            'review_comment': comment
        })
    return review_list, total_num_review


def scraping(id_list):
    # webdriver 경로 설정
    PATH = "/Applications/chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.implicitly_wait(0.1)

    #------------- 특정 병원의 리뷰 URL 불러오기 -------------#
    review_lists = []
    soups = []
    review_counts = []
    for id in id_list:
      hospital_review_url = get_review_page(id)
      driver.get(hospital_review_url)
    #------------- 리뷰 더보기 클릭 --------------#
      clicking_more_reviews(hospital_review_url, driver)
    
    #------------- 평균평점 가져오기 --------------#
    # 페이지 소스 가져오기
      html = driver.page_source
    # 객체 생성
      soup = BeautifulSoup(html, 'html.parser')
      
    #------------- 유저 평점 및 평가 전부 가져오기 --------------#
      review_list, review_count = get_reviews(soup)
      review_lists.append(review_list)
      review_counts.append(review_count)
    #------------- soup 전부 가져오기 --------------#
      soups.append(soup)
    driver.quit()

    return soups, review_lists, review_counts




###### Testing Zone ##########
search_word = "평택항문외과"
page, soup = get_first_page(search_word)

id_list = get_hospital_naverid(soup)

category_list = get_info('span', '_3lc1U', soup) # 진료종목
name_list = get_info('a', '_2pag2', soup) # 병원이름
address_list = get_info('a', '_2ZvRd _2pfMW', soup) # 병원주소


state, city = get_state_city(address_list)

contact_list = get_contact_info(soup)    
blog_address = get_blog_address(id_list[0])    


# soups, review_lists, review_counts = scraping(id_list)

