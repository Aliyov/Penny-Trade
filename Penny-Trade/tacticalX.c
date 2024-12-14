#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h> 
#include <dirent.h>

#include "tacticalX.h"

#define INITIAL_WALLET 200.0
#define THRESHOLD_RISE 0.10 // 10% rise threshold
#define THRESHOLD_FALL 0.05 // 5% fall threshold



void get_files_for_logging() {
    const char *directory = "../SimulationPool/";  // Initialize the directory path
    struct dirent *entry;
    DIR *dp = opendir(directory);

    if (dp == NULL) {
        perror("opendir");
        return;
    }

    printf("  Available 'SIMULATION'.txt files for applying 'Tactical' in directory '%s':\n  Output will save in 'Tactical_Logs' directory.\n", directory);
    while ((entry = readdir(dp)) != NULL) {
        // Check if the file has a .txt extension
        if (strstr(entry->d_name, ".txt") != NULL) {
            printf("-->");
            printf("%s\n", entry->d_name);
        }
    }
    printf("\n\n\n");
    closedir(dp);
}


void buy(Wallet *wallet, double price, double percent, const char *date, FILE *logFile) {
    double amountToSpend = wallet->cash * percent;
    double quantityBought = amountToSpend / price;
    
    wallet->btc += quantityBought;
    wallet->cash -= amountToSpend;
    wallet->buyPrice = price;
    strcpy(wallet->date, date);

    fprintf(logFile, "BUY: $%.2f of BTC at $%.2f on %s. Quantity: %.6f BTC\n", amountToSpend, price, wallet->date, quantityBought);
}

void sell(Wallet *wallet, double price, double percent, const char *date, FILE *logFile) {
    double amountToSell = wallet->btc * percent;
    double cashGained = amountToSell * price;
    
    wallet->btc -= amountToSell;
    wallet->cash += cashGained;
    wallet->sellPrice = price;
    fprintf(logFile, "SELL: %.6f BTC at $%.2f on %s. Cash gained: $%.2f\n", amountToSell, price, date, cashGained);
}

void simulate_trading(FILE *inputFile, FILE *logFile) {
    Wallet wallet = {INITIAL_WALLET, 0.0, 0.0, 0.0};
    char date[20];
    int price, previousPrice = 0;
    int firstBuy = 1;

    while (fscanf(inputFile, "%*s [%*d]: %d, Volume: %*d, Date: %s,", &price, date) != EOF){
        if (firstBuy) {
            // First purchase with 50% of wallet
            buy(&wallet, price, 0.5, date, logFile);
            firstBuy = 0;
            previousPrice = price;
            continue;
        }
        
        if (price > wallet.buyPrice * (1 + THRESHOLD_RISE)) {
            // Price has risen by 10% since buyPrice, sell 75%
            sell(&wallet, price, 0.75, date, logFile);
        } else if (price < wallet.sellPrice * (1 - THRESHOLD_FALL) && wallet.sellPrice > 0) {
            // Price has dropped 10% since sellPrice, buy 50% of remaining cash
            buy(&wallet, price, 0.5, date, logFile);
        } else if (price < previousPrice * (1 - THRESHOLD_FALL)) {
            // Price has dropped 5%, buy 50% of remaining cash
            buy(&wallet, price, 0.5, date, logFile);
        }

        previousPrice = price;
    }
    
    fprintf(logFile, "Final wallet: $%.2f cash, %.6f BTC\n", wallet.cash, wallet.btc);
}

void first_tactic_main() {
    char data_filename[20];
    char output_filename[20];
    char input_full_path[100];

    get_files_for_logging();

    // Define the pre-given path for input and output files
    const char *input_path = "../SimulationPool/";

    // Prompt for the input file name and build the full path
    printf("\nEnter filename which has simulation data: ");
    scanf("%s", data_filename);
    snprintf(input_full_path, sizeof(input_full_path), "%s%s", input_path, data_filename);

    // Open the input file
    FILE *inputFile = fopen(input_full_path, "r");
    if (inputFile == NULL) {  // Corrected condition
        printf("Error opening market data file: %s\n", input_full_path);
        return;
    }

    // Prompt for the output file name
    printf("\nEnter output filename: ");
    scanf("%s", output_filename);

    // Build the full path for the output file
    char full_path[100];
    snprintf(full_path, sizeof(full_path), "../Tactical_Logs/%s", output_filename);

    // Open the output file
    FILE *logFile = fopen(full_path, "w");
    if (logFile == NULL) {
        printf("Error writing log data to file: %s\n", full_path);
        fclose(inputFile);  // Close the input file before returning
        return;
    }

    // Perform the trading simulation
    simulate_trading(inputFile, logFile);

    // Close the files
    fclose(inputFile);
    fclose(logFile);

    printf("Done.\n");
    return;
}
