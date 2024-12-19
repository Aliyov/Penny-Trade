# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -g

# Source files
SRCS = main.c menu.c simulation.c tacticalX.c visual.c 

# Object files (Correct this to create .o files, not .c)
OBJS = $(SRCS:.c=.o)

# Header files (for dependencies)
DEPS = menu.h simulation.h tacticalX.h visualization.h 

# Output executable name
TARGET = trade_app

# Rule to build the final executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Rule to compile .c files into .o files
%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean the build (remove object files and executable)
clean:
	rm -f $(OBJS)

# Run the program
run: $(TARGET)
	./$(TARGET)

