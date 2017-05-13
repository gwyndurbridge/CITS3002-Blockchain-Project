import hashlib, sys, time, random
random.seed()

text = 'example'

difficulty = 20


def test(text, difficulty): 
    nonce = random.randint(0,9999999999999)
    loop = True
    best = 0
    timer = time.time()


    while loop:
        nonce = random.randint(0,9999999999999)

        val = (text + str(nonce)).encode('utf-8')

        h = hashlib.sha256()
        h.update(val)
        h = h.digest()


        bits = ''

        for i in h:
            bits += bin(i)[2:].zfill(8)

        for i in range(0,difficulty + 1):
            if int(bits[i]) == 0:
                if int(i) > best:
                    best = int(i)
                sys.stdout.write('Best: %d  \r' % best)
                sys.stdout.flush()

                if int(i) == difficulty:
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


