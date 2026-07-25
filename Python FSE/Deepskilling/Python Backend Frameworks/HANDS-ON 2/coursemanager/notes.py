"""
HANDS-ON 1 - Task 1: Request-Response Cycle notes
Digital Nurture 5.0 | Python Backend Frameworks

1) JOURNEY OF A GET /api/courses/ REQUEST THROUGH DJANGO
--------------------------------------------------------
Browser
   -> HTTP request hits the WSGI/ASGI server (e.g. gunicorn/uvicorn)
   -> Django's URL Router (urls.py / ROOT_URLCONF) matches the path
      "/api/courses/" against urlpatterns and resolves it to a View
   -> Middleware stack processes the request on the way in (top to
      bottom), e.g. SecurityMiddleware, SessionMiddleware, CsrfViewMiddleware
   -> The View function/class runs the business logic. It talks to the
      Model layer to query the database (e.g. Course.objects.all())
   -> The Model executes an ORM query -> translated into SQL -> DB returns rows
   -> The View builds a Response (HttpResponse / JsonResponse / DRF Response)
   -> Middleware processes the response on the way out (bottom to top)
   -> Response is sent back to the browser

2) MIDDLEWARE
-------------
Middleware sits BETWEEN the web server and the View - every request
passes through each middleware class (in order) before reaching the
view, and every response passes back through them (in reverse order)
before leaving Django.

Two built-in Django middleware classes:
- SecurityMiddleware: adds security-related HTTP headers (HSTS,
  X-Content-Type-Options, SSL redirect enforcement, etc.)
- AuthenticationMiddleware: attaches the `request.user` object to every
  incoming request based on the session, so views can check who is logged in.

3) WSGI vs ASGI
----------------
- WSGI (Web Server Gateway Interface): a SYNCHRONOUS interface between
  Python web apps and web servers. One thread/process handles one
  request at a time until it finishes.
- ASGI (Asynchronous Server Gateway Interface): an ASYNCHRONOUS
  successor to WSGI. Supports async/await views, WebSockets, and long
  lived connections, allowing many requests to be handled concurrently
  on a single thread via an event loop.
- Django uses WSGI BY DEFAULT (wsgi.py is generated with every project).
- Switch to ASGI when you need: async views, WebSocket support (e.g.
  Django Channels), Server-Sent Events, or high-concurrency I/O-bound
  workloads where blocking on WSGI would waste resources.

4) MVC -> MVT MAPPING
----------------------
Classic MVC (Model-View-Controller):
- Model: manages data and business rules
- View: presentation / what the user sees
- Controller: handles input, talks to the Model, chooses a View

Django's MVT (Model-View-Template):
- Model      -> Model      (identical role: data + DB schema via the ORM)
- Template   -> View (MVC) (Django's Template is what renders the HTML/
                             output the user sees - this is MVC's "View")
- View       -> Controller (MVC) (Django's View function/class receives
                             the request, applies logic, talks to the
                             Model, and picks a Template/Response - this
                             is MVC's "Controller")

In short: Django's "View" does the job of a Controller, and Django's
"Template" does the job of MVC's "View".
"""
