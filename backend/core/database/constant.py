import os

USER = os.environ['mongo_user']
PASSWORD = os.environ['mongo_password']
CONNECTION_URL = f'mongodb+srv://{USER}:{PASSWORD}@cluster0.dkda1.mongodb.net/FamilyTree?retryWrites=true&w=majority'