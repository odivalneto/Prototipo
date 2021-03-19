from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
import io
import pyrebase
import tempfile

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
storage = firebase.storage()


def del_line_bug(url):
    with open(url, "r") as x:
        lineNull = x.readlines()
        x.close()

    if 'bug_type' in lineNull[0]:
        del lineNull[0]
        new_file = open(url, 'w+')
        for line in lineNull:
            new_file.write(line)
        new_file.close()
        print('ok')
    else:
        print('error')


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

    panicString = ''
    build = ''
    model = ''
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

        finally:
            temp.close()
            load.close()
            print('End of Life')


    return render(request, 'singin.html', {'panic': panicString, 'model': model, 'build': build})


def postsingin(request):
    # email = request.POST.get('email')
    # pwd = request.POST.get('pass')
    # user = authe.sign_in_with_email_and_password(email,pwd)

    return render(request, 'postsigin.html', )
