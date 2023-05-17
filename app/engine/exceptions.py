import traceback
from flask import current_app, render_template
from werkzeug.exceptions import HTTPException
import datetime


def exception_handler(e):
    if isinstance(e, HTTPException) and e.code == 404:
        return render_template('errors/error.jinja', code=404, message=e), 404
    else:
        log_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f = open(f"{current_app.root_path}/{current_app.config['ERROR_LOG']}", "a")
        f.write(f"\n[{log_datetime}] " + str(e) + "\n")
        traceback.print_exc(file=f)
        f.close()
        return e
