#ifndef TACTICALX_H
#define TACTICALX_H

#define DATE 20


typedef struct {
    double cash;
    double btc;
    double buyPrice;
    double sellPrice;
    char date[20];
} Wallet;

void buy(Wallet *wallet, double price, double percent, const char *date, FILE *logFile);
void sell(Wallet *wallet, double price, double percent, const char *date, FILE *logFile);
void simulate_trading(FILE *inputFile, FILE *logFile);
void first_tactic_main();
void get_files_for_logging();
#endif 
