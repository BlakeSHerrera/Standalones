import urllib, requests, bs4, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

arrow = '→'
path = 'problems/'

class File:

    def __init__(self, pathname, desc, retn, name, params):
        self.filename = pathname + '/' + name + '.c'
        self.filename = self.filename.replace('/', '\\')
        self.description = desc
        self.return_type = retn
        self.function_name = name
        self.parameters = File.process_params(params)
        #self.tests = self.process_tests(tests)
        print(self.function_name)

    def save(self):
        f = open(self.filename, 'w')
        f.write(str(self))
        f.close()

    def process_params(s):
        data = s.split(',')
        if data[0] == '':
            return []
        params = []
        for i in data:
            typee, name = i.strip().split(' ')
            params.append(Param(typee, name))
        return params

    def process_tests(self, arr):
        global arrow
        tests = []
        for i in arr:
            for j in range(len(i)):
                if i[j] == '(':
                    start = j + 1
                elif i[j] == ')':
                    params = i[start : j]
                    break
            expected = i.split(arrow)[1].strip()
            params += ', ' + expected
            parameters = ['']
            in_brackets = False
            for j in params:
                if j == '[':
                    in_brackets = True
                elif j == ']':
                    in_brackets = False
                elif j == ',' and not in_brackets:
                    parameters[-1] = parameters[-1].strip()
                    parameters.append('')
                    continue
                parameters[-1] += j
            parameters[-1] = parameters[-1].strip()
            tests.append(parameters)
        self.tests = tests

    def __str__(self):
        s = ''
        s += '#include<stdio.h>\n'
        s += '#include<stdlib.h>\n'
        s += '#include<string.h>\n'
        s += '\n'
        s += '#define TRUE 1\n'
        s += '#define FALSE 0\n'
        s += '\n'
        s += '/*\n'
        s += self.get_description() + '\n'
        s += '*/\n'
        s += '\n'
        s += self.get_return_type() + ' ' + self.function_name
        s += '(' + self.format_parameters() + ')\n'
        s += '{\n'
        s += '    \n'
        s += '}\n'
        s += '\n'
        s += 'void printarr(int * arr, int size)\n'
        s += '{\n'
        s += '    int i;\n'
        s += '    printf("{");\n'
        s += '    for(i=0; i<size; i++)\n'
        s += '    {\n'
        s += '        if(i != 0)\n'
        s += '        {\n'
        s += '            printf(", %d", arr[i]);\n'
        s += '        }\n'
        s += '        else\n'
        s += '        {\n'
        s += '            printf("%d", arr[i]);\n'
        s += '        }\n'
        s += '    }\n'
        s += '    printf("}");\n'
        s += '}\n'
        s += '\n'
        s += 'int * ialloc(int arr[])\n'
        s += '{\n'
        s += '    int size = sizeof(arr);\n'
        s += '    int * i = (int *) malloc(size * sizeof(int));\n'
        s += '    for(size = size-1; size>=0; size--)\n'
        s += '    {\n'
        s += '        i[size] = arr[size];\n'
        s += '    }\n'
        s += '    return i;\n'
        s += '}\n'
        s += '\n'
        ps = self.format_parameters()
        s += 'int test('
        if len(ps) > 0:
            s += self.format_parameters() + ', '
        grt = self.get_return_type()
        if grt == 'int *':
            s += grt + ' expected, int expectedSize)\n'
        else:
            s += grt + ' expected)\n'
        s += '{\n'
        s += self.get_test_body() + '\n'
        s += '}\n'
        s += '\n'
        s += 'int main()\n'
        s += '{\n'
        s += self.get_main_body()
        s += '}\n'
        return s

    def get_description(self):
        s = self.description
        s = replace(s).replace('\\"', '"')
        tokens = s.split(' ')
        r = [tokens[0]]
        for t in tokens[1:]:
            if len(r[-1]) + len(t) > 64:
                r.append(t)
            else:
                r[-1] += ' ' + t
        s = ''
        for i in r:
            s += i + '\n'
        return s[:-1]

    def get_return_type(self):
        s = self.return_type
        if s == 'boolean':
            s = 'int'
        elif s == 'String':
            s = 'char *'
        elif s == 'int[]':
            return 'int *'
        return s

    def format_parameters(self):
        s = ''
        for i in self.parameters:
            typee = i.typee
            add = False
            if typee == 'boolean':
                typee = 'int'
            elif typee == 'String':
                typee = 'char *'
            elif typee == 'int[]':
                s += 'int ' + i.name + '[], '
                s += 'int ' + i.name + 'Size, '
                continue
            s += typee + ' ' + i.name + ', '
        return s[:-2]

    def format_parameters_no_type(self):
        s = ''
        for i in self.parameters:
            s += i.name + ', '
            if i.typee == 'int[]':
                s += i.name + 'Size, '
        return s[:-2]

    def get_test_body(self):
        s = ''
        t = self.get_return_type()
        if t == 'int':
            s += '    int returned = ' + self.function_name
            s += '(' + self.format_parameters_no_type() + ');\n'
            s += '    printf("%d Expected\\n", expected);\n'
            s += '    printf("%d Returned\\n\\n", returned);\n'
            s += '    return expected == returned;'
        elif t == 'char *':
            s += '    char * returned = ' + self.function_name
            s += '(' + self.format_parameters_no_type() + ');\n'
            s += '    printf("%s Expected\\n", expected);\n'
            s += '    printf("%s Returned\\n\\n", returned);\n'
            s += '    int res = strcmp(expected, returned) == 0;\n'
            s += '    free(returned);\n'
            s += '    free(expected);\n'
            s += '    return res;'
        elif t == 'int *':
            s += '    int * returned = ' + self.function_name
            s += '(' + self.format_parameters_no_type() + ');\n'
            s += '    printarr(expected, expectedSize);\n'
            s += '    printf(" Expected\\n", expected);\n'
            s += '    printarr(returned, expectedSize);\n'
            s += '    printf(" Returned\\n\\n", returned);\n'
            s += '    int res = memcmp(expected, returned, expectedSize * sizeof(int)) == 0;\n'
            s += '    free(returned);\n'
            s += '    free(expected);\n'
            s += '    return res;'
        return s

    def get_main_body(self):
        s = ''
        s += '    int correct = 0;\n'
        s += '    int total = 0;\n'
        for i in self.tests:
            s += '    printf("Sent: '
            s += replace(', '.join(str(j) for j in i[:-1])) + '\\n");\n'
            s += '    correct += test('
            s += self.format_all_inputs(i).replace('\\"', '"') + ');\n'
            s += '    total++;\n'
            s == '    \n'
        s += '    printf("%d / %d correct\\n", correct, total");\n'
        s += '    return 0;\n'
        return s

    def format_all_inputs(self, inputs):
        if inputs[0] == '':
            del inputs[0]
        ins = []
        for i in inputs[:-1]:
            s = ''
            in_bracket = False
            count = 0
            for j in i:
                if j == '[':
                    j = '{'
                    s += '(int[])'
                    in_bracket = True
                elif j == ']':
                    j = '}'
                    in_bracket = False
                    s += j
                    s += ', ' + str(count + 1)
                    count = 0
                    continue
                elif j == ',' and in_bracket:
                    count += 1
                s += j
            ins.append(s)
        i = inputs[-1]
        s = ''
        in_bracket = False
        count = 0
        for j in i:
            if j == '[':
                j = '{'
                s += 'ialloc((int[])'
                in_bracket = True
            elif j == ']':
                j = '}'
                in_bracket = False
                s += j + ')'
                s += ', ' + str(count + 1)
                count = 0
                continue
            elif j == ',' and in_bracket:
                count += 1
            s += j
        ins.append(s)
        return replace(', '.join(i for i in ins))

    def get_appropriate_return(self):
        if self.return_type == 'boolean':
            return 'return false;'
        if self.return_type == 'int':
            return 'return 0;'
        return 'return null;'
    
class Param:

    def __init__(self, typee, name):
        self.typee = typee
        self.name = name

def getsrc(url):
    time.sleep(1)
    return requests.get(url).text

def get_params(proto):
    i = proto.index('(')
    j = proto.index(')')
    return proto[i+1 : j]

def get_return(proto):
    return proto.split(' ')[1]

def get_name(proto):
    i = proto.index(' ')
    i = proto.index(' ', i + 1)
    j = proto.index('(')
    return proto[i + 1:j]

def replace(s):
    s = s.replace('true', 'TRUE')
    s = s.replace('false', 'FALSE')
    s = s.replace('boolean', 'int')
    s = s.replace('String', 'char *')
    s = s.replace('"', '\\"')
    s = s.replace('null', 'NULL')
    return s

driver = webdriver.Firefox()
try:
    url = 'http://codingbat.com'
    urls = []
    src = getsrc(url + '/java')
    soup = bs4.BeautifulSoup(src, 'html.parser')
    for item in soup.findAll('div', {'class':'summ'}):
        newurl = url + item.find('a')['href']
        urls.append(newurl)

    moreurls = []
    for u in urls[:-4]:
        print(u)
        src = getsrc(u)
        soup = bs4.BeautifulSoup(src, 'html.parser')
        foldername = u[u.rindex('/') + 1:]
        for item in soup.findAll('td', {'width':'200'}):
            newurl = url + item.find('a')['href']
            moreurls.append(newurl)
            print(newurl)
            driver.get(newurl)
            src = driver.page_source
            soup = bs4.BeautifulSoup(src, 'html.parser')
            item = soup.find('td', {'width':'700', 'valign':'top'})
            #main code prototype
            prob_desc = item.find('div', {'class':'minh'}).text
            proto = soup.find('div', {'id':'ace_div'}).text
            if proto[:6] != 'public':
                proto = 'public ' + proto
            form = driver.find_element_by_name('codeform')
            button = driver.find_element_by_xpath("//button[@class='go']")
            file = File(path + foldername, prob_desc, get_return(proto),
                        get_name(proto), get_params(proto))
            form.send_keys(file.get_appropriate_return())
            time.sleep(.5)
            button.click()
            time.sleep(.5)
            src = driver.page_source
            soup = bs4.BeautifulSoup(src, 'html.parser')
            item = soup.find('td', {'width':'500', 'valign':'top'})
            #code returns found here
            item = item.find('table', {'class':'out'})
            tests = []
            for i in item.findAll('tr')[1:]:
                if 'other tests' in i.text or 'xpected' in i.text:
                    continue
                test = i.find('td')
                tests.append(test.text)
            file.process_tests(tests)
            file.save()
finally:
    driver.quit()
