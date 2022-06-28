import logging
from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse

from ..db.manager import DbManager


def add_static_handler(app: FastAPI):
    @app.get('')
    @app.get('/')
    def return_static_page(request: Request):
        request_domain = request.base_url.hostname

        logging.debug(f'got domain: {request_domain}, {request.base_url}')

        data = DbManager().get_domain(request_domain)

        return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    {data.fb_meta_tag}
    <title>Funnel end</title>
  </head>
  <body>
    <h1>
        Have a nice day!
    </h1>
    <p>
        Domain id = {data.id}
    </p>
  </body>
</html>""")