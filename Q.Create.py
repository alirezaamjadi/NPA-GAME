import json
import random

def create_item(sequence):
    # عدد بعدی طبق اختلاف بین دو عدد اول محاسبه می‌شود
    answer = sequence[1] + (sequence[1] - sequence[0])
    return {
        "sequence": sequence,
        "answer": answer,
        "attempts": 0,
        "solved": False
    }

def generate_level(level_num):
    level = []
    start = random.randint(5, 20)  # عدد شروع منطقی برای کلاس دهمی
    count = 10

    if level_num == 1:
        # مرحله 1 - خیلی آسان: جمع ثابت ساده +5
        for i in range(count):
            seq = [start + i * 5, start + (i + 1) * 5, None]
            level.append(create_item(seq))

    elif level_num == 2:
        # مرحله 2 - جمع ثابت ساده +3
        for i in range(count):
            seq = [start + i * 3, start + (i + 1) * 3, None]
            level.append(create_item(seq))

    elif level_num == 3:
        # مرحله 3 - ضرب ثابت ساده ×2
        for i in range(count):
            seq = [start * (2 ** i), start * (2 ** (i + 1)), None]
            level.append(create_item(seq))

    elif level_num == 4:
        # مرحله 4 - ضرب ثابت ×3
        for i in range(count):
            seq = [start * (3 ** i), start * (3 ** (i + 1)), None]
            level.append(create_item(seq))

    elif level_num == 5:
        # مرحله 5 - جمع با عدد متغیر (مثل +2، +4، +6، ...)
        for i in range(count):
            diff = 2 * (i + 1)
            seq = [start + sum(2 * j for j in range(i)), start + sum(2 * j for j in range(i + 1)), None]
            level.append(create_item(seq))

    elif level_num == 6:
        # مرحله 6 - متوسط: جمع با اعداد متغیر یا ضرب ساده
        for i in range(count):
            diff = i + 2
            seq = [start + sum(range(i)) * diff, start + sum(range(i + 1)) * diff, None]
            level.append(create_item(seq))

    elif level_num == 7:
        # مرحله 7 - متوسط رو به سخت: الگوهای دو مرحله‌ای (مثلاً +5، ×2)
        for i in range(count):
            if i % 2 == 0:
                a = start + i * 5
                b = a * 2
            else:
                a = start + i * 5
                b = a + 5
            seq = [a, b, None]
            level.append(create_item(seq))

    elif level_num == 8:
        # مرحله 8 - چالش برانگیز: اختلاف‌هایی که با دقت قابل تشخیص هستن
        for i in range(count):
            diff = 3 + i
            a = start + i * diff
            b = a + diff + 1
            seq = [a, b, None]
            level.append(create_item(seq))

    elif level_num == 9:
        # مرحله 9 - سخت: اعداد اول
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for i in range(count):
            seq = [primes[i], primes[i+1], None]
            level.append(create_item(seq))

    elif level_num == 10:
        # مرحله 10 - سخت: تغییر تصاعد در اختلاف‌ها (مثل 3، 6، 10، ?)
        diffs = [3, 6, 10, 15, 21, 28, 36, 45, 55, 66]
        for i in range(count):
            a = start + sum(diffs[:i])
            b = start + sum(diffs[:i+1])
            seq = [a, b, None]
            level.append(create_item(seq))

    elif level_num == 11:
        # مرحله 11 - خیلی سخت: الگوهایی که دو بخش دارن (جمع و تقسیم همزمان)
        for i in range(count):
            a = start + i * 4
            b = (a * 2) // 3
            seq = [a, b, None]
            level.append(create_item(seq))

    elif level_num == 12:
        # مرحله 12 - خیلی سخت: ترکیب چند عملیات: مثل ×2 سپس −1، بعد +3
        for i in range(count):
            a = (start + i) * 2 - 1
            b = (start + i + 1) * 2 - 1
            seq = [a + 3, b + 3, None]
            level.append(create_item(seq))

    elif level_num == 13:
        # مرحله 13 - چالش ذهنی: الگویی که نیاز به آزمایش چند حالت داره
        for i in range(count):
            a = start + i * 3 + (i % 2) * 4
            b = start + (i + 1) * 3 + ((i + 1) % 2) * 4
            seq = [a, b, None]
            level.append(create_item(seq))

    elif level_num == 14:
        # مرحله 14 - تقریباً معمایی: الگوی پیچیده اما قابل کشف با دقت و حوصله
        for i in range(count):
            a = (start + i)**2 - i
            b = (start + i + 1)**2 - (i + 1)
            seq = [a, b, None]
            level.append(create_item(seq))

    elif level_num == 15:
        # مرحله 15 - سخت ولی منطقی: الگوی سخت ریاضی ولی بدون نیاز به فرمول خاص
        for i in range(count):
            a = (start + i) * (i + 1) + 7
            b = (start + i + 1) * (i + 2) + 7
            seq = [a, b, None]
            level.append(create_item(seq))

    else:
        # اگر عدد مرحله خارج از محدوده بود، یه سری ساده بساز
        for i in range(count):
            seq = [start + i, start + i + 1, None]
            level.append(create_item(seq))

    return level

def generate_all_levels():
    all_levels = []
    for lvl in range(1, 16):
        level = generate_level(lvl)
        all_levels.append(level)
    return all_levels

def save_to_json(data, filename="lvl.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    all_data = generate_all_levels()
    save_to_json(all_data)
    print("✅ فایل lvl.json با ۱۵۰ آیتم ساخته شد.")
