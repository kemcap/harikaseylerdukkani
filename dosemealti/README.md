# Harika Şeyler Dükkânı – Döşemealtı yerel mağaza kategorileri

Fiziksel mağaza için statik HTML/CSS/JavaScript kategori sayfaları. WooCommerce veya online sipariş sistemi değildir.

## Kategori hiyerarşisi

1. [Bijuteri & Aksesuar](./bijuteri/)
2. [Kırtasiye](./kirtasiye/)
3. [Oyuncak](./oyuncak/)
4. [Hediyelik Eşya](./hediyelik-esya/)

Her kategoride bir `index.html` bulunur. Ortak kaydırma ve bölüm animasyonları `assets/category.js` dosyasından yüklenir. **Tüm kategori stilleri, menü ve footer için tek bir CSS dosyası kullanılır:** `assets/site.css`. Hero çerçevesi ve renk paleti ortaktır. Kırtasiye görselinin odak noktası `.category-kirtasiye` seçicisiyle ayarlanır. Görseller `assets/` içindedir. Mobil kategori gezinmesi `assets/category-navigation.js` kullanır.

## Üst menü ve mobil kategori gezinmesi

Döşemealtı ana sayfası ve dört kategori alt sayfası aynı üst menü yapısını kullanır. Logo, Döşemealtı ana sayfasına bağlantı olarak korunur.

- **Geniş ekran / masaüstü (1061 px ve üzeri):** logo solda, doğrudan dört kategori bağlantısı tam ortada (Bijuteri & Aksesuar, Kırtasiye, Oyuncak, Hediyelik Eşya), sağda orijinal `@_harikaseylerdukkani` Instagram simgesi ve bağlantısı. Eski `Yakından bak` ve `Sık sorulanlar` bağlantıları üst menüden kaldırılmıştır.
- **Tablet ve telefon (1060 px ve altı):** logo solda, `Dört dünya` adlı açılır menü ve Instagram simgesi sağ tarafta. Açılır menüde sadece dört kategori bulunur; ayrı bir ana sayfa bağlantısı veya sabit alt kategori çubuğu yoktur.
- Instagram için yalnızca doğrulanmış profil kullanılır; doğrulanmamış sosyal ağ bağlantıları eklenmez.
- Menü kodu: `assets/site.css` ve `assets/category-navigation.js` (kategori sayfaları); `scripts/update_homepage_navigation.py` ve `.github/workflows/update-homepage-links.yml` (Turhost'taki canlı ana sayfanın mevcut dosyasını yedekleyip yerinde güncelleme). Ana sayfa tasarımı, sticky hikâye animasyonları, diğer içerikler ve SEO korunur.

## Ana sayfayla ortak footer ve tipografi

Alt kategori sayfalarının footer HTML yapısı, yayımdaki Döşemealtı ana sayfası için kullanılan `sticky-discovery/index.html` kaynak footer'ından doğrudan alınmıştır: dört sütun, logo, Instagram, kategori bağlantıları, mağaza bağlantıları, konum, iletişim ve telif satırı. Sadece kategori bağlantıları alt sayfalara ve iç bağlantılar uygun hedefe uyarlanmıştır. `assets/site.css` ana sayfanın footer tasarımını ve tipografi düzenini ortak olarak uygular: başlıklarda Georgia, normal metinlerde Inter / Segoe UI / Arial. Mevcut çevrimiçi font indirme bağımlılığı eklenmedi.

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
- `assets/blog.css` yalnızca blog tasarımına aittir; ortak üst menü ve footer `assets/site.css` üzerinden gelir. Mevcut kategori sayfalarındaki Blog bağlantısı ürün dünyalarından ayrı tutulur.
- Blog sayfaları canonical/OG meta, uygun Article veya CollectionPage yapılandırılmış veri ve kategori iç bağlantıları içerir. Gerçek ürünlerin mevcut olduğu veya fiyatının sabit olduğu iddia edilmez.
- FTPS iş akışı artık `blog/` klasörünü de gönderir, fakat Turhost ana sayfasını ve uzaktaki `sitemap.xml` dosyasını korur. Yeni URL'leri canlı `sitemap.xml` içine güvenle **birleştir**, mevcut site haritasının üzerine yazma.
- Canlı ana sayfa navigasyonuna blog bağlantısı eklemek için Turhost'taki ana sayfa şablonunu ayrıca kontrollü şekilde güncelle. Ana sayfaya bu daldaki değişikliklerle otomatik müdahale edilmez.
- Yayından önce editoryal kontrol yap: metin, görsel-ürün uyumu, mobil görünüm, iç bağlantılar, güncel stok/kampanya iddiaları.
