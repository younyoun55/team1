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
        url = request.POST.get('url')

        titles = []
        urls =[]
        
        while True:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            entries = soup.select('.archive-entries section h1.entry-title a')
        
            for entry in entries:
                titles.append(entry.text)
                urls.append(entry['href'])

            next_page = soup.select('.pager .pager-next a')
            if not next_page:
                break

        context = {
            'account_name': account_name,
            'titles': titles,
            'urls': urls,
        }
        request.session['blog_info'] = context
        return render(request, 'personality_diagnosis/result.html', context)
    else:
        return render(request, 'personality_diagnosis/index.html')

#get_infoでgetしたurlをすべてスクレイピングしてjsonファイルに格納する
def get_json(request):
    blog_info = request.session.get('blog_info')

    if blog_info:
        titles = blog_info.get('titles', [])
        urls = blog_info.get('urls', [])

        articles = []

        for url in urls:
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            article_text = soup.select_one('.article-body').text.strip()  
            articles.append({'title': titles[urls.index(url)], 'text': article_text})

        json_filename = 'blog_data.json'
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(articles, json_file, ensure_ascii=False, indent=4)

        return HttpResponse(f'JSONファイル "{json_filename}" が作成されました。')
    else:
        return HttpResponse('セッションにブログ情報が存在しません。')



