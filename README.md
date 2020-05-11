## Setup

1. Create a Python virtual environment.
   - Run `python -m venv .venv`
2. Activate the virtual environment.
   - Run `source .venv/bin/activate`
3. Install dependencies.
   - Run `pip install -r requirements.txt`

## Twisted Server

### Setup

Start the server by running:

`python twisted/server.py`

You'll need to restart the server every time you make a change. If that gets annoying, I recommend running it using `nodemon` (an npm package):

`nodemon --exec python twisted/server.py`

I recommend using [Postman](https://www.postman.com) to play around with the routes. But you can just use `curl` if you're feeling spicy.

### Usage

Routes:

- `GET localhost:8000`
- `GET localhost:8000/slow`
- `GET localhost:8000/widgets`
- `POST localhost:8000/widgets`

Stuff to do:

- Try hitting `GET localhost:8000`. You should see the "Welcome!" message.
- Try hitting `GET localhost:8000/widgets`. You should see the a list of "widget" objects.
- Try hitting `POST localhost:8000/widgets` with an object as the body. Hitting `GET localhost:8000/widgets` should show the same object.
- Try hitting `GET localhost:8000/slow`. It'll take 10 seconds to response, but you can still hit the other routes in the meantime. That's because the route is non-blocked.
