
__author__="peon"
__date__ ="$22 mars 2013 10:29:40$"

import urllib2
import sys
import re
import base64



def try_logAndPass(url,username, password):

    req = urllib2.Request(url)
    try:
        handle = urllib2.urlopen(req)
    except IOError, e:
        # here we *want* to fail
        pass
    else:
        # If we don't fail then the page isn't protected
        print "This page isn't protected by authentication."
        sys.exit(1)

    if not hasattr(e, 'code') or e.code != 401:
        # we got an error - but not a 401 error
        print "This page isn't protected by authentication."
        print 'But we failed for another reason.'
        sys.exit(1)

    authline = e.headers['www-authenticate']
    # this gets the www-authenticate line from the headers
    # which has the authentication scheme and realm in it


    authobj = re.compile(
        r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
        re.IGNORECASE)
    # this regular expression is used to extract scheme and realm
    matchobj = authobj.match(authline)

    if not matchobj:
        # if the authline isn't matched by the regular expression
        # then something is wrong
        print 'The authentication header is badly formed.'
        print authline
        sys.exit(1)

    scheme = matchobj.group(1)
    realm = matchobj.group(2)
    # here we've extracted the scheme
    # and the realm from the header
    if scheme.lower() != 'basic':
        print 'This example only works with BASIC authentication.'
        sys.exit(1)

    base64string = base64.encodestring(
                    '%s:%s' % (username, password))[:-1]
    authheader =  "Basic %s" % base64string
    req.add_header("Authorization", authheader)
    try:
        handle = urllib2.urlopen(req)
    except IOError, e:
        # here we shouldn't fail if the username/password is right
        print "It looks like the username or password is wrong."
        sys.exit(1)
    thepage = handle.read()

if __name__ == "__main__":
    from urllib2 import URLError,HTTPError
    username = 'zzzzzzz'
    password = 'zzzzzzz'
    theurl = "www.url.org/rutorrent"
    # *no* http:// !!
    url="http://www.url.org/rutorrent"

# if you want to run this example you'll need to supply
# a protected page with your username and password

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
# this creates a password manager
    passman.add_password(None, theurl, username, password)
# because we have put None at the start it will always
# use this username/password combination for  urls
# for which `theurl` is a super-url

    authhandler = urllib2.HTTPBasicAuthHandler(passman)
# create the AuthHandler

    opener = urllib2.build_opener(authhandler)
    #opener.open(a_url)
    urllib2.install_opener(opener)
# All calls to urllib2.urlopen will now use our handler
# Make sure not to include the protocol in with the URL, or
# HTTPPasswordMgrWithDefaultRealm will be very confused.
# You must (of course) use it when fetching the page though.
    try:
        pagehandle = urllib2.urlopen(url)
    except IOError, e:
        print e
        print 'Reason: ', e.reason
        print 'Error COde : ', e.code
    else:
        print pagehandle.read()    
    print username,password
     
