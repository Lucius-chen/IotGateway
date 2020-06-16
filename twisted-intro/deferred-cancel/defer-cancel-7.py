from twisted.internet import defer

def canceller(d):
    print "I need to cancel this deferred:", d
    print "Firing the deferred with an error"
    d.errback(Exception('error!'))

def callback(res):
    print 'callback got:', res

def errback(err):
    print 'errback got:', err

d = defer.Deferred(canceller) # created by lower-level code
d.addCallbacks(callback, errback) # added by higher-level code
d.cancel()
print 'done'
