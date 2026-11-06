/* SEO optimizasyonlu Türkçe görsel kataloğu. */
window.HarikaSeoImages={"bijuteri":{"folder":"taki-ve-aksesuar","items":[["altin-renk-katmanli-tasli-kolye-seti-bej-stand.webp","Katmanlı Kolye Seti","Bej takı standında taş detaylı, ince zincirli altın renk katmanlı kolye seti."],["altin-renk-katmanli-tasli-kolye-seti-siyah-stand.webp","Altın Renk Kolyeler","Siyah takı standında taş sallantılı ve ince zincirli altın renk kolyeler."],["yesil-kordonlu-iki-kadin-saati-yilan-bileklik.webp","Yeşil Kordonlu Saatler","Krem taş üzerinde iki yeşil kordonlu kadın saati ve altın renk yılan başlı bileklik."],["altin-renk-coklu-figurlu-charm-bileklik.webp","Figürlü Charm Bileklik","Krem renk taş üzerinde tarak, ayna, bavul ve yelkenli figürlü altın renk charm bileklik."],["altin-renk-gunes-ay-figurlu-kolye.webp","Güneş ve Ay Figürlü Kolye","Bej takı standında güneş ve ay figürlü, altın renk sallantılı kolye."],["gumus-renk-gunes-ay-yildiz-figurlu-zincir-kolyeler.webp","Gümüş Renk Kolyeler","Siyah takı standında güneş, ay ve yıldız figürlü taş detaylı gümüş renk zincir kolyeler."],["bordo-kadranli-altin-renk-celik-kordonlu-kol-saati.webp","Bordo Kadranlı Saat","Açık renk taş üzerinde bordo kadranlı, taş indeksli ve altın renk metal kordonlu kadın saati."],["renkli-tas-detayli-altin-renk-zincir-bileklik.webp","Renkli Taşlı Bileklik","Açık renk taş üzerinde renkli taş detayları bulunan iri halkalı altın renk zincir bileklik."],["yesil-kordonlu-saatler-ve-yilan-basli-zincir-bileklik.webp","Saat ve Bileklik Seçkisi","İki yeşil kordonlu altın renk saat ve yılan başı motifli kalın zincir bileklik."],["bordo-kadranli-altin-renk-metal-kordonlu-saat-alternatif.webp","Bordo Kadranlı Saat Detayı","Doğal taş üzerinde koyu bordo kadranlı ve altın renk metal bilezikli kadın kol saati."]]},"kirtasiye":{"folder":"canta-ve-kirtasiye","items":[["pastel-pembe-mor-spiralli-defter-seti.webp","Pastel Spiralli Defterler","Açık renk doğal taş üzerinde dizilmiş pembe ve mor tonlarında spiralli defterler."],["pastel-renkli-spiralli-defterler-yakin-plan.webp","Spiralli Defter Detayı","Lila, mor ve pembe tonlarda kapak desenleri farklı spiralli defterlerin yakın plan görünümü."],["mor-tuy-detayli-cicekli-kalem-kutusu.webp","Mor Tüylü Kalem Kutusu","İçi kalemlerle dolu, mor tüylü ve çiçek süslemeli fermuarlı kalem kutusu."],["muggle-dragons-mavi-turuncu-cocuk-sirt-cantasi.webp","Muggle Dragons Çocuk Çantası","MUGGLE Dragons yazılı mavi, turuncu ve yeşil detaylı ejderha desenli çocuk sırt çantası."],["haki-renk-panther-yazili-gunluk-sirt-cantasi.webp","Haki Panther Sırt Çantası","Koyu yeşil arka planda Panther baskılı, ön fermuarlı cepli haki günlük sırt çantası."],["lacivert-pembe-kareli-cok-cepli-okul-cantasi.webp","Lacivert Okul Çantası","Pembe kareli cepli, şeffaf ön bölmeli ve fermuarlı lacivert okul sırt çantası."],["pastel-renk-deniz-kizi-desenli-cocuk-sirt-cantasi.webp","Deniz Kızı Desenli Çanta","Pastel tonlu pullu desenli, parlak deniz kızı kuyruğu baskılı çocuk sırt çantası."],["us-polo-siyah-gunluk-sirt-cantasi.webp","Siyah Günlük Sırt Çantası","Koyu yeşil fon önünde beyaz U.S. Polo baskılı ve fermuarlı ön cepli siyah sırt çantası."],["muggle-shine-bright-pembe-kiz-cocuk-sirt-cantasi.webp","Shine Bright Pembe Çanta","SHINE BRIGHT yazılı, holografik figürlü ve açık yeşil ponponlu pembe MUGGLE çocuk sırt çantası."]]}};
/* Harika Şeyler Dükkanı — SEO görsel eşleştirmesi.
   Görseller mevcut değilse eski sayfa olduğu gibi kalır. Ürün ve stok garantisi verilmez. */
(function(){
  "use strict";
  var match=location.pathname.match(/\/(bijuteri|kirtasiye)\/?(?:index\.html)?$/);
  if(!match)return;
  var config=window.HarikaSeoImages && window.HarikaSeoImages[match[1]];
  if(!config)return;
  var base="../assets/seo/"+config.folder+"/";
  var url=function(item){return base+item[0]};
  var images=config.items;
  var hero=document.querySelector(".hero-photo-frame img");
  if(!hero)return;
  function replaceImg(img,item){
    if(!img||!item)return;
    img.src=url(item);
    img.alt=item[2];
    img.setAttribute("decoding","async");
    img.setAttribute("width","1600");
    img.setAttribute("height","1600");
  }
  function renderGallery(){
    var discovery=document.querySelector(".discovery");
    if(!discovery || document.getElementById("urunlerden-kareler"))return;
    var section=document.createElement("section");
    section.className="seo-gallery wrap";
    section.id="urunlerden-kareler";
    section.setAttribute("aria-labelledby","seo-gallery-heading");
    var header=document.createElement("div");
    header.className="seo-gallery-heading";
    var intro=document.createElement("div");
    var eyebrow=document.createElement("span");
    eyebrow.className="eyebrow";
    eyebrow.textContent="HARİKA ŞEYLER DÜKKÂNI · DÖŞEMEALTI";
    var heading=document.createElement("h2");
    heading.id="seo-gallery-heading";
    heading.textContent=match[1]==="bijuteri"?"Takılardan birkaç kare.":"Renkli keşiflerden kareler.";
    intro.append(eyebrow,heading);
    var hint=document.createElement("p");
    hint.textContent="Diğer görseller için yana kaydır →";
    header.append(intro,hint);
    var rail=document.createElement("div");
    rail.className="seo-gallery-rail";
    rail.setAttribute("role","region");
    rail.setAttribute("aria-label","Ürün fotoğrafları, yatay kaydırılabilir");
    rail.setAttribute("tabindex","0");
    images.slice(4).forEach(function(item){
      var figure=document.createElement("figure");
      figure.className="seo-gallery-card";
      var img=document.createElement("img");
      img.src=url(item);
      img.alt=item[2];
      img.loading="lazy";
      img.decoding="async";
      img.width=1600;
      img.height=1600;
      var caption=document.createElement("figcaption");
      caption.textContent=item[1];
      figure.append(img,caption);
      rail.appendChild(figure);
    });
    var note=document.createElement("p");
    note.className="seo-gallery-note";
    note.textContent="Fotoğraflar örnek amaçlıdır. Mağazamızdaki ürünler ve stok durumu değişebilir.";
    section.append(header,rail,note);
    discovery.insertAdjacentElement("afterend",section);
  }
  /* Önce ana görseli yokla: henüz yüklenmeyen medya için mevcut tasarımı koru. */
  var probe=new Image();
  probe.onload=function(){
    if(match[1]!=="bijuteri")replaceImg(hero,images[0]);
    for(var i=0;i<3;i++){
      replaceImg(document.querySelector('.visual-layer[data-visual="'+i+'"] img'),images[i+1]);
      replaceImg(document.querySelector('.discovery-chapter[data-chapter="'+i+'"] .chapter-mobile-photo img'),images[i+1]);
    }
    var og=document.querySelector('meta[property="og:image"]');
    if(og && match[1]!=="bijuteri")og.setAttribute("content",new URL(url(images[0]),location.href).href);
    renderGallery();
  };
  probe.src=url(images[0]);
})();
