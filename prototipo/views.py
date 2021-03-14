from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadhandler import TemporaryFileUploadHandler
import pyrebase
import json

config = {
    'apiKey': "AIzaSyBAkbN_DM06JcqaqHVai6PMXwVFZ5yDB80",
    'authDomain': "readpanic.firebaseapp.com",
    'databaseURL': "https://readpanic-default-rtdb.firebaseio.com",
    'projectId': "readpanic",
    'storageBucket': "readpanic.appspot.com",
    'messagingSenderId': "469310617028",
    'appId': "1:469310617028:web:20084545141944e7266091"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def read_Panic(modelid, panicString):
    error = ''
    panic_reader = ''
    model_id = ''
    iphone = database.child('iPhones').get()
    string = database.child('iPhones').child('iPhone X').child('string').get()

    for product_ids in database.child('iPhones').child('iPhone X').get().each():
        if modelid in product_ids.val():
            print(modelid)
            for panics in string.each():
                if panics.key() in panicString:
                    print(panics.key())
                    print(panics.val())
                    panic_reader = panics.val()
                    break
            else:
                panic_reader = 'Error Panic não encontrado'
            break
        else:
            error = 'Modelo não encontrado!'
            break
    return


def singIn(request):
    if request.method == 'POST' and request.FILES['document']:
        myfile = request.FILES['document']
        fs = FileSystemStorage('media/')
        fs.save(myfile.name, myfile)

        with open('media/' + myfile.name, 'r+') as f:
            panic = json.load(f)

            panicString = (panic['panicString'])
            model_id = (panic['product'])

            read_Panic(model_id, panicString)

        fs.delete(myfile.name)

        print(myfile.name)

    return render(request, 'singin.html', {})


def postsingin(request):
    # email = request.POST.get('email')
    # pwd = request.POST.get('pass')
    # user = authe.sign_in_with_email_and_password(email,pwd)

    return render(request, 'postsigin.html', )
