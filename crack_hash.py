import hashlib

# البصمة المشفرة لكلمة المرور التي نريد كسرها (البصمة الحقيقية لكلمة "password")
target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"

print("[-] بدء هجوم القاموس على البصمة المشفرة...")

# قائمة كلمات المرور الشائعة (القاموس)
wordlist = ["123456", "admin", "password", "test", "wifi", "algeria", "root", "qwerty"]

for word in wordlist:
    # تشفير الكلمة باستخدام خوارزمية MD5
    hashed_word = hashlib.md5(word.encode()).hexdigest()
    
    # إذا تطابقت البصمة، فقد كسرنا كلمة المرور!
    if hashed_word == target_hash:
        print(f"[+] تم العثور على كلمة المرور: {word}")
        break
else:
    print("[-] لم يتم العثور على كلمة المرور في هذا القاموس.")

