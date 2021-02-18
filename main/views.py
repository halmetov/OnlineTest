from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from main.models import Test,TestItem, Subject, Class, User, UserTestItem, UserTestItemVariant

# Create your views here.

def indexHandler (request):
    current_user = request.session.get('user_id', None)
    if request.session.get('endtest', 0):
        request.session['test_question_id'] = None
        request.session['active_test_id'] = None
        request.session['endtest'] = 0

    active_test_id = request.session.get('active_test_id', None)
    test_question_id = request.session.get('test_question_id',None)
    test_question = None
    choosen_variant_info = None
    endtest = None
    active_test_questions = []
    classs = []
    active_test = None
    if current_user:
        tests = Test.objects.all()
        current_user = User.objects.get(id=int(current_user))
        if active_test_id:
            active_test = UserTestItem.objects.get(id=int(active_test_id))
            active_test_questions = TestItem.objects.filter(test__id=int(active_test.test.id))

            if test_question_id:
                test_question_id = int(test_question_id)
                test_question = TestItem.objects.get(id=test_question_id)
            elif active_test_questions:
                test_question = active_test_questions[0]
                test_question_id = test_question.id
            if test_question_id:
                utvs = UserTestItemVariant.objects.filter(user_test_item__id=active_test.id).filter(test_item__id=test_question.id)
                if utvs:
                    choosen_variant_info = utvs[0]



        if request.POST:
            action = request.POST.get('action', '')
            if action == 'start_test':
                test_id = int(request.POST.get('test_id', 0))
                if test_id:
                    choosen_test = Test.objects.get(id=test_id)
                    new_user_test = UserTestItem()
                    new_user_test.start_date = timezone.now()
                    new_user_test.stop_date = timezone.now()+timedelta(minutes=choosen_test.limit)
                    new_user_test.test = choosen_test
                    new_user_test.user = current_user
                    new_user_test.save()
                    request.session['active_test_id'] = new_user_test.id
                    active_test = new_user_test

                return JsonResponse({'success': True, 'errorMsg': '', '_success': True})
            elif action == 'choose_question':
                test_question_id = int(request.POST.get('test_question_id', 0))
                request.session['test_question_id'] = test_question_id
                return JsonResponse({'success': True, 'errorMsg': '', '_success': True})
            elif action == 'choose_variant':
                utvs = UserTestItemVariant.objects.filter(user_test_item__id=active_test.id).filter(test_item__id=test_question.id)
                if utvs:
                    utv = utvs[0]
                else:
                    utv = UserTestItemVariant()
                    utv.user_test_item = active_test
                    utv.test_item = test_question
                    utv.correct_variant = test_question.correct_answer
                utv.ball = 0
                utv.user_variant = int(request.POST.get('variant', 0))
                if utv.user_variant == utv.correct_variant:
                    utv.ball = 1
                utv.save()
                return JsonResponse({'success': True, 'errorMsg': '', '_success': True})
            elif action == 'endtest':
                active_test_questions = UserTestItemVariant.objects.filter(user_test_item__id=active_test.id)
                s = 0
                for atq in active_test_questions:
                    if atq.user_variant == atq.correct_variant and atq.user_variant != 0:
                        s += 1
                active_test.count_question = len(active_test_questions)
                active_test.ball = s
                active_test.stop_date = timezone.now()
                active_test.save()
                request.session['endtest'] = 1
                return JsonResponse({'success': True, 'errorMsg': '', '_success': True})





    else:
        if request.POST:
            print('***' * 100)
            print(request.POST)
            new_user = User()
            new_user.last_name = request.POST.get('ln', '')
            new_user.first_name = request.POST.get('fn', '')
            clas_id = int(request.POST.get('class', 0))
            if clas_id:
                new_user.clas = Class.objects.get(id=int(clas_id))
            old_user = User.objects.filter(last_name=new_user.last_name).filter(first_name=new_user.first_name).filter(clas__id=int(clas_id))
            if old_user:
                new_user = old_user[0]
            else:
                new_user.save()
            request.session['user_id'] = new_user.id
            current_user = User.objects.get(id=int(new_user.id))

        tests = Test.objects.all()
        classs = Class.objects.all()

    return render(request, 'index.html', {
        'tests': tests,
        'classs': classs,
        'current_user': current_user,
        'active_test': active_test,
        'active_test_questions':active_test_questions,
        'test_question':test_question,
        'choosen_variant_info': choosen_variant_info,
        'endtest': endtest,
    })

def davayHandler(request):
    request.session['user_id'] = None
    request.session['active_test_id'] = None

    return render(request, 'davay.html')


def resultsHandler(request):
    if not request.user.is_authenticated:
        tests = []
        current_user = request.session.get('user_id', None)
        if current_user:
            current_user = User.objects.get(id=int(current_user))
            if current_user:
                tests = UserTestItem.objects.filter(user__id=int(current_user.id))
    else:
        tests = UserTestItem.objects.all()

    return render(request, 'results.html', {'tests':tests})