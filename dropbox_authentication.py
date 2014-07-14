# Include the Dropbox SDK
import dropbox
from string import Template

# Get your app key and secret from the Dropbox developer website
app_key = 'app key here'
app_secret = 'app secret here'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()

# Have the user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)

t = Template(""" 
# Dropbox keys
D_APP_KEY = '${appkey}'
D_APP_SECRET = '${appsecret}'
D_ACCESS_TOKEN = '${accesstoken}'
""")
with open('access_tokens.py', 'a') as f:
    f.write(t.substitute(appkey=app_key,
                         appsecret=app_secret,
                         accesstoken=access_token))

print 'Success!  Access token saved to access_tokens.py.'
