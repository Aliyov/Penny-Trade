#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define TABLE_SIZE 500
#define MAX_LINE_LENGTH 1024
#define COUNTRY_TABLE_SIZE 196
// Structure to hold a word and its corresponding weight and flag
typedef struct Words {
    char *word;
    int weight;
    int flag;
} Words;

// Hash table structure
typedef struct HashTable {
    Words **table;  // Array of pointers to Words structure
    int size;
} HashTable;

// Set structure to track processed words
typedef struct Set {
    char **words;
    int size;
    int capacity;
} Set;

typedef struct country{
    char **country;
}country;

// Simple hash function to hash a word
unsigned int hash(const char *word, int size) {
    unsigned int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++) {
        hash_value = hash_value * 31 + word[i];
    }
    return hash_value % size;
}

// Convert a string to lowercase
void toLowerCase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower((unsigned char)str[i]);
    }
}

// Function to create a hash table
HashTable *createHashTable(int size) {
    HashTable *new_table = (HashTable *)malloc(sizeof(HashTable));
    if (new_table == NULL) {
        printf("Error allocating memory for hash table\n");
        return NULL;
    }
    new_table->table = (Words **)malloc(size * sizeof(Words *));
    if (new_table->table == NULL) {
        printf("Error allocating memory for hash table entries\n");
        free(new_table);
        return NULL;
    }
    for (int i = 0; i < size; i++) {
        new_table->table[i] = NULL;  // Initialize all buckets as empty
    }
    new_table->size = size;
    return new_table;
}

// Function to create a set for tracking processed words
Set *createSet(int capacity) {
    Set *new_set = (Set *)malloc(sizeof(Set));
    if (new_set == NULL) {
        printf("Error allocating memory for set\n");
        return NULL;
    }
    new_set->words = (char **)malloc(capacity * sizeof(char *));
    if (new_set->words == NULL) {
        printf("Error allocating memory for set words\n");
        free(new_set);
        return NULL;
    }
    new_set->size = 0;
    new_set->capacity = capacity;
    return new_set;
}

// Function to add a word to the set
bool addToSet(Set *set, const char *word) {
    // Check if the word is already in the set
    for (int i = 0; i < set->size; i++) {
        if (strcmp(set->words[i], word) == 0) {
            return false;  // Word already processed
        }
    }

    // If the set is full, expand its capacity
    if (set->size >= set->capacity) {
        set->capacity *= 2;
        char **new_words = realloc(set->words, set->capacity * sizeof(char *));
        if (new_words == NULL) {
            printf("Error reallocating memory for set\n");
            return false;
        }
        set->words = new_words;
    }

    // Add the word to the set
    set->words[set->size] = strdup(word);
    set->size++;
    return true;
}

// Function to insert a word into the hash table using linear probing
void insert(HashTable *hash_table, const char *word, int weight, int flag) {
    unsigned int index = hash(word, hash_table->size);

    // Linear probing: Find next available slot
    while (hash_table->table[index] != NULL) {
        if (strcmp(hash_table->table[index]->word, word) == 0) {
            // Word already exists, update the weight and flag
            hash_table->table[index]->weight = weight;
            hash_table->table[index]->flag = flag;
            return;
        }
        index = (index + 1) % hash_table->size;  // Move to next slot
    }

    // Insert the new word
    Words *new_word = (Words *)malloc(sizeof(Words));
    if (new_word == NULL) {
        printf("Error allocating memory for new word\n");
        return;
    }
    new_word->word = strdup(word);
    if (new_word->word == NULL) {
        printf("Error allocating memory for word string\n");
        free(new_word);
        return;
    }
    new_word->weight = weight;
    new_word->flag = flag;
    hash_table->table[index] = new_word;
}

// Function to search for a word in the hash table
Words *search(HashTable *hash_table, const char *word) {
    unsigned int index = hash(word, hash_table->size);

    // Linear probing: Search for the word
    while (hash_table->table[index] != NULL) {
        if (strcmp(hash_table->table[index]->word, word) == 0) {
            return hash_table->table[index];  // Return the word structure
        }
        index = (index + 1) % hash_table->size;  // Move to next slot
    }

    return NULL;  // Word not found
}

// Function to read the dictionary file and populate the hash table
void readFileAndInsert(FILE *dp, HashTable *hash_table) {
    if (dp == NULL) {
        printf("Error: File cannot be opened.\n");
        return;
    }

    char buffer[MAX_LINE_LENGTH];
    int weight, flag = 0;

    // Read the file line by line
    while (fgets(buffer, MAX_LINE_LENGTH, dp) != NULL) {
        // Remove trailing newline, if any
        buffer[strcspn(buffer, "\n")] = '\0';

        // Extract the word and integers
        char word[MAX_LINE_LENGTH];
        int items_read = sscanf(buffer, "%s %d %d", word, &weight, &flag);

        // Handle cases based on the number of items read
        if (items_read == 2) {
            flag = 0;  // Default flag to 0 if not specified
        } else if (items_read < 2) {
            continue;  // Skip invalid lines
        }

        // Convert the word to lowercase
        toLowerCase(word);

        // Insert into the hash table
        insert(hash_table, word, weight, flag);
    }
}

// Function to read the news content file and sum the weights of words found in the hash table
int sumWeightsAndFlagsFromFile(FILE *dp, HashTable *hash_table, Set *processed_set) {
    if (dp == NULL) {
        printf("Error: File cannot be opened.\n");
        return -1;
    }

    char buffer[MAX_LINE_LENGTH];
    int total_weight = 0;
    int total_flag = 0;

    // Read the news content file line by line
    while (fgets(buffer, MAX_LINE_LENGTH, dp) != NULL) {
        char *word = strtok(buffer, " ,.-!?"); // Tokenize the string to extract words

        // For each word in the line, hash and search in the hash table
        while (word != NULL) {
            // Convert the word to lowercase
            toLowerCase(word);

            // Process the word only if it is successfully added to the set
            if (addToSet(processed_set, word)) {
                Words *found_word = search(hash_table, word);
                if (found_word != NULL) {
                    total_weight += found_word->weight;  // Sum the weight if the word is found
                    total_flag += found_word->flag;     // Sum the flag if the word is found
                }
            }

            word = strtok(NULL, " ,.-!?");  // Get the next word
        }
    }

    printf("Total flags of words found: %d\n", total_flag); // Output the total flags

    FILE *check = fopen("telegramCheck.txt", "w");
    if (check != NULL) {
        fprintf(check, "%d %d", total_flag, total_weight);
        fclose(check); // Ensure the file is properly closed
    }
    return total_weight;
}

int main() {
    FILE *fCountry = fopen("countries.txt", "r");
    if(fCountry == NULL){
      printf("Error: cant open countries.txt");
      return 1;
    }
    
    
    FILE *dp = fopen("dictionary.txt", "r");
    if (dp == NULL) {
        printf("Error: Cannot open file.\n");
        return 1;
    }

    // Create a hash table with linear probing
    HashTable *hash_table = createHashTable(TABLE_SIZE);
    if (hash_table == NULL) {
        return 1;  // Memory allocation failed
    }

    // Create a set to track processed words
    Set *processed_set = createSet(TABLE_SIZE);
    if (processed_set == NULL) {
        return 1;  // Memory allocation failed
    }

    // Read dictionary file and populate hash table
    readFileAndInsert(dp, hash_table);
    fclose(dp);

    // Open the news content file
    FILE *news_file = fopen("news_content.txt", "r");
    if (news_file == NULL) {
        printf("Error: Cannot open news content file.\n");
        return 1;
    }

    // Sum the weights and flags of the words found in the news content file
    int total_weight = sumWeightsAndFlagsFromFile(news_file, hash_table, processed_set);
    fclose(news_file);

    // Output the final result
    printf("Total weight: %d\n", total_weight);
    return 0;
}

