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

if __name__ == '__main__':
    # try_textract()
    try_tika()
