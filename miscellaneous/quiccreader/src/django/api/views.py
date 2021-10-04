from django.shortcuts import render
import os

def fetch(request):
    SANDBOX_FOLDER = os.getenv("SANDBOX_FOLDER", "~/Projects/WebCtf")
    ret = ''
    if(request.method == 'POST'):
        print(f"IN: {request.POST['filename']}")
        if(not request.POST['filename']):
            return render(request, 'index.html', {'ret': 'You have to specify a filename!'})
        try:
            ret = os.popen(f'cd {SANDBOX_FOLDER}; {SANDBOX_FOLDER}/admin_reader ' + request.POST['filename']).read().encode().decode()
        except:
            ret = 'An error has occurred.'
    return render(request, 'index.html', {'ret': ret})
