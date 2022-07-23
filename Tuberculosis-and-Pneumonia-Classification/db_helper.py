import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data.db")

conn = sqlite3.connect(db_path, check_same_thread=False)
c = conn.cursor()

def create_table():

	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT, location TEXT, postdate DATE)')

def add_data(author,title,article,location,postdate):

	c.execute('INSERT INTO blogtable(author,title,article,location,postdate) VALUES (?,?,?,?,?)',(author,title,article,location,postdate))
	conn.commit()

def view_all_notes():

	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data

def view_all_titles():

	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data

def get_single_blog(title):
    
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_title(title):

	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_author(author):

	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data

def get_blog_by_msg(article):

	c.execute("SELECT * FROM blogtable WHERE article like '%{}%'".format(article))
	data = c.fetchall()
	return data

def edit_blog_author(author,new_author):

	c.execute('UPDATE blogtable SET author ="{}" WHERE author="{}"'.format(new_author,author))
	conn.commit()
	data = c.fetchall()
	return data

def edit_blog_title(title,new_title):

	c.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_title,title))
	conn.commit()
	data = c.fetchall()
	return data

def edit_blog_article(article,new_article):

	c.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_article,article))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(title):

	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()