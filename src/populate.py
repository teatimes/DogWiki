from src.apps.authentication.models import WORK_TITLES, WORK_FIELD, YEAR_CHOICES Users as User

from src.apps.litterature.models import Topic

topics = [
	'agility',
	'hunting',
	'obidience',
	'therapydog',
	'clickertraining',
	'police dog'
]

def create_topics():
	for topic in topics:
		t = Topic.objects.create(name=topic)
		t.save()


users = {
	[
		'Kari', 'Nordmann', 'karin', YEAR_CHOICES[1950], 'kari@examlple.com', None, 
		'agility', '123qwe123qwe'
	], 
	[

		'Ola', 'Nordmann', 'olan', YEAR_CHOICES[1972], 'ola@examlple.com', None,
		'clickertraining, therapy dog', '123qwe123qwe'
	],
	[
		'Truls', 'Hansen', 'trulsh', YEAR_CHOICES[1991], 'truls@examlple.com', None,
		'hunting', '123qwe123qwe'
	]
}

def create_users():
	for user in users:
		u = Users.objects.create(
				first_name=user[0],
				last_name=user[1],
				username=user[2],
				birth_year=user[3],
				email=user[4],
				profile_image=user[5],
				competence=user[6],
			)
		u.save()
		u.setPassword