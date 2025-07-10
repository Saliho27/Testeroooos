from instabot import Bot
import time # لإضافة تأخيرات

def get_account_details():
    accounts_list = []
    print("أدخل تفاصيل الحسابات (اترك اسم المستخدم فارغًا للإنهاء):")
    while True:
        username = input("اسم المستخدم (Username): ").strip()
        if not username:
            break
        password = input("كلمة المرور (Password): ").strip()
        proxy = input("البروكسي (مثال: http://user:pass@ip:port أو http://ip:port): ").strip()

        accounts_list.append({
            "username": username,
            "password": password,
            "proxy": proxy
        })
        print("-" * 30) # خط فاصل للتنظيم
    return accounts_list

def login_and_control(account_info):
    bot = Bot()
    try:
        if account_info["proxy"]:
            bot.proxy(account_info["proxy"])
        else:
            print(f"لا يوجد بروكسي للحساب: {account_info['username']}. سيتم استخدام اتصال مباشر.")

        if bot.login(username=account_info["username"], password=account_info["password"]):
            print(f"تم تسجيل الدخول بنجاح للحساب: {account_info['username']}")
            return bot
        else:
            print(f"فشل تسجيل الدخول للحساب: {account_info['username']}")
            return None
    except Exception as e:
        print(f"حدث خطأ أثناء تسجيل الدخول للحساب {account_info['username']}: {e}")
        return None

def report_user(bot_instance, target_username, report_type="fake_account"):
    try:
        user_id = bot_instance.get_user_id_from_username(target_username)
        if user_id:
            if bot_instance.report_user(user_id, report_type=report_type):
                print(f"تم الإبلاغ عن المستخدم {target_username} كـ {report_type} بنجاح.")
                return True
            else:
                print(f"فشل الإبلاغ عن المستخدم {target_username}.")
                return False
        else:
            print(f"لم يتم العثور على المستخدم {target_username}.")
            return False
    except Exception as e:
        print(f"حدث خطأ أثناء الإبلاغ عن المستخدم {target_username}: {e}")
        return False

def main():
    accounts = get_account_details()

    if not accounts:
        print("لم يتم إدخال أي حسابات. سيتم إنهاء البرنامج.")
        return

    target_account_to_report = input("أدخل اسم المستخدم للحساب الذي تريد الإبلاغ عنه: ").strip()
    if not target_account_to_report:
        print("لم يتم إدخال حساب للإبلاغ عنه. سيتم إنهاء البرنامج.")
        return

    print(f"\nبدء عملية الإبلاغ عن الحساب: {target_account_to_report}")
    for account in accounts:
        print(f"\nمحاولة تسجيل الدخول باستخدام الحساب: {account['username']}")
        bot = login_and_control(account)
        if bot:
            report_user(bot, target_account_to_report, report_type="fake_account")
            # انتظر قليلاً بين العمليات لتجنب الحظر
            time.sleep(5) # تأخير 5 ثوانٍ
            # bot.logout() # قد تحتاجها بعض المكتبات أو في نهاية كل عملية

    print("\nانتهت العملية.")

if name == "main":
    main()
