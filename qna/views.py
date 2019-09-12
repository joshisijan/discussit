from django.shortcuts import render, get_object_or_404, redirect

from .models import Question, Category, Vote, Answer

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, logout, login

from django.http import HttpResponseRedirect

from django.db.models import Q

from django.core.paginator import Paginator


def home_view(request):
    questions = Question.objects.all().order_by('-pub_date')
    paginator = Paginator(questions,5)
    page = request.GET.get('page')
    question = paginator.get_page(page)
    new = Question.objects.all().order_by('-pub_date')[:5]
    categories = Category.objects.all()
    context = {
        'questions' : question,
        'categories' : categories,
        'new' : new,
        'home_active' : 'active',
    }
    return render(request,'home.html',context)

def about_view(request):
    new = Question.objects.all().order_by('-pub_date')[:5]
    context = {
        'about_active' : 'active',
        'new' : new,
    }
    return render(request,'about.html',context)

def category_view(request):
    new = Question.objects.all().order_by('-pub_date')[:5]
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'category_active' : 'active',
        'new' : new,
    }
    return render(request,'category.html',context)

def search_view(request):
    categories = Category.objects.all()
    prefilled_keyword = ""
    new = Question.objects.all().order_by('-pub_date')[:5]
    if request.method == "POST":
        searchword = request.POST['searchword']
        prefilled_keyword = searchword   
        result = Question.objects.filter(Q(title__contains = searchword) | Q(body__contains = searchword) | Q(category__name__contains = searchword))
        context = {
            'categories' : categories,
            'new' : new,
            'prefilled_keyword' : prefilled_keyword,
            'result': result,
        }
        return render(request,'search.html',context)
    else:
        return redirect('home_page')

def login_view(request):
    categories = Category.objects.all()
    new = Question.objects.all().order_by('-pub_date')[:5]
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        user_invalid = ""
        pass_invalid = ""
        login_error = ""
        filled_user = ""
        filled_pass = ""
        if request.method == 'POST':
            username = request.POST['username'].strip()
            password = request.POST['password'].strip()
            user = authenticate(request,username = username, password = password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                return redirect('addquestion_page')
            else:
                login_error = "Username or Password do not match"
                user_invalid = "is-invalid"
                pass_invalid = "is-invalid"
            filled_user = username
            filled_pass = password

        context = {
            'categories' : categories,
            'login_active' : 'active',
            'user_invalid' : user_invalid,
            'pass_invalid' : pass_invalid,
            'login_error' : login_error,
            'filled_user' : filled_user,
            'filled_pass' : filled_pass,
            'new' : new,
        }
        return render(request,'login.html',context)

def signup_view(request):
    categories = Category.objects.all()
    new = Question.objects.all().order_by('-pub_date')[:5]
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        
        user_invalid = ""
        pass_invalid = ""
        email_invalid = ""
        signup_error = ""
        p_fname = ""
        p_lname = ""
        p_user = ""
        p_email = ""
        p_pass = ""
        p_pass1 = ""
        if request.method == 'POST':
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password1 = request.POST['password1']
            p_fname = fname
            p_lname = lname
            p_email = email
            p_user = username
            p_pass = password
            p_pass1 = password1
            if fname == "" or lname == "" or email == "" or username == "" or password == "" or password1 == "":
                signup_error = "Fillout Empty Fields First"
            else:
                if User.objects.filter(username=username).exists():
                    signup_error = "Username Already Exists"
                    user_invalid = "is-invalid"
                else:
                    if User.objects.filter(email=email).exists():
                        signup_error = "Email Already Exists"
                        email_invalid = "is-invalid"
                    else:
                        if password == password1:
                            user = User.objects.create_user(username=username, password=password,email=email,
                                    first_name=fname,last_name=lname)
                            user.save()
                            user = authenticate(request,username = username, password = password)
                            login(request,user)
                            if 'next' in request.POST:
                                return redirect(request.POST['next'])
                            return redirect('home_page')
                        else:
                            signup_error = "Passwords Do not Match"
                            pass_invalid = "is-invalid"
        context = {
            'signup_active' : 'active',
            'new' : new,
            'user_invalid' : user_invalid,
            'pass_invalid' : pass_invalid,
            'email_invalid' : email_invalid,
            'signup_error' : signup_error,
            'p_fname' : p_fname,
            'p_lname' : p_lname,
            'p_user' : p_user,
            'p_email' : p_email,
            'p_pass' : p_pass,
            'p_pass1' : p_pass1,
            'categories' : categories,
        }
        return render(request,'signup.html',context)



def question_view(request,question_id):
    categories = Category.objects.all()
    new = Question.objects.all().order_by('-pub_date')[:5]
    question = get_object_or_404(Question, pk = question_id)
    context = {
        'categories' : categories,
        'question' : question,
        'new' : new,
    }
    return render(request,'question.html',context)

def addquestion_view(request):
    categories = Category.objects.all()
    new = Question.objects.all().order_by('-pub_date')[:5]
    pre_title = ""
    pre_body = ""
    pre_category = ""
    question_error = ""
    question_success = ""
    if request.user.is_authenticated:
        all_category = Category.objects.all()
        if request.method == 'POST':
            question_title = request.POST['question_title'].strip()
            question_body = request.POST['question_body'].strip()
            category = request.POST['question_category'].strip()
            question_category = Category.objects.get(name=category)
            pre_title = question_title
            pre_body = question_body
            pre_category = category
            if question_title == "" or question_body == "":
                question_error = "Fillout Question's body first"
            elif len(question_title) > 500:
                question_error = "Questions title should not be more than 500 chars"
            elif len(question_body) > 1000:
                question_error = "Questions body should not be more than 1000 chars"
            else:
                question = Question.objects.create(title=question_title,body=question_body,category=question_category,creator=request.user)
                question.save()
                pre_title = pre_body = pre_category = ""
                question_success = "Successfully Added Question"
        context = {
            'categories' : categories,
            'prefilled_title' : pre_title,
            'prefilled_body' : pre_body,
            'prefilled_category' : pre_category,
            'question_error' : question_error,
            'question_success' : question_success,
            'category' : all_category,
            'new' : new,
        }
        return render(request,'add_question.html',context)
    else:
        return redirect('login_page')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        if 'next' in request.GET:
            next_page = request.GET['next']
        return redirect(next_page)
    else:
        return redirect('home_page')


def profile_view(request,user_id):
    categories = Category.objects.all()
    new = Question.objects.all().order_by('-pub_date')[:5]
    context = {
        'categories' : categories,
        'new' : new,
    }
    return render(request,'profile.html',context)