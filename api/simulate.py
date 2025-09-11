from varsha.app import app  # import your Flask app

# Vercel requires a handler function
def handler(request, response):
    return app(request.environ, response.start_response)
