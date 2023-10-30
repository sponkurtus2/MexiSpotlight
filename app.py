from flask import Flask, render_template

app = Flask(__name__)




class ApiClient:
    apiKey = '21D487D40AFD9B56F3F8369E11C599B4566067F18D8B19065DE6E9C89B0717D314D3485030D904674554E0D792C606DD'
    apiUri = 'https://api.elasticemail.com/v2'

    def Request(method, url, data):
        data['apiKey'] = ApiClient.apiKey
        if method == 'POST':
            result = requests.post(ApiClient.apiUri + url, data=data)
        elif method == 'PUT':
            result = requests.put(ApiClient.apiUri + url, data=data)
        elif method == 'GET':
            attach = ''
            for key in data:
                attach = attach + key + '=' + data[key] + '&'
            url = url + '?' + attach[:-1]
            result = requests.get(ApiClient.apiUri + url)

        jsonMy = result.json()

        if jsonMy['success'] is False:
            return jsonMy['error']

        return 'Correo enviado con exito :D'



def Send(request):
    body_html = request.form.get('bodyHtml') or request.form.get('bodyHtml')

    return ApiClient.Request('POST', '/email/send', {
        'subject': request.form.get('subject'),
        'from': 'mexispotlight@gmail.com',
        'fromName': 'Carlitos API',
        'to': request.form.get('to'),
        'bodyHtml': f'<h1>{body_html}</h1>',
        'bodyText': '',
        'isTransactional': False
    })


@app.route('/send-email', methods=['POST'])
def SendEmail():
    return Send(request)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
