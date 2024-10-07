#ifndef SIMULATION_H
#define SIMULATION_H

#define DATE 20

typedef struct Price {
    int price;
    long int volume;
    char date[DATE];
    struct Price* next; 
} Price;

Price* create_price_node(int price, long int volume, char* date);
char* generate_new_date(char* date);
Price *generate_price(int initial_input_price, int total_case, float user_probability, float acceleration, char *user_input_date);
void print_simulation_prices(Price* head, int total_case);
int write_file_prices(struct Price *head);
void free_price_list(Price* head);

#endif 
