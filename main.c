#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include "util.h"
#include "key.h"
#include <regex.h>    

extern char *key;
extern char *email;

// Considering REGEX for data tokenization
void printData(char *data) {
    char *token;
	if(data == NULL) {
        printf("Null data");
        return ;
    }
	while ((token = strsep(&data, ",")) != NULL) {
        printf("%s\n", token);
    }
}

int main(int argc, char *argv[]) {
    if( argc != 2 ) {
        printf("usage: try './curl [url]' to make a get request.\n");
        return 1;
    }
    // "https://developer.nrel.gov/api/nsrdb/v2/solar/spectral-ondemand-download.json?"
    char* link = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-download.json?&limit=1&location_ids=681462&years=2020&equipment=one_axis";
    // Add modification options such as years, location_ids, limit and such
    char* link_key = malloc((strlen(link) + strlen(key) + strlen(email)) * sizeof(char));    
    strcat(link_key, link); 
    strcat(link_key, email);
    strcat(link_key, key);

    struct MemoryStruct chunk;
    chunk.memory = malloc(1);
    chunk.size = 0;

    CURL *curl_handle = curl_easy_init();
    if(curl_handle) {
        printf("\nLink: %s", link_key);
        curl_easy_setopt(curl_handle, CURLOPT_URL, link_key);
        curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);

        CURLcode res = curl_easy_perform(curl_handle);

        if(res != CURLE_OK) {
            fprintf(stderr, "error: %s\n", curl_easy_strerror(res));
        } else {
            printf("\nSize: %lu\n", (unsigned long)chunk.size);
            printData(chunk.memory);
            //printf("\nData: %s\n", chunk.memory);
        }
        curl_easy_cleanup(curl_handle);
        free(chunk.memory);
    }
    return 0;
}