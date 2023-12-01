from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import json
from django.http import HttpResponse
from django.http import HttpResponse
from django.urls import path
from django.template.loader import get_template

#ホーム
def index(request):
    return render(request, 'personality_diagnosis/index.html')

#urlとアカウント名に基づいてその人が作成したブログとurlを抽出
def get_info(request):
    if request.method == 'POST':
        account_name = request.POST.get('account_name')
        account_id = request.POST.get('account_id')
        url = request.POST.get('url')
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        titles = []
        urls = []      
        for title in soup.find_all('a',class_='recent-entries-title'):
            titles.append(title.text.strip())
           
        for a in soup.find_all('a', class_='recent-entries-title'):
            url = a.get('href')
            if url:
                urls.append(url)
        
        context = {
            'account_name': account_name,
            'account_id':account_id,
            'titles': titles,
            'urls': urls,
            }
        
        request.session['get_info'] = context   
        return render(request, 'personality_diagnosis/result.html', context)
    else:
        return render(request, 'personality_diagnosis/index.html')

#get_infoでgetしたurlをすべてスクレイピングしてjsonファイルに格納する
def get_json(request):
    if request.method == 'POST':
        blog_info = request.session.get('get_info')
        urls = blog_info.get('urls', [])
        account_id = blog_info.get('account_id')

        print(f"urls:{urls}")

        articles = []

        for url in urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            article_texts = ' '.join([p.text.strip() for p in soup.find_all(class_='hatenablog-entry')]) 
            articles.append(article_texts)

           
        
        filename = f'{account_id}.json'

        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(articles, json_file, ensure_ascii=False, indent=4)

        with open(filename, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
    else:
        return HttpResponse('jsonファイルのダウンロードに失敗しました。')
        
    

   




