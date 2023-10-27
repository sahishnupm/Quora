from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from datetime import datetime

from users.models import Users
from home.models import Question, QuestionDetails, Likes

# Create your views here.



class Dashboard(View):
    def getQuestionDetails(self, question_id, user_id):
        question_details = []
        questionQuery = QuestionDetails.objects.filter(question_id = question_id)\
        .select_related("users")\
        .values("responds", "respondand_id__name", "responds_time", "id")

        for q in questionQuery:
            question_details.append({
                'question_detail_id' : q['id'],
                'responds' : q['responds'],
                'username' : q['respondand_id__name'],
                'responds_time' : q['responds_time'],
                'likes' : Likes.objects.filter(question_id = q['id']).count(),
                'like_status' : Likes.objects.filter(question_id = q['id'], liked_by = user_id).count() > 0
            })

        return question_details

    def get(self, request):
        user_id = request.session.get('user')
        print(user_id)
        if user_id:
            user_data = Users.objects.filter(id = user_id).values("name")[0]
            questionQuery = Question.objects\
            .select_related('users')\
            .order_by("-updated_by")\
            .values(
                "user_id__name", "name", "description", "updated_by", "user_id", 'id'
            )

            questions = []

            for q in questionQuery:
                questions.append({
                    'username'      : q['user_id__name'],
                    'question_name' : q['name'],
                    'description'   : q['description'],
                    'updated_by'    : q['updated_by'],
                    'user_id'       : q['user_id'],
                    'question_id'   : q['id'],
                    'replies'       : self.getQuestionDetails(q['id'], user_id)
                })

            # print(questions)
            
            context = {
                'username' : user_data['name'],
                'questions' : questions
            }
            return render(request, 'home/home.html', context=context)
        else:
            return redirect('/home')
        

class PostQuestion(View):
    def post(self, request):
        question = request.POST.get('question')
        description = request.POST.get('description')

        user_id = request.session.get('user')

        if not user_id:
            return JsonResponse({'status' : False, "msg" : 'login'})

        if(question):
            # print(Users.objects.get(id = user_id)) 
            ques = Question(
                name = question,
                description = description,
                user_id = Users.objects.get(id = user_id),
                updated_by = datetime.now()
            )

            ques.save()
            return JsonResponse({'status' : True})

        else:
            return JsonResponse({'status' : False}, status=500)
        

class AddReply(View):
    def post(self, request):
        reply = request.POST.get('reply')
        question_id = request.POST.get('question_id')

        user_id = request.session.get('user')

        print("user_id = " ,user_id)

        if not user_id:
            return JsonResponse({'status' : False, "msg" : 'login'})
        
        if reply and question_id:
            respond = QuestionDetails(
                question_id = Question.objects.get(id = question_id),
                responds = reply,
                respondand_id = Users.objects.get(id = user_id),
                responds_time = datetime.now() 
            )
            respond.save()
            return JsonResponse({'status' : True})
        else:
            return JsonResponse({'status' : False}, status=500)


class ToggleLike(View):
    def post(self, request):
        context = request.POST.get('context')
        question_id = request.POST.get('question_id')

        user_id = request.session.get('user')
        if not user_id:
            return JsonResponse({'status' : False, "msg" : 'login'})


        if question_id and context:
            if context == 'unlike':
                Likes.objects.filter(question_id = question_id, liked_by = user_id).delete()
            else:
                like = Likes(
                    question_id = QuestionDetails.objects.get(id = question_id),
                    liked_by = Users.objects.get(id = user_id)
                )
                like.save()
            
            return JsonResponse({'status' : True})

        else:
            return JsonResponse({'status' : False}, status=500)