# Include Twython
import twython
from string import Template

# Get your app key and secret from the Twitter developer website
app_key = 'app key here'
app_secret = 'app secret here'

twitter = twython.Twython(app_key, app_secret)
auth = twitter.get_authentication_tokens()

# Have the user sign in and authorize this token
print '1. Go to: ' + auth['auth_url']
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization PIN code.'
code = raw_input("Enter the authorization code here: ").strip()

# This will fail if the user enters an invalid authorization code
twitter = Twython(app_key, app_secret,
                  auth['oauth_token'], auth['oauth_token_secret'])
final_step = twitter.get_authorized_tokens(code)

t = Template(""" 
# Twitter keys
T_APP_KEY = '${appkey}'
T_APP_SECRET = '${appsecret}'
T_OAUTH_TOKEN = '${oauthtoken}'
T_OAUTH_TOKEN_SECRET = '${oauthtokensecret}'
""")
with open('access_tokens.py', 'a') as f:
    f.write(t.substitute(appkey=app_key,
                         appsecret=app_secret,
                         oauthtoken=final_step['oauth_token'],
                         oauthtokensecret=final_step['oauth_token_secret']))

print 'Success!  OAuth tokens saved to access_tokens.py.'
