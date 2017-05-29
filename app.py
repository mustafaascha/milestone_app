from flask import Flask, render_template, request, redirect

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

colors = {
        'Black': '#000000', 
        'Red': '#FF0000',
        'Green': '#00FF00',
        'Blue': '#0000FF'
        }

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

@app.route("/")
def polynomial():
    #get arguments from flask URL
    args = flask.request.args

    #get form arguments from url, with defaults
    color = getitem(args, 'color', 'Black')
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    #make graph
    x = list(range(_from, to + 1))
    fig = figure(title = 'Polynomial')
    fig.line(x, [i ** 2 for i in x], color = colors[color], line_width = 2)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = flask.render_template(
            'embed.html',
            plot_script = script,
            plot_div = div,
            js_resources = js_resources,
            css_resources = css_resources,
            color = color,
            _from = _from,
            to = to
            )

    return encode_utf8(html)

#@app.route('/')
#def main():
#  return redirect('/index')

@app.route('/index')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  print(__doc__)
  app.run(port=33507)
