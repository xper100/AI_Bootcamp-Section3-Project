from hospital_app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    review_star = db.Column(db.Float, nullable = False)
    review_comment = db.Column(db.VARCHAR(500))
    

    # tweets = db.relationship('Tweet', backref = 'user', cascade = "all,delete")
    def __repr__(self):
        return f"Id: {self.id}, Hospital_id: {self.hospital_id}"


