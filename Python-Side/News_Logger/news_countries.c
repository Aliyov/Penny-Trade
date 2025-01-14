#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define TABLE_SIZE 1000

// Define the structure for the hash table
typedef struct HashNode {
    char* country;
    int value;  // Integer value associated with the country
    struct HashNode* next;
} HashNode;

HashNode* hashTable[TABLE_SIZE];

// Hash function to calculate index
unsigned int hash(const char* str) {
    unsigned int hashValue = 0;
    while (*str) {
        hashValue = hashValue * 31 + tolower(*str);
        str++;
    }
    return hashValue % TABLE_SIZE;
}

// Function to create a new hash node
HashNode* createNode(const char* country, int value) {
    HashNode* newNode = (HashNode*)malloc(sizeof(HashNode));
    newNode->country = strdup(country);
    newNode->value = value;
    newNode->next = NULL;
    return newNode;
}

// Function to insert a country and its associated value into the hash table
void insert(const char* country, int value) {
    unsigned int index = hash(country);
    HashNode* newNode = createNode(country, value);
    if (!hashTable[index]) {
        hashTable[index] = newNode;
    } else {
        HashNode* current = hashTable[index];
        while (current->next) {
            current = current->next;
        }
        current->next = newNode;
    }
}

// Function to check if a country exists in the hash table and get its value
int find(const char* country) {
    unsigned int index = hash(country);
    HashNode* current = hashTable[index];
    while (current) {
        if (strcmp(current->country, country) == 0) {
            return current->value;  // Return the value associated with the country
        }
        current = current->next;
    }
    return -1;  // Return -1 if country is not found
}

// Function to lowercase a string
void lowercase(char* str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

// Function to remove punctuation from a string
void removePunctuation(char* str) {
    int j = 0;
    for (int i = 0; str[i]; i++) {
        if (isalpha(str[i])) {
            str[j++] = str[i];
        }
    }
    str[j] = '\0';
}

// Function to read country names and their associated values from the file and store them in the hash table
void loadCountries(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open countries.txt");
        exit(1);
    }

    char line[200];
    while (fgets(line, sizeof(line), file)) {
        char country[150];
        int value;
        
        // Parse the line to extract the country and value
        char* token = strtok(line, "\n");
        if (token) {
            char* last_space = strrchr(token, ' ');  // Find the last space character
            if (last_space) {
                // Separate country and value
                *last_space = '\0';  // Terminate country string
                value = atoi(last_space + 1);  // Convert the last part to integer (value)
                strcpy(country, token);  // Copy the country name to 'country'
                lowercase(country);  // Convert country name to lowercase
                insert(country, value);
            }
        }
    }
    fclose(file);
}

// Function to process the news content and check for country names
void processNewsContent(FILE *ff, const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Unable to open news_content.txt");
        exit(1);
    }

    char word[100];
    int found = 0;
    while (fscanf(file, "%99s", word) != EOF) {
        // Remove punctuation and convert to lowercase
        removePunctuation(word);
        lowercase(word);

        
        // Check if the word is a country
        int value = find(word);
        if (value != -1) {
            fprintf(ff, "%s %d\n", word, value);
            found = 1;
        }
    }
    
    if (!found) {
        fprintf(ff, "NA");  // Debugging print
    }

    fclose(file);
}

int main() {
    FILE *ff = fopen("countriesCheck.txt", "w");
	if(ff == NULL) return 1;
	// Load countries and process news content
    loadCountries("countries.txt");
    processNewsContent(ff, "news_content.txt");
	
    return 0;
}

