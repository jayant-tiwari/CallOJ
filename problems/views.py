from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import AllProblems,Question
import os, zipfile
import shutil
import time

from django.core.files.storage import FileSystemStorage
# Create your views here.

@login_required
def correctFormView(request):
    return render(request,'thanks.html')

@login_required
def dashboardView(request):
    return render(request,'dashboard.html')

@login_required
def problemsView(request):
    questions = Question.objects.all()
    all_questions = []
    for ques in questions:
        if ques.access == 1 or ques.creator == request.user.username:
            all_questions.append(ques)
    return render(request,'problems.html',{'all_problems':all_questions})

@login_required
def showProblemView(request,problem_id):
    problem_to_show = Question.objects.get(id=problem_id)
    return render(request,'problem.html',{'problem':problem_to_show})

@login_required
def submitProblemView(request,problem_id):
    usercode = request.POST['code']
    language = request.POST['language']
    print(usercode,language)
    return render(request,'thanks.html')

@login_required
def createProblemView(request):
    if request.method == 'POST':
        exists = 0
        length=10
        yml_file = request.FILES['uploadFiles']
        directory = request.POST['problemCode']
        parent_dir = os.path.expanduser('~/CallOJ/media')
        path = os.path.join(parent_dir,directory)
        #directory permissions in octal
        mode = 0o777
        # os.mkdir(path,mode)
        inputFileWrong = 0
        print('hello')
        # uploaded_file = request.FILES['hoji']
        # print(uploaded_file.name)
        print(request.FILES)
        # problemCode = request.POST['problemCode']

        #Check that problemCode should not match with any problemCode already in the database
        #if problem code matches return message and reload the page
        #else execute further
        for f in request.FILES.getlist('uploadFiles'):
            filename = f.name
            reqname = "init.yml"
            if filename == reqname:
                print()
                # fs = FileSystemStorage()
                # fs.save(f.name,f)
            else:
                print("not yml")
                #code to reload the page and print message goes here

        for f in request.FILES.getlist('uploadedFiles'):
            filename = f.name
            length = len(filename)
            if filename[length-1]!='t' or filename[length-2]!='x' or filename[length-3]!='t' or filename[length-4]!='.':
                inputFileWrong = 1
                break

        if inputFileWrong == 0:
            problem_code = request.POST['problemCode']
            problem_name = request.POST['problemName']
            problem_statement = request.POST['problemStatement']
            time_limit = request.POST['timeLimit']
            memory_limit = request.POST['memoryLimit']
            problemType = request.POST['problemType']
            # ioi = bool(request.POST.get('problemType')=='1')
            print(int(problemType))
            if int(problemType) == 1:
                marking = 1
            else:
                marking = 2
            visibility = request.POST['visibility']
            print(int(visibility))
            if int(visibility) == 1:
                access = 1
            else:
                access = 2
            creator = request.user.username
            all_questions = Question.objects.all()
            for ques in all_questions:
                if ques.problemCode == problem_code:
                    exists = 1
                    break
            if exists == 1:
                return render(request,'createproblem.html')
            newProblem = Question(problemCode=problem_code,problemName=problem_name,problemStatement=problem_statement,timeLimit=time_limit,memoryLimit=memory_limit,marking=marking,access=access,creator=creator,editorialist=creator)
            newProblem.save()
            all_files = request.FILES.getlist('uploadedFiles')
            length = len(request.FILES.getlist('uploadedFiles'))
            loop = 0
            index = 0
            os.mkdir(path,mode)
            fs = FileSystemStorage()
            fs.save(yml_file.name,yml_file)
            src=os.path.expanduser('~/CallOJ/media/init.yml')
            #dest=os.path.expanduser()
            shutil.move(src,path)
            while loop<length:
                    file_input = all_files[loop]
                    file_input.name = "tc" + str(index) + ".in"
                    fs = FileSystemStorage()
                    fs.save(file_input.name,file_input)
                    src=os.path.expanduser('~/CallOJ/media/'+file_input.name)
                    shutil.move(src,path)
                    
                    file_output = all_files[loop+1]
                    file_output.name = "tc" + str(index) + ".out"
                    fs = FileSystemStorage()
                    fs.save(file_output.name,file_output)
                    src=os.path.expanduser('~/CallOJ/media/'+file_output.name)
                    shutil.move(src,path)
                    loop=loop+2
                    index=index+1

            print((path+"/"+directory+".zip"))
            zf = zipfile.ZipFile((path+"/"+directory+".zip"), "w")
            notdelete = directory+".zip"
            for root,subdirs,files in os.walk("/home/jayant/CallOJ/media/"+directory):
                for filename in files:
                    if filename != "init.yml" and filename!=notdelete:
                        zf.write(os.path.join(root, filename), filename, zipfile.ZIP_DEFLATED)
            
            zf.close()
            loop=0
            index=0
            while loop<length:
                file_input = all_files[loop]
                # file_input.name = "tc" + str(index) + ".in"
                src=os.path.expanduser('~/CallOJ/media/'+directory+'/'+file_input.name)
                os.remove(src)
                file_output = all_files[loop+1]
                # file_output.name = "tc" + str(index) + ".out"
                src=os.path.expanduser(('~/CallOJ/media/'+directory+'/')+file_output.name)
                os.remove(src)
                loop=loop+2
                index=index+1

            
        else:
            print("Not valid input cases")
            #code to reload the page with error message input file wrong
        # ymlfile = request.FILES['inFile']
        # normalfile = request.FILES['ip0']
        # print(problemCode)
        # uploaded_files = request.FILES.getlist('file_field')
        # for file in uploaded_files:
        #     print('1')
        #     print(file.name)
        #     print(file.size)

    return render(request,'createproblem.html')

