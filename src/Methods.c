/*
 * File: Methods.c
 * 
 * Desc: Data Analysis methods for use in other files 
 * given the parameters passed in for respective method are appropriate
 * 
 * Author: Ethan Nunez     ern1274@rit.edu
 *          
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "Methods.h"

/**
* Compares two doubles and returns values based on 'a' left hand side and 'b' right hand side
* @param a first double to compare
* @param b second double to compare
* @return returns either 1, -1, or 0 based on 'a' relative to 'b'
*/
int compare_function(const void *a,const void *b) {
    double *x = (double *) a;
    double *y = (double *) b;
    if (*x < *y) { return -1; }
    else if (*x > *y) { return 1; }
    return 0;
}
/**
* Calculates Median given sorted double array and its length
* @param data array of doubles
* @param amount length of data array
* @return returns the data in the middle of the array
*/
double calcMedian(double data[], int amount) {
    if(amount < 1) {
        return -1;
    }
    /*else if(amount == 1) {
        return data[amount-1];
    }*/
    else if(amount % 2 == 0) {
        return (data[amount/2] + data[(amount/2) - 1]) / 2;
    }
    return data[amount/2];
}
/**
* Calculates Mode given sorted double array and its length
* @param data array of doubles
* @param amount length of data array
* @return returns the data with the highest reoccurrence in the array
*/
double calcMode(double data[], int amount) {
    if(amount < 1) {
        return -1;
    }
    double mode;
    int count = 0;
    double curr;
    int curr_count = 0;
    bool initial_curr = false;
    bool initial_mode = false;
    for (int i = 0; i < amount; i++)
    {
        if(!initial_curr) {
            initial_curr = true;
            curr = data[i];
        }
        if(data[i] != curr) {
            if(!initial_mode) {
                initial_mode = true;
                mode = curr;
                count = curr_count;
            } else {
                if(curr_count > count) {
                    mode = curr;
                    count = curr_count;
                }
            }
            curr = data[i];
            curr_count = 0;
        }
        curr_count++;
    }
    if(!initial_mode) {
        mode = curr;
        count = curr_count;
    }
    //printf("Result of Mode is %f with count %d" , mode, count);
    return mode;
}
/**
* Calculates Mean given sorted double array and its length
* @param data array of doubles
* @param amount length of data array
* @return returns the sum of all values in data array divided by its amount/length
*/
double calcMean(double data[], int amount) {
    if(amount < 1) {
        return -1;
    }
    double total = 0;
    for (int i = 0; i < amount; i++)
    {
        total += data[i];
    }
    //printf("Result of Mean is %f" , total/amount);
    return total/amount;
}
/**
* Sorts the data array in ascending order and
* calculates Median, Mode and Mean values of said array and prints it
* @param data array of doubles
* @param amount length of data array
*/
double* centralTendency(double data[], int amount) {
    //printf("Calculating Central Tendencies: Median, Mode, and Mean\n");
    qsort(data, amount, sizeof(double), compare_function);
    double median = calcMedian(data, amount);
    double mode = calcMode(data, amount);
    double mean = calcMean(data, amount);
    //printf("Results: \nMedian: %f \nMode: %f \nMean: %f", median, mode, mean);
    static double result[3];
    result[0] = median;
    result[1] = mode;
    result[2] = mean;
    return result;
}
/*int main(int argc, char *argv[]) {
    printf("Main");
}*/
