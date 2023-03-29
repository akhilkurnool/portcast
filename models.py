from peewee import SqliteDatabase, Model, AutoField, TextField, IntegerField

db = SqliteDatabase('portcast.db')

class BaseModel(Model):
  class Meta:
    database = db

class Paragraphs(BaseModel):
  id = AutoField(primary_key=True)
  paragraph = TextField()

class WordFrequency(BaseModel):
  word = TextField(primary_key=True)
  frequency = IntegerField()


db.connect()
db.create_tables([Paragraphs, WordFrequency])

