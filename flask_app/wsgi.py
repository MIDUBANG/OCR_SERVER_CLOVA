from app import server
# do some production specific things to the app
# app.config['DEBUG'] = False

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)