from flask import render_template

def error_handlers(app):
    """ @app.errorhandler(404)
    def invalid_route(e):
        return render_template("error.html", error_message="The source you are looking forward does not exist. Please return to the homepage."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("error.html", error_message="Internal Server Error"), 500

    @app.errorhandler(Exception)
    def handle_all_errors(e):
        return render_template('error.html', error_message='An unexpected error occurred'), 500 """
