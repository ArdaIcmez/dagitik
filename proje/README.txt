PROJEYI TEST ETMEK ICIN GEREKEN ADIMLAR

1- Proje ile ilgili gerekli dosyalar indirilir

2- python negotiator.py komutu ile negotiator baslatilir. Negotiator ip = "localhost" ve port = 11111 olarak baslar.
Bütün peer.py dosyasında da Negotiator un ip ve port u sabittir.

3- python peer.py <Peerip> <Peerport> komutu ile peer baslatilir. Orn: python peer.py localhost 12345

4- Resim, peer dosyasi ile acilan arayuze Load butonu ile yuklenir.

5- Filtre secildikten sonra Start butonu ile gonderme islemi baslar.

Eger herhangi bir peerın arayüz penceresini kapatırsanız, 2-3 saniye içerisinde o peera son verilir. 

Yuklediginiz resimin boyutuna gore islemin tamamlanma zamani farklilik gosterebilir.

Program calisirken, 2 tane dosya yaratir(append olarak): workerLog ve patchLog 
workerLog, Peer-Server kisminin calistirdigi worker threadlerin baslama mesajini tutar
patchLog, mesaj gonderilirken hatali mesajlarin girdisini tutar.
Eger mesaj : "Peerdan servera eksik mesaj geldi" ise Peer-Client tan Peer-Server a atilan mesajda eksiklik olmustur.
Eger mesaj : "PATNO geldi" ise Peer-Server tarafindan işlenmiş patch Peer-Client a yollanırken eksik gelmiştir, Peer-Client bu mesajı kabul
etmemiştir.

Ayrıca, terminal kısmında print edilen birçok bilgiyi bulabilirsiniz. 
