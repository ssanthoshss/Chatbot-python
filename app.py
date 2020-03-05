from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from markupsafe import escape
import Execute

app = Flask(__name__, template_folder= 'Templates')
context_set = ""

@app.route('/', methods = ['POST', 'GET'])
def index():
  if request.method == 'GET':
    global context_set
    val = request.args.get('text')
    val = str(val)
    
    if len(context_set) == 0:
      out_val, context_set = (Execute.chat(val))
    else:
      out_val = getattr(Execute, context_set)(val)
      context_set = ""
      return render_template('index.html', val=out_val)

    if out_val != None:
      return render_template('index.html', val=out_val)
    
    

if __name__ == '__main__':
  app.run(debug=True)
