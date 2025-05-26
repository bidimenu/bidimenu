from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'bidimenu-secret-key-2024'

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/iletisim', methods=['POST'])
def iletisim():
    """İletişim formu işleme"""
    if request.method == 'POST':
        # Form verilerini al
        name = request.form.get('name')
        email = request.form.get('email')
        restaurant = request.form.get('restaurant')
        message = request.form.get('message')
        
        # Basit validasyon
        if not name or not email or not message:
            flash('Lütfen zorunlu alanları doldurun (Ad, E-posta, Mesaj).', 'error')
            return redirect(url_for('index') + '#iletisim')
        
        # Email validasyonu
        if '@' not in email or '.' not in email:
            flash('Lütfen geçerli bir e-posta adresi girin.', 'error')
            return redirect(url_for('index') + '#iletisim')
        
        try:
            # Mesajı konsola yazdır (geliştirme amaçlı)
            print("=" * 50)
            print("YENİ İLETİŞİM MESAJI")
            print("=" * 50)
            print(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
            print(f"Ad Soyad: {name}")
            print(f"E-posta: {email}")
            print(f"Restoran: {restaurant if restaurant else 'Belirtilmemiş'}")
            print(f"Mesaj: {message}")
            print("=" * 50)
            
            # İsteğe bağlı: Mesajı bir dosyaya kaydet
            log_message = f"""
                        Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
                        Ad Soyad: {name}
                        E-posta: {email}
                        Restoran: {restaurant if restaurant else 'Belirtilmemiş'}
                        Mesaj: {message}
                        {'='*50}
                        """
            
            # logs klasörü yoksa oluştur
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            # Mesajı log dosyasına ekle
            with open('logs/iletisim_mesajlari.txt', 'a', encoding='utf-8') as f:
                f.write(log_message)
            
            flash('Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.', 'success')
            
        except Exception as e:
            print(f"Hata oluştu: {e}")
            flash('Mesaj gönderilirken bir hata oluştu. Lütfen tekrar deneyin.', 'error')
        
        return redirect(url_for('index') + '#iletisim')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)