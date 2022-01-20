import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from faker.providers.person.en import Provider

import sqlite3


def data_to_csv(items, csv_name):
    """
    Writes all the data to a csv file
    """
    data = []
    for post in items:
        data.append(post)

    df = pd.DataFrame(data)
    data_dir = f'{os.getcwd()}/data'
    csv_url = f'{data_dir}/{csv_name}.csv'
    df.to_csv(csv_url, index=False)


def show_tables():
    """
    Shows all the tables present in the database
    """
    sqlEngine = create_engine(
        'mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)

    dbConnection = sqlEngine.connect()

    frame = pd.read_sql("select * from test.frizzl", dbConnection)
    pd.set_option('display.expand_frame_repr', False)
    dbConnection.close()

    print(frame)


def get_most_liked_post():
    """
    Gets information about the most lliked post and write it to a csv
    """

    conn = sqlite3.connect('frizzl') 
    c = conn.cursor()
                    
    c.execute('''SELECT * FROM posts''')

    df = pd.DataFrame(c.fetchall(), columns = ['likes'])
    max_likes = df['likes'].count().max()
   
    print(f'Max likes: {max_likes}')
    return df.to_json()
    

def generate_random_users(n):
    """
    Generates random users and adds them to the database and
    returns users
    """
    conn = sqlite3.connect('frizzl')
    df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate'])
    for _ in range(n):
        df['First'] = random_names('first_names')
        df['Last'] = random_names('last_names') 
        df['Gender'] = random_genders()
        df['Birthdate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2008-01-01'), size=size)


    df.to_sql('users', con=conn, if_exists='append')
    return df.to_json()




















def random_names(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)

def random_genders(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)

def random_dates(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)


