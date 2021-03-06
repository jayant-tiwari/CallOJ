from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib import auth
from .models import UserPlaylist
from problems.models import PlaylistProblems
from problems.models import Question
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import shutil
import os
import pathlib
# Create your views here.
def profileView(request):
    # UserPlaylistEntry = UserPlaylist.objects.create(userId_id=request.user.id,playlistCategory="DP",problemCount=0)
    # UserPlaylistEntry.save()
    profilePhotoPath = "/media/submittedFiles/"+request.user.username+"/"+request.user.username+".jpg"
    playlistEntries = []
    allEntries = UserPlaylist.objects.all()
    for entry in allEntries:
        if entry.userId_id == request.user.id:
            playlistEntries.append(entry)
    return render(request,'profilepage.html',{'playlistEntries':playlistEntries,'profilePhotoPath':profilePhotoPath})

def updateProfileView(request):
    return render(request,'updateProfile.html')

def changesToProfileView(request):
    if request.method == 'POST':
        current_user=request.user
        username = request.POST["username"]
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        profilePhoto = request.FILES["profilePhoto"]
        extension = ""
        indexOfExtension = 0
        currIndex=0
        for character in str(profilePhoto.name):
            if character == '.':
                indexOfExtension =currIndex
            currIndex = currIndex + 1
        print("Index:",indexOfExtension)
        for index in range(indexOfExtension,len(profilePhoto.name)):
            extension = extension + profilePhoto.name[index] 
        print("Extension:",extension)
        profilePhoto.name = request.user.username + extension
        all_users = User.objects.all()
        credentials_exist = 0
        password_ok = 0
        if password1 != password2:
            messages.info(request,'Password did not match')
            return HttpResponseRedirect('/userprofile/updateProfile/')
        if request.user.username != username:
            for user in all_users:
                if user.username!=request.user.username and user.username == username:
                    messages.info(request,'Username already exist')
                    return HttpResponseRedirect('/userprofile/updateProfile/')
        password_length = len(password1)
        current_user.username = username
        current_user.first_name = firstName
        current_user.last_name = lastName
        parentDirPath = os.path.dirname(__file__).rsplit('/',1)[0]
        path = os.path.join(parentDirPath,'media/submittedFiles/'+ request.user.username)
        fileSystem = FileSystemStorage()
        fileSystem.save(profilePhoto.name, profilePhoto)
        src = os.path.join(parentDirPath,'media/'+request.user.username+ extension)
        if profilePhoto:
            file_to_rem = pathlib.Path(path+"/"+request.user.username+ extension)
            file_to_rem.unlink()
        shutil.move(src, path)
        if password_length!=0:
            print("Change Hogaya Bhyii")
            current_user.set_password(password1)
        current_user.save()
        if password_length!=0:
            auth.logout(request)
            messages.info(request,'Password successfully changed please login again')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/userprofile/')

def showUserProfileView(request,searchedUser):
    print("OHO",searchedUser)
    requestedUserInfo = User.objects.get(username=searchedUser)
    profilePhotoPath = "/media/submittedFiles/"+requestedUserInfo.username+"/"+requestedUserInfo.username+".jpg"
    print("Sahi hua ?",requestedUserInfo)
    return render(request,'profilepage.html',{'searchedUser':requestedUserInfo,'profilePhotoPath':profilePhotoPath})

def playlistCategoryProblemsView(request,playlistCategory):
    categoryEntry = UserPlaylist.objects.get(userId_id=request.user.id,playlistCategory=playlistCategory)
    problems = categoryEntry.problems.all()
    profilePhotoPath = "/media/submittedFiles/"+request.user.username+"/"+request.user.username+".jpg"
    return render(request,'profilepage.html',{'categoryProblems':problems,'category':playlistCategory,'profilePhotoPath':profilePhotoPath})

def addCategoryView(request):
    print('Rangdebasanti')
    categoryName = request.POST["category"]
    newEntry = UserPlaylist.objects.create(userId_id=request.user.id,playlistCategory=categoryName,problemCount=0)
    newEntry.save()
    url = reverse('initialProfile')
    return HttpResponseRedirect(url)

def addQuestionToPlaylistView(request,playlistCategory):
    problemlink = request.POST['problemLink']
    problemname = request.POST['problemName']
    contestname = request.POST['contestName']
    difficultylevel = request.POST['difficulty']
    difficulty = int(difficultylevel)
    newPlaylistProblemsEntry = PlaylistProblems.objects.create(problemOfUser_id=request.user.id,problemLink=problemlink,problemName=problemname,contestName=contestname,difficultyLevel=difficulty)
    newPlaylistProblemsEntry.save()
    categoryEntry = UserPlaylist.objects.get(userId_id=request.user.id,playlistCategory=playlistCategory)
    if categoryEntry:
        print('Chalo')
    categoryEntry.problemCount = (categoryEntry.problemCount + 1)
    categoryEntry.save()
    categoryEntry.problems.add(newPlaylistProblemsEntry)
    problems = categoryEntry.problems.all()
    print(problems)
    url = reverse('categoryQuestions',args=[playlistCategory])
    return HttpResponseRedirect(url)

def addCallOjProblemView(request,problemId):
    link = "http://127.0.0.1:8000/dashboard/problems/"+str(problemId)+"/"
    category = request.POST['categoryOfProblem']
    difficulty = int(request.POST['difficulty'])
    problem = Question.objects.get(id=problemId)
    name = problem.problemName
    contestName = "CallOJ"
    newPlaylistProblemsEntry = PlaylistProblems.objects.create(problemOfUser_id=request.user.id,problemLink=link,problemName=name,contestName=contestName,difficultyLevel=difficulty)
    newPlaylistProblemsEntry.save()
    categoryEntry = UserPlaylist.objects.get(userId_id=request.user.id,playlistCategory=category)
    categoryEntry.problemCount = (categoryEntry.problemCount + 1)
    categoryEntry.save()
    categoryEntry.problems.add(newPlaylistProblemsEntry)
    return HttpResponseRedirect('/dashboard/problems/')
# def categoryQuestionsView(request,category):
#     userPlaylistEntry = UserPlaylist.objects.get(userId_id=request.user.id,playlistCategory=category)
#     questions = userPlaylistEntry.problems.all()
#     return render(request,'profilepage.html',{'questionsInCategory':questions})
    







