import flask
import apicode.apiquery as apiquery

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/search', methods=['POST'])
def course_lookup():
    data = flask.request.get_json()
    dept_short = data['dept_short']
    number  = int(data['number'])

    q = apiquery.Query()
    c = q.get_course_by_dept_and_number(dept_short, number)
    return flask.json.dumps({'dept_short' : c.dept_short, 'number' : c.number,
        'title' : c.title})

if __name__ == '__main__':
   app.run(debug = True)
