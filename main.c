#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include "util.h"
#include "key.h"

extern char *key;
int main(int argc, char *argv[]) {
    if( argc != 2 ) {
        printf("usage: try './curl [url]' to make a get request.\n");
        return 1;
    }
    
    char* link = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json?limit=1&api_key=";
    char* link_key = malloc((strlen(link) + strlen(key)) * sizeof(char));    strcat(link_key, link);
    strcat(link_key, key);

    struct MemoryStruct chunk;
    chunk.memory = malloc(1);
    chunk.size = 0;

    CURL *curl_handle = curl_easy_init();
    if(curl_handle) {
        printf("\nLink: %s", link_key);
        curl_easy_setopt(curl_handle, CURLOPT_URL, link_key);
        //curl_easy_setopt(curl_handle, CURLOPT_FOLLOWLOCATION, 1L);
        //curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);
        //curl_easy_setopt(curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0");

        CURLcode res = curl_easy_perform(curl_handle);

        if(res != CURLE_OK) {
            fprintf(stderr, "error: %s\n", curl_easy_strerror(res));
        } else {
            printf("Size: %lu\n", (unsigned long)chunk.size);
            printf("Data: %s\n", chunk.memory);
        }
        curl_easy_cleanup(curl_handle);
        free(chunk.memory);
    }
    return 0;
}