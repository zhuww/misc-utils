import cPickle
def save(filename,*objects):
    """save objects into a compressed diskfile"""
    file = open(filename, 'wb')
    for obj in objects: 
        cPickle.dump(obj, file, -1)
    file.close()

def load(filename):
    """reload objects from a compressed diskfile"""
    file = open(filename, 'rb')
    while True:
        try: yield cPickle.load(file)
        except EOFError: break
    file.close()
