from apputils.http_verb import HttpVerb

def test_http_verb():
    assert HttpVerb.DELETE == 'DELETE'
    assert HttpVerb.GET == 'GET'
    assert HttpVerb.POST == 'POST'
    assert HttpVerb.PUT == 'PUT'
