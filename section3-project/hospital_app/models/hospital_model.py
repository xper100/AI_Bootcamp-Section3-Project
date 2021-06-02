from hospital_app import db


class Hospital(db.Model):
    __tablename__ = 'hospital'

    id = db.Column(db.VARCHAR(100), primary_key = True)
    category = db.Column(db.VARCHAR(100), nullable = False)
    hospitalname = db.Column(db.VARCHAR(100), nullable = False)
    address = db.Column(db.VARCHAR(100), nullable = False)
    avg_star = db.Column(db.Float)
    city = db.Column(db.VARCHAR(64))
    state = db.Column(db.VARCHAR(64))
    contact_num = db.Column(db.VARCHAR(100))
    blog_address = db.Column(db.VARCHAR(200))
    
    # reviews = db.relationship('Review', backref='hospital', cascade = "all,delete")
    def __repr__(self):
        return '<Hospital %r>' % self.hospitalname


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key = True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable = False)
    review_star = db.Column(db.Float, nullable = False)
    review_comment = db.Column(db.VARCHAR(500))
    
    

    # tweets = db.relationship('Tweet', backref = 'user', cascade = "all,delete")
    def __repr__(self):
        return '<User %r>' % self.hospital_id



def delete_hospital(id):
    hospital = Hospital.query.filter(Hospital.id == id).first()
    db.session.delete(hospital)
    db.session.commit()


# def update_hospital(id):
#     hospital = Hospital.query.filter(Hospital.id == id).\
#         update()

#     db.session.commit()

# def add_hospital(raw_data):
#     new_data = Hospital(
#         id = raw_data['id'],
#         category = raw_data['category'],
#         hospitalname = raw_data['hospitalname'],
#         address = raw_data['address'],
#         avg_star = raw_data['avg_star'],
#         city = raw_data['city'],
#         state = raw_data['state'],
#         contact_num = raw_data['contact_num'],
#         blog_address = raw_data['blog_address'],
#     )
#     if Hospital.query.filter(Hospital.id == new_data.id).first() == None:
#         db.session.add(new_data)
#         db.session.commit()


# def get_hospitals():
#     return Hospital.query.all()

# def delete_user(hospital_id):
#     hospital = Hospital.query.filter(Hospital.id == hospital_id).first()
#     db.session.delete(hospital)
#     db.session.commit()
#%%
# from hospital_app.models.scrape_data import get_first_page, get_hospital_naverid, get_info, get_state_city, get_contact_info, \
#                                             get_review_page, get_home_page, get_blog_address, clicking_more_reviews, get_reviews,\
#                                             scraping, get_avg_stars
# import pandas as pd
# import csv

# search_word = '평택항문외과'
# def get_data_as_list(search_word):
#     page, soup = get_first_page(search_word)
#     # 2. 병원 Naver ID리스트 얻기
#     id_list = get_hospital_naverid(soup)
#     # 3. 병원 정보 얻기 [진료과목, 병원이름, 병원주소, 시, 도시, 병원 전화번호]
    
#     category_list = get_info('span', '_3lc1U', soup) # 진료과목
#     name_list = get_info('a', '_2pag2', soup) # 병원이름
#     address_list = get_info('a', '_2ZvRd _2pfMW', soup) # 병원주소
    
#     # 병원주소의 시, 도시
#     state_list = []
#     city_list = []
#     for i in range(len(address_list)):
#         state, city = get_state_city(address_list[i])
#         state_list.append(state)
#         city_list.append(city) 
#     # 전화번호
    
#     contact_list = get_contact_info(soup) 

#     # 4. 병원 리뷰관련 정보 얻기
#     avg_star_list = get_avg_stars(soup)
#     breakpoint()
#     hospital_review_urls = []
#     home_urls = []
#     blog_address_list = []
#     for id in id_list:
#         hospital_id = id_list[id]
#         hospital_review_url =  get_review_page(hospital_id)
#         home_url = get_home_page(hospital_id)
#         blog_address = get_blog_address(hospital_id)
        
#         # Append
#         hospital_review_urls.append(hospital_review_url)
#         home_urls.append(home_url)
#         blog_address_list.append(blog_address)

    
    

#     return df



# idx = 0
# df = pd.DataFrame(columns = ('id', 'category', 'hospitalname','address','avg_star', 'city', \
#                              'state', 'contact_num', 'blog_address', 'avr_star')) 

# df.loc[idx] = 


# id = db.Column(db.Integer, primary_key = True)
# category = db.Column(db.VARCHAR(100), nullable = False)
# hospitalname = db.Column(db.VARCHAR(100), nullable = False)
# address = db.Column(db.VARCHAR(100), nullable = False)
# avg_star = db.Column(db.Float)
# city = db.Column(db.VARCHAR(64))
# state = db.Column(db.VARCHAR(64))
# contact_num = db.Column(db.VARCHAR(100))
# blog_address = db.Column(db.VARCHAR(200))
# avg_star    
# %%
