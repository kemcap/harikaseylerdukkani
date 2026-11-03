# Harika Şeyler Dükkanı — Döşemealtı Kategori Sayfaları

Bu dizin, fiziksel mağazaya ait statik ve Türkçe kategori alt sayfalarını içerir. WooCommerce mağazası değildir.

## Kategori sırası
1. /dosemealti/bijuteri/ — Bijuteri & Aksesuar
2. /dosemealti/kirtasiye/ — Kırtasiye
3. Oyuncak — henüz ayrı sayfa hazırlanmadı
4. Hediyelik Eşya — henüz ayrı sayfa hazırlanmadı

İlk iki kategori her birinde index.html, category.css ve category.js dosyalarını kullanır. Görseller /dosemealti/assets/ içinde yer alır.

## Yerel SEO ve indeksleme

- Birincil hedef: “Döşemealtı Bijuteri”, “Döşemealtı Kırtasiye”.
- İkincil hedef: “Antalya Bijuteri”, “Antalya Kırtasiye” (Türkçe metinde “Antalya'da bijuteri/kırtasiye” doğal biçimde geçer).
- Title, açıklama, görünen tek H1, iç metinler, canonical, Open Graph, BreadcrumbList ve CollectionPage verileri güncellendi.
- Turhost'ta yayınlandığında HTML robots meta etiketi: **index, follow, max-image-preview:large**.
- **Yalnızca** hostname `*.github.io` ise yinelenen önizleme sayfalarının dizine eklenmesini önlemek için küçük bir script robots meta'yı `noindex` yapar. Turhost üzerinde bunu yapmaz.
- /dosemealti/sitemap.xml anasayfayı ve ilk iki kategori adresini içerir. Yayında halihazırda sitemap varsa bununla **birleştirilmeli**, başka sayfalar silinmemelidir.

## Yayına alma kontrol listesi

- Mevcut Turhost /dosemealti/ ana sayfası, robots.txt, HTTP X-Robots-Tag ve mevcut sitemap kontrol edilmeli.
- Ana sayfadaki kategori bağlantıları ilk iki gerçek kategori URL'sine güncellenmeli. Bu değişiklik henüz yapılmadı.
- Yeni dosyalar Turhost'a yüklenip 200/robots/canonical/asset yolları doğrulanmalı.
- Google Search Console'da URL Denetimi ve sitemap gönderimi yapılmalı. İndeksleme garanti değildir.
- Ürünlerin görseli, çeşidi veya stoku günlük olarak doğrulanmadı; sayfalar örnek görseller ve mağaza ziyaretine davet içerir.

Henüz Turhost'a dosya yüklemesi yapılmadı; GitHub'daki bu sürüm geliştirme kaynağıdır.
