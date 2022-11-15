import heroku3
heroku_conn = heroku3.from_key('HEROKU_API_KEY')
app = heroku_conn.apps()['APP_NAME']

print(app.get_log(dyno='worker.1', lines=20, source='app'))