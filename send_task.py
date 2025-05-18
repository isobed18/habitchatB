# send_task.py
from habit_tracker.tasks import add

# Görev gönderme
result = add.delay(4, 6)  # 4 ve 6 sayıları ile add görevini gönderiyoruz

# Görev kimliğini yazdır
print(f"Görev ID'si: {result.id}")
print(f"sonuc: {result.get(timeout=3)}")