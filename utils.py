def isDebug():
    import sys
    return True if sys.gettrace() else False