#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "simulation.h"


Price* create_price_node(int price, long int volume,char* date) {
    Price* newNode = (Price*)malloc(sizeof(Price));
    newNode->price = price;
    newNode->volume = volume;
    strcpy(newNode->date, date);
    newNode->next = NULL; 
    return newNode;
}

char* generate_new_date(char* date) {
    int day, month, year, hour, minute;
    static char new_date[DATE];

    sscanf(date, "%d-%d-%d|%d:%d", &day, &month, &year, &hour, &minute);
    hour += 4; 

    if (hour >= 24) {
        hour -= 24; 
        day++;

        if ((month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10) && day > 31) {
            day = 1;
            month++;
        } else if ((month == 4 || month == 6 || month == 9 || month == 11) && day > 30) {
            day = 1;
            month++;
        } else if (month == 2) { 
            if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) {
                if (day > 29) {
                    day = 1;
                    month++;
                }
            } else {
                if (day > 28) {
                    day = 1;
                    month++;
                }
            }
        }

        if (month > 12) {
            month = 1;
            year++;
        }
    }

    snprintf(new_date, DATE, "%02d-%02d-%04d|%02d:%02d", day, month, year, hour, minute);

    return new_date;
}




void generate_price(int initial_input_price, int total_case, float user_probability, float acceleration, char *user_input_date) {
    Price* head = create_price_node(initial_input_price, 0, user_input_date); 
    Price* current = head;
    char new_date[DATE];
    srand(time(0));
    float probability = 50.0 + user_probability;

    for (int i = 1; i < total_case; i++) {
        int current_price = current->price;

        float random_price = (float)(rand() % 100);

      
        int new_price;
        if (random_price < probability) {
            new_price = (int)(current_price * (1 + acceleration));
        } else {
            new_price = (int)(current_price * (1 - acceleration));
        }

        strcpy(user_input_date, generate_new_date(user_input_date));


        Price* newNode = create_price_node(new_price, 0, user_input_date);
        current->next = newNode;
        current = newNode; 
    }


    int answer;
    printf("\nDo you want to print simulation prices? [0-1]: ");
    scanf("%d", &answer);
    
    if (answer == 1) {
        print_simulation_prices(head, total_case);
    }

  
    current = head;
    while (current != NULL) {
        Price* temp = current;
        current = current->next;
        free(temp);
    }
}


void print_simulation_prices(Price* head, int total_case) {
    Price* current = head;
    int index = 0;
    while (current != NULL) {
        printf("Price [%d]: %d, Volume: %ld, Date: %s\n", index++, current->price, current->volume, current->date);
        current = current->next;
    }
    printf("\n");
}
