# Exercice : Armstrong

## Les nombres d'Armstrong

Un nombre d'Armstrong, ou nombre narcissique, est un nombre égal à la somme de ses chiffres, chacun élevé à la puissance du nombre de chiffres de ce nombre. Pour un nombre $n$ de $k$ chiffres $d_{k-1} \ldots d_1 d_0$ :

$$
n = \sum_{i=0}^{k-1} d_i^{\,k}
$$

Par exemple :

- 9 est un nombre d'Armstrong car `9 == pow(9, 1)` ;
- 10 n'est **pas** un nombre d'Armstrong car `10 != pow(1, 2) + pow(0, 2)` ;
- 153 est un nombre d'Armstrong car `153 == pow(1, 3) + pow(5, 3) + pow(3, 3)` ;
- 154 n'est **pas** un nombre d'Armstrong car `154 != pow(1, 3) + pow(5, 3) + pow(4, 3)`.

Un nombre négatif n'est jamais un nombre d'Armstrong.

## Cahier des charges

Le programme `armstrong` reçoit un nombre entier en argument. Sans argument, il le lit sur l'entrée standard (*stdin*). Il affiche le résultat sur la sortie standard et le retourne par son statut de sortie :

- `0` si le nombre est un nombre d'Armstrong ;
- `1` si le nombre n'est pas un nombre d'Armstrong ;
- `2` en cas d'erreur : l'entrée n'est pas un nombre entier, ou il y a trop d'arguments. Le programme affiche alors un message d'erreur sur la sortie d'erreur (*stderr*) et rien sur la sortie standard.

Voici le comportement attendu :

```console
$ ./armstrong 153
Le nombre 153 est un nombre d'Armstrong.
$ echo $?
0
$ ./armstrong 154
Le nombre 154 n'est pas un nombre d'Armstrong.
$ echo $?
1
$ echo 153 | ./armstrong
Le nombre 153 est un nombre d'Armstrong.
$ ./armstrong foo
usage: ./armstrong [NUMBER]
$ echo $?
2
```

Le texte affiché doit être exactement celui de l'exemple : les tests le comparent.

## Première phase : le diagramme de flux

Avant de coder, prenez une feuille de papier et dessinez le diagramme de flux de votre algorithme. Ce diagramme comportera :

- des rectangles arrondis pour le début et la fin de l'algorithme ;
- des rectangles pour les actions ;
- des losanges pour les décisions.

Cet algorithme deviendra une fonction dont le prototype est :

```c
bool is_armstrong(int number);
```

Réfléchissez aux questions suivantes : comment compter les chiffres d'un nombre ? Comment extraire le dernier chiffre d'un nombre, puis l'enlever ? La somme des puissances tient-elle toujours dans un `int` (essayez avec `2147483647`) ?

## Deuxième phase : la structure du programme

Écrivez d'abord le programme sans l'algorithme : il traite la ligne de commande et affiche le résultat, mais `is_armstrong` répond pour l'instant au hasard. Voici un point de départ, qui ne lit que l'argument :

```c
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

bool is_armstrong(int number)
{
    return rand() % 2;  // Provisoire : répond au hasard
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s [NUMBER]\n", argv[0]);
        return 2;
    }

    int number;
    if (sscanf(argv[1], "%d", &number) != 1) {
        fprintf(stderr, "usage: %s [NUMBER]\n", argv[0]);
        return 2;
    }

    if (is_armstrong(number)) {
        printf("Le nombre %d est un nombre d'Armstrong.\n", number);
        return 0;
    } else {
        printf("Le nombre %d n'est pas un nombre d'Armstrong.\n", number);
        return 1;
    }
}
```

Complétez-le pour qu'il lise le nombre sur l'entrée standard quand il n'est pas donné en argument. La fonction `scanf` lit l'entrée standard comme `sscanf` lit une chaîne ; toutes deux retournent le nombre de valeurs lues. Essayez par exemple :

```c
int main(void)
{
    int number = 0;
    int n = scanf("%d", &number);
    printf("n = %d, number = %d\n", n, number);
}
```

Ce point de départ se répète : le message d'usage est écrit deux fois, de même que les deux `printf` du résultat. Améliorez-le.

## Troisième phase : l'algorithme

Remplacez l'implémentation provisoire de `is_armstrong` par l'algorithme conçu à la première phase.

## Compiler et tester

```shell
make          # compile armstrong et libarmstrong.so
make test     # compile puis lance les tests
```

Le `Makefile` compile avec `-Werror` : une alerte du compilateur est une erreur, corrigez-la. Les tests utilisent `pytest` ; s'il n'est pas installé :

```shell
sudo apt install -y python3-pytest
```

Les tests unitaires (`tests/test_is_armstrong.py`) appellent directement votre fonction `is_armstrong` depuis `libarmstrong.so` : respectez son prototype. Les tests fonctionnels (`tests/test_cli.py`) lancent le programme comme le ferait un utilisateur.

## Évaluation

Les critères d'évaluation figurent dans [criteria.yml](criteria.yml). La réussite des tests compte pour une grande part de la note ; le reste porte sur la conception et la qualité de votre code. Ne modifiez ni `criteria.yml`, ni `README.md`, ni les tests : ces fichiers sont protégés.

Pour aller plus loin (bonus) : versionnez votre diagramme de flux dans le dépôt (photo, export [draw.io](https://draw.io) ou diagramme Mermaid), et ajoutez une option `--help`.
