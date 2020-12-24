from tools_hex import pair_generator, gen_key, encrypt, decrypt, sign, verify, sendKey, receiveKey
import random

pq = pair_generator()

A_keys = gen_key(pq[0], pq[1])
B_keys = gen_key(pq[2], pq[3])

M = random.randint(0, 256)
print('Initial message ', M)

encd = encrypt(M, A_keys[1])

decd = decrypt(encd, A_keys[0])
print('Decrypted message', decd)

signature = sign(M, A_keys[0])
print('Verification ', verify(M, signature, A_keys[1]))

n = A_keys[1][1]

n1 = B_keys[1][1]

print('n < n1: ', n < n1)

k = random.randint(0, n)

message = sendKey(k, A_keys, B_keys[1])
print('Authentification ', receiveKey(message, A_keys[1], B_keys))








