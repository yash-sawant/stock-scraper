import datetime
from flask import Flask, request, render_template, redirect, url_for
from graph_funcs import plot_single_graph, plot_eval_graph
from stock_info import get_historical
from db_funcs import load_database, refresh_database
from web_scraping import get_stock_news, get_new_articles
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from prediction import predict, evaluate

# Initialize Flask App
app = Flask(__name__)

DEFAULT_STOCK = 'GOOG'
NEWS_LIMIT = 10


# df = refresh_database()


@app.route('/')
def index():
    return redirect(url_for('market'))


@app.route('/news')
def news():
    df = load_database(last_n=NEWS_LIMIT)
    dt_str = lambda x: datetime.datetime.strftime(datetime.datetime.fromisoformat(x), '%b %d, %Y, %H:%M %Z')
    articles = [(row[0], row[1], row[2], dt_str(row[3])) for i, row in df.iloc[::-1].iterrows()]
    print('Rendering news page.')
    return render_template('news.html', articles=articles[:NEWS_LIMIT])


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        stock_name = dict(request.form).get('search')
        data = get_historical(stock_name)
        content = plot_single_graph(stock_name, data)
        return render_template('dashboard.html', content=content)
    else:
        return redirect(url_for('index'))


@app.route('/market', methods=['POST', 'GET'])
def market():
    if request.method == "POST":
        stock_name = dict(request.form).get('search')
    else:
        stock_name = DEFAULT_STOCK
    news = get_stock_news(stock_name)
    data = get_historical(stock_name)
    pred = predict(data)
    content = plot_single_graph(stock_name, data, pred=pred)
    return render_template('dashboard.html', content=content, news=news[:NEWS_LIMIT])


@app.route('/evaluation', methods=['POST', 'GET'])
def evaluation():
    if request.method == "POST":
        stock_name = dict(request.form).get('search')
    else:
        stock_name = DEFAULT_STOCK
    data = get_historical(stock_name)

    pred, true = evaluate(data)

    content = plot_eval_graph(stock_name, data, pred, true)
    return render_template('evaluation.html', content=content)


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 8000))
    # app.run(threaded=False, host='0.0.0.0', port=port)
    app.run(debug=True, threaded=False, host='0.0.0.0', port=8080)
