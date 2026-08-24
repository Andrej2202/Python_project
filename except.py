class TooYoungError(Exception):
    """Исключение: покупатель слишком молод"""
    pass


def buy_alcohol(age):
    if age < 18:
        raise TooYoungError(f"Вам {age} лет. Продажа алкоголя с 18 лет!")
    
    print(f"Продажа разрешена. Вам {age} лет.")

def try_alcohol(age):
    buy_alcohol(10)

print("--- Покупатель 1 ---")
try:
    try_alcohol(20)  
except Exception as e:
    print(f"Отказ в продаже: {e}")

print("\n--- Покупатель 2 ---")
try:
    buy_alcohol(16)  
except TooYoungError as e:
    print(f"Отказ в продаже: {e}")


f1 -> f2 -> f3 -> ... -> f_n