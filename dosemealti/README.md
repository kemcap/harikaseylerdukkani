# Harika Şeyler Dükkânı – Döşemealtı yerel mağaza kategorileri

Fiziksel mağaza için statik HTML/CSS/JavaScript kategori sayfaları. WooCommerce veya online sipariş sistemi değildir.

## Kategori hiyerarşisi

1. [Bijuteri & Aksesuar](./bijuteri/)
2. [Kırtasiye](./kirtasiye/)
3. [Oyuncak](./oyuncak/)
4. [Hediyelik Eşya](./hediyelik-esya/)

Her kategoride `index.html` ve `category.js` bulunur. **Tüm kategori stilleri, menü ve footer için tek bir CSS dosyası kullanılır:** `assets/site.css`. Kategoriye özgü renk ve resim ayarları bu dosyada `.category-kirtasiye`, `.category-oyuncak` vb. seçicilerle ayrılmıştır. Görseller `assets/` içindedir. Mobil kategori gezinmesi `assets/category-navigation.js` kullanır.

## Üst menü ve mobil kategori gezinmesi

Döşemealtı canlı ana sayfasının başlık düzeni korunur: Harika Şeyler Dükkanı logosu, **Dört dünya**, **Yakından bak**, **Sık sorulanlar**, Instagram ve **Online-Mağazamız**. Kategori sayfalarında ikinci ve üçüncü bağlantı, sayfanın kendi keşif ve SSS bölümlerine gider. Koyu Hero üzerinde logo beyaz; aşağı kaydırıldıktan sonra yarı saydam açık renk menüde logo koyudur.

- **Desktop / tablet (761 px ve üzeri):** `Dört dünya` başlığı dört kategoriyi ve Döşemealtı ana sayfasını içeren bir alt menü açar. Diğer canlı ana sayfa menü öğeleri değişmez.
- **Telefon (760 px ve altı):** canlı ana sayfadaki üst menü korunur. İlk kaydırmanın ardından altta dört kategoriye ve ana sayfaya giden beş öğeli, aktif sayfayı vurgulayan sabit bir kategori gezintisi belirir; güvenli ekran alt boşluğu desteklenir.
- Kod: `assets/site.css` (üst menü, 100svh hero, mobil kategori gezinmesi, footer, tipografi) ve `assets/category-navigation.js` (menü ve kaydırma görünürlüğü).

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
