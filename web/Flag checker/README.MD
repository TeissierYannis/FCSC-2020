<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">Flag Checker</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

Voici un service qui permet simplement de vérifier si le flag est correct.

URL : http://challenges2.france-cybersecurity-challenge.fr:5005/

Pour commencer on va analyser le fonctionnement du site. Donc lorsque l'on rentre un texte un message d'erreur s'affiche.

Allons voir du côté du code. (Voir index.php)

Dans l'index ont peut voir une fonction 

```js
checkFlag()
```

Cette fonction par déduction, nous permet de verifier le flag ?

Sinon, un index.js est inclu (Voir index.js)

```html
 <script src=index.js async></script>
 ```

 Allons voir son contenu...

En cherchant un peu cette ligne m'interpelle 
```js
var wasmBinaryFile = "index.wasm";
```

Tapons index.wasm dans l'URL. Il nous télécharge un fichier index.wasm (voir index.wasm)

Le wasm est un fichier WebAssembler, il faut d'abord le décrypter pour le lire.

Rendons-nous sur https://webassembly.github.io/wabt/demo/wasm2wat/ et uploadons le fichier.

(Voir index.wat)

Après avoir plus ou moins lu les lignes de ce fichier, la dernière ligne m'intèrepelle. Pour quoi une string aussi grande se balladerait dans un fichier comme ca.

```js
  (data $d0 (i32.const 1024) "E@P@x4f1g7f6ab:42`1g:f:7763133;e0e;03`6661`bee0:33fg732;b6fea44be34g0~"))
```

Tentons de mettre ce string sur [CyberChef](https://gchq.github.io/CyberChef)
Le mode magic en intensive mode nous indiques pas mal de choses.

Mais surtout....
..

...


Le flag !!!!!
```
FCSC{7e2d4e5ba971c2d9e944502008f3f830c5552caff3900ed4018a5efb77af07d3}
```






## ⛓️ Sources <a name = "limitations"></a>

Graphql : https://graphql.org/

Git - swisskyrepo : https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection
