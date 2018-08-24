from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch()

@app.route('/')
def search_main():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    searchtext=request.args.get('searchtext', '')
    searchpage=request.args.get('page', '')
    
    searchDSL = {
        "from" : int(searchpage)*10, "size" : 10,
        "query": {
            #match or term or range": {col: keyword}
            "match": {"text" : searchtext}
        },
        "highlight" : {
            "fields" : {
                "text":{}
            }
        }
    }

    searchrespond = es.search(index="tor", body=searchDSL)

    spenttime = searchrespond['took']   #unit = mili sec = ms
    numhit = searchrespond['hits']['total']
    #Process searchrespond
    #Format: searchrespond['hits']['hits'][0 or other array index]['_source']['title' or other].encode('utf-8')
    #return '<h1>Title: '+str(searchrespond['hits']['hits'][0]['_source']['title'].encode('utf-8'))+'</h1>'
    return render_template('show_result.html', search_source=searchrespond['hits']['hits'], defaulttext=searchtext, nowpage=int(searchpage), thetime=spenttime, thehit=numhit)

'''
Helpful site:
https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html
https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch.Elasticsearch.search
https://elasticsearch-py.readthedocs.io/en/master/#example-usage

'''