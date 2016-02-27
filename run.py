__author__ = 'hzhigeng'

from rent_shop import create_app


if __name__ == '__main__':
    global app
    app = create_app()
    # app.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0')
    app.run()
