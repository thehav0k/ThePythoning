import pickle

def xor_decrypt(data, key):
    key = (key * (len(data) // len(key) + 1))[:len(data)]
    return bytes([a ^ b for a, b in zip(data, key.encode())])

with open("encrypted.pki", "rb") as f:
    encrypted = pickle.load(f)

password = input("Enter the password: ")
decrypted = xor_decrypt(encrypted, password)
print("Decrypted message:", decrypted.decode())