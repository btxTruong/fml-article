from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
from config import config
from postgresql import PostgreSQL

app = Flask(__name__)

PARAMS = config()


def query_db(query, args=(), one=False):
    with PostgreSQL(PARAMS) as cur:
        cur.execute(query, args)
        rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def rows_database(table, length=False):
    rows = query_db('select * from {}'.format(table))
    return len(rows) if length else rows


def fetch_data(table, offset=0, per_page=10):
    return rows_database(table)[offset: offset + per_page]


@app.route("/")
def index():
    return render_template('fml_index.html')


@app.route("/python")
def python():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total_article = rows_database('Python', length=True)
    data_python = fetch_data('Python', offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total_article,
                            css_framework='bootstrap4')

    return render_template('fml_python.html',
                           pythons=data_python,
                           page=page,
                           per_page=per_page,
                           pagination_python=pagination)


@app.route('/command')
def command():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total_article = rows_database('Command', length=True)
    data_command = fetch_data('Command', offset=offset,
                              per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total_article,
                            css_framework='bootstrap4')

    return render_template('fml_command.html',
                           commands=data_command,
                           page=page,
                           per_page=per_page,
                           pagination_command=pagination)


@app.route('/sysadmin')
def sysadmin():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total_article = rows_database('sysadmin', length=True)
    data_sysadmin = fetch_data('sysadmin', offset=offset,
                               per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total_article,
                            css_framework='bootstrap4')

    return render_template('fml_sysadmin.html',
                           sysadmins=data_sysadmin,
                           page=page,
                           per_page=per_page,
                           pagination_sysadmin=pagination)


@app.route('/topnews')
def topnews():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total_article = rows_database('topnews', length=True)
    data_topnews = fetch_data('topnews', offset=offset,
                              per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total_article,
                            css_framework='bootstrap4')

    return render_template('fml_topnews.html',
                           topnews=data_topnews,
                           page=page,
                           per_page=per_page,
                           pagination_topnews=pagination)


if __name__ == '__main__':
    app.run(debug=True)
