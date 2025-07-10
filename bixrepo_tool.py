from instabot import Bot
import time
import os

# لتخزين الحسابات والبروكسيات
# كل حساب سيكون قاموسًا يحتوي على 'username', 'password', 'proxy'
accounts_data = []
proxies_data = [] # يمكن استخدامها لاحقًا لتخصيص بروكسي من قائمة موجودة

def clear_screen():
    """ينظف شاشة الطرفية."""
    os.system('cls' if os.name == 'nt' else 'clear')

def login_and_control(account_info):
    bot = Bot()
    try:
        # إذا كان هناك بروكسي محدد للحساب، استخدمه
        if account_info["proxy"]:
            bot.proxy(account_info["proxy"])
        else:
            # إذا لم يكن هناك بروكسي، instabot سيستخدم الـ IP المحلي تلقائيًا
            print(f"الحساب: {account_info['username']} سيستخدم اتصال مباشر (IP محلي).")

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
    """
    يبلغ عن مستخدم معين.
    report_type يمكن أن تكون "fake_account", "spam", "violence", etc. (تحقق من وثائق instabot لمزيد من التفاصيل)
    """
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

def add_proxy():
    """يضيف بروكسي جديد إلى القائمة."""
    proxy = input("أدخل البروكسي الجديد (مثال: http://user:pass@ip:port): ").strip()
    if proxy and proxy not in proxies_data:
        proxies_data.append(proxy)
        print(f"تمت إضافة البروكسي: {proxy}")
    elif proxy in proxies_data:
        print("هذا البروكسي موجود بالفعل.")
    else:
        print("لم يتم إدخال بروكسي صالح.")
    input("\nاضغط Enter للمتابعة...")

def add_account():
    """يضيف حساب انستغرام جديد."""
    username = input("اسم المستخدم (Username): ").strip()
    password = input("كلمة المرور (Password): ").strip()

    print("\nاختر بروكسي للحساب:")
    if not proxies_data:
        print("لا توجد بروكسيات متاحة. سيتم إضافة الحساب بدون بروكسي.")
        proxy_choice = ""
    else:
        for i, p in enumerate(proxies_data):
            print(f"{i+1}. {p}")
        print("0. لا تستخدم بروكسي")
        try:
            choice = int(input("أدخل رقم البروكسي الذي تريد استخدامه: "))
            if 1 <= choice <= len(proxies_data):
                proxy_choice = proxies_data[choice - 1]
            elif choice == 0:
                proxy_choice = ""
            else:
                print("اختيار غير صالح. لن يتم استخدام بروكسي.")
                proxy_choice = ""
        except ValueError:
            print("إدخال غير صالح. لن يتم استخدام بروكسي.")
            proxy_choice = ""

    if username and password:
        accounts_data.append({
            "username": username,
            "password": password,
            "proxy": proxy_choice
        })
        print(f"تمت إضافة الحساب: {username} (البروكسي: {proxy_choice if proxy_choice else 'لا يوجد'})")
    else:
        print("اسم المستخدم وكلمة المرور مطلوبان لإضافة حساب.")
    input("\nاضغط Enter للمتابعة...")

def start_report_with_filter(use_proxy_accounts_only):
    """
    يبدأ عملية الإبلاغ بناءً على ما إذا كان الحساب يستخدم بروكسي أو IP محلي.
    :param use_proxy_accounts_only: True للإبلاغ بالحسابات التي لها بروكسي فقط، False للحسابات التي ليس لها بروكسي فقط.
    """
    if not accounts_data:
        print("لا توجد حسابات مضافة لبدء عملية الإبلاغ.")
        input("\nاضغط Enter للمتابعة...")
        return

    target_account_to_report = input("أدخل اسم المستخدم للحساب الذي تريد الإبلاغ عنه: ").strip()
    if not target_account_to_report:
        print("لم يتم إدخال حساب للإبلاغ عنه. سيتم إلغاء العملية.")
        input("\nاضغط Enter للمتابعة...")
        return

    filtered_accounts = []
    if use_proxy_accounts_only:
        filtered_accounts = [acc for acc in accounts_data if acc["proxy"]]
        print("\nبدء عملية الإبلاغ باستخدام الحسابات التي لديها بروكسي فقط...")
    else:
        filtered_accounts = [acc for acc in accounts_data if not acc["proxy"]]
        print("\nبدء عملية الإبلاغ باستخدام الحسابات التي تستخدم IP محلي فقط...")

    if not filtered_accounts:
        print("لا توجد حسابات مطابقة للمعايير المحددة.")
        input("\nاضغط Enter للمتابعة...")
        return

    print(f"الإبلاغ عن الحساب: {target_account_to_report}")
    for account in filtered_accounts:
        print(f"\nمحاولة تسجيل الدخول باستخدام الحساب: {account['username']}")
        bot = login_and_control(account)
        if bot:
            report_user(bot, target_account_to_report, report_type="fake_account")
            time.sleep(5) # تأخير 5 ثوانٍ بين كل عملية إبلاغ
            # bot.logout() # قد تحتاجها بعض المكتبات أو في نهاية كل عملية
    print("\nانتهت عملية الإبلاغ.")
    input("\nاضغط Enter للمتابعة...")

def main_menu():
    """يعرض القائمة الرئيسية ويتعامل مع اختيارات المستخدم."""
    while True:
        clear_screen()
        print("BİXRepo")
        print("1. بدء الإبلاغ باستخدام البروكسي (للحسابات التي لها بروكسي)")
        print("2. بدء الإبلاغ باستخدام IP محلي (للحسابات التي ليس لها بروكسي)")
        print("3. إضافة بروكسي")
        print("4. إضافة حساب")
        print("5. عرض الحسابات والبروكسيات المضافة")
        print("6. خروج")

        choice = input("أدخل اختيارك: ").strip()

        if choice == '1':
            start_report_with_filter(True) # True تعني استخدم حسابات البروكسي فقط
        elif choice == '2':
            start_report_with_filter(False) # False تعني استخدم حسابات الـ IP المحلي فقط
        elif choice == '3':
            add_proxy()
        elif choice == '4':
            add_account()
        elif choice == '5':
            print("\n--- الحسابات المضافة ---")
            if accounts_data:
                for acc in accounts_data:
                    print(f"اسم المستخدم: {acc['username']}, البروكسي: {acc['proxy'] if acc['proxy'] else 'لا يوجد'}")
            else:
                print("لا توجد حسابات مضافة.")
            print("\n--- البروكسيات المضافة ---")
            if proxies_data:
                for p in proxies_data:
                    print(p)
            else:
                print("لا توجد بروكسيات مضافة.")
            input("\nاضغط Enter للمتابعة...")
        elif choice == '6':
            print("جاري الخروج من BİXRepo. إلى اللقاء!")
            break
        else:
            print("اختيار غير صالح. يرجى المحاولة مرة أخرى.")
            input("\nاضغط Enter للمتابعة...")

if __name__ == "__main__":
    main_menu()
