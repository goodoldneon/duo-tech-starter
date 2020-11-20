import json
import sys

import twisted.python.log
from twisted.internet import defer, reactor

from cyclone.web import Application, RequestHandler

twisted.python.log.startLogging(sys.stdout)


def main():
    app = Application(
        [
            (r"/slow", SlowHandler),
            (r"/widgets", WidgetsHandler),
            (r"/widgets/([0-9].*)", WidgetHandler),
        ]
    )

    reactor.listenTCP(8000, app)
    reactor.run()


widgets = [{"id": 1, "name": "foo"}]


class WidgetHandler(RequestHandler):
    def get(self, widget_id: str) -> None:
        """
        Path parameters become arguments.
        """

        matched_widget = None

        for widget in widgets:
            if widget["id"] == int(widget_id):
                matched_widget = widget

        if matched_widget:
            self.add_header("Content-Type", "application/json")
            self.write(json.dumps(widget))
            self.finish()
        else:
            self.set_status(404)
            self.finish()


class WidgetsHandler(RequestHandler):
    def get(self):
        self.add_header("Content-Type", "application/json")
        self.write(json.dumps(widgets))
        self.finish()

    def post(self):
        widget = json.loads(self.request.body)
        widget["id"] = len(widgets) + 1
        widgets.append(widget)
        self.finish()


def slowComputation():
    d = defer.Deferred()
    seconds = 10
    reactor.callLater(seconds, d.callback, "Done")
    return d


class SlowHandler(RequestHandler):
    @defer.inlineCallbacks
    def get(self):
        """
        The `@defer.inlineCallbacks` decorator makes this method asynchronous. While
        this method is executing, the server can still handle other requests. This is
        called "non-blocked", since IO it doesn't block IO.

        Decorating a method with `@defer.inlineCallbacks` is similar to making it
        `async`, if you were using the `asyncio` library.
        """

        """
        The `yield` keyword will make the method's execution pause until the called
        function finishes.

        This is similar to the `await` keyword, if you were using the `asyncio` library.
        """
        val = yield slowComputation()

        self.write(val)
        self.finish()


if __name__ == "__main__":
    main()
