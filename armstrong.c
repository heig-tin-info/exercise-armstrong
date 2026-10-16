/**
 * armstrong: tell whether a number is an Armstrong (narcissistic) number,
 * a number equal to the sum of its digits each raised to the number of digits.
 *
 * Usage:  ./armstrong [NUMBER]   (NUMBER is read from stdin when omitted)
 * Exit:   0 if NUMBER is an Armstrong number, 1 if not, 2 on invalid input.
 */
#include <stdbool.h>
#include <stdio.h>

bool is_armstrong(int number)
{
    if (number < 0) {
        return false;
    }

    int digits = 0;
    for (int n = number; n > 0; n /= 10) {
        digits++;
    }

    // Ten nines to the tenth power overflow an int: sum in a wider type.
    long long sum = 0;
    for (int n = number; n > 0; n /= 10) {
        long long power = 1;
        for (int i = 0; i < digits; i++) {
            power *= n % 10;
        }
        sum += power;
    }
    return sum == number;
}

// The trailing " %c" matches only if something follows the integer.
static bool read_number(int argc, char *argv[], int *number)
{
    char extra;
    if (argc == 1) {
        return scanf("%d %c", number, &extra) == 1;
    }
    if (argc == 2) {
        return sscanf(argv[1], "%d %c", number, &extra) == 1;
    }
    return false;
}

int main(int argc, char *argv[])
{
    int number;
    if (!read_number(argc, argv, &number)) {
        fprintf(stderr, "usage: %s [NUMBER]\n", argv[0]);
        return 2;
    }

    bool armstrong = is_armstrong(number);
    printf("Le nombre %d %s un nombre d'Armstrong.\n", number,
           armstrong ? "est" : "n'est pas");
    return armstrong ? 0 : 1;
}
