import flickr_api
from string import Template

# Get your app key and secret from the Flickr developer website
app_key = 'app key here'
app_secret = 'app secret here'

flickr_api.set_keys(api_key=app_key, api_secret=app_secret)
auth = flickr_api.auth.AuthHandler()

# Have the user sign in and authorize this token
print '1. Go to: ' + auth.get_authorization_url("write")
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the oauth_verifier tag.'
code = raw_input("Enter the authorization code here: ").strip()

auth.set_verifier(code)
flickr_api.set_auth_handler(auth)

auth.save("flickr_access_token.txt")

print 'Success!  OAuth tokens saved to flickr_access_token.txt.'
