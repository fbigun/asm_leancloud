@app.before_request
def before_request():
    g.user = leancloud.User.get_current()


@app.route('/')
def index():
    return redirect(url_for('todos.show'))


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/robots.txt')
@app.route('/favicon.svg')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])