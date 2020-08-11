# from platypos import db
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(254), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     name = db.Column(db.String(255), nullable=False)
#     surname = db.Column(db.String(255), nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.email}','{self.name}','{self.surname}')"
