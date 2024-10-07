#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "simulation.h"

void loadLogo(){
    char ch;
    int logoCantLoad=1;

    for(int i=0; i<60;i++){
        printf("\n");
    }

    FILE *fp = fopen("./Logos/tradeLogo.txt", "r");
    if(fp == NULL){
        printf("\n:::LOGO CANT LOAD:::\n:::NO PROBLEM YOU CAN USE IT ANYWAYS:::\n");
        logoCantLoad=0;
    }

    if(logoCantLoad == 1){
        while(fscanf(fp, "%c", &ch)!= EOF){
        printf("%c",ch);
        }
        printf("\n");
    }
}

void simulation_logo(){
    char ch;
    int logoCantLoad=1;
    for(int i=0; i<60;i++){
        printf("\n");
    }
    FILE *fp = fopen("./Logos/simulation_logo.txt", "r");
    if(fp == NULL){
        printf("\n:::LOGO CANT LOAD:::\n:::NO PROBLEM YOU CAN USE IT ANYWAYS:::\n");
        logoCantLoad=0;
    }

    if(logoCantLoad == 1){
        while(fscanf(fp, "%c", &ch)!= EOF){
        printf("%c",ch);
        }
        printf("\n");
    }
}

void menu_sleep(int seconds) {
    clock_t start_time = clock();
    while ((clock() - start_time) < seconds * CLOCKS_PER_SEC);
}

void simulation_menu(){
    int price, total_case;
    float user_probability, acceleration;
    char  user_date[DATE];

    simulation_logo();

    printf("\nEnter initial price: ");
    scanf("%d", &price);

    printf("Enter total simulation cases: ");
    scanf("%d", &total_case);

    printf("Enter probability of increase: ");
    scanf("%f", &user_probability);

    printf("Enter acceleration factor (percentage, e.g., 0.03 for 3%%): ");
    scanf("%f", &acceleration);

    printf("Enter start date (01-01-2024|08:00): ");
    scanf("%s", user_date);

    printf("\nAll set! ^_^");

    Price *head_list = generate_price(price, total_case, user_probability, acceleration, user_date);

    int answer;
    printf("\n\nWhere do you want to print simulation prices?\nConsole [1]\nFile[2]\n\nChoice o_O: ");
    scanf("%d", &answer);
    if (answer == 1) {
        print_simulation_prices(head_list, total_case);
    } else if(answer == 2) {
        int output_wfp = write_file_prices(head_list);
        if(output_wfp != 1){
            printf("\nCan't write the file.... >_<");
        }else{
            printf("Simulation successfully written to the file. ^_^\nReturning to the menu.");
        }
    }

    free_price_list(head_list);
    menu_sleep(5);
}

void menu(){
    int choice=0;
    do{
        loadLogo();
        printf("\t:Menu:\n1. Simulation [1]\n2. Configuration [2]\n3. Exit [3]\n\nChoice: ");
        scanf("%d", &choice);

        if(choice == 1){
            simulation_menu();
        }

    }while(choice != 3);
}
