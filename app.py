import flask
import apicode.query as query

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/search', methods=['POST'])
def course_lookup():
    data = flask.request.get_json()

    q = query.Query()
    c = q.parse_search(data['search'])

    return flask.jsonify(c.as_json())

if __name__ == '__main__':
   app.run(debug = True)
