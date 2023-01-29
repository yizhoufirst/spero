import tweepy
from flask import Flask

# create a flask app
app = Flask(__name__)

consumer_key = ''
consumer_secret = ''
callback = 'http://http://192.168.43.211:5000/callback'


@app.route('/twitter/login/')
def login():
    # 获取授权跳转地址redirect_url
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        redirect_url = auth.get_authorization_url()
        print("redirect_url: " + redirect_url)
        if redirect_url:
            return render_template('Twitter_login.html', redirect_url=redirect_url)
    except Exception as e:
        print('Error! Failed to get request token: ' + str(e))
        return ''



@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    print("redirect_url(method 2): " + url)
    session['request_token'] = auth.request_token
    return redirect(url)
	
@app.route('/app')
def request_twitter():
    token, token_secret = session['token']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    return api.me()

@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)

    return redirect('/app')	
    
    
@app.route("/")
def index():
    return "Hello world !"


if __name__ == '__main__':
    # run server
    app.run(host="0.0.0.0", port=5000)