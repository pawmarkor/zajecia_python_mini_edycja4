import hashlib
# https://en.wikipedia.org/wiki/Pigeonhole_principle
# https://pl.wikipedia.org/wiki/Zasada_szufladkowa_Dirichleta

CHUNK_SIZE = 1024


def get_hash(f_path, mode='md5'):
    h = hashlib.new(mode)
    with open(f_path, 'br') as f:
        buffer = f.read(CHUNK_SIZE)
        while buffer:
            h.update(buffer)
            buffer = f.read(CHUNK_SIZE)

    hash_text = h.hexdigest()
    return hash_text
    
#print(get_hash('plik_testowy'))
#print(get_hash('sha1_collisions/shattered-1.pdf', mode='sha1'))
#print(get_hash('sha1_collisions/shattered-2.pdf', mode='sha1'))

# eb63071881718ed66bb75ce670e65b9e
# eb63071881718ed66bb75ce670e65b9e

