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

**Maintainer:** [Bekir Alişoğlu/alisoglu@yahoo.com]  
**Last Updated:** 30.06.2026

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



## Lisans

MIT Lisansı - Ayrıntılar için LICENSE dosyasına bakın

## Katkı Yapmak

Katkılar hoş karşılanır! Lütfen bir Pull Request göndermekten çekinmeyin.

## Sorumluluk Reddi

Bu araç yalnızca eğitim ve yasal amaçlar için tasarlanmıştır. Kullanıcılar bu yazılımı kullanırken kendi eylemlerinden sorumludur. Geliştirici kötüye kullanım için hiçbir sorumluluğu kabul etmez.

---

**Bakıcı:** [Bekir Alişoğlu/alisoglu@yahoo.com]  
**Son Güncelleme:** 30.06.2026
