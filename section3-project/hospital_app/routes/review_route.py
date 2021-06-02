
from flask import Blueprint, request, redirect, url_for, Response
from hospital_app import db

from hospital_app.models.hospital_model import Hospital, delete_hospital
from hospital_app.models.scrape_data import get_avg_stars, get_first_page, get_hospital_naverid, get_info, get_state_city, get_contact_info, \
                                            get_review_page, get_home_page, get_blog_address, clicking_more_reviews, get_reviews,\
                                            scraping




bp = Blueprint('review', __name__)
