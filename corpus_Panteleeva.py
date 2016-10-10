import urllib.request
import re
import os

def download_page(page_site):
    try:
        page = urllib.request.urlopen(page_site)
        text = page.read().decode('UTF-8')
#        print(text)
    except:
        print('Error at', page_site)
        text = ''
    return text

def article(text):
    reg_art = '<!-- article-content -->(.+?)<!-- /article-content -->'
    art_list = re.findall(reg_art, text, flags = re.DOTALL)
    art_txt = ''.join(art_list)
    return art_txt

def author(text):
    reg_author = 'title="Посмотреть все записи автора (.+?)">'
    author_list = re.findall(reg_author, text, flags = re.DOTALL)
    author_txt = ''.join(author_list)
    if author_txt == '':
        author_txt = 'Noname'
    return author_txt   
    
def header(text):
    reg_header = '<title>(.+?) \| Газета &quot;Октябрь&quot;</title>'
    header_list = re.findall(reg_header, text, flags = re.DOTALL)
    header_txt = ''.join(header_list)
    header_txt = header_txt.replace('&#8212;', '-')
    header_txt = header_txt.replace('&#171;', '«')
    header_txt = header_txt.replace('&#187;', '»')
    header_txt = header_txt.replace('&#215;', '×')  
    print(header_txt)
    return header_txt

def created(text):
    reg_created = '<span class="entry-date" title="[0-9:]+">(.+?)</span>'
    created_list = re.findall(reg_created, text, flags = re.DOTALL)
    created_txt = ''.join(created_list)
    if created_txt == '':
        created_txt = 'Nodate'
    return created_txt

def topic(text):
    reg_topic = 'rel="category">(.+?)</a>'
    topic_list = re.findall(reg_topic, text, flags = re.DOTALL)
    topic_txt = ''.join(topic_list)
    if topic_txt == '':
        topic_txt = 'Notopic'
    return topic_txt

def source(text):
    reg_source = '<link rel="canonical" href="(.+?)" />'
    source_list = re.findall(reg_source, text, flags = re.DOTALL)
    source_txt = ''.join(source_list)
    return source_txt

def year(created_txt):
    reg_year = '[0-9]{2}.[0-9]{2}.([0-9]{4})'
    year_list = re.findall(reg_year, created_txt, flags = re.DOTALL)
    year_txt = ''.join(year_list)
    if year_txt == '':
        year_txt = 'Noyear'
    return year_txt

def month(created_txt):
    reg_month = '[0-9]{2}.([0-9]{2}).[0-9]{4}'
    month_list = re.findall(reg_month, created_txt, flags = re.DOTALL)
    month_txt = ''.join(month_list)
    if month_txt == '':
        month_txt = 'Nomonth'
    return month_txt

def cleaning(text):
    regTag = re.compile('<.*?>', re.DOTALL)
    regScript = re.compile('<script>.*?</script>', re.DOTALL)
    regComment = re.compile('<!--.*?-->', re.DOTALL)
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    return clean_t

def table(path, author_txt, header_txt, created_txt, topic_txt, source_txt, year_txt):
    f = open('D:\\corpus\\metadata.csv', 'a', encoding = 'UTF-8')
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная(если районная)\t%s\tназвание газеты\t\t%s\tгазета\tРоссия\tкакой-то регион\tru\n'
    file = f.write (row % (path, author_txt, header_txt, created_txt, topic_txt, source_txt, year_txt))
    f.close()

def makingdirs(year_txt, month_txt, author_txt, header_txt, created_txt, topic_txt, source_txt, article_txt, i):
    if not os.path.exists('D:\\corpus\\plain\\' + year_txt + '\\' + month_txt):
        os.makedirs('D:\\corpus\\plain\\' + year_txt + '\\' + month_txt)
    filew = open('D:\\corpus\\plain\\' + year_txt + '\\' + month_txt + '\\' + str(i) + '.txt', 'w', encoding = 'UTF-8')
    filew.write('@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n' % (author_txt, header_txt, created_txt, topic_txt, source_txt) + article_txt)
    filew.close()

def mystem1(year_txt, month_txt, path, pathstem1):
    if not os.path.exists('D:\\corpus\\mystem1\\' + year_txt + '\\' + month_txt):
        os.makedirs('D:\\corpus\\mystem1\\' + year_txt + '\\' + month_txt)
    os.system('D:\\mystem.exe -cdi ' + path  + ' ' + pathstem1)

def mystem2(year_txt, month_txt, path, pathstem2):
    if not os.path.exists('D:\\corpus\\mystem2\\' + year_txt + '\\' + month_txt):
        os.makedirs('D:\\corpus\\mystem2\\' + year_txt + '\\' + month_txt)
    os.system('D:\\mystem.exe -cdi --format xml ' + path  + ' ' + pathstem2)

def main():
    common_in_pages = 'http://oktyabrsel.ru/?p='
    for i in range(1,256):
        page_site = common_in_pages + str(i)
        html = download_page(page_site)
        if html != '':
            month_txt = month(created(html))
            year_txt = year(created(html))
            path = 'D:\\corpus\\plain\\' + year_txt + '\\' + month_txt + '\\' + str(i) + '.txt'
            article_txt = cleaning(article(html))
            author_txt = author(html)
            header_txt = header(html)
            created_txt = created(html)
            topic_txt = topic(html)
            source_txt = source(html)
            makingdirs(year_txt, month_txt, author_txt, header_txt, created_txt, topic_txt, source_txt, article_txt, i)
            table(path, author_txt, header_txt, created_txt, topic_txt, source_txt, year_txt)
            pathstem1 = 'D:\\corpus\\mystem1\\' + year_txt + '\\' + month_txt + '\\' + str(i) + '.xml'
            pathstem2 = 'D:\\corpus\\mystem2\\' + year_txt + '\\' + month_txt + '\\' + str(i) + '.txt'
            mystem1(year_txt, month_txt, path, pathstem1)
            mystem2(year_txt, month_txt, path, pathstem2)

if __name__ == "__main__":
    main()
