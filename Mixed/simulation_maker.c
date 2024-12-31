#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>

#define DATE 20

typedef struct Price {
    int stdout_price;
    long int volume;
    char date[DATE];
    struct Price* next; 
} Price;

Price* create_price_node(int price, long int volume, char* date) {
    Price* newNode = (Price*)malloc(sizeof(Price));
    newNode->stdout_price = price;
    newNode->volume = volume;
    strcpy(newNode->date, date);
    newNode->next = NULL; 
    return newNode;
}

char* generate_new_date(char* date) {
    int day, month, year, hour, minute;
    static char new_date[DATE];

    sscanf(date, "%d-%d-%d|%d:%d", &day, &month, &year, &hour, &minute);
    hour += 1; 

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

        if (day == 31 && month == 12) {
            day = 1;
            month = 1;
            year++;
        }
    }

    snprintf(new_date, DATE, "%02d-%02d-%04d|%02d:%02d", day, month, year, hour, minute);

    return new_date;
}

Price* generate_price(int initial_input_price, int total_case, float initial_user_probability, float initial_user_acceleration, char* user_input_date) {
    Price* head = create_price_node(initial_input_price, 0, user_input_date); 
    Price* current = head;

    float probability = 50.0 + initial_user_probability;

    for (int i = 1; i < total_case; i++) {
        int current_price = current->stdout_price;

        float random_price = (float)(rand() % 100);

        int new_price;
        if (random_price < probability) {
            new_price = (int)(current_price * (1 + initial_user_acceleration));
        } else {
            new_price = (int)(current_price * (1 - initial_user_acceleration));
        }
    
        strcpy(user_input_date, generate_new_date(user_input_date));

        Price* newNode = create_price_node(new_price, 0, user_input_date);
        current->next = newNode;
        current = newNode; 
    }

    return head;
}

int write_file_prices(Price* head, int counter) {
    char filename[50];
    sprintf(filename, "sim_%d.txt", counter);

    FILE* fp = fopen(filename, "w");
    if (fp == NULL) {
        perror("\n:::Can't write the file\n:::");
        return 0;
    }

    Price* current = head;
    int index = 0;
    while (current != NULL) {
        fprintf(fp, "Price [%d]: %d, Volume: %ld, Date: %s\n", index++, current->stdout_price, current->volume, current->date);
        current = current->next;
    }

    fclose(fp);
    return 1;
}

void free_price_list(Price* head) {
    Price* current = head;
    while (current != NULL) {
        Price* temp = current;
        current = current->next;
        free(temp);
    }
}

int main() {
    char user_input_date[DATE] = "01-01-2025|00:00";
    int total_sim = 1;
    int counter = 0;

    srand(time(NULL)); // Seed random number generator once

    for (int i = 0; i < total_sim; i++) {
        for (int j = 0; j < 2; j++) {
            char current_date[DATE];
            strcpy(current_date, user_input_date); // Use a copy of the original date
            Price* head = generate_price(80000, 3000, j, 0.009, current_date);
            write_file_prices(head, counter);
            free_price_list(head);
            counter++;
        }
    }

    return 0;
}
