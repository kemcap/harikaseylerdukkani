# Harika Şeyler Dükkânı — GitHub → Turhost otomatik yayın (FTPS)

> **Durum:** Başarılı FTPS dry-run testinden sonra kategori dosyaları için otomatik yayımlama etkinleştirildi. `main` dalındaki kategori dosyaları değişince Turhost'a FTPS ile yüklenir; gerçek yüklemeleri durdurmak için GitHub Actions Variables altında `TURHOST_DEPLOY_ENABLED=false` ayarla. İş akışı `.github/workflows/deploy-turhost.yml` dosyasındadır.

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
| `TURHOST_DEPLOY_ENABLED` | İsteğe bağlı: gerçek yüklemeleri geçici durdurmak için `false`; ayarlanmadıysa otomatik yayımlama etkindir |

Özellikle `TURHOST_REMOTE_DIR` hatalı verilirse dosyalar yanlış klasöre yüklenebilir. FTP hesabını yalnızca `dosemealti` dizinine kısıtlamak en güvenli çözümdür.

## 4. Önce zararsız Dry-run (otomatik yayın kapalıyken de çalışır)

GitHub → **Actions** → **Deploy Döşemealtı categories to Turhost (FTPS)** → **Run workflow**.

- Branch: `main`
- **dry_run: true** (bu test için `TURHOST_DEPLOY_ENABLED` değerini `true` yapmana gerek yok; değişkeni boş veya `false` bırak)
- Çalıştır ve log'u kontrol et. Bağlantı kurulmalı; dosyalar yüklenmemeli.
- Hata varsa hostname, FTP yetkisi, sunucu sertifikası ve uzak dizini doğrula. `ssl_verify_certificate` ayarını kapatma; doğru hostname kullan.

## 5. Gerçek yayın

Üç FTP secret'ı, `TURHOST_REMOTE_DIR` ve başarılı dry-run testinden sonra kategori dosyalarına yapılan `main` değişiklikleri otomatik gerçek yüklemeyi başlatır. İşlem durdurulmuşsa `TURHOST_DEPLOY_ENABLED` değerini sil veya `true` olarak değiştir.

Aynı workflow'u yeniden çalıştır ve **dry_run: false** seç. Başarılıysa şu adresleri kontrol et:

- `https://harikaseylerdukkani.com/dosemealti/bijuteri/`
- `https://harikaseylerdukkani.com/dosemealti/kirtasiye/`
- `https://harikaseylerdukkani.com/dosemealti/oyuncak/`
- `https://harikaseylerdukkani.com/dosemealti/hediyelik-esya/`

Daha sonra `main` dalında `dosemealti/assets/**` veya dört kategori klasöründe yapılan değişiklikler workflow'u otomatik başlatır. `TURHOST_DEPLOY_ENABLED=false` gerçek yüklemeleri durdurur; dry-run testleri çalışabilir.

## Güvenlik ve kapsam

- FTPS/TLS zorunludur; doğrulanabilir sertifika gerekir.
- Dosya silme (`delete`) **kapalı**. Sunucuda yalnızca yüklenen isimlerle eşleşen dosyalar güncellenir.
- Hazırlık aşamasında sadece `dosemealti/assets/`, `dosemealti/bijuteri/`, `dosemealti/kirtasiye/`, `dosemealti/oyuncak/` ve `dosemealti/hediyelik-esya/` alınır.
- **Mevcut `dosemealti/index.html`, `sitemap.xml` ve diğer sunucu dosyaları upload paketinde yoktur.** Canlı ana sayfanın navigasyon bağlantıları daha sonra, onaylı kaynakla ayrıca güncellenmelidir.
- `TURHOST_DEPLOY_ENABLED=false` yaparak gelecekteki gerçek yüklemeleri durdurabilirsin.
- Turhost `public_html` yerine başka bir yayın kökü kullanıyorsa paneldeki **gerçek** dosya yolunu esas al.
