import psycopg2.extras
from ..db.database import get_connection
from .. import app


class Compliment(object):

    def __init__(self, text, published=False):
        self.text = text
        self.published = published

    @classmethod
    def _execute_query(cls, *query):
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(*query)
            conn.commit()
            return cur
        except Exception as e:
            if e.pgcode == '23505':
                raise Exception('That compliment already exists.')
            app.logger.error(e)

    @classmethod
    def get_all(cls):
        cur = cls._execute_query(
            "SELECT * FROM compliments WHERE published = True")
        return cur.fetchall()

    @classmethod
    def get_by_id(cls, id):
        cur = cls._execute_query(
            "SELECT * FROM compliments WHERE id = %s and published = True", (id,))
        return cur.fetchone()

    @classmethod
    def get_random(cls):
        cur = cls._execute_query(
            "SELECT * FROM compliments WHERE published = True ORDER BY RANDOM() LIMIT 1")
        return cur.fetchone()

    def save(self):
        return self.__class__._execute_query("INSERT INTO compliments (text, published) VALUES (%s, %s)", (self.text, self.published))
