# Habit Tracker - Sosyal Alışkanlık Takip Uygulaması

Kullanıcıların alışkanlıklarını takip edebileceği, arkadaşlarıyla ilerlemelerini paylaşabileceği ve başarılar kazanabileceği sosyal bir alışkanlık takip uygulaması.

## Özellikler

- Zaman ve sayım bazlı alışkanlık takibi
- Sosyal özellikler (arkadaş sistemi, fotoğraf paylaşımı)
- Başarı ve ödül sistemi
- Özelleştirilebilir avatarlar
- Gerçek zamanlı sohbet
- Grup meydan okumaları

## Backend Kurulumu

1. Repoyu klonlayın:
```bash
git clone https://github.com/isobed18/habitchatB.git
cd habitchatB
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Ortam değişkenlerini ayarlayın:
Kök dizinde `.env` dosyası oluşturun:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

5. settings.py dosyasını oluşturun:
```bash
cp habit_tracker/settings_template.py habit_tracker/settings.py
```
Ardından `settings.py` dosyasını düzenleyin:
- Yeni bir SECRET_KEY oluşturun
- Gerekirse ALLOWED_HOSTS'u güncelleyin
- Veritabanı ayarlarınızı yapılandırın

6. Migrasyonları çalıştırın:
```bash
python manage.py migrate
```

7. Süper kullanıcı oluşturun:
```bash
python manage.py createsuperuser
```

8. Geliştirme sunucusunu başlatın:
```bash
python manage.py runserver
```

9. Celery worker'ı başlatın (ayrı bir terminal'de):
```bash
celery -A habit_tracker worker -l info
```

## Frontend Kurulumu

Bu projenin iki frontend seçeneği vardır:

1. Web Arayüzü:
Backend sunucusunu başlattıktan sonra, web arayüzüne şu adresten erişebilirsiniz:
```
http://127.0.0.1:8000/
```

2. React Native Mobil Uygulama:
Mobil uygulama için lütfen şu adresi ziyaret edin:
```
https://github.com/isobed18/habitchatF
```

## Önemli Komutlar ve Yapılandırmalar

### Sunucu Yapılandırması
- Belirli bir portta sunucuyu başlatın:
```bash
python manage.py runserver 8000
```
- WiFi ağındaki tüm IP'lere izin verin:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Celery Komutları
1. Celery Beat'i başlatın:
```bash
celery -A habit_tracker.my_celery beat --loglevel=debug --max-interval 5
```

2. Celery Worker'ı başlatın (Windows için):
```bash
celery -A habit_tracker.my_celery worker --loglevel=info --pool=solo
```

### Geliştirme Ortamı
1. Sanal Ortam:
- Komutları çalıştırmadan önce sanal ortamı aktifleştirin
- Modül bulunamadı hataları alırsanız, sanal ortamda olduğunuzdan emin olun

2. Ortam Değişkenleri:
- Kök dizinde `.env` dosyası oluşturun
- Gerekli değişkenler:
  ```
  DEBUG=True
  SECRET_KEY=your-secret-key
  DATABASE_URL=your-database-url
  REDIS_URL=redis://localhost:6379/0
  ```

### Yaygın Sorunlar ve Çözümleri
1. Veritabanı Sorunları:
- Migrasyonlar başarısız olursa:
```bash
python manage.py migrate --fake
python manage.py migrate --fake-initial
```

2. Redis Bağlantı Sorunları:
- Redis'in çalıştığından emin olun
- Redis URL'sini kontrol edin
- Redis portunu kontrol edin (varsayılan: 6379)

3. WebSocket Sorunları:
- Daphne'nin çalıştığından emin olun
- Redis bağlantısını kontrol edin
- CORS ayarlarını kontrol edin
- Routing yapılandırmasını kontrol edin 