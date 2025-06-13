import pickle

def xor_encrypt(data, key):
    key = (key * (len(data) // len(key) + 1))[:len(data)]
    return bytes([a ^ b for a, b in zip(data, key.encode())])

message = input("Enter the message to encrypt: ")
password = input("Enter the password: ")

encrypted = xor_encrypt(message.encode(), password)

with open("encrypted.pki", "wb") as f:
    pickle.dump(encrypted, f)

print("Message encrypted and saved to 'encrypted.pki'.")