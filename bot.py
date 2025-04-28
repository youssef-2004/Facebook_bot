import requests
import time

PAGE_ACCESS_TOKEN = 'EAAKE4ZBIOlaUBO87URCi3ZCdWk07ribfPqUNGKlsHUQrQTtFFFIfMtTJhlZBorCmrwFcD72UilMTZCZCQ0GWvNyn6O4jkB17kuLYthLGhXZCfR4S63ZAV7NvoIa3kEAldDL66w1ZBDXHTOZCFAZANANXIwZCWHvCbpOdCBbzJuyUe3RyUFqhpMEVZCpLxpZA8t0A0fNCjjNIoHObcqIXKx4wQVhvW0MZA81YLzQUNqotI2RNlMU2wx'
POST_ID = 'pfbid02X8uwzathu8PKb49UTeYtPZ9CQi1nBVz7WLkgHrW94Z8Tf4EoVMDhN87SPYEVRNLDl'

# وظيفة لجلب التعليقات من البوست
def get_comments():
    url = f"https://graph.facebook.com/v18.0/{POST_ID}/comments?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    return response.json()

# وظيفة للرد على الكومنت في نفس البوست
def reply_to_comment(comment_id):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/comments"
    payload = {
        'message': 'شكرا لتعليقك ❤️، شرفنا بتواصلك معانا!',
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload)
    return response.json()

# وظيفة لإرسال رسالة خاصة للمستخدم
def send_private_message(user_id):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "text": "🎉 عرض خاص لك 🎉\n\nسعر الطقم: 300 جنيه 🤑\nويتكون من:\n👕 تيشرت\n👖 شورت\n\n💥 وعندك عرض تاني 💥:\n2 تيشرت + 2 شورت بس بـ 500 جنيه 🎁\n\n⏰ العرض لفترة محدودة! سريع قبل ما يفوتك!"
        }
    }
    response = requests.post(url, json=payload)
    return response.json()

# حفظ الكومنتات اللي تم الرد عليها
seen_comments = set()

# بدء المراقبة للتعليقات الجديدة
while True:
    data = get_comments()
    if 'data' in data:
        for comment in data['data']:
            comment_id = comment['id']
            sender_id = comment['from']['id']
            if comment_id not in seen_comments:
                print(f"New comment: {comment['message']} from {comment['from']['name']}")
                # الرد على الكومنت
                reply_to_comment(comment_id)
                # إرسال رسالة خاصة
                send_private_message(sender_id)
                # إضافة الكومنت للقائمة عشان منردش عليه تاني
                seen_comments.add(comment_id)
    else:
        print("No comments found or Error!")

    time.sleep(30)  # ينتظر 30 ثانية ثم يعيد التحقق
