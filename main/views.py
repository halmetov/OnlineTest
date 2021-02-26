from django.shortcuts import render
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from main.models import Test,TestItem, Subject, Class, User, UserTestItem, UserTestItemVariant
import random
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
    tests = []
    left_time_min = 0
    left_time_sec = 0
    left_time = 0
    if current_user:
        current_user = User.objects.get(id=int(current_user))
        tests = Test.objects.filter(clas__id=current_user.clas.id)

        if active_test_id:
            active_test = UserTestItem.objects.get(id=int(active_test_id))
            left_time = active_test.stop_date - timezone.now()
            left_time = int(left_time.total_seconds())
            if left_time < 0:
                left_time = 0
            left_time_min = int(left_time/60)
            left_time_sec = int(left_time%60)
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
            new_user = User()
            new_user.last_name = request.POST.get('ln', '')
            new_user.first_name = request.POST.get('fn', '')
            clas_id = int(request.POST.get('class', 0))
            if clas_id:
                new_user.clas = Class.objects.get(id=int(clas_id))
                tests = Test.objects.filter(clas__id=int(clas_id))
            old_user = User.objects.filter(last_name=new_user.last_name).filter(first_name=new_user.first_name).filter(clas__id=int(clas_id))
            if old_user:
                new_user = old_user[0]
            else:
                new_user.save()
            request.session['user_id'] = new_user.id
            current_user = User.objects.get(id=int(new_user.id))



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
        'left_time': left_time,
        'left_time_min': left_time_min,
        'left_time_sec': left_time_sec
    })

def davayHandler(request):
    request.session['user_id'] = None
    request.session['active_test_id'] = None

    return render(request, 'davay.html')


def get_random_variants():
    vs = []
    while(len(vs)!=5):
        rn = random.randint(1,5)
        if rn not in vs:
            vs.append(rn)
    return vs

def insertHandler(request):
    success_variants_count = 0
    test_created = False
    if request.POST:
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        limit = int(request.POST.get('limit', 40))
        subject_id = int(request.POST.get('subject_id', 0))
        clas_id = int(request.POST.get('clas_id', 0))
        questions = request.POST.get('questions','')
        print('*****'*100)
        if title and subject_id and clas_id and questions:
            all_questions = questions.split('*')
            new_test = Test()
            new_test.title = title
            new_test.limit = limit
            new_test.description = description
            new_test.clas = Class.objects.get(id=int(clas_id))
            new_test.subject = Subject.objects.get(id=int(subject_id))
            new_test.start_time = timezone.now()
            new_test.stop_time = timezone.now() + timedelta(minutes=60*24*365)
            new_test.save()
            test_created = True

            for aq in all_questions:
                one_question = aq.strip()
                ques_and_variants = one_question.split('$')
                if len(ques_and_variants) > 5:
                    new_test_item = TestItem()
                    new_test_item.test = new_test
                    new_test_item.question = ques_and_variants[0].strip()
                    random_variants = get_random_variants()
                    new_test_item.correct_answer = random_variants.index(1) + 1
                    for i in range(5):
                        j = random_variants[i]
                        if i == 0:
                            new_test_item.answer_1 = ques_and_variants[j].strip()
                        elif i == 1:
                            new_test_item.answer_2 = ques_and_variants[j].strip()
                        elif i == 2:
                            new_test_item.answer_3 = ques_and_variants[j].strip()
                        elif i == 3:
                            new_test_item.answer_4 = ques_and_variants[j].strip()
                        elif i == 4:
                            new_test_item.answer_5 = ques_and_variants[j].strip()

                    new_test_item.save()
                    success_variants_count=success_variants_count+1
    else:
        pass
    subjects = Subject.objects.all()
    classes = Class.objects.all()
    return render(request, 'insert.html', {'subjects': subjects, 'classes': classes,'success_variants_count':success_variants_count, 'test_created':test_created})



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

    return render(request, 'results.html', {'tests': tests})


def analizeHandler(request, test_id):
    test_info = None
    test_id = test_id
    test_user_item_variants = []
    if not request.user.is_authenticated:
        tests = []
        current_user = request.session.get('user_id', None)
        if current_user:
            current_user = User.objects.get(id=int(current_user))
            if current_user:
                test_info = UserTestItem.objects.filter(user__id=int(current_user.id)).filter(id=test_id)
                if test_info:
                    test_info = test_info[0]
    else:
        test_info = UserTestItem.objects.get(id=test_id)

    if test_info:
        test_user_item_variants = UserTestItemVariant.objects.filter(user_test_item__id = test_id)


    return render(request, 'analize.html', {'test_user_item_variants':test_user_item_variants, 'test_info':test_info})