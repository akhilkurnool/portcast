from peewee import SqliteDatabase, Model, AutoField, TextField, IntegerField
import os

database_url = os.getenv('DATABASE_URL', 'portcast.db')
db = SqliteDatabase(database_url)

class BaseModel(Model):
  class Meta:
    database = db

class Paragraphs(BaseModel):
  id = AutoField(primary_key=True)
  paragraph = TextField()

class WordFrequency(BaseModel):
  word = TextField(primary_key=True)
  frequency = IntegerField(default=0)

db.connect()
db.create_tables([Paragraphs, WordFrequency])
