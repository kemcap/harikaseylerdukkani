# Harika Şeyler Dükkânı – Hero Prototipi

Bu klasör GitHub Pages için hazırlandı.

## İçerik

- `index.html` – ana sayfa
- `assets/placeholder-gift.png`
- `assets/placeholder-stationery.png`
- `assets/placeholder-jewelry.png`
- `.nojekyll` – GitHub Pages'in dosyaları doğrudan yayınlaması için
- `.gitignore`

## GitHub'a yükleme

1. GitHub'da yeni bir repository oluştur.
2. Bu ZIP dosyasının içeriğini repository'nin **ana dizinine** yükle.
3. `index.html` dosyasının repository'nin kökünde olduğundan emin ol.
4. Commit et.

## GitHub Pages ile yayınlama

Repository içinde:

**Settings → Pages**

Ardından:

- **Source:** `Deploy from a branch`
- **Branch:** `main`
- **Folder:** `/ (root)`
- **Save**

GitHub kısa süre sonra sana bir Pages adresi verir.

Örnek:
`https://KULLANICI-ADI.github.io/REPOSITORY-ADI/`

Site içindeki asset yolları göreceli (`assets/...`) olduğu için proje repository adı altında da çalışır.

## Not

Bu paket statik HTML/CSS/JavaScript'tir. Build işlemi, npm, Node.js veya sunucu gerektirmez.
