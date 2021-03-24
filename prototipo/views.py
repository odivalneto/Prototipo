from django.shortcuts import render, redirect
import pyrebase
import tempfile
import json

config = {
    'apiKey': "AIzaSyCq-qTw7NU13Y1TmaLvSc7ri7Gs9GKvOm8",
    'authDomain': "prototipopanic.firebaseapp.com",
    'databaseURL': "https://prototipopanic-default-rtdb.firebaseio.com/",
    'projectId': "prototipopanic",
    'storageBucket': "prototipopanic.appspot.com",
    'messagingSenderId': "591884154403",
    'appId': "1:591884154403:web:34f2daffbd9b37f27da396"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


def login(request):

    return render(request, 'login.html')

def singIn(request):
    usr = request.POST.get('email')
    pwd = request.POST.get('password')

    a = authe.sign_in_with_email_and_password(usr, pwd)

    print(a['idToken'])

    try:
        myFile = database.child('iPhones').get().val()

        if request.method == 'POST' and request.FILES['document']:
            myfile = request.FILES['document'].read().decode('utf-8')
            temp = tempfile.TemporaryFile(mode='w+t')
            load = tempfile.TemporaryFile(mode='w+t')
            try:
                temp.write(myfile)
                temp.seek(0)
                out = temp.readlines()

                if 'bug_type' in out[0]:
                    del out[0]
                    for line in out:
                        load.write(line)
                else:
                    print('error')

                load.seek(0)
                panic = json.load(load)

                panicString = panic['panicString']
                build = panic['build']
                model = panic['product']

                for models in myFile:
                    if model in myFile[models]['product_id']:
                        for panicsRead in myFile[models]['string']:
                            if panicsRead in panicString:
                                panicLoad = myFile[models]['string'][panicsRead]
                                return render(request, 'result.html',
                                              {'model': models, 'panic_key': panicsRead, 'panic': panicLoad,
                                               'build': build}, a['idToken'])
                        else:
                            error = "Panic não cadastrado no banco de dados"
                            return render(request, 'error.html', {'error': error})
                else:
                    error = "Modelo não encontrado"
                    return render(request, 'error.html', {'error': error})
            finally:
                temp.close()
                load.close()
    except KeyError:
        pass
        # return redirect('index')

    return render(request, 'singin.html')


def postsingin(request):
    # email = request.POST.get('email')
    # pwd = request.POST.get('pass')
    # user = authe.sign_in_with_email_and_password(email,pwd)

    return render(request, 'postsigin.html', )


def new_panic(request):

    list_iphones = []

    try:

        list = database.child('iPhones').get()

        for i in list.each():
            list_iphones.append(i.key())

        if request.method == 'POST':
            select = request.POST.get('select')
            panic = request.POST.get('panic')
            solution = request.POST.get('solution')

            data = {
                panic: solution
            }
    except KeyError:
        pass
        print('not logged')


    return render(request, 'newpanic.html', {'list': list_iphones})


def create_new_model(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        product1 = request.POST.get('product1')
        product2 = request.POST.get('product2')
        if not product2:
            data2 = {0: 'iPhone' + product1}
        else:
            data2 = {0: 'iPhone' + product1, 1: 'iPhone' + product2}

        database.child('iPhones').child(model).child('product_id').set(data2)

    return redirect('/newpanic/')
