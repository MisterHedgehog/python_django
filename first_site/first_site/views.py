from django.http import HttpResponse

def index(request):
    return HttpResponse(
        """
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-iwidth, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>LolKek</title>
        </head>
        <body style="background:#A5CC3E">
        <h3>Main page Hello, Olezha<h3>
        </body>
        </html>
        """
        )