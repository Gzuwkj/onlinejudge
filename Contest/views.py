from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import MatchList, MatchRegister, MatchSubmit, MatchRank
from Issue.models import Problem
from functools import cmp_to_key
import json
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt

def register_status(contests, username):
    status_list = []
    for con in contests:
        flag = MatchRegister.objects.filter(matchName=con.matchName, username=username).count()
        print(con.matchName + ':   '+str(flag))
        if not flag:
            status_list.append(0)
        else:
            time1 = con.startTime.replace(tzinfo=None)     # 比赛开始时间
            time2 = datetime.datetime.now()       # 当前系统时间
            time3 = time1+datetime.timedelta(minutes=int(con.howLong))     # 比赛结束时间
            if time1 > time2:
                status_list.append(1)
            elif time2 < time3:
                status_list.append(2)
            elif time2 > time3:
                status_list.append(3)
    print(status_list)
    return status_list


def show_contest(request):  # 比赛列表
    username = request.user
    match_name = request.POST.get('matchName', '')  # 默认值为''
    cnt = []
    if match_name == '':
        contest = list(reversed(MatchList.objects.filter(attribute='公开')))
        status_list = register_status(contest, username)
    else:
        contest = list(reversed(MatchList.objects.filter(matchName=match_name, attribute='公开')))
        status_list = register_status(contest, username)
    for con in contest:
        num = MatchRegister.objects.filter(matchName=con.matchName).count()
        cnt.append(num)
    return render(request, 'contestList.html', {'contest': contest, 'cnt': cnt, 'status': json.dumps(status_list)})


def ratio(match, problems):  # 通过率
    ratio_list = []
    for prob in problems:
        nums = MatchSubmit.objects.filter(matchName=match, probID=prob).exclude(result='0')
        ac_nums = nums.filter(result='1')
        nums = len(nums)
        ac_nums = len(ac_nums)
        if ac_nums != 0:
            ratio_list.append('%.3f' % (ac_nums/nums))
        else:
            ratio_list.append('0.000')
    return ratio_list


def is_accepted(contest, user, probs):
    ac_list = []
    for prob in probs:
        cnt = len(MatchSubmit.objects.filter(matchName=contest, userName=user, probID=prob, result='1'))
        if cnt != 0:
            ac_list.append('yes')
        else:
            ac_list.append('')
    return ac_list


def show_problem(request, match_id):  # 比赛包含的题目
    problems = []
    match = MatchList.objects.filter(id=match_id)
    for contest in match:                   # 从比赛中获取题目列表
        request.session['contest_name'] = contest.matchName
        prob_nos = contest.matchInclude.split(',')
        for no in prob_nos:
            prob = Problem.objects.filter(no=no)
            problems.append(prob)
        ratio_list = ratio(contest, prob_nos)
        username = request.user
        if str(username) != 'AnonymousUser':
            ac_list = is_accepted(contest, username, prob_nos)

    statuses = status(request, 0)
    rankResult = rank(request)

    sorted_list = rankResult['sorted_list']
    nos = rankResult['nos']
    no_list = rankResult['no_list']
    print(nos)
    return render(request, 'contest.html', locals())


def match_register(request, cid):                                # 比赛注册
    user_name = request.user
    if str(user_name) == 'AnonymousUser':
        return HttpResponseRedirect("/login/?next=/contest/match/")
    else:
        match_name = MatchList.objects.get(id=cid)
        print(match_name)
        MatchRegister.objects.create(matchName=match_name, username=user_name)
        time1 = match_name.startTime.replace(tzinfo=None)  # 比赛开始时间
        time2 = datetime.datetime.now()  # 当前系统时间
        time3 = time1 + datetime.timedelta(minutes=int(match_name.howLong))  # 比赛结束时间
        if time1 > time2:
            JsonResponse('比赛未开始', safe=False)
        elif time2 < time3:
            JsonResponse('火热进行中', safe=False)
        elif time2 > time3:
            JsonResponse('比赛已结束')
    return render(request, 'contestList.html')


def change_status(status_list):  # 提交状态
    for item in status_list:
        if item.result == '0':
            item.result = 'Queueing'
        elif item.result == '1':
            item.result = 'Accepted'
        elif item.result == '2':
            item.result = 'Presentation Error'
        elif item.result == '3':
            item.result = 'Wrong Answer'
        elif item.result == '4':
            item.result = 'Time Limit Exceeded'
        elif item.result == '5':
            item.result = 'Memory Limit Exceeded'
        elif item.result == '6':
            item.result = 'Output Limit Exceeded'
        elif item.result == '7':
            item.result = 'Runtime Error'
        elif item.result == '8':
            item.result = 'Compilation Error'
        elif item.result == '9':
            item.result = 'Compile Output Limit'


# post: 0表示提交代码 1表示查询数据    get: 0表示查询自己的所有运行状态
@csrf_exempt
def status(request, prob_id):  # 提交状态
    if request.method == 'POST':
        if str(prob_id) == '1':
            run_id = request.POST.get('runID', '')   # 默认值为''
            if run_id != '':
                statuses = MatchSubmit.objects.filter(runID=run_id)
            else:
                prob_no = request.POST.get('proId', '')   # 默认值为''
                author = request.POST.get('userName', '')
                language = request.POST.get('language', 'All')
                status1 = request.POST.getlist('status', 'All')[0]
                if status1 == 'All':
                    statuses = MatchSubmit.objects.all()
                else:
                    statuses = MatchSubmit.objects.filter(result=status1)
                if prob_no != '':
                    statuses = statuses.filter(probID=prob_no)
                if author != '':
                    statuses = statuses.filter(userName=author)
                if language != 'All':
                    statuses = statuses.filter(language=language)
            statuses = list(reversed(statuses))
            change_status(statuses)
            return statuses
        else:                                                                       # 创建新的提交数据
            username = request.user
            if str(username) == 'AnonymousUser':
                return HttpResponseRedirect('/login/?next=/contest/match/')
            contest = request.session.get('contest_name', '')
            prob_no = request.session.get('prob_no', '')
            if contest == '' or prob_no == '':
                return HttpResponseRedirect('/contest/match/')
            language = request.POST.getlist('language')[0]
            content = request.POST.get('editor', '')
            print(content)
            if content != '':
                MatchSubmit.objects.create(
                    matchName=contest,
                    userName=username,
                    probID=prob_no,
                    content=content,
                    result="0",
                    language=language
                )
            result = MatchSubmit.objects.filter(matchName=contest,
                                                userName=username,
                                                probID=prob_no)
        #return HttpResponseRedirect('/problem/page/'+str(prob_id), json.dump(result))
        return render(request, 'login.html')
    else:
        if str(prob_id) == '0':
            username = request.user
            if str(username) == 'AnonymousUser':
                return HttpResponseRedirect("/login/?next=/contest/status/0/")
            contest = request.session.get('contest_name', '')
            if contest == '':
                return HttpResponseRedirect("/contest/match/")
            statuses = list(reversed(MatchSubmit.objects.filter(matchName=contest, userName=username)))
            change_status(statuses)
            return statuses
        else:
            username = str(request.user)
            contest = request.session.get('contest_name', '')
            if contest == '':
                return HttpResponseRedirect("/contest/match/")
            statuses = list(reversed(MatchSubmit.objects.filter(matchName=contest, userName=username, probID=str(prob_id))))
            change_status(statuses)
            return statuses


'''
    先通过比赛名称查找出注册比赛的用户和比赛包含的题目，然后根据题目去查找用户的A题个数，最后整合后排序
'''


def rank(request):  # 排名
    if request.method == 'POST':
        contest = request.session.get('contest_name', '')
        username = request.POST.get('keyword', '')
        if contest == '':
            return HttpResponseRedirect("/contest/match/")
        elif username == '':
            return HttpResponseRedirect("/contest/rank/")
        else:
            matchs = MatchList.objects.filter(matchName=contest)
            nos = None
            for contest in matchs:  # 从比赛中获取题目列表
                nos = contest.matchInclude.split(',')
            user_rank = MatchRank.objects.filter(matchName=contest, userName=username)
            return render(request, 'rank.html', {'rank_list': user_rank, 'nos': nos})
    else:
        cur_match = request.session.get('contest_name', '')
        if cur_match == '':
            return HttpResponseRedirect("/contest/match/")
        users = MatchRegister.objects.filter(matchName=cur_match)  # 从注册比赛的用户中查找用户
        # users = MatchSubmit.objects.all().values('userName').distinct()   # 从提交比赛代码的用户中查找用户
        matchs = MatchList.objects.filter(matchName=cur_match)
        nos = None
        for contest in matchs:  # 从比赛中获取题目列表
            nos = contest.matchInclude.split(',')
        rank_list = []
        for user in users:
            username = user.username
            info = dict(userName=user.username)
            score = 0
            wrong_time_count = 0
            l1 = []
            result_list = []
            for no in nos:
                is_ac = len(MatchSubmit.objects.filter(matchName=cur_match,
                                                       userName=username,
                                                       probID=no,
                                                       result='1'))
                if is_ac != 0:  # 如果当前编号的题目过了，A题个数加一，并且A题标记置为1防止提交多次通过的代码的情况
                    score += 1
                    is_ac = 1
                wrong_time = len(MatchSubmit.objects.filter(matchName=cur_match,
                                                            userName=username,
                                                            probID=no).exclude(result='1').exclude(
                    result='0'))
                if wrong_time != 0:
                    wrong_time_count += wrong_time
                l1.append((is_ac, wrong_time))
            result_list.append(l1)
            info['result_list'] = result_list
            info['sort_time'] = wrong_time_count
            info['score'] = score
            rank_list.append(info)
        sorted_list = sorted(rank_list, key=lambda e: (e.__getitem__('score'), e.__getitem__('sort_time')))
        no_list = range(1, len(sorted_list)+1)
        return {'sorted_list': sorted_list, 'nos': nos, 'no_list': no_list}


def check_code(request, run_id):
    code = MatchSubmit.objects.filter(runID=run_id)
    return render(request, 'check.html', {'code': code})
