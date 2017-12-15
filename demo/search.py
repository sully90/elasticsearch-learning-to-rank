baseLtrQuery = {
  "query": {
      "match": {
          "_all": "test"
       }
   },
  "rescore": {
      "window_size": 1000,
      "query": {
        "rescore_query": {
            "sltr": {
                "params": {
                    "keywords": ""
                },
                "model": "",
            }
         }
      }
   }
}

baseQuery = {
  "query": {
      "match": {
          "_all": "test"
       }
   }
}

def ltrQuery(keywords, modelName):
    import json
    baseLtrQuery['rescore']['query']['rescore_query']['sltr']['model'] = model
    baseLtrQuery['query']['match']['_all'] = keywords
    baseLtrQuery['rescore']['query']['rescore_query']['sltr']['params']['keywords'] = keywords
    print("%s" % json.dumps(baseLtrQuery))
    return baseLtrQuery


def query(keywords):
    import json
    baseQuery['query']['match']['_all'] = keywords
    print("%s" % json.dumps(baseQuery))
    return baseQuery

if __name__ == "__main__":
    import configparser
    from sys import argv
    from elasticsearch import Elasticsearch

    config = configparser.ConfigParser()
    config.read('settings.cfg')
    esUrl=config['DEFAULT']['ESHost']

    es = Elasticsearch(esUrl, timeout=1000)
    model = "test_6"
    results = None
    if len(argv) > 2:
        model = argv[2]
        results = es.search(index='tmdb', doc_type='movie', body=ltrQuery(argv[1], model))
    else:
        results = es.search(index='tmdb', doc_type='movie', body=query(argv[1]))

    for result in results['hits']['hits']:
                 print(result['_source']['title'] + " : " + str(result["_source"]["id"]))

