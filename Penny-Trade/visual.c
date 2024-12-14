#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h> 
#include <dirent.h>
#include <string.h>

#include "visual.h"

void visualization(){
    get_files_for_visualization();

    char *filename = get_filename();

    pid_t pid = fork(); // Create a child process
    if (pid == 0) {
        // Child process: Run the Python script with the filename as an argument
        char command[512];
        snprintf(command, sizeof(command), "python3 ../Visualization/visual.py ../SimulationPool/%s", filename);
        printf("Child process: Running visualization with file '%s'...\n", filename);
        int result = system(command);
        if (result != 0) {
            printf("Error running Python script.\n");
        }
        printf("Child process: Visualization finished.\n");
        exit(0); // Exit the child process
    } else if (pid > 0) {
        // Parent process: Wait for the user to continue
        printf("Visualization process started in the background. Press Enter to return to the menu...\n");
        getchar(); // Consume the newline character left by scanf
        getchar(); // Wait for the user to press Enter
    } else {
        // Fork failed
        perror("Failed to fork");
    }
}

void get_files_for_visualization() {
    const char *directory = "../SimulationPool/";  // Initialize the directory path
    struct dirent *entry;
    DIR *dp = opendir(directory);

    if (dp == NULL) {
        perror("opendir");
        return;
    }

    printf("  Available 'SIMULATION'.txt files in directory for graph visualization '%s':\n", directory);
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


char *get_filename(){
    char filename[20];
    char *p_filename;
    printf("\nEnter filename you want to visualize: ");
    scanf("%s", filename);
    p_filename = strdup(filename);
    return p_filename;
}