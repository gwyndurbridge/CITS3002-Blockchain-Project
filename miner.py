import hashlib, sys, time

text = 'example'


difficulty = 1


def test(text, difficulty): 
    nonce = 0
    loop = True
    best = 0
    timer = time.time()


    while loop:
        nonce += 1

        val = (text + str(nonce)).encode('utf-8')

        h = hashlib.sha256()
        h.update(val)
        h = h.digest()

        for i in range(0,difficulty + 1):
            if h[i] == 0:
                if i > best:
                    best = i
                sys.stdout.write('Best: %d  \r' % best)
                sys.stdout.flush()

                if i == difficulty:                    
                    loop = False
            else:
                break

    print(time.time() - timer)
    print('successful nonce: ', nonce)
    return nonce

checkNonce = test(text, difficulty)

h = hashlib.sha256()
check = (text + str(checkNonce)).encode('utf-8')
h.update(check)
h = h.digest()
print('====Check Nonce====')
print('hash : ', h)
print('bytes: ',h[0],h[1],h[2],h[3],h[4],h[5],h[6],h[7],h[8])


