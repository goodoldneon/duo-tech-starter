## Setup

1. Create a Python virtual environment.
   - Run `python -m venv .venv`
2. Activate the virtual environment.
   - Run `source .venv/bin/activate`
3. Install dependencies.
   - Run `pip install -r requirements.txt`

## Cyclone Server

### Background

Our backend uses Twisted and Cyclone.

Twisted is used for networking and asynchronicity. We make heavy use of its deferreds to create asynchronous, non-blocking servers. We originally used deferreds because they allowed us to write asynchronous code before the `asyncio` module existed. Eventually, we want to migrate from `twisted.internet.defer.inlineCallbacks` generators to `async`/`await` coroutines, and also start using the standard library's event loop.

Cyclone is a web framework that implements the Tornado API. We originally picked Cyclone because it let us use Twisted's event loop, but Tornado had its own. Eventually we want to migrate from Cyclone to Tornado, since Tornado can now use the standard library's event loop.

### Setup

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the server by running:

```bash
python cyclone/server.py
```

You'll need to restart the server every time you make a change. If that gets annoying, I recommend running it using `nodemon` (an npm package):

```bash
nodemon --exec python cyclone/server.py
```

I recommend using [Postman](https://www.postman.com) to play around with the routes. But you can just use `curl` if you're feeling spicy.

### Usage

Routes:

- `GET localhost:8000`
- `GET localhost:8000/slow`
- `GET localhost:8000/widgets`
- `POST localhost:8000/widgets`

Stuff to do:

- Hit `GET localhost:8000`. You should see the "Welcome!" message.
- Hit `GET localhost:8000/widgets`. You should see the a list of "widget" objects.
- Hit `POST localhost:8000/widgets` with an object as the body. Hitting `GET localhost:8000/widgets` should show the same object.
- Hit `GET localhost:8000/slow`. It'll take 10 seconds to response, but you can still hit the other routes in the meantime. That's because the route is non-blocked.
- Look at the comments in `cyclone/server.py` for more stuff to do.

## Testing

We use the `mock` library frequently in our unit tests.

### Setup

Activate the virtual environment:

```bash
source .venv/bin/activate
```

### Usage

Run tests:

```bash
pytest testing
```
