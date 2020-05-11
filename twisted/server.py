import json
import sys
import time

from twisted.internet import reactor, threads
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET, Site


log.startLogging(sys.stdout)


# In a production app, you'd want to persist this data in a DB. But storing in
# memory is good enough for this example.
widgets = [{"name": "foo"}]


class IndexHandler(Resource):
    def render_GET(self, request):
        # Responses always need to be in bytes. The `b` prefix will make this a
        # byte string, rather than unicode. Try removing the `b` prefix and see
        # what the response looks like.
        res = b"Welcome!"

        return res


class WidgetHandler(Resource):
    def render_GET(self, request):
        # Tells the client to expect JSON, rather than a string. Try commenting
        # this out and see what the response looks like.
        request.responseHeaders.addRawHeader(
            b"Content-Type", b"application/json")

        # Responses always need to be in bytes. So convert `widget` into a byte
        # string.
        res = json.dumps(widgets).encode("utf-8")

        return res

    def render_POST(self, request):
        # Request bodies (`request.content`) are a byte string. For this route,
        # we expect the body to be valid JSON, so we can use `json.loads` to
        # convert the byte string into a dict.
        data = json.loads(request.content.read())

        widgets.append(data)
        res = json.dumps(data).encode("utf-8")
        return res


def slowComputation():
    time.sleep(10)
    return "Done"


class SlowHandler(Resource):
    def success(self, result, request):
        request.write(result.encode("utf-8"))
        request.finish()

    def failure(self, err, request):
        request.write(str(err))
        request.finish()

    def render_GET(self, request):
        # Defer the `slowComputation` to a thread, which will prevent this
        # route from "blocking" other routes.
        d = threads.deferToThread(slowComputation)

        d.addCallback(self.success, request)
        d.addErrback(self.failure, request)

        return NOT_DONE_YET


root = Resource()

# Requests sent to localhost:8000/ will go to the `IndexHandler`.
root.putChild(b"", IndexHandler())

# Requests sent to localhost:8000/widgets will go to the `WidgetHandler`.
root.putChild(b"widgets", WidgetHandler())

# Requests sent to localhost:8000/slow will go to the `SlowHandler`.
root.putChild(b"slow", SlowHandler())

factory = Site(root)
reactor.listenTCP(8000, factory)
reactor.run()
