"""
    get html source code file from imdb based on test id list.
    if it can be automated, automating it please.
"""
from urllib import request


test_id_list = ['tt0000001', 'tt1234567', 'tt0460648', 'tt2345678', 'tt4346792', 'tt3107288', 'tt0395865',
                'tt3783958', 'tt0000004', 'tt0000007', 'tt0000502', 'tt0001304', 'tt0000869', 'tt0000019',
                'tt0000025', 'tt0010781', 'tt0000481', 'tt0000012', 'tt0000399', 'tt0039624', 'tt0030298',
                'tt0039445']

for item in test_id_list:
    site = request.urlretrieve('http://www.imdb.com/title/{}'.format(item), item + ".html")
