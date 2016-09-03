import NaaS
from flask import json
from NaaS.compliments.models import Compliment
import unittest


class NaaSTestCase(unittest.TestCase):

    def setUp(self):
        NaaS.app.config.from_object('config.TestingConfig')
        self.app = NaaS.app.test_client()
        with NaaS.app.app_context():
            NaaS.db.database.init_db()

    def tearDown(self):
        with NaaS.app.app_context():
            conn = NaaS.db.database.get_connection()
            conn.set_isolation_level(0)
            conn.cursor().execute('TRUNCATE compliments')

    def test_home(self):
        rv = self.app.get('/')
        assert json.loads(rv.data) == {"message": "Hi, this is an API that you can use to get a nice compliment."}

    def test_empty_db_index(self):
        rv = self.app.get('/compliments')
        assert json.loads(rv.data) == []

    def test_multiple_published_compliments(self):
        with NaaS.app.app_context():
            compliment1 = Compliment('You\'re my best friend.', True)
            compliment2 = Compliment('I would feel bad if we were stranded on an island and I had to eat you.', True)
            compliment1.save()
            compliment2.save()
        rv = self.app.get('/compliments')
        assert len(json.loads(rv.data)) == 2

    def test_unpublished_compliments(self):
        with NaaS.app.app_context():
            compliment1 = Compliment('I would share my fruit Gushers with you.', True)
            compliment2 = Compliment('Your body fat percentage is perfectly suited for your height.', False)
            compliment1.save()
            compliment2.save()
        rv = self.app.get('/compliments')
        assert len(json.loads(rv.data)) == 1

    def test_get_single_compliment(self):
        with NaaS.app.app_context():
            compliment1 = Compliment('I would share my fruit Gushers with you.', True)
            compliment1.save()
        rv = self.app.get('/compliments/1')
        assert json.loads(rv.data)['text'] == 'I would share my fruit Gushers with you.'

    def test_get_unpublished_compliment(self):
        with NaaS.app.app_context():
            compliment1 = Compliment('Is Heaven missing an angel? If so, I\'m sure you could find it.', False)
            compliment1.save()
        rv = self.app.get('/compliments/1')
        assert json.loads(rv.data)['message'] == 'Oops, nothing to see here.'

    def test_get_random(self):
        with NaaS.app.app_context():
            compliment1 = Compliment('Our time together is like a nap; it never lasts long enough.', True)
            compliment2 = Compliment('Aside from food, you\'re my favorite.', True)
            compliment1.save()
            compliment2.save()
            compliments = [compliment1.text, compliment2.text]
        rv = self.app.get('/compliments/random')
        assert json.loads(rv.data)['text'] in compliments

    def test_submit_compliment(self):
        rv = self.app.post('/compliments', data={'text': 'Your feet aren\'t even gross.'})
        assert json.loads(rv.data)['message'] == 'Compliment added but is waiting for review!'

    def test_submit_duplicate_compliment(self):
        rv = self.app.post('/compliments', data={'text': 'I love the peach fuzz on your lower back.'})
        rv = self.app.post('/compliments', data={'text': 'I love the peach fuzz on your lower back.'})
        assert json.loads(rv.data)['message'] == 'That compliment already exists.'

if __name__ == '__main__':
    unittest.main()
