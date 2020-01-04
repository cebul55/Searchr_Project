from tika import parser


# def try_textract():
#     text = textract.process('/Users/bartoszcybulski/Downloads/z_57_2016.pdf', 'utf-8', 'pdf')
#     print('PDF File: ' + str(text))
#
#     # text =textract.process()

def try_tika():
    '''
    ps aux | grep java | grep Tika
    kill -9 PID

    :return:
    '''
    raw = parser.from_file('/Users/bartoszcybulski/Downloads/z_57_2016.pdf')
    # print(raw['content'])
    print(raw)


def try_combinations():
    import itertools
    combinations = []
    stuff = '["test word doc"]'
    import ast
    x = u'' + stuff
    x = ast.literal_eval(x)
    stuff = x
    stuff = [n.strip() for n in stuff]
    for L in range(1, len(stuff) + 1):
        for subset in itertools.combinations(stuff, L):
            combinations.append(subset)

    for combination in combinations:
        print(combination)
        for i in combination:
            print(i)

def try_any():
    titles = ['<title>dlugi tytul</title>', '<title>krotki tytul</title>']
    title = 'krotki tytul'
    phrases = ['tytul', 'krotki']
    if all(phrase in title for phrase in phrases):
        print(title)

def try_soup():
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2"><span>Lacie</span></a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc, 'html.parser')

    tag = soup.find('span')
    print(tag)
    print(tag.parent)
    print(tag.parent.name)

if __name__ == '__main__':
    # try_textract()
    try_soup()
