from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextId = 4
topics = [
    {"id": 1, "title": "Model", "body": "Model is ..."},
    {"id": 2, "title": "View", "body": "View is ..."},
    {"id": 3, "title": "routing", "body": "Routing is ..."}
]


def HTMLTemplate(articleTag ,id = None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action = "/delete/" method = "post">
                    <input type = "hidden" name = "id" value = {id}>
                    <input type = "submit" value = "delete">
                </form>
            </li>
            <li><a href = "/update/{id}/"> update</a></li>
        '''
    ol = ''

    for topic in topics:
        ol = ol + f'<li><a href = "/read/{topic["id"]}/">{topic["title"]}</a></li>'

    return f'''
    <html lang="en">
    <head>
    <body>
        <h1><a href = "/">Django</a></h1>
        <ol>    
            {ol}
        </ol>
        {articleTag}
        
        <ul>
            <li><a href = "/create/">create</a></li>
            {contextUI}
        </ul>
    
    </body>
    </html>
        '''


def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello Django!
    '''
    return HttpResponse(HTMLTemplate(article))


@csrf_exempt
def create(request):
    global nextId

    if request.method == 'GET':
        article = '''
        <form action = "/create/" method = "post">
            <p><input type = "text" name = "title" placeholder = "title"></p>
            <p><textarea name = "body" placeholder = "body"></textarea></p>
            <p><input type = "submit"></p>
        </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        print(request.POST)
        title = request.POST['title']
        body = request.POST['body']
        newTopics = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopics)
        url = '/read/' + str(nextId)
        nextId = nextId + 1
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics

    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')

def read(request, id):
    global topics
    article = ''

    for topic in topics:
        if topic['id'] == int(id):
            article =f'''
                <h2>{topic["title"]}</h2>
                <h3>{topic["body"]}</h3>
            '''

    return HttpResponse(HTMLTemplate(article, id))


@csrf_exempt
def update(request, id):
    global topics

    if request.method == "GET":
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title" : topic['title'],
                    "body" : topic['body']
                }

        article = f'''
                <form action = "/update/{id}/" method = "post">
                    <p><input type = "text" name = "title" placeholder = "title" value = {selectedTopic["title"]}></p>
                    <p><textarea name = "body" placeholder = "body">{selectedTopic["body"]} </textarea></p>
                    <p><input type = "submit" value = "수정"></p>
                </form>
                '''
        return HttpResponse(HTMLTemplate(article,id))

    elif request.method == "POST":
        print(request.POST)

        for updateTopics in topics:
            if updateTopics['id'] == int(id):
                updateTopics['title'] = request.POST['title']
                updateTopics['body'] = request.POST['body']

        return redirect(f'/read/{id}/')