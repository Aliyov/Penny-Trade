#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "tacticalX.h"

#define INITIAL_WALLET 200.0
#define THRESHOLD_RISE 0.10 // 10% rise threshold
#define THRESHOLD_FALL 0.05 // 5% fall threshold


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

void first_tactic_main(){

    char data_filename[20];
    char output_filename[20];

    printf("\nEnter filename which has simulation data: ");
    scanf("%s", data_filename);
    FILE *inputFile = fopen(data_filename, "r");
    if (inputFile == NULL) {
        printf("Error opening market data file.\n");
        return;
    }

    printf("\nEnter output filename: ");
    scanf("%s", output_filename);
    FILE *logFile = fopen(output_filename, "w");    

    if(logFile == NULL){
        printf("Error writing log data.\n");
        return;
    }

    simulate_trading(inputFile, logFile);

    fclose(inputFile);
    fclose(logFile);

    printf("Done");
    return;
}

