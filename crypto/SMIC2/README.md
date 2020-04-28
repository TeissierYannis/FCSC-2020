<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">SMIC2</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)<br>
[![CTF](https://img.shields.io/badge/intro-purple.svg)](#)
[![CTF](https://img.shields.io/badge/-crypto-green.svg)](#)
[![CTF](https://img.shields.io/badge/-RSA-blue.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Résolution](#resolution)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

La sécurité du cryptosystème RSA repose sur un problème calculatoire bien connu.

On vous demande de déchiffrer le "message" chiffré c ci-dessous pour retrouver le "message" en clair m associé à partir de la clé publique (n, e).

Valeurs :

* e = 65537
* n = 632459103267572196107100983820469021721602147490918660274601
* c = 63775417045544543594281416329767355155835033510382720735973
  
Le flag est FCSC{xxxx} où xxxx est remplacé par la valeur de m en écriture décimale.

```
INDICE :
La sécurité de RSA se ramène au problème de la factorisation de n en produit de deux facteurs premiers p*q.
Vous devez factoriser n.
```

## 🥶 Résolution <a name = "resolution"></a>

La force du RSA réside dans le fait que chaque clé publique sous forme (n, e) est difficile à factoriser. Le nombre *n* est en réalité le produit de deux nombres premiers *p* et *q* (n = p * q).
Qui eux, doivent impérativement rester secret ! Vous allez me dire mais comment on resout ce problème ? Et bien *n* est ici assez petit pour pouvoir être factorisé.


Comme vous le savez si vous avez résolu [SMIC1](https://github.com/TeissierYannis/FCSC-2020/tree/master/crypto/SMIC1). Vous savez que pour chiffrer le message il faut faire : 

<h3 align="center">

m^e ≡ c (mod n)

</h3>

De manière logique, si la clé de déchiffrement est *d* et *c* le message à déchiffrer. Nous obtenons la formule suivante pour déchiffrer :

<h3 align="center">

c^d ≡ m (mod n)

</h3>

Pour trouver *m* (et donc le flag). Il nous faut donc trouver *d*. L'équation qui suit est démontrée grâce au petit théorème de Fermat et dépasse les limites de cet exercice.
Si vous voulez plus d'infos, voir les [sources](#idea). Convainquez-vous simplement de l'équation suivante :

<h3 align="center">

e*d ≡ 1 (mod φ(n))

</h3>

Vous remarquez que le modulo n'est plus *n* mais *φ(n)*. Il s'agit de [l'indication d'Euler](https://fr.wikipedia.org/wiki/Indicatrice_d%27Euler). Dans notre cas précis :

<h3 align="center">

φ(n) = (p - 1)(q - 1)

</h3>

Voilà donc pourquoi il est si important de garder *p* et *q* secrets. Car si on les trouve, on trouve *φ(n)* et par la suite on trouve *d*.

Trouvons donc comment factoriser *n* en *p* et *q*. Vous pouvez utiliser le logiciel [SageMath](www.sagemath.org) avec la fonction *factor()* ou comme moi sur http://factordb.com/ !
Ce n'est pas en réalité un calculateur mais une base de donnée de plein de factorisations déjà renseignées.

J'obtiens donc *p* et *q* (avec http://factordb.com) et je calcule *φ(n)* (avec [Wolframalpha](https://www.wolframalpha.com/input/?i=650655447295098801102272374366+*+972033825117160941379425504502))

```
p = 650655447295098801102272374367
q = 972033825117160941379425504503

φ(n) = 632459103267572196107100983818846332449189887748436962395732
```

Grâce à la propriété intrinsèque des modulos, on peut convertir l'équation _e*d ≡ 1 (mod φ(n))_ en :

<h3 align="center">

e*d + φ(n)*k = 1

</h3>

Où k est un nombre entier random. Il faut savoir que nous avons ici 2 inconnues, d et k. Mais nous savons qu'ils sont tout deux entiers.
Ce qui fait donc de cette équation, une équation diophantienne. On va donc trouver non pas une solution (d, k) mais un ensemble de solutions.
Sous Wolfram, ils les appellent des _"Examples of integer solutions"_.

Il suffit simplement de prendre une de ces solutions, par exemple avec *d* le plus petit, pour faciliter le calcul de déchiffrement et le tour est joué !

Il existe une formule sur [Wolframalpha](https://www.wolframalpha.com/input/?i=solve+65537*d+%2B+632459103267572196107100983818846332449189887748436962395732*k+%3D+1+over+the+integers), très utile pour résoudre les équations diophantiennes (en remplaçant les paramètres e et φ(n) par leur valeurs bien sûr)

<h3 align="center">

solve e*d + φ(n)*k = 1 over the integers

</h3>

Le tour est joué ! C'était long mais instructif. On obtient alors la clé de déchiffrement:

```
d = 800878107345050108835195439921605173926573074665532982471877
```

Il suffit alors de faire la même démarche que pour [SMIC1](https://github.com/TeissierYannis/FCSC-2020/tree/master/crypto/SMIC1) mais en remplaçant *m* par *c* et *e* par *d*.
Comme dans la deuxième équation citée dans ce document. Vous pouvez utiliser un widget de Wolframalpha pour les modulos : [Wolframalpha modulo](https://www.wolframalpha.com/widgets/view.jsp?id=570e7445d8bdb334c7128de82b81fc13)

Nous avons donc trouvé *m*  et avons le flag !

```
m = 563694726501963824567957403529535003815080102246078401707923
```

## ⛓️ Sources <a name = "idea"></a>

RSA : https://fr.wikipedia.org/wiki/Chiffrement_RSA<br>
FactorDB : http://factordb.com/<br>
SageMath : www.sagemath.org<br>
Indicatrice d'Euler : https://fr.wikipedia.org/wiki/Indicatrice_d%27Euler<br>
Petite théorème de Fermat : https://fr.wikipedia.org/wiki/Petit_th%C3%A9or%C3%A8me_de_Fermat