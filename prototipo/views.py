from django.shortcuts import render, redirect
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


def singIn(request):
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

            for model_list in database.child('iPhones').get().each():
                print(model_list.key())
                for load_list in database.child('iPhones').child(model_list.key()).child('product_id').get().each():
                    print(load_list.val())
                    if model in load_list.val():
                        print('achou')
                        for product_ids in database.child('iPhones').child(model_list.key()).get().each():
                            if model in product_ids.val():
                                for panics in database.child('iPhones').child(model_list.key()).child(
                                        'string').get().each():
                                    if panics.key() in panicString:
                                        panic_val = panics.val()
                                        panic_key = panics.key()
                                        return render(request, 'result.html',
                                                      {'panic': panic_val, 'model': model_list.key(),
                                                       'build': build,
                                                       'panic_key': panic_key})
                                else:
                                    panic_reader = 'Panic não cadastrado no banco de dados'
                                    return render(request, 'result.html',
                                                  {'panic': panic_reader, 'model': model_list.key()})
            else:
                error = 'Modelo não encontrado!'
                print('Parou')
                return render(request, 'error.html', {'error': error})

        finally:
            temp.close()
            load.close()
            print('End of Life')

    return render(request, 'singin.html')


def postsingin(request):
    # email = request.POST.get('email')
    # pwd = request.POST.get('pass')
    # user = authe.sign_in_with_email_and_password(email,pwd)

    return render(request, 'postsigin.html', )
