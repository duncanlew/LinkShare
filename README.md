# LinkShare
LinkShare is a simple Google Spaces clone written in Django. It is meant to be self-hosted.

## Requirements
Set up a server with Python3.6. Install the requirements with:
`pip3 install -r requirements.txt`
And set it up with your favourite web server.

Once you've set it up, run the following commands:
`python3 manage.py migrate`
`python3 manage.py createsuperuser`

Right now, you need to create users manually using that command. Expect this to change soon.

## Alpha
Currently, LinkShare is still in alpha phase. It is currently under active development since Google shut down Spaces, albeit it is a side project. I am also working on a React Native app for LinkShare, but I am still learning that framework so don't expect much.
