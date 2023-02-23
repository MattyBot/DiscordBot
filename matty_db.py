import sqlite3

class Database():
    def __init__(self) -> None:
        self.filename = 'matty_db.sqlite'

    def startup(self):
        create_faqs_table = '''
            CREATE TABLE IF NOT EXISTS faqs_db(
            faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id TEXT,
            question TEXT,
            answer TEXT,
            creator TEXT,
            datecreated TEXT
            )
            '''
        create_events_table = '''
            CREATE TABLE IF NOT EXISTS events_db(
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            server_id INTEGER,
            event_name TEXT,
            date TEXT,
            time TEXT,
            location TEXT,
            description TEXT,
            creator TEXT,
            datecreated TEXT
            )
            '''
        create_responses_table = '''
            CREATE TABLE IF NOT EXISTS responses_db(
            response_id INTEGER PRIMARY KEY,
            event_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            response TEXT NOT NULL,
            FOREIGN KEY(event_id) REFERENCES events_db(event_id)
            )
            '''
        self.query(create_faqs_table)
        self.query(create_events_table)
        self.query(create_responses_table)
        
    def query(self, query):
        db = sqlite3.connect(self.filename)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        db.close()
    
    def query_input(self, query, vals):
        db = sqlite3.connect(self.filename)
        cursor = db.cursor()
        cursor.execute(query,vals)
        db.commit()
        db.close()

    def query_fetch(self, query, params=()):
        db = sqlite3.connect(self.filename)
        cursor = db.cursor()
        cursor.execute(query, params)
        db.commit()
        result = cursor.fetchall()
        db.close()
        return result
        

        