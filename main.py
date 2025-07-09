print("Welcome to the encryption/decryption program!!!")
print("What would you like to do today?")

characterset = ("abcdefghijklmnopqrstuvwxyz0123456789!?/,.:;+=-<>@#$%^&*")
num_char = len(characterset)

# Encryption function
def encrypt_message(message, key):
    encrypted_message = ""
    for i in message:
        if i == " ": 
            encrypted_message += " "
        else:
            index = characterset.find(i.lower())
            new_index = index + key
            if new_index >= num_char:
                new_index -= num_char
            encrypted_message += characterset[new_index]
    return encrypted_message

# Decryption function
def decrypt_message(message, key):
    decrypted_message = ""
    for i in message:
        if i == " ":  
            decrypted_message += " "
        else:
            index = characterset.find(i.lower())
            new_index = index - key
            if new_index < 0:
                new_index += num_char
            decrypted_message += characterset[new_index]
    return decrypted_message

while True: 
    user_input = input("Enter E for encrypt and D for decrypt: ").upper()

    if user_input == "E":
        key = int(input("Please enter the key as integer: "))
        message = input("Enter the message you want to encrypt in lowercase: ")
        encrypted_message = encrypt_message(message, key)
        print(encrypted_message)
        
    elif user_input == "D":
        key = int(input("Please enter the key as integer: "))
        encrypted_message = input("Enter the message you want to decrypt: ")
        decrypted_message = decrypt_message(encrypted_message, key)
        print(decrypted_message)
        
    else: 
        print("Invalid entry")
            
    print("Would you like to encrypt/decrypt another message?")
    choice = input("yes or no?: ").lower()
    if choice != "yes":
        print("Thank you for using the encryption/decryption program. Goodbye!")
        break
