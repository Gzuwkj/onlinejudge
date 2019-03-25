from django.shortcuts import render
from .models import Problem
from Contest.models import MatchRegister, MatchList, MatchSubmit
from Contest.views import ratio
from django.http import HttpResponseRedirect


def problem_page(request, prob_id):    # 题目列表
    error = []
    if request.method == "GET":
        if str(prob_id) == '0':
            problems = Problem.objects.all()
            if len(problems) == 0:
                error.append("题库中没有题目数据，请先添加题目")
            return render(request, 'problemList.html', {'problems': problems, 'error': error})
        else:
            prob_no = str(prob_id)
            problem = Problem.objects.filter(no=prob_no)
            if len(problem) != 0:
                request.session['prob_no'] = prob_no
            else:
                error.append("未查找到您要查找的题目")
            contest_name = request.session.get('contest_name', '')
            prob_no = request.session.get('prob_no', '')
            code = MatchSubmit.objects.filter(userName=str(request.user), probID=prob_no,
                                               matchName=str(contest_name)).order_by('-runID')
            size = code.count()
            if size:
                code = code[0].content
            else:
                code = ''
        return render(request, 'problem.html', locals())
    else:
        prob_name = request.POST.get('probName', '')
        prob_author = request.POST.get('probSource', '')
        if prob_name != '':
            problems = Problem.objects.filter(probName=prob_name)
        if prob_author != '':
            problems = Problem.objects.filter(probSource=prob_author)
    if len(problems) == 0:
        error.append("未查找到您要查找的题目")
    return render(request, 'problemPage.html', locals())


def edit(request):
    username = request.user
    if str(username) == 'AnonymousUser':
        return HttpResponseRedirect("/login/?next=/contest/match/")
    prob_no = request.session.get('prob_no', '')
    contest_name = request.session.get('contest_name', '')
    if prob_no == '' or contest_name == '':
        return HttpResponseRedirect("/contest/match/")
    # error = []
    # is_register = MatchRegister.objects.filter(matchName=contest_name, username=username)
    # if len(is_register) == 0:
    #     error.append('对不起，您未注册该场比赛，无法参与作答！')
    #     problems = []
    #     match = MatchList.objects.filter(matchName=contest_name)
    #     for contest in match:  # 从比赛中获取题目列表
    #         nos = contest.matchInclude.split(',')
    #         for no in nos:
    #             prob = Problem.objects.filter(no=no)
    #             problems.append(prob)
    #         ratio_list = ratio(contest, nos)
    #     return render(request, 'contest.html', {'problems': problems, 'ratio_list': ratio_list, 'error': error})
    return render(request, 'codeEditor.html')


def all_status(request):
    return render(request, 'status.html')
