# Harika Şeyler Dükkânı – Döşemealtı yerel mağaza kategorileri

Fiziksel mağaza için statik HTML/CSS/JavaScript kategori sayfaları. WooCommerce veya online sipariş sistemi değildir.

## Kategori hiyerarşisi

1. [Bijuteri & Aksesuar](./bijuteri/)
2. [Kırtasiye](./kirtasiye/)
3. [Oyuncak](./oyuncak/)
4. [Hediyelik Eşya](./hediyelik-esya/)

Her kategoride bir `index.html` bulunur. Ortak kaydırma ve bölüm animasyonları `assets/category.js` dosyasından yüklenir. **Tüm kategori stilleri, menü ve footer için tek bir CSS dosyası kullanılır:** `assets/site.css`. Hero çerçevesi ve renk paleti ortaktır. Kırtasiye görselinin odak noktası `.category-kirtasiye` seçicisiyle ayarlanır. Görseller `assets/` içindedir. Mobil kategori gezinmesi `assets/category-navigation.js` kullanır.

## Üst menü ve mobil kategori gezinmesi

Döşemealtı ana sayfası, dört kategori alt sayfası ve Harika Fikirler blogu aynı global üst menü yapısını kullanır. Logo, Döşemealtı ana sayfasına bağlantı olarak korunur.

- **Geniş ekran / masaüstü (1061 px ve üzeri):** logo solda, doğrudan dört kategori bağlantısı tam ortada (Bijuteri & Aksesuar, Kırtasiye, Oyuncak, Hediyelik Eşya), sağda ayrı `Harika Fikirler` bağlantısı ve orijinal `@_harikaseylerdukkani` Instagram simgesi/bağlantısı. Eski `Yakından bak` ve `Sık sorulanlar` bağlantıları üst menüden kaldırılmıştır.
- **Tablet ve telefon (1060 px ve altı):** logo solda, `Dört dünya` açılır menüsü, ekran dar olduğunda `Blog` olarak kısaltılan `Harika Fikirler` bağlantısı ve Instagram simgesi sağ tarafta. Açılır menüde sadece dört kategori bulunur; ayrı bir ana sayfa bağlantısı veya sabit alt kategori çubuğu yoktur.
- Instagram için yalnızca doğrulanmış profil kullanılır; doğrulanmamış sosyal ağ bağlantıları eklenmez.
- Menü kodu: kanonik HTML için `components/header.html` ve `components/footer.html`; kategori stilleri için `assets/site.css`, blog stilleri için `assets/blog.css` ve mevcut anasayfa CSS'si. `scripts/render_shared_components.py` dağıtıma hazırlanmış HTML'leri derler. `scripts/update_homepage_navigation.py` ile `scripts/update_homepage_blog.py` yalnızca anasayfadaki ilgili CSS/etkileşimleri hazırlar; Turhost'taki canlı anasayfa mevcut dosyası yedeklenerek yerinde güncellenir. Ana sayfa tasarımı, sticky hikâye animasyonları, diğer içerikler ve SEO korunur.

## Ana sayfayla ortak footer ve tipografi

Her sayfanın footer HTML yapısı tek kanonik `components/footer.html` şablonundan derleme sırasında üretilir: dört sütun, logo, Instagram, kategori bağlantıları, mağaza bağlantıları, konum, iletişim ve telif satırı. Tüm iç bağlantılar `/dosemealti/` adresine göre tanımlıdır ve kategori veya blog açılış sayfası olduğunda ilgili üst menü bağlantısı otomatik `aria-current` alır. `assets/site.css` ana sayfanın footer tasarımını ve tipografi düzenini ortak olarak uygular: başlıklarda Georgia, normal metinlerde Inter / Segoe UI / Arial. Mevcut çevrimiçi font indirme bağımlılığı eklenmedi.

## Yerel SEO ve indexleme

- Birincil kelimeler: Döşemealtı Bijuteri, Döşemealtı Kırtasiye, Döşemealtı Oyuncak, Döşemealtı Hediyelik Eşya.
- İkincil odak: Antalya'da bijuteri/kırtasiye/oyuncak/hediyelik eşya.
- Her sayfada özgün title, meta açıklama, H1, canonical, BreadcrumbList ve CollectionPage yapılandırılmış verisi var.
- Gerçek yayın alanında `robots: index, follow`, GitHub Pages önizlemesinde yinelenen sayfayı önlemek için dinamik `noindex` kullanılır.
- Her kategoride önceliklendirilmiş sekiz soru-cevap bulunur. Fiyat, stok veya hizmet konusunda doğrulanmamış garanti verilmez.
- `sitemap.xml` fiziksel mağaza anasayfasını ve dört kategori URL'sini içerir. Canlı sunucuda mevcut sitemap varsa **birleştirilmelidir**, körlemesine üzerine yazılmamalıdır.

## Yayın notu

GitHub Actions iş akışı `.github/workflows/deploy-turhost.yml` dosyasındadır. Başarılı FTPS testinden sonra `main` dalındaki kategori dosyaları için otomatik gerçek FTP yüklemesi etkinleştirildi. İstenirse **TURHOST_DEPLOY_ENABLED** değişkenini `false` yaparak gerçek yüklemeler durdurulabilir; `dry_run: true` testleri yine çalışır. `main` dalındaki kategori dosyası veya `assets/` değişiklikleri FTPS üzerinden yalnızca dört kategori klasörünü ve `assets/` klasörünü yükler; **ana sayfa index.html, README ve mevcut Turhost sitemap.xml dosyası korunur**, uzak dosya silme kapalıdır. Önce Actions üzerinden `dry_run: true` ile test et. FTP kurulum yönergeleri: [`DEPLOYMENT.md`](./DEPLOYMENT.md). Canlı sunucudaki ana sayfa kategori bağlantılarını daha sonra ayrıca güncellemek, Turhost robots ve sitemap kontrollerini yapmak gerekir.

## Harika Fikirler – blog (taslak inceleme)

- `blog/index.html`: marka çizgisinde, mobil uyumlu editoryal blog arşivi.
- Üç özgün Türkçe rehber: `blog/dogum-gunu-hediyesi-nasil-secilir/`, `blog/cocuklar-icin-oyuncak-secerken/`, `blog/kucuk-butceyle-anlamli-hediyeler/`.
- `assets/blog.css` yalnızca blog tasarımına aittir; ortak HTML `components/header.html` ve `components/footer.html` içinden üretilir. Blog ayrıca mevcut ana sayfa `style.css` dosyasını kullanır. Mevcut kategori sayfalarındaki Blog bağlantısı ürün dünyalarından ayrı tutulur.
- Blog sayfaları canonical/OG meta, uygun Article veya CollectionPage yapılandırılmış veri ve kategori iç bağlantıları içerir. Gerçek ürünlerin mevcut olduğu veya fiyatının sabit olduğu iddia edilmez.
- FTPS iş akışı artık `blog/` klasörünü de gönderir, fakat Turhost ana sayfasını ve uzaktaki `sitemap.xml` dosyasını korur. Yeni URL'leri canlı `sitemap.xml` içine güvenle **birleştir**, mevcut site haritasının üzerine yazma.
- Canlı ana sayfaya **Harika Fikirler** bağlantısı eklemek için mevcut Turhost `index.html` dosyası FTPS üzerinden indirilir, özgün logo/header/ana içerik korunur ve `scripts/update_homepage_blog.py` üst menüye (ürün dünyalarından ayrı) ve footer'a tek bağlantı ekler. Bu adım `.github/workflows/update-homepage-links.yml` içinde mevcut navigasyon yamasından **sonra** uygulanır. `main` dalına merge, otomatik canlı yükleme başlatabilir; öncesinde workflow `dry_run: true` ile denenmelidir.
- Yayından önce editoryal kontrol yap: metin, görsel-ürün uyumu, mobil görünüm, iç bağlantılar, güncel stok/kampanya iddiaları.

## Harika Fikirler tasarım eşleştirmesi

Blog ve üç makale sayfasında anasayfanın **gerçek header/footer HTML yapısı** ve `/dosemealti/style.css?v=20` stili kullanılır. Logo dosyası `/dosemealti/assets/harika-seyler-dukkani-logo.webp` değişmez. Ek `assets/blog.css` yalnızca blog editoryal bölümlerinin stillerini yönetir; sitedeki Georgia/Inter fontları, `#132F25` orman yeşili, `#faf6ed` krem ve altın tonları korunur. Dört ürün kategorisi ayrı kalır; `Harika Fikirler` menü bağlantısı dar ekranlarda erişilebilir tam adı korunarak `Blog` etiketiyle görünür. Blog, mağaza ürün stokları veya fiyatları için garanti vermez.

## Global header/footer — tek kaynak, build sırasında HTML

Header ve footer içeriği artık sadece iki dosyadan yönetilir:

- `dosemealti/components/header.html`
- `dosemealti/components/footer.html`

`scripts/render_shared_components.py` tüm kategori ve blog sayfalarına bu şablonları **yayına hazırlarken** ekler. Böylece ziyaretçiye gönderilen HTML tamdır; JavaScript ile sonradan header/footer çağrısı yapılmaz. Aktif kategori veya Harika Fikirler sayfasının `aria-current="page"` işareti otomatik oluşturulur.

Kullanılan site, bağımsız iki FTPS iş akışına sahiptir. `deploy-turhost.yml` en az sekiz alt sayfayı (4 kategori + 4 mevcut blog; yeni blog yazıları otomatik dahil) derler ve yalnızca bu klasörleri ve asset'leri yükler. `update-homepage-links.yml`, **canlı** anasayfa HTML'sini güvenli FTPS ile indirip yedekler, kategori CTA/CSS güncellemelerini uygular, ardından **aynı global header ve footer'ı** final dosyaya ekleyerek sadece anasayfayı yükler. Şablon dosyalarının değiştirilmesi iki iş akışını da tetikler. Hiçbiri Turhost'taki mevcut `sitemap.xml` dosyasını değiştirmez.

### Kontrollü yerel doğrulama

```bash
python3 -m unittest discover -s tests -p 'test_shared_components.py' -v
mkdir -p preview/dosemealti
cp -R dosemealti/bijuteri dosemealti/kirtasiye dosemealti/oyuncak dosemealti/hediyelik-esya dosemealti/blog preview/dosemealti/
python3 scripts/render_shared_components.py --site-root preview/dosemealti --min-pages 8
python3 scripts/render_shared_components.py --site-root preview/dosemealti --min-pages 8 --check
```

`.github/workflows/test-shared-components.yml` führt dieselben Tests ohne FTP bei Pull Requests aus. Vor einem Merge immer PR/Workflow prüfen. Änderungen am `main` Branch können bei aktivem `TURHOST_DEPLOY_ENABLED` die Livesite aktualisieren.

**Hinweis zur GitHub-Pages-Vorschau:** Die HTML-Quelldateien enthalten für direkte Branch-/GitHub-Pages-Ansichten weiterhin einen letzten Header/Footer-Stand als Fallback. Dieser wird beim Build vollständig durch die zwei globalen Vorlagen ersetzt. Deshalb künftig nur die beiden Dateien in `components/` bearbeiten; die freigegebenen Livesite-Dateien entstehen ausschließlich über den Build.
