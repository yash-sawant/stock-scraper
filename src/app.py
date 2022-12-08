from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
from graph_funcs import get_candlestick
from stock_info import get_historical

# Initialize Flask App
app = Flask(__name__)

import base64
from io import BytesIO
from matplotlib.figure import Figure


def fig_2_img(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig.clf()
    return data


@app.route('/')
def index():
    return plot_single_graph('AAPL')


def plot_single_graph(stock_name):
    title = f"{stock_name} - Last 6 months"
    content = [(fig_2_img(get_candlestick(get_historical(stock_name), title=title)), title)]
    return render_template('dashboard.html', content=content)


@app.route('/search',methods = ['POST'])
def search():
    if request.method == "POST":
        stock_name = dict(request.form).get('search')
    else:
        return redirect(url_for('/'))

    return plot_single_graph(stock_name)


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 8000))
    # app.run(threaded=False, host='0.0.0.0', port=port)
    app.run(threaded=False, host='0.0.0.0', port=8000)
