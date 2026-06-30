# Lightweight Tor VPN

[🇬🇧 English](#english) | [🇹🇷 Türkçe](#türkçe)

---

<a name="english"></a>

## 🇬🇧 English

A lightweight, easy-to-use Tor VPN client with a graphical user interface (GUI) for Linux systems. This project provides transparent Tor proxying through a simple GUI or command-line interface.

## Features

✨ **Key Features:**
- 🎯 Transparent Tor proxy setup with a single click
- 🖥️ User-friendly GUI (system tray integration)
- 🔐 Anonymous networking through Tor network
- 💻 Command-line interface support
- 🛠️ Standalone executable (compiled with PyInstaller)
- 📝 Automatic torrc configuration and backup
- 🔄 Easy enable/disable with automatic cleanup
- 🐧 Optimized for Linux systems

## Requirements

- **OS:** Linux (Debian/Ubuntu or similar)
- **Python:** 3.8+
- **Tor:** Must be installed (`apt install tor` on Debian/Ubuntu)
- **Root Access:** Required to configure iptables and Tor
- **Dependencies:**
  - `pystray` - System tray integration
  - `Pillow` - Image processing for tray icon

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/lightweight-TOR-VPN.git
cd lightweight-TOR-VPN
```

### 2. Install Tor
```bash
sudo apt install tor
```

### 3. Install Python Dependencies
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Usage

### Option 1: GUI (Recommended)
Run the graphical interface with system tray integration:
```bash
sudo python3 gui.py
# or
sudo bash run_gui.sh
```

### Option 2: Command-Line
Start the Tor tunnel programmatically:
```bash
sudo python3 start_vpn.py
```

### Option 3: Bash Scripts
Direct bash script execution:
```bash
sudo bash bash/tor.sh      # Start Tor tunnel
sudo bash bash/undo-tor.sh # Stop Tor tunnel
```

## Building a Standalone Executable

Convert the project into a standalone executable:
```bash
bash build_linux.sh
```

The compiled binary will be available in the `build/tor-vpn/` directory.

## How It Works

1. **Tor Configuration:** Automatically configures `/etc/tor/torrc` for transparent proxying
2. **Transparent Proxy:** Sets up iptables rules to route all traffic through Tor
3. **DNS Handling:** Configures DNS through Tor on port 5353
4. **User Interface:** Provides a system tray icon to easily toggle the tunnel on/off
5. **Backup & Recovery:** Automatically backs up the original torrc configuration

### Ports Used
- **TransPort:** 9040 (transparent proxy)
- **DNSPort:** 5353 (DNS resolution through Tor)

## Configuration

The default settings can be modified in `start_vpn.py`:

```python
TORRC_PATH = "/etc/tor/torrc"
TOR_USER = "debian-tor"
TRANS_PORT = "9040"
DNS_PORT = "5353"
```

## File Structure

```
.
├── gui.py              # Main GUI application
├── start_vpn.py        # Tor tunnel initialization module
├── start-vpn.py        # Alternative entry point
├── requirements.txt    # Python dependencies
├── build_linux.sh      # Build script for PyInstaller
├── run_gui.sh          # GUI launcher script
├── tor-vpn.spec        # PyInstaller specification
├── bash/
│   ├── tor.sh          # Bash script to start tunnel
│   └── undo-tor.sh     # Bash script to stop tunnel
└── systemd/            # SystemD integration files (optional)
```

## Troubleshooting

### Issue: "Tor is not installed"
**Solution:** Install Tor with `sudo apt install tor`

### Issue: "Permission denied"
**Solution:** Run with sudo: `sudo python3 gui.py` or `sudo bash run_gui.sh`

### Issue: GUI doesn't appear
**Solution:** Check if GTK3 is installed: `apt install python3-gi gir1.2-gtk-3.0`

### Issue: Restore original Tor configuration
```bash
sudo cp /etc/tor/torrc.bak /etc/tor/torrc
sudo systemctl restart tor
```

## Important Security Notes

⚠️ **Please Note:**
- This tool routes traffic through the Tor network for anonymity
- Your ISP/network administrator can still see that you're using Tor
- Some websites may block or limit Tor users
- Always keep Tor updated for security patches
- This is not a substitute for a full VPN service in all scenarios

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and lawful purposes only. Users are responsible for their own actions when using this software. The developer assumes no liability for misuse.

---

**Maintainer:** [Your Name/Organization]  
**Last Updated:** 2024

---

<a name="türkçe"></a>

## 🇹🇷 Türkçe

Linux sistemleri için hafif ve kullanımı kolay bir Tor VPN istemcisi. Basit bir GUI veya komut satırı arayüzü aracılığıyla şeffaf Tor proxy'si sağlayan bir projedir.

## Özellikler

✨ **Ana Özellikler:**
- 🎯 Tek tıklamayla şeffaf Tor proxy kurulumu
- 🖥️ Sistem tepesi entegrasyonlu kullanıcı dostu arayüz
- 🔐 Tor ağı üzerinden anonim ağ bağlantısı
- 💻 Komut satırı arayüzü desteği
- 🛠️ Bağımsız çalıştırılabilir dosya (PyInstaller ile derlenmiş)
- 📝 Otomatik torrc yapılandırması ve yedekleme
- 🔄 Otomatik temizleme ile kolay etkinleştirme/devre dışı bırakma
- 🐧 Linux sistemleri için optimize edilmiş

## Gereksinimler

- **İşletim Sistemi:** Linux (Debian/Ubuntu veya benzeri)
- **Python:** 3.8+
- **Tor:** Kurulu olması gerekir (`apt install tor` Debian/Ubuntu'da)
- **Yönetici Erişimi:** iptables ve Tor yapılandırması için gerekli
- **Bağımlılıklar:**
  - `pystray` - Sistem tepesi entegrasyonu
  - `Pillow` - Tepsi simgesi için görüntü işleme

## Kurulum

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/kullanıcıadınız/lightweight-TOR-VPN.git
cd lightweight-TOR-VPN
```

### 2. Tor'u Kurun
```bash
sudo apt install tor
```

### 3. Python Bağımlılıklarını Kurun
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Kullanım

### Seçenek 1: GUI (Önerilen)
Sistem tepesi entegrasyonlu grafik arayüzü çalıştırın:
```bash
sudo python3 gui.py
# veya
sudo bash run_gui.sh
```

### Seçenek 2: Komut Satırı
Tor tünelini programlı olarak başlatın:
```bash
sudo python3 start_vpn.py
```

### Seçenek 3: Bash Betikleri
Doğrudan bash betiği çalıştırma:
```bash
sudo bash bash/tor.sh      # Tor tünelini başlat
sudo bash bash/undo-tor.sh # Tor tünelini durdur
```

## Bağımsız Çalıştırılabilir Derleme

Projeyi bağımsız çalıştırılabilir bir dosyaya dönüştürün:
```bash
bash build_linux.sh
```

Derlenmiş ikili dosya `build/tor-vpn/` dizininde kullanılabilir olacaktır.

## Nasıl Çalışır?

1. **Tor Yapılandırması:** `/etc/tor/torrc` dosyasını şeffaf proxy için otomatik olarak yapılandırır
2. **Şeffaf Proxy:** Tüm trafiği Tor üzerinden yönlendirecek iptables kurallarını ayarlar
3. **DNS İşleme:** DNS'yi 5353 portunda Tor üzerinden yapılandırır
4. **Kullanıcı Arayüzü:** Tüneli kolayca açıp kapatmak için sistem tepesi simgesi sağlar
5. **Yedekleme ve Kurtarma:** Orijinal torrc yapılandırmasını otomatik olarak yedekler

### Kullanılan Portlar
- **TransPort:** 9040 (şeffaf proxy)
- **DNSPort:** 5353 (Tor üzerinden DNS çözümü)

## Yapılandırma

Varsayılan ayarlar `start_vpn.py` dosyasında değiştirilebilir:

```python
TORRC_PATH = "/etc/tor/torrc"
TOR_USER = "debian-tor"
TRANS_PORT = "9040"
DNS_PORT = "5353"
```

## Dosya Yapısı

```
.
├── gui.py              # Ana GUI uygulaması
├── start_vpn.py        # Tor tüneli başlatma modülü
├── start-vpn.py        # Alternatif giriş noktası
├── requirements.txt    # Python bağımlılıkları
├── build_linux.sh      # PyInstaller derleme betiği
├── run_gui.sh          # GUI başlatıcı betiği
├── tor-vpn.spec        # PyInstaller spesifikasyonu
├── bash/
│   ├── tor.sh          # Tüneli başlatmak için Bash betiği
│   └── undo-tor.sh     # Tüneli durdurmak için Bash betiği
└── systemd/            # SystemD entegrasyon dosyaları (isteğe bağlı)
```

## Sorun Giderme

### Sorun: "Tor kurulu değil" hatası
**Çözüm:** Tor'u kurun: `sudo apt install tor`

### Sorun: "İzin reddedildi"
**Çözüm:** Sudo ile çalıştırın: `sudo python3 gui.py` veya `sudo bash run_gui.sh`

### Sorun: GUI görünmüyor
**Çözüm:** GTK3'ün kurulu olup olmadığını kontrol edin: `apt install python3-gi gir1.2-gtk-3.0`

### Sorun: Orijinal Tor yapılandırmasını geri yükleyin
```bash
sudo cp /etc/tor/torrc.bak /etc/tor/torrc
sudo systemctl restart tor
```

## Önemli Güvenlik Notları

⚠️ **Lütfen Dikkat Edin:**
- Bu araç Tor ağı üzerinden anonim olması amacıyla trafiği yönlendirir
- İSS'niz/ağ yöneticiniz yine de Tor kullandığınızı görebilir
- Bazı web siteleri Tor kullanıcılarını engelleyebilir veya sınırlayabilir
- Her zaman Tor'u güvenlik yamaları için güncelin
- Tüm senaryolarda tam bir VPN hizmetinin yerine geçmez

## Lisans

MIT Lisansı - Ayrıntılar için LICENSE dosyasına bakın

## Katkı Yapmak

Katkılar hoş karşılanır! Lütfen bir Pull Request göndermekten çekinmeyin.

## Sorumluluk Reddi

Bu araç yalnızca eğitim ve yasal amaçlar için tasarlanmıştır. Kullanıcılar bu yazılımı kullanırken kendi eylemlerinden sorumludur. Geliştirici kötüye kullanım için hiçbir sorumluluğu kabul etmez.

---

**Bakıcı:** [Adınız/Kuruluşunuz]  
**Son Güncelleme:** 2024
