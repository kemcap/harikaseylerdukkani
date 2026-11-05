# Harika Şeyler Dükkânı — GitHub → Turhost otomatik yayın (FTPS)

> **Durum:** İş akışı hazırlanmıştır ama varsayılan olarak kapalıdır. Turhost'a henüz hiçbir dosya yüklenmemiştir. İş akışı `.github/workflows/deploy-turhost.yml` dosyasındadır.

## 1. Turhost'ta ayrı bir FTP hesabı oluştur

Turhost müşteri paneli → **Hizmetler → Hizmet Listesi → Yönetim** → **cPanel'e Bağlan** → **FTP Hesapları**.

- Mümkünse yalnızca **`public_html/dosemealti`** klasörüne erişen yeni, ayrı bir FTP hesabı aç.
- Ana hosting / cPanel şifreni GitHub'a koyma.
- FTP hostname'in (geçerli SSL sertifikalı sunucu adresi), kullanıcı adın ve şifreni Turhost panelinden öğren.
- Hosting hesabı cPanel yerine Plesk ise dizin ve menü adları farklıdır. FTP sunucunun **explicit FTPS (FTP over TLS, TCP 21)** desteklediğini doğrula.
- Hesabı FileZilla gibi istemciyle şifreli FTPS modunda test ederek login sonrası görünen klasörün gerçekten `dosemealti` olduğuna emin ol.

## 2. GitHub Secret'larını ekle

Repository: `kemcap/harikaseylerdukkani` → **Settings → Secrets and variables → Actions → Secrets → New repository secret**.

Aşağıdaki üç **Secret** gereklidir:

| Secret adı | Değer |
| --- | --- |
| `TURHOST_FTP_HOST` | FTP sunucusunun hostname'i; **`ftp://` olmadan, port olmadan** |
| `TURHOST_FTP_USER` | Ayrı FTP hesabı kullanıcı adı |
| `TURHOST_FTP_PASSWORD` | Ayrı FTP hesabı parolası |

**Parolayı sohbete, README'ye veya git commit'ine yazma.**

## 3. GitHub Actions Variables

Aynı ekranda **Variables → New repository variable**:

| Variable adı | Değer |
| --- | --- |
| `TURHOST_REMOTE_DIR` | FTP hesabının `dosemealti` yayın klasörüne göre doğruladığın hedef yol. Sadece `public_html/dosemealti` dizinine kısıtlı hesabın kökünde `./` olabilir. Genel FTP hesabında yol farklı olabilir; tahmin etme. |
| `TURHOST_DEPLOY_ENABLED` | Hazır olduktan sonra `true` |

Bu iki değerden özellikle `TURHOST_REMOTE_DIR` hatalı verilirse dosyalar yanlış klasöre yüklenebilir. FTP hesabını yalnızca `dosemealti` dizinine kısıtlamak en güvenli çözümdür.

## 4. Önce zararsız Dry-run

GitHub → **Actions** → **Deploy Döşemealtı categories to Turhost (FTPS)** → **Run workflow**.

- Branch: `main`
- **dry_run: true**
- Çalıştır ve log'u kontrol et. Bağlantı kurulmalı; dosyalar yüklenmemeli.
- Hata varsa hostname, FTP yetkisi, sunucu sertifikası ve uzak dizini doğrula. `ssl_verify_certificate` ayarını kapatma; doğru hostname kullan.

## 5. Gerçek yayın

Aynı workflow'u yeniden çalıştır ve **dry_run: false** seç. Başarılıysa şu adresleri kontrol et:

- `https://harikaseylerdukkani.com/dosemealti/bijuteri/`
- `https://harikaseylerdukkani.com/dosemealti/kirtasiye/`
- `https://harikaseylerdukkani.com/dosemealti/oyuncak/`
- `https://harikaseylerdukkani.com/dosemealti/hediyelik-esya/`

Daha sonra `main` dalında `dosemealti/**` altında yapılan her değişiklik workflow'u otomatik başlatır (`TURHOST_DEPLOY_ENABLED=true` kaldığı sürece).

## Güvenlik ve kapsam

- FTPS/TLS zorunludur; doğrulanabilir sertifika gerekir.
- Dosya silme (`delete`) **kapalı**. Sunucuda yalnızca yüklenen isimlerle eşleşen dosyalar güncellenir.
- Hazırlık aşamasında sadece `dosemealti/assets/`, `dosemealti/bijuteri/`, `dosemealti/kirtasiye/`, `dosemealti/oyuncak/` ve `dosemealti/hediyelik-esya/` alınır.
- **Mevcut `dosemealti/index.html`, `sitemap.xml` ve diğer sunucu dosyaları upload paketinde yoktur.** Canlı ana sayfanın navigasyon bağlantıları daha sonra, onaylı kaynakla ayrıca güncellenmelidir.
- `TURHOST_DEPLOY_ENABLED=false` yaparak otomatik yayını anında durdurabilirsin.
- Turhost `public_html` yerine başka bir yayın kökü kullanıyorsa paneldeki **gerçek** dosya yolunu esas al.
