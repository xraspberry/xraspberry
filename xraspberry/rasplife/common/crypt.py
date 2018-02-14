from Crypto.Cipher import AES


def aes_encrypt(plaintext, key, fill=False):
    blocksize = 16
    reminder_len = len(plaintext) % blocksize
    reminder = ''
    if reminder_len > 0:
        if fill:
            plaintext += '\0' * (blocksize - reminder_len)
        else:
            plaintext, reminder = plaintext[:-reminder_len], plaintext[-reminder_len:]
    aes = AES.new(key, AES.MODE_CBC, key[11:27])
    return aes.encrypt(plaintext) + reminder


def aes_decrypt(ciphertext, key, strip=False):
    blocksize = 16
    reminder_len = len(ciphertext) % blocksize
    if not strip and reminder_len > 0:
        ciphertext, reminder = ciphertext[:-reminder_len], ciphertext[-reminder_len:]
    else:
        reminder = ''

    aes = AES.new(key, AES.MODE_CBC, key[11:27])

    if strip:
        return aes.decrypt(ciphertext).rstrip('\0')
    else:
        return aes.decrypt(ciphertext) + reminder
