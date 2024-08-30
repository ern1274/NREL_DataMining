
default: build
build: clean
	gcc -Wall -o analyze Methods.c -lcurl
	cc -fPIC -shared -o analyze.so Methods.c

clean:
	rm -rf analyze

test: build
	./analyze https://freegeoip.app/json/ 
