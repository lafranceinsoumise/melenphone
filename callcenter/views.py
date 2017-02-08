from django.shortcuts import render
import requests

def agent_key(request):
    data = {"username":"DarckouneAgentTest", "password":"jambon75"}
    key = requests.post('https://api.callhub.io/v2/agent-key/', data=data)
    print "Agent Key", key.json()
    return render(request, 'callcenter/test.html', locals())

def agent_status(request):
    key = "Token d97812bc859466a7b9826c67e944c3ca96fd4aa6"
    url = "https://api.callhub.io/v2/agent-status/"
    headers = {"Authorization": key}
    r = requests.get(url, headers=headers)
    print r.text
    return render(request, 'callcenter/agent_status.html', locals())

def set_webhook(request):
    key = 'Token ' # API KEY
    url = "https://api.callhub.io/v1/webhooks/"
    headers = {"Authorization": key}
    data = {'event':'cc.notes', 'target':'http://requestb.in/1bas5go1'}
    r = requests.post(url, data=data, headers=headers)
    return render(request, 'callcenter/test.html', locals())

def get_webhook(request):
    key = 'Token ' #API KEY
    headers = {'Authorization': key}
    url = 'https://api.callhub.io/v1/webhooks/'
    r = requests.get(url, headers=headers)
    return render(request, 'callcenter/webhooks.html', locals())

def campaign_info(request):
    key = 'Token d97812bc859466a7b9826c67e944c3ca96fd4aa6'
    headers = {'Authorization': key}
    url = 'https://api.callhub.io/v2/campaign-info/?id=[5335]'
    r = requests.get(url, headers=headers)
    return render(request, 'callcenter/campaign_info.html', locals())

def is_trophy(request):
    campaign = "5338"
    key = 'Token d97812bc859466a7b9826c67e944c3ca96fd4aa6'
    headers = {'Authorization': key}
    url = 'https://api.callhub.io/v2/is-trophy/' + campaign + '/'
    r = requests.get(url, headers=headers)
    return render(request, 'callcenter/is_trophy.html', locals())
