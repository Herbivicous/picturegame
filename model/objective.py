""" model.objective """

from random import choice
from string import ascii_lowercase
from os.path import isfile, join

from model import db, ma

# pylint: disable=no-member

class Objective(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	points = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String, nullable=False)

	def __repr__(self):
		return f'<Objective "{self.description}" for {self.points} points>'

class Picture(db.Model):
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
	objective_id = db.Column(db.Integer, db.ForeignKey('objective.id'), primary_key=True)

	filename = db.Column(db.String, nullable=False)
	status = db.Column(db.Integer, nullable=False)

	objective = db.relationship('Objective', backref=db.backref('teams', cascade='all, delete'))

	def __repr__(self):
		return f'<Picture for {self.objective} by {self.team.name}, status={self.status}>'

# =================================== SCHEMA ===================================

class ObjectiveSchema(ma.Schema):
	class Meta:
		model = Objective
		fields = ('id', 'points', 'description')

class PictureSchema(ma.Schema):
	class Meta:
		model = Picture
		fields = ('objective', 'filename', 'status')
	objective = ma.Pluck(ObjectiveSchema, 'id')

# ==================================== UTILS ====================================

from path import PATH
def save_file(file):
	while True:
		filename = ''.join(choice(ascii_lowercase) for i in range(10)) + '.jpg'
		if not isfile(join(PATH, 'uploads', filename)):
			file.save(join(PATH, 'uploads', filename))
			return filename
