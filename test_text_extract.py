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

if __name__ == '__main__':
    # try_textract()
    try_any()
