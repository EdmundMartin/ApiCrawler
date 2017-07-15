
def parse_results(url):
    results = []
    params = url.split("?")
    for param in params:
        params = param.split('=')
        pairs = zip(params[0::2], params[1::2])
        answer = dict((k, v) for k, v in pairs)
        if answer != {}:
            results.append(answer)
    return results

if __name__ == '__main__':
    a = parse_results('http://edmundmartin.com/wp-includes/js/wp-emoji-release.min.js?ver=4.7.5?blah=276')
    print(a)