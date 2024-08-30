
default: build
build: clean
	gcc -Wall -o analyze main.c -lcurl

clean:
	rm -rf analyze

test: build
	./analyze https://freegeoip.app/json/ 
