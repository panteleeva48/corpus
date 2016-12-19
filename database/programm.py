import re,os

def file(name):
    f = open(name, 'r', encoding = 'utf-8')
    fr = f.read()
    f.close()
    return fr

def writefile(namefile,result):
    file = open(namefile, "w", encoding = "utf-8")
    file.write(result)
    file.close()

def listing():
    fr = file('text.txt')
#    print(fr)
    fr = re.sub(r'—',r'-',fr)
    fr = re.sub(r'\n- ([а-яА-ЯЁёa-zA-Z])',r'\n-\1',fr)
    fr = re.sub(r'([а-яА-ЯЁёa-zA-Z]) - ([а-яА-ЯЁёa-zA-Z])',r'\1- -\2',fr)
    fr = re.sub(r'([\W]) - ([а-яА-ЯЁёa-zA-Z])',r'\1- -\2',fr)
    fr = re.sub(r'\)([\W])',r'\) \1',fr)
    list_words = fr.split()
#    print(list_words)
    return list_words

def list_punct():
    list_words = listing()
    new_list = []
    for word in list_words:
        word_l = re.sub(r'^(\W)', r' \1 ', word)# отделяет знаки препинания пробелом от слова в начале
        word_l = re.sub(r'([\W]+)$', r' \1 ', word_l)# отделяет знаки препинания пробелом от слова в конце
        new_list.append(word_l)
    list_list = []
    for el in new_list:
        el = el.split()
        list_list.append(el)
#    print(new_list)
#    print(list_list)
    return list_list

def createbase():
    list_list = list_punct()
#    print(list_list)
    string = ''
    num_text = 1
    for el in list_list:
        if len(el) == 1:# если только слово
            form = el[0]
            punct_left = ''
            punct_right = ''
#            print(punct_left + '&' + form + '&' + punct_right)
        elif len(el) == 2:
            sign = re.findall(r'[а-яА-ЯЁёa-zA-Z0-9]+',el[0])
#            print(sign)
            if len(sign) == 1:# если сначала слово, потом - знак препинания
                form = el[0]
                punct_left = ''
                punct_right = el[1]
#                print(punct_left + '&' + form + '&' + punct_right)
            else:# если сначала знак препинания, потом - слово
                form = el[1]
                punct_left = el[0]
                punct_right = ''
#                print(punct_left + '&' + form + '&' + punct_right)
        elif len(el) == 3:# если сначала знак препинания, потом - слово, потом - знак препинания
            form = el[1]
            punct_left = el[0]
            punct_right = el[2]
#        print(punct_left + '&' + form + '&' + punct_right)
        string = string + 'insert into base(form,punct_left,punct_right,num_text,id_analyse)\
 values ("%s","%s","%s","%s","0");' %(form,punct_left,punct_right,num_text)
        num_text += 1
    writefile('base.txt',string)
    return string

def analyse():
    list_words = listing()
#    print(list_words)
    str_form = ''
    for word in list_words:
        word = word.lower()
        word = word.strip(" .,()[];:?!«»{}-")
        str_form = str_form + word + '\n'
#    print(str_form)
    writefile('forms.txt',str_form)

def mystem():
    os.system("D:\\mystem.exe -cd D:\\proga\\database\\forms.txt form_lemma.txt")

def list_lemms():
    fr = file('form_lemma.txt')
    fr = re.sub(r'\?\?',r'',fr)
    fr = re.sub(r'\?',r'',fr)
    fr = fr.split('\n')
    str_j = ''
    for j in fr:
        if '{' not in j:
            j = '%s{%s}' %(j,j)
        str_j = str_j + '\n' + j
    writefile('form_lemma.txt',str_j)
    find = file('form_lemma.txt')
    whole_phrase = re.findall("[a-zA-Zа-яё0-9-]+{[a-zа-яё0-9|-]+}", find, flags=re.DOTALL)
    whole_phrase = list(set(whole_phrase))
#    print(whole_phrase)
    form_lemma_list = []
    for el in whole_phrase:
        form = re.findall("([а-яёa-zA-Z0-9-]+){[а-яёa-z0-9|-]+}", el, flags=re.DOTALL)
        lemma = re.findall("[а-яёa-zA-Z0-9-]+{([а-яёa-z0-9|-]+)}", el, flags=re.DOTALL)
        form_lemma_list.append(form + lemma)
    return form_lemma_list

def createanalyse():
    form_lemma_list = list_lemms()
    string = ''
    k = 1
#    print(form_lemma_list)
    for el in form_lemma_list:
        form = el[0]
        lemma = el[1]
        string = string + 'insert into analyse(id,form,lemma) values ("%s","%s","%s");' %(str(k),form,lemma)
        k += 1
    writefile('analyse.txt',string)
    return string

def mass(mas):
    l = []
    for x in mas:
        x = x.strip("()")
        x = x.strip('""')
        x = x.split('","')
        l.append(x)
    return l

def alltables():
    one = createbase()
    two = createanalyse()
#    print(one)
    first = re.findall('\(".+?\)', one, flags=re.DOTALL)
    second = re.findall('\(".+?\)', two, flags=re.DOTALL)
    base = mass(first)
    analyse = mass(second)
#    print(base)
#    print(analyse)
    for x in base:
        word = x[0].lower()
        i = 1
        for y in analyse:
            if word == y[1]:
                x = x.append(i)
            i += 1
    str_base = ''
    for el in base:
        if len(el) == 6:
            str_base = str_base + "insert into base(form,punct_left,punct_right,num_text,id_analyse)\
 values ('%s','%s','%s','%s','%s');" %(el[0],el[1],el[2],el[3],el[5])
        else:
            str_base = str_base + "insert into base(form,punct_left,punct_right,num_text,id_analyse)\
 values ('%s','%s','%s','%s','%s');" %(el[0],el[1],el[2],el[3],str(0))
    return str_base

def onefile():
    str_base = alltables()
    str_analyse = createanalyse()
    result = str_base  + '\n' + str_analyse
    writefile('onefile.txt',result)
    
def main():
    createbase()
    analyse()
    mystem()
    list_lemms()
    onefile()
    
if __name__ == '__main__':
    main()
