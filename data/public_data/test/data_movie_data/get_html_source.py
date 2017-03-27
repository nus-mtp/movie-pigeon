"""
    get html source code file from imdb based on test id list.
    if it can be automated, automating it please.
"""
from urllib import request

test_id_list = ['tt2771200', 'tt3227946', 'tt3271078', 'tt6023350', 'tt0068918', 'tt0125590',
                'tt0378422', 'tt2016315', 'tt0141399', 'tt0142231', 'tt3107288', 'tt0034517']

for item in test_id_list:
    site = request.urlretrieve('http://www.imdb.com/title/{}'.format(item), item + ".html")
