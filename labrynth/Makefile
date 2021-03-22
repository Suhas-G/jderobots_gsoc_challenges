CXX := g++
INPUT := sample
OUTPUT := output
EXECUTABLE := main


all: $(EXECUTABLE)

$(EXECUTABLE):
	$(CXX) $(EXECUTABLE).cpp -o $(EXECUTABLE).out

clean:
	$(RM) $(EXECUTABLE).out
	$(RM) $(OUTPUT)/*

run: clean all
	@echo "Running sample 1"
	./$(EXECUTABLE).out $(INPUT)/labrynth-1.txt $(OUTPUT)/output-1.txt
	@echo "Running sample 2"
	./$(EXECUTABLE).out $(INPUT)/labrynth-2.txt $(OUTPUT)/output-2.txt
	@echo "Running sample 3"
	./$(EXECUTABLE).out $(INPUT)/labrynth-3.txt $(OUTPUT)/output-3.txt
