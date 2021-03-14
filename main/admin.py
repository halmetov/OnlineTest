from django.contrib import admin
from main.models import *
# Register your models here.


class SubjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subject, SubjectAdmin)





class ClassAdmin(admin.ModelAdmin):
    pass

admin.site.register(Class, ClassAdmin)





class TestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Test, TestAdmin)




class TestItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(TestItem, TestItemAdmin)





class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)




class UserTestItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserTestItem, UserTestItemAdmin)




class UserTestItemVariantAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserTestItemVariant, UserTestItemVariantAdmin)





########################################################################

class SurveyCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SurveyCategory, SurveyCategoryAdmin)



########################################################################

class SurveyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Survey, SurveyAdmin)



########################################################################

class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question, QuestionAdmin)




########################################################################

class UserSurveyAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserSurvey, UserSurveyAdmin)



########################################################################

class UserSurveyItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserSurveyItem, UserSurveyItemAdmin)



########################################################################

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)




























