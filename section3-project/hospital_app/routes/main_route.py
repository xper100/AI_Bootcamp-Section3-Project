from flask import Blueprint, render_template, request, redirect
from hospital_app import db, engine, session
from hospital_app.models.hospital_model import Hospital
from hospital_app.models.scrape_data import get_avg_stars, get_first_page, get_hospital_naverid, get_info, get_state_city, get_contact_info, \
                                            get_review_page, get_home_page, get_blog_address, clicking_more_reviews, get_reviews,\
                                            scraping

bp = Blueprint('main', __name__)

@bp.route('/', methods=['POST','GET']) 
def index():
    if request.method == 'POST':
        search_word = request.form['local-category']

        # 검색단어를 토대로 데이터 스크래핑하기
        # 1. page와 soup 얻기 ["https://search.naver.com/search.naver?sm=mtp_hty.top&where=m&query=" + str(search_word)]
        page, soup = get_first_page(search_word)
        # 2. 병원 Naver ID리스트 얻기
        id_list = get_hospital_naverid(soup)
        # 3. 병원 정보 얻기 [진료과목, 병원이름, 병원주소, 시, 도시, 병원 전화번호]
        
        category_list = get_info('span', '_3lc1U', soup) # 진료과목
        name_list = get_info('a', '_2pag2', soup) # 병원이름
        address_list = get_info('a', '_2ZvRd _2pfMW', soup) # 병원주소
        
        # 병원주소의 시, 도시
        state_list, city_list = get_state_city(address_list)
        # 전화번호
        
        contact_list = get_contact_info(soup) 
        
        # 4. 병원 리뷰관련 정보 얻기
        hospital_review_urls = []
        home_urls = []
        blog_address_list = []
        avg_star_list = []
        
        for id in id_list:
            hospital_review_url =  get_review_page(id)
            home_url = get_home_page(id)
            blog_address = get_blog_address(id)
            avg_star = get_avg_stars(id)
          
            # Append
            hospital_review_urls.append(hospital_review_url)
            home_urls.append(home_url)
            blog_address_list.append(blog_address)
            avg_star_list.append(avg_star)

        with session:
            session.begin()
            try:
                # 5. 모든 정보 가져오기
                data_list = []
                for i in range(len(id_list)):
                    searched_data = Hospital(
                        id = id_list[i],
                        category = category_list[i],
                        hospitalname = name_list[i],
                        address = address_list[i],
                        avg_star = avg_star_list[i],
                        city = city_list[i],
                        state = state_list[i],
                        contact_num = contact_list[i],
                        blog_address = blog_address_list[i],
                    )

                data_list.append(searched_data)


                session.add_all(data_list)
                
            except:
                session.rollback()
                raise
                
            else:
                session.commit()
                return "stored data successfully"
        # try:
            
        #     # 5. 모든 정보 가져오기
        #     data_list = []
        #     for i in range(len(id_list)):
        #         searched_data = Hospital(
        #             id = id_list[i],
        #             category = category_list[i],
        #             hospitalname = name_list[i],
        #             address = address_list[i],
        #             avg_star = avg_star_list[i],
        #             city = city_list[i],
        #             state = state_list[i],
        #             contact_num = contact_list[i],
        #             blog_address = blog_address_list[i],
        #         )
        #         data_list.append(searched_data)
                
        #     db.session.add_all(data_list)
        #     db.session.commit()
            
        #     return "stored data successfully"
        # except:
        #     return 'There was an issue searching for your hospital'
            
    else:
        # search_history = Hospital.query.all()
        return render_template('index.html')
