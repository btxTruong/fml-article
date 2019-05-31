import logging
import queue
import threading
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
from config import config
from postgresql import PostgreSQL


logger = logging.getLogger(__name__)

PARAMS = config()


def crawl_by_label(label, callback_db, num_thread):
    if label == 'topnews':
        base = 'https://www.familug.org'
    else:
        base = 'https://www.familug.org/search/label/{}'.format(label)
    s = requests.Session()

    data = queue.Queue()
    data.put(base)

    def crawl():
        while True:
            try:
                url = data.get(block=False)
            except queue.Empty:
                break

            resp = s.get(url)

            tree = BeautifulSoup(resp.text, 'html.parser')
            older = tree.select('a[class=blog-pager-older-link]')
            try:
                data.put(older[0].get('href'))
            except IndexError:
                logger.info('No more page')
                break

            titles = tree.select('h3 > a')
            for tlt in titles:
                if label == 'topnews' and num_rows_database(label) >= 10:
                    raise SystemExit
                link_article = tlt.get('href')
                callback_db(label, tlt.text, link_article)

    threads = []
    while len(threads) < num_thread and not data.empty():
        thrd = threading.Thread(target=crawl)
        threads.append(thrd)
        thrd.start()

    for thread in threads:
        thread.join()


def database_manipulation(query, args=()):
    with PostgreSQL(PARAMS) as cur:
        cur.execute(query, args)


def create_database(table):
    query = 'CREATE TABLE IF NOT EXISTS {} (title varchar , url varchar )'.format(
        table)
    database_manipulation(query)


def row_exists(tabel, title):
    with PostgreSQL(PARAMS) as cur:
        query = 'select exists(select 1 from {} where title=%s)'.format(tabel)
        cur.execute(query, (title,))
        return cur.fetchone()[0]


def insert_database(table, title, url):
    if not row_exists(table, title):
        query = '''INSERT INTO {0} (title, url) VALUES(%s, %s)'''.format(table)
        database_manipulation(query, args=(title, url))


def num_rows_database(table):
    with PostgreSQL(PARAMS) as cur:
        query = 'select * from {}'.format(table)
        cur.execute(query)
        rv = cur.fetchall()
    return len(rv)


if __name__ == '__main__':
    labels = ['Python', 'Command', 'sysadmin', 'topnews']
    processes = []
    for lb in labels:
        create_database(lb)
        pro = Process(target=crawl_by_label, args=(lb, insert_database, 5))
        processes.append(pro)
        pro.start()

    for p in processes:
        p.join()
