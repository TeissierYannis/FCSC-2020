<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">Revision</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)

</div>

--- 

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

La société Semper est spécialisée en archivage de documents électroniques. Afin de simplifier le travail des archivistes, un outil simple de suivi de modification a été mis en ligne. Depuis quelques temps néanmoins, cet outil dysfonctionne. Les salariés se plaignent de ne pas recevoir tous les documents et il n'est pas rare que le système plante. Le développeur de l'application pense avoir identifié l'origine du problème. Aidez-le à reproduire le bug.

Note : La taille totale des fichiers est limitée à 2Mo.

URL : http://challenges2.france-cybersecurity-challenge.fr:5003/

Pour résoudre cette exercice ont peut voir dans le script python que si il y a moins de 2 pdf alors le flag apparait.

```python
attachments = set([f1_hash, f2_hash])
# Debug debug...
if len(attachments) < 2:
    raise StoreError([f1_hash, f2_hash], self._get_flag())
```

Le script récupere la signature sha1 des deux fichiers pdf, si les deux signatures sont identiques alors il y a collision. 

L'utilisation de [PDF collider](https://alf.nu/SHA1) à été d'une grande aide, il suffit de mettre deux fichiers pdf, et nous donne des fichiers pdf avec le même sha1.

Ensuite, il suffit d'envoyer les fichiers sur l'interface web. BOUM Colision : 

```
Bravo, vous avez trouvé une collision sha1 pour le fichier "d35666a1b85c3f9794c120ca664624cb9c0c1ad5" : FCS :{8f95b0fc1a793e102a65bae9c473e9a3c2893cf083a539636b082605c40c00c1}
```


## ⛓️ Sources <a name = "limitations"></a>

PDF Collider : https://alf.nu/SHA1

Git - EmpireCTF : https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-05-12-DEF-CON-CTF-Qualifier/README.md#104-easy-pisy