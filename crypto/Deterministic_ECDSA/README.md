<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">Deterministic ECDSA</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-crypto-green.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Résolution](#resolution)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

On vous demande d'évaluer la sécurité d'un serveur de stockage de données en cours de développement.

Service : `nc challenges1.france-cybersecurity-challenge.fr 2000`

Fichier : <a href="https://github.com/TeissierYannis/FCSC-2020/tree/master/crypto/Deterministic_ECDSA/decdsa.py">decdsa.py</a>

❗ Il vous faudra les librairies **[fastecdsa](https://fastecdsa.readthedocs.io/en/latest/installation.html)** ainsi que **[pycryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)** pour lancer le programme ❗

## 🥶 Résolution <a name = "resolution"></a>

<h3 align="center">
Courbes elliptiques tu dis ?
</h3>

La méthode de cryptographie ECDSA est basée sur des courbes (d'où le nom Elliptic Curve Digital Signature Algorithm).

Nous pourrions nous jeter dans le problème sans s'informer de quoi s'agit-il, mais ce n'est pas une bonne idée.
Vous allez ramer pendant plusieurs jours (expérience vécue !). On va donc faire un peu de théorie avant d'y aller.

Afin de mieux vous représenter, voîci une courbe générée au hasard qui nous servira de support pour générer des points, qui, dans le programme Python est appelée `C` :

<div align="center">
  <img src="https://github.com/TeissierYannis/FCSC-2020/blob/master/crypto/Deterministic_ECDSA/img/simpleCurve.png"></img>
</div>

Cette courbe **C** est générée dans le programme comme ceci :

```python
C = Curve(
    "ANSSIFRP256v1",                                                    # name
    0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C03, # p
    0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C00, # a
    0xEE353FCA5428A9300D4ABA754A44C00FDFEC0C9AE4B1A1803075ED967B7BB73F, # b
    0xF1FD178C0B3AD58F10126DE8CE42435B53DC67E140D2BF941FFDD459C6D655E1, # q
    0xB6B3D4C356C139EB31183D4749D423958C27D2DCAF98B70164C97A2DD98F5CFF, # G.x
    0x6142E0F7C8B204911F9271F0F3ECEF8C2701C307E8E4C9E183115A1554062CFB  # G.y
)
```

Elle est composée des attributs suivants :
* name (str) : Nom donné à la courbe
* p (int) : Valeur de `p` dans une équation de courbe
* a (int) : Valeur de `a` dans une équation de courbe
* b (int) : Valeur de `b` dans une équation de courbe
* q (int) : L'ordre du point générateur `G`
* G.x (int) : Coordonnée X du point générateur `G`
* G.y (int) : Coordonnée Y du point générateur `G`

Commençons par expliquer les 3 premiers attributs. Il faut savoir qu'une courbe elliptique de ce type peut être définie grâce à l'équation dite de Weierstrass : 

<h3>
y^2 ≡ x^3 + ax + b (mod p)
</h3>

Nous retrouvons donc belle et bien nos attributs `a`, `b` et `p` ! Ces trois points définissent à eux seuls la courbe en elle-même.

Les autres attributs sont utiles dans le cadre de la cryptographie. Avant de voir l'attribut `q`, penchons-nous sur l'attribut `G`. Dans les courbes elliptiques,
la notion "d'additionner" des points n'est pas la même que dans un plan à deux dimensions. Afin de faciliter la compréhension, voici des images représentant l'addition
dans des courbes elliptiques pour que vous essayiez de comprendre de manière intuitive :

<div align="center">
  <img src="https://github.com/TeissierYannis/FCSC-2020/blob/master/crypto/Deterministic_ECDSA/img/pointsAddition.png "></img>
</div>

Il y a deux cas, prenons les exemples avec le point Q :
* Addition avec lui-même (2Q = Q + Q) :
  1. Tracer la tangente de la courbe au point Q.
  2. L'intersection de cette tangente avec la courbe C devient le point P
  3. Effectuer une symétrie axiale de l'abscisse pour trouver le point P' qui est votre point 2Q.
* Addition avec d'autres points (P + Q) :
  1. Tracer la droite QP.
  2. L'intersection de cette droite avec la courbe C devient un point que nous appellerons K.
  3. Effectuer une symétrie axiale de l'abscisse pour trouver le point K' qui est votre point P + Q.

▶ Si vous n'avez toujours pas compris l'addition, regardez cette séquence d'une vidéo de Computerphile sur le sujet => https://youtu.be/NF1pwjL9-DE?t=103.

Maintenant que vous avez compris cela, sachez que `G` est un point de cette courbe. `G` sera le point qui générera tous les autres points de cette courbe en s'additionnant à lui-même
à l'aide de la méthode vue ci-dessus. C'est en quelque sorte le point initial.

Revenons donc à l'attribut `q`. L'attribut `q` est un **nombre** qui "renvoie" le point `G` à un point sur l'abcisse (et non pas l'origine comme on pourrait le croire). Il satisfait donc l'équation :

<h3>
qG = 0
</h3>

Si vous n'avez pas compris, pas grave ! Ce n'est pas indispensable pour la suite.

Je crois que nous avons les bases de géométrie analytique qu'il nous faut pour résoudre ce CTF !
Maintenant passons à la signature électronique (DSA = Digital Signature Algorithm).

---

<h3 align="center">
La signature électronique
</h3>

ECDSA est signé par la paire `(r, s)` qui sont tout deux des entiers. Voici la fonction qui signe le message dans notre programme :

```python
def sign(C, sk, msg):
	ctx = sha256()
	ctx.update(msg.encode())
	k = int(ctx.hexdigest(), 16)

	ctx = sha512()
	ctx.update(msg.encode())
	h = int(ctx.hexdigest(), 16)

	P = k * C.G
	r = P.x
	assert r > 0, "Error: cannot sign this message."

	s = (modinv(k, C.q) * (h + sk * r)) % C.q
	assert s > 0, "Error: cannot sign this message."

	return (r, s)
```

C'est en somme assez simple. On doit créer deux nombres entiers pour cela :
* `k` : Généré à partir du hash SHA-256 du message que l'on veut signer.
* `h` : Généré à partir du hash SHA-512 du message que l'on veut signer.
* `P` : Un point de la courbe généré par le produit `kG` (voir addition)

Pour ce qui est de la signature :
* `r` : Coordonnée X du point P (ne dépend que de `k` en fait)
* `s` : Calcul de modulo avec `k`, `q`, `h`, `r` ainsi que la clé privée `sk`.

**Le couple `(r, s)` est donc la signature de notre message !**

Je n'en ai pas parlé mais la clé privée est nommée `sk` dans notre programme. Elle est secrète.
Si on la trouve, on casse la protection est on peut calculer toutes les signatures que l'on veut.

Je n'en ai pas parlé mais il existe un point, qui dans le programme est appelé `Q`. C'est en fait le point publique
de notre ECDSA. Ce point fait office de clé publique en quelque sorte. Pour ce CTF, il ne nous sera pas très utile car on veut simplement casser
ce programme et non pas envoyé des messages avec !

Il est seulement utilisé dans la fonction `verify()` qui ne vaut pas la peine d'être parcourue. Elle est complexe et ne nous servira pas.

---

<h3 align="center">
Bon, ça vient cette résolution ?
</h3>

C'était long je suis d'accord, mais ça vallait la peine de s'y attarder, vous me remercierez la prochaine fois que vous serez confronter à de l'ECDSA !

Observons tout d'abord, ce que fait le programme après l'initialisation de tous les attributs cités ci-dessus :

```python
print("What is your name?")
while True:
  username = input(">>> ")
  if "|" not in username: break

print("Here are a few user tokens:")
for i in range(4):
  uid = "{}_#{:02x}".format(username, i)
  r, s = sign(C, sk, uid)
  token = b64e("{}|{}|{}".format(uid, r, s).encode()).decode()
  print(token)
```

On voit directement qu'il nous imprime 4 token en fonction d'un username rentré au préalable. Et qu'il nous demande un "admin token" pour accéder au flag.
Par exemple si l'on rentre : "test". Le programme nous sortira :
```
dGVzdF8jMDB8ODQ0NDMxNzgyNzkyNTQwMTQ0NDc5NDM1OTk3MjU2OTM3MzI1Mzg0MjE1Njk1MjE5NjA5MDE5Nzc5OTg4NTk
0NjM4MzAzOTIxMjkzMzZ8MjMwNTU5OTU3NjUyMjQ5NzcwNTA4MzAyMTg0ODA3MzI0NTczMTQ0NTkwMzg2MjY5Mzk1NDcyMD
cwMTQ2NDkxMzA2Mjg2OTU4MzA1MA==
dGVzdF8jMDF8Mzg3MTA3MDIzMDAwMDQ2MjY4NjkzNzE5NTE5NTA1MjQwODQ3MzI5NDUzMDM5Nzg5ODEyOTcxNDM0Njk0NzA
0NDEyNzYyOTg3OTc5Njl8MTAwNjY3MTMwNTkyODkxNjA5MjUzMzM5OTkzMjg0NTU5ODE4MjEwNTk1NjQ1MDc3MzIzMTQ0Mj
k3MDg3MzAyNjI0OTI5MTU2MzE4Mzk=
dGVzdF8jMDJ8NzMxMjI1MzQ4MzE1NjkxODMxODY4MzgxMzQ5NjA0OTc4MTc1OTA2NTE2MTEzNjU0OTI0MjU5NzU0MDY5NTg
wMjMwNDU1OTU5NjQwMzN8MzgzNTU4NDMxODE2OTYwMjE1NzczMDg0NTI4NjkyODYyMDk1MDgwMjYxMzk1ODM3MjE4NjIxMz
E3NDQ1NzIyNTM2NDAyMTQ4NDU3MTg=
dGVzdF8jMDN8Njk1MDU0ODU5MzExNjA2MjAyNjg1NTY2NjExMDAxNjY1Mzc5OTAxMzEzNzM2NTExNjY0MjEzMTM0NDg5OTk
4MTY2NDQzODU3Njc1MTl8Mzk3ODA4MTIxMjExMjE1NTE0MDQ4OTg2NzgzNTYyODk2MTk2NDQxOTE5NjkxMDkzNzA1MTE4OD
E0MDU2MzcyNTg5MDU1MjAxMDU2NjM=
```

En ayant regarder un minimum le code, on voit que c'est encodé en base 64. Grâce à [CyberChef](https://gchq.github.io/CyberChef/), vous pourrez facilement retrouver le texte correspondant :

```
test_#00|84443178279254014447943599725693732538421569521960901977998859463830392129336|2305599576522497705083021848073245731445903862693954720701464913062869583050
test_#01|38710702300004626869371951950524084732945303978981297143469470441276298797969|10066713059289160925333999328455981821059564507732314429708730262492915631839
test_#02|73122534831569183186838134960497817590651611365492425975406958023045595964033|38355843181696021577308452869286209508026139583721862131744572253640214845718
test_#03|69505485931160620268556661100166537990131373651166421313448999816644385767519|39780812121121551404898678356289619644191969109370511881405637258905520105663
```

On remarque alors que les token **l'encodage en base 64 d'un string de forme "{str}|{int}|{int}".**

En se penchant plus sur le code :

```python
for i in range(4):
  uid = "{}_#{:02x}".format(username, i)
  r, s = sign(C, sk, uid)
  token = b64e("{}|{}|{}".format(uid, r, s).encode()).decode()
  print(token)
```

On remarque qu'en réalité les token sont de forme : *"{uid}|{r}|{s}"* avec les fameux `r` et `s` de la signature électronique vue ci-dessus.
Et que la fonction `sign()` a été appelée avec les paramètres suivants pour trouver `(r, s)` :
* C : C (courbe à utiliser)
* sk : sk (clé privée)
* msg : uid (message à envoyer)

Nous savons maintenant ce que nous devons envoyer. Si on regarde juste en dessous :

```python
print("Access to flag is limited to admin user.")
print("Enter admin token:")
token = input(">>> ")
token = b64d(token.encode()).decode().split('|')
if token[0] != "admin":
  print("Error: access forbidden")
  exit(1)

r, s = map(int, token[1:]) # récupère r et s du token donné
if verify(C, Q, "admin", r, s):
  flag = open("flag.txt", "r").read()
  print("Here is the stored flag: {}".format(flag))
else:
  print("Error: access forbidden")
```

L'instruction `if token[0] != "admin"` nous indique que le token a rentré doit être sous forme "admin|r|s".

Mais nous ne pouvons pas simplement rentrer admin et récupérer un token que le programme nous donne, car il rajoute un "_#00" après "admin".

Pour franchir ce premier if, il faut donc remplacer l'uid par "admin".

Le deuxième, `if verify(C, Q, "admin", r, s):` vérifie simplement que c'est la bonne signature de "admin". La faille n'est pas ici.

Il faut donc impérativement trouver le signature `(r, s)` assigné au message "admin" pour trouver le flag.

---

<h3 align="center">
Faille de l'implémentation
</h3>

Comme vous l'imaginez, il va nous falloir trouver le couple `(r, s)` pour pénétrer dans la base de donnée.

Comme vous l'imaginez aussi, il va falloir trouver la clé privée `sk` qui apparaît dans la fonction `sign()`.

*PS : `sk` n'est pas calculable en faisant `Q / C.G` pour les petits malins. La division n'est pas définie pour les points d'une ellipse 😉*

L'endroit où `sk` apparaît est dans l'équation pour trouver `s` :

```
s = (modinv(k, C.q) * (h + sk * r)) % C.q
```

Or, il nous manque certaines valeurs en local dans cette équation : `k`, `h` (et `sk`)

En réalité, pas vraiment 😈

Nous remarquons qu'en réalité, `k` et `h` sont entièrement calculables.
Car `k` est égal au hash SHA-256 de notre uid. Et nous pouvons, par extension, calculer également la valeur `h` (hash SHA-512).

Reprenons un token demandé précédemment :

```
test_#01|38710702300004626869371951950524084732945303978981297143469470441276298797969|10066713059289160925333999328455981821059564507732314429708730262492915631839
```

L'uid = "test_#01". Faisons un peu de python en console pour trouver son `k` et son `h` correspondant :

```python
>>> from hashlib import sha256
>>> ctx = sha256()
>>> ctx.update("test_#01".encode())
>>> k = int(ctx.hexdigest(), 16)
>>> k
70733819118195826681301792940683243052880016025243997154863438540652504449380
>>> ctx = sha512()
>>> ctx.update("test_#01".encode())
>>> h = int(ctx.hexdigest(), 16)
>>> h
1544461881294758573948802975326216816261488143147200983446003882855751099271603629121642960225347476612356698727897238006014871528157491774548977039638779
```

Magnifique ! Voici un petit tableau récapitulatif de ce que nous avons actuellement :

*PS : `q` est égal à la valeur décimal de l'hexadécimal de `C.q` dans la déclaration de la courbe.*


| Lettre | Valeur                                                                                                                                                     |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| r      | 38710702300004626869371951950524084732945303978981297143469470441276298797969                                                                              |
| s      | 10066713059289160925333999328455981821059564507732314429708730262492915631839                                                                              |
| q      | 109454571331697278617670725030735128146004546811402412653072203207726079563233                                                                             |
| k      | 70733819118195826681301792940683243052880016025243997154863438540652504449380                                                                              |
| h      | 1544461881294758573948802975326216816261488143147200983446003882855751099271603629121642960225347476612356698727897238006014871528157491774548977039638779 |

Pour les calculs qui suivent, je vous conseille d'utiliser [Wolframalpha](https://www.wolframalpha.com/). Si certains calculs sont trop grand pour Wolframalpha, utiliser le logiciel [SageMath](http://www.sagemath.org/download.html)
Notamment pour calculer des modulos avec de grands nombres.

Reprenons notre équation et faisons un peu d'algèbre pour isoler `sk`.
Attention, il faut savoir gérer les modulos. Je ne vais pas vous apprendre ça ici, je vous inviter à vous informer comment résoudre une équation linéaire avec des modulos.

Voici les étapes de résolution :

```
s = (modinv(k, C.q) * (h + sk * r)) % C.q
# modinv(k, C.q) est l'inverse modulaire, on peut donc le supprimer et mettre k de l'autre côté
s * k = (h + sk * r) % C.q
s * k - sk * r = h % C.q
sk * r = (s * k - h) % C.q
sk = modinv(r, C.q) * ((s * k - h) % C.q)
```

Faites les étapes de calcul petit à petit pour ne pas vous trompez.

Vous trouvez enfin la clé privée sk
```
sk = 54989754048227462611102989128045902162485610361467521385775315607843320555920791685002430018879566596375253771775903449820104290331781361533849382269525
```

Changez donc la valeur de `sk` dont vous n'avez pas accès en local.

N'oubliez pas d'enlever l'extension "_#00" dans la boucle for qui transforme votre message et pourra tout casser.

Rentrer ensuite "admin" comme username dans votre script Python.

▶ Si vous n'êtes pas sûr, j'ai mis à disposition le code modifié => [modifiedCode.py](https://github.com/TeissierYannis/FCSC-2020/blob/master/crypto/Deterministic_ECDSA/modifiedCode.py)

Récupérer le token et le tour est joué !

```zsh
hugo@kali:~/Desktop$ python3 ./decdsa.py
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
=-= ECC-Based Secure Flag Storage =-=
=-=      (under development)      =-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Public Point Q:
  Q.x: 0x40276f768df2ee9c83d935f10036734ea50c235b2c5c48295e498776ec02c4b6
  Q.y: 0xd3e076127e072d8a5743828683a9d16ee12c9d8d3c6782a37c2fbda11fd77d81
What is your name?
>>> admin
Here are a few user tokens:
YWRtaW58ODI1NjM5Mzg3NzA1ODAxMzA2MDA3OTA3NzQ1MjQyMzM1Mjc5MDIwMjYwMzI2MDc1O
TQyODQ3MjIwNjM5MDI2OTkwNjY5OTY4NTk2NDV8ODAwNjkyMDYzMjg5NDk1Mjk1MTg2MjA1NT
g0MTQ4NzI5NDQ1Mjg1Mjk3NDQ5MTY1MTczNjAzMDk5MjQ1ODMwNDczNjg1ODkzNTI2MTQ=
```

Connectez-vous ensuite au service :

```zsh
hugo@kali:~/Desktop$ nc challenges1.france-cybersecurity-challenge.fr 2000
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
=-= ECC-Based Secure Flag Storage =-=
=-=      (under development)      =-=
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
Public Point Q:
  Q.x: 0x40276f768df2ee9c83d935f10036734ea50c235b2c5c48295e498776ec02c4b6
  Q.y: 0xd3e076127e072d8a5743828683a9d16ee12c9d8d3c6782a37c2fbda11fd77d81
What is your name?
>>> rien
Here are a few user tokens:
cmllbl8jMDB8NDAyMjE5MjY5ODUxNjE0NDU2ODk0MTIwMjI5Njk0MTk5MDM0MzE4MjkwNzM3NDM3NDI3Mzc5NzMwODMxOTA3MjgyOTA1NzE0OTM4MTh8Mjg0NjM3OTc2NzQ3MDcyMjc3MTMxMzg5MjQ4NzI0NDY0MDMxNjIxMDU2OTM5NjM2NjQ1Nzk4Mjc4MDgxMzYyMjU3MDQxNDI4ODA5MjU=
cmllbl8jMDF8MzU1NDMzMjc0OTAzMzQwNTU4NTE0MjU1MzM3MDMxMTg5NTAyNzI2OTQzMTQxNDY5NzY0ODUzMjc2MDI3NTQ0NzE2Mjk4NzEwMDA5NjZ8MjM3Mzk1MDM3MzQwNDAxOTg1MTY5ODg4NzM5ODQ3NzMzNTU1OTAzNDM3OTg1OTMyNjkwMzEyMzU5NjA4NDM5NTQ3Nzc3MTY2Mjg4ODM=
cmllbl8jMDJ8NzY3OTMwMDk2Nzk2MTUyMDgzNzMwNzkyMzg5ODM4MDMxMzEwODExOTYyNjI3Njk1NjY2ODUyNDkwMTcyNjM1NzcyNjUwMDczMzZ8MTA0MzM3NTYxODY5NDQxMzAyNTk1ODAwNzQ1NDAzMzYxODY4NzA5NjE0ODIxNDIwNDE1Mzg1NDkxOTQ4MjIyODU5NTI0MjQzMjkyMTc0
cmllbl8jMDN8NDEyMDY5OTkwNDU2MDM0Mzc0NzgxMTEyOTkzMTU4NTAyMjY3OTM1Njg5ODA1NjkzOTk1NzQ0NjgyNTczMTU1NDk4NDc4NzA1MDAwNjV8NDMzMDMzNjkzMDcyMjE3MjM5MDAyNzA2MzM5ODY5NTkwMTQxNzc3NzUwNzI5OTI5MzQ4ODQyNDI0MzIxNDA1OTk5OTg2MjQ3MzcxNQ==
Access to flag is limited to admin user.
Enter admin token:
>>> YWRtaW58ODI1NjM5Mzg3NzA1ODAxMzA2MDA3OTA3NzQ1MjQyMzM1Mjc5MDIwMjYwMzI2MDc1OTQyODQ3MjIwNjM5MDI2OTkwNjY5OTY4NTk2NDV8ODAwNjkyMDYzMjg5NDk1Mjk1MTg2MjA1NTg0MTQ4NzI5NDQ1Mjg1Mjk3NDQ5MTY1MTczNjAzMDk5MjQ1ODMwNDczNjg1ODkzNTI2MTQ=
Here is the stored flag: FCSC{2d6d125887b96c90cc3e4243b5d2ed13e0f18caccf117cb923ebf3d1f327c036}
```

## ⛓️ Sources <a name = "idea"></a>

Courbe elliptique (FR) : https://fr.wikipedia.org/wiki/Courbe_elliptique<br>
Courbe elliptique (EN) : https://en.wikipedia.org/wiki/Elliptic_curve<br>
ECDSA (FR) : https://fr.wikipedia.org/wiki/Elliptic_curve_digital_signature_algorithm<br>
ECDSA (EN) : https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm<br>
RFC 6979 : https://tools.ietf.org/html/rfc6979<br>
Computerphile (YT) "Elliptic Curves" : https://www.youtube.com/watch?v=NF1pwjL9-DE<br>
GitHub de fastecdsa : https://github.com/AntonKueltz/fastecdsa<br>
CyberChef : https://gchq.github.io/CyberChef/<br>
Le programme Python modifié : [modifiedCode.py](https://github.com/TeissierYannis/FCSC-2020/blob/master/crypto/Deterministic_ECDSA/modifiedCode.py)