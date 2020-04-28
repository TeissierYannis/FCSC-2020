<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">FindMe</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-forensic-yellow.svg)](#)

</div>

--- 

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

Vous avez accès à un fichier find_me qui semble renfermer un secret bien gardé, qui n'existe peut-être même plus. Retrouvez son contenu !

Fichiers : <a href="">find_me</a>

Pour commencer il faut analyser le fichier.

```
binwalk find_me
```

```
 Linux EXT filesystem, blocks count: 30720, image size: 31457280, rev 1.0, ext4 filesystem data
 ```
 On se rend compte que c'est une partition.

 Essayons de la monter.

 ```
 mount find_me /mnt/findme/
 ```

 Maintenant nous avons accès au volume en allant dans /mnt/findme/
 
 Dans ce volume il y a un dossier vide, un fichier unlock_me et pass.b64

 Ces fichiers ne peuvent pas s'ouvrir à part pass.b64 qui contient 

 ```
 Retrouver les fichiers supprimés
 ```
    
 Pour récuperer les fichiers supprimés il faut utiliser [testdisk](https://www.cgsecurity.org/wiki/TestDisk_FR)

 Tout un tas de fichier ont été recuperés : part0-19

 En affichant l'interieur de chaque fichier ont peut voir des caractères.

 J'ai essayé de les ajouter bout à bout dans  l'ordre ce qui ma donné ca :

```
TWYtOVkyb01OWm5IWEtzak04cThuUlRUOHgzVWRZ
```

Etant donnée que le fichier pass.b64 contient base64 et que la chaîne de caractère ressemble beaucoup à du base64 j'ai converti la chaîne en ascci.
```
Mf-9Y2oMNZnHXKsjM8q8nRTT8x3UdY
```

Une fois la passkey récuperé, il faut déverouiller le fichier unlock_me

En analysant le fichier avec binwalk, le type de cryptage est luks.

Pour décrypter du luks, le paquet [cryptsetup](https://doc.ubuntu-fr.org/cryptsetup) nous permet de faire ca.

```
cryptsetup open unlock_me /mnt/findme/ Mf-9Y2oMNZnHXKsjM8q8nRTT8x3UdY
```

Et hop le flag apparait ! 

FCSC{750322d61518672328c856ff72fac0a80220835b9864f60451c771ce6f9aeca1}

## ⛓️ Sources <a name = "limitations"></a>

testdisk : https://www.cgsecurity.org/wiki/TestDisk_FR

cryptsetup : https://doc.ubuntu-fr.org/cryptsetup