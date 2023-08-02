import sqlite3

CONN = sqlite3.connect("lib/dogs.db")
CURSOR = CONN.cursor()


class Dog:
    def __init__(self, name, breed, id=1):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
        id INTEGER PRIMARY KEY,
        name TEXT,
        breed TEXT
        )
    """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
        DROP TABLE if EXISTS dogs
    """
        CURSOR.execute(sql)

    def save(self):
        sql = """
        INSERT INTO dogs (name, breed)
        VALUES (?,?)
    """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = """
        SELECT * FROM dogs
    """
        dogs = CURSOR.execute(sql).fetchall()
        all = [cls.new_from_db(row) for row in dogs]
        return all

    @classmethod
    def find_by_name(cls, name):
        sql = """
        SELECT * FROM dogs
        WHERE name = ?
        LIMIT 1
    """
        row = CURSOR.execute(sql, (name,)).fetchone()
        dog = cls.new_from_db(row)
        return dog

    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT * FROM dogs
        WHERE id = ?
        LIMIT 1
    """
        row = CURSOR.execute(sql, (id,)).fetchone()
        dog = cls.new_from_db(row)
        return dog

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
        SELECT * FROM dogs
        WHERE name = ? AND breed = ?
        LIMIT 1
    """
        dog = CURSOR.execute(sql, (name, breed)).fetchone()

        if not dog:
            new_dog = cls.create(name, breed)
            return new_dog

        found = cls.new_from_db(dog)
        return found

    # not working

    def update(self):
        sql = """
        UPDATE dogs SET name = ?
        WHERE name = ?
    """
        old_name = CURSOR.execute(
            """SELECT * FROM dogs WHERE id =? """, (self.id,)
        ).fetchone()[1]
        CURSOR.execute(sql, (self.name, old_name))
