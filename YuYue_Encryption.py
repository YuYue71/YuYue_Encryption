import base64
import zlib
import os

# 凱薩加密（也能用來解密，shift是負的就行）
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isupper():
            ascii_offset = 65
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text += encrypted_char
        elif char.islower():
            ascii_offset = 97
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            encrypted_text += encrypted_char
        elif char.isdigit():
            ascii_offset = 48
            encrypted_char = chr((ord(char) - ascii_offset + shift) % 10 + ascii_offset)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

# 柵欄加密
def rail_fence_encrypt(text, rails):
    if rails == 1:
        return text
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    rail = 0
    direction = 1
    for idx, char in enumerate(text):
        fence[rail][idx] = char
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    encrypted = ''.join(c for row in fence for c in row if c)
    return encrypted

# 柵欄解密
def rail_fence_decrypt(cipher, rails):
    if rails == 1:
        return cipher
    pattern = ['' for _ in range(len(cipher))]
    rail = 0
    direction = 1
    idxs = [[] for _ in range(rails)]
    for idx in range(len(cipher)):
        idxs[rail].append(idx)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    pos = 0
    for r in range(rails):
        for idx in idxs[r]:
            pattern[idx] = cipher[pos]
            pos += 1
    rail = 0
    direction = 1
    result = []
    for idx in range(len(cipher)):
        result.append(pattern[idxs[rail].pop(0)])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(result)

# 字元轉ASCII二進位並串接
def ascii_to_binary_concat(text):
    return ''.join(format(ord(c), '08b') for c in text)

# 二進位轉16進位
def binary_to_hex(binary_string):
    if len(binary_string) % 4 != 0:
        binary_string = binary_string.zfill(len(binary_string) + (4 - len(binary_string) % 4))
    hex_string = hex(int(binary_string, 2))[2:]
    return hex_string

# 16進位轉2進位
def hex_to_binary_string(hex_string):
    binary_string = bin(int(hex_string, 16))[2:]
    if len(binary_string) % 8 != 0:
        binary_string = binary_string.zfill((len(binary_string) + 7) // 8 * 8)
    return binary_string

# 二進位轉回ASCII
def binary_to_ascii(binary_string):
    chars = []
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

# 壓縮並base64編碼
def compress_and_base64(text):
    compressed_data = zlib.compress(text.encode('utf-8'))
    encoded_data = base64.b64encode(compressed_data).decode('utf-8')
    return encoded_data

# 解壓縮並解碼
def decompress_and_base64(encoded_text):
    compressed_data = base64.b64decode(encoded_text)
    decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data.decode('utf-8')

# 主加密程序
def full_encrypt(text, caesar_shift1=3, rail_rails=3, caesar_shift2=5):
    step1 = caesar_encrypt(text, caesar_shift1)                         # 第一次凱薩加密
    step2 = rail_fence_encrypt(step1, rail_rails)                       # 柵欄加密
    step3 = base64.b64encode(step2.encode('utf-8')).decode('utf-8')     # base64加密
    step4 = ascii_to_binary_concat(step3)                               # 轉ASCII二進位
    step5 = binary_to_hex(step4)                                        # 二進位轉16進位
    step6 = caesar_encrypt(step5, caesar_shift2)                        # 第二次凱薩加密
    step7 = base64.b32encode(step6.encode('utf-8')).decode('utf-8')     # base32加密
    final_result = compress_and_base64(step7)                           # 壓縮+base64
    return final_result

# 主解密程序
def full_decrypt(cipher_text, caesar_shift1=3, rail_rails=3, caesar_shift2=5):
    step1 = decompress_and_base64(cipher_text)                           # 解壓縮
    step2 = base64.b32decode(step1.encode('utf-8')).decode('utf-8')      # base32解碼
    step3 = caesar_encrypt(step2, -caesar_shift2)                        # 第二次凱薩解密
    step4 = hex_to_binary_string(step3)                                  # 16進位轉二進位
    step5 = binary_to_ascii(step4)                                       # 二進位轉ASCII
    step6 = base64.b64decode(step5.encode('utf-8')).decode('utf-8')      # base64解碼
    step7 = rail_fence_decrypt(step6, rail_rails)                        # 柵欄解密
    step8 = caesar_encrypt(step7, -caesar_shift1)                        # 第一次凱薩解密
    return step8

# ===== 主程式 =====
if __name__ == "__main__":
    print(f'''
          
    使用到之加密法 :
        1. 凱薩加密 (Caesar Cipher)
        2. 柵欄加密 (Rail Fence Cipher)
        3. ASCII二進位轉換 (ASCII to Binary Conversion)
        4. 二進位轉16進位 (Binary to Hexadecimal Conversion)
        5. Base64編碼 (Base64 Encoding)
        6. Base32編碼 (Base32 Encoding)
        7. 壓縮 (Compression)

          
    +==============================================+
    |             安安大來路不明的朋友             |
    |      謝謝你願意下載並使用 YuYue 加密小工具   |
    |                     說明 :                   |
    |         這是個用來加密和解密的神奇小工具     |
    |          由於作者本人還只是一個Code小白      |
    |             所以有不足之處還請見諒           |
    |        如果有任何問題或建議，歡迎聯繫我！    |
    +==============================================+
          
                    YuYue Encryption               
                    版本 : 1.0.1                   
                    作者 : YuYue                   

                幽月YuYue保有所有權利
                    2025/04/29
    
    ''')
    while True:
        mode = input("請選擇模式 (1: 加密, 2: 解密, 0: 結束): ").strip()
        if mode == "1":
            plain_text = input("請輸入要加密的內容: ")
            encrypted_text = full_encrypt(plain_text)
            print(f"\n原始文本: {plain_text}")
            print(f"加密後: {encrypted_text}")
        elif mode == "2":
            cipher_text = input("請輸入加密後的內容: ")
            try :
                decrypted_text = full_decrypt(cipher_text)
            except Exception as e:
                print(f"解密失敗，請檢查輸入的內容是否正確。錯誤信息: {e}")
                continue
            print(f"\n加密後文本: {cipher_text}")
            print(f"解密後: {decrypted_text}")
        elif mode == "0":
            print("程式結束")
            break
        else:
            print("無效的選項，請重新選擇。")

        input("\n按下 Enter 鍵繼續...")
