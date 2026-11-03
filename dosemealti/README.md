# Harika Şeyler Dükkânı – Döşemealtı yerel mağaza kategorileri

Fiziksel mağaza için statik HTML/CSS/JavaScript kategori sayfaları. WooCommerce veya online sipariş sistemi değildir.

## Kategori hiyerarşisi

1. [Bijuteri & Aksesuar](./bijuteri/)
2. [Kırtasiye](./kirtasiye/)
3. [Oyuncak](./oyuncak/)
4. [Hediyelik Eşya](./hediyelik-esya/)

Her kategoride `index.html`, `category.css`, `category.js` bulunur. Görseller `assets/` içinde tutulur. Ortak üst menü görünümü `assets/category-nav.css` dosyasındadır.

## Üst menü

Yayımlanan Döşemealtı ana sayfasındaki menü esas alındı: Harika Şeyler Dükkanı logosu, **Dört dünya**, **Yakından bak**, **Sık sorulanlar**, Instagram ve **Online-Mağazamız**. Kategori sayfalarında ikinci ve üçüncü bağlantı, sayfanın kendi keşif ve SSS bölümlerine gider. Koyu Hero üzerinde logo beyaz; aşağı kaydırıldıktan sonra yarı saydam açık renk menüde logo koyudur. Mobil düzen de ana sayfayı takip eder.

## Yerel SEO ve indexleme

- Birincil kelimeler: Döşemealtı Bijuteri, Döşemealtı Kırtasiye, Döşemealtı Oyuncak, Döşemealtı Hediyelik Eşya.
- İkincil odak: Antalya'da bijuteri/kırtasiye/oyuncak/hediyelik eşya.
- Her sayfada özgün title, meta açıklama, H1, canonical, BreadcrumbList ve CollectionPage yapılandırılmış verisi var.
- Gerçek yayın alanında `robots: index, follow`, GitHub Pages önizlemesinde yinelenen sayfayı önlemek için dinamik `noindex` kullanılır.
- Her kategoride önceliklendirilmiş sekiz soru-cevap bulunur. Fiyat, stok veya hizmet konusunda doğrulanmamış garanti verilmez.
- `sitemap.xml` fiziksel mağaza anasayfasını ve dört kategori URL'sini içerir. Canlı sunucuda mevcut sitemap varsa **birleştirilmelidir**, körlemesine üzerine yazılmamalıdır.

## Yayın notu

Bu GitHub deposundaki kategori dosyalarını değiştirmek Turhost üzerinde otomatik yayın yapmak **anlamına gelmez**. Ana sayfa (`/dosemealti/`) Turhost üzerindedir ve bu işlemde değiştirilmemiştir. Yayına alma sırasında ana sayfanın dört kategori bağlantısını bu yeni URL'lere yönlendirmek, Turhost'taki dosya/başlık/robots/sitemap kontrollerini yapmak gerekir.
