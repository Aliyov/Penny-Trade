#include <stdio.h>
#include <stdlib.h>
#include "simulation.h"

#define DATE 20
int main() {
    int price, total_case;
    float user_probability, accelaration;
    char  user_date[DATE];

    printf("Enter initial price: ");
    scanf("%d", &price);

    printf("Enter total simulation cases: ");
    scanf("%d", &total_case);

    printf("Enter probability of increase: ");
    scanf("%f", &user_probability);

    printf("Enter acceleration factor (percentage, e.g., 0.03 for 3%%): ");
    scanf("%f", &accelaration);

    printf("Enter start date (01-01-2024|08:00): ");
    scanf("%s", user_date);
    struct Price *head = generate_price(price, total_case, user_probability, accelaration, user_date);
	

    return 0;
}

