from flask import Flask
from stand.backend.app.urls import urls

app = Flask('app')
app.register_blueprint(urls)
