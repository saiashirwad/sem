from socialnetwork import app
import os 

app.secret_key = os.urandom(24)
port = int(os.environ.get('PORT', 5000))
app.run('0.0.0.0', port)
