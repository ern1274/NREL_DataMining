#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

int compare_function(const void *a,const void *b) {
    double *x = (double *) a;
    double *y = (double *) b;
    if (*x < *y) { return -1; }
    else if (*x > *y) { return 1; }
    return 0;
}

double calcMedian(double data[], int amount) {
    printf("Result of Median is %f" , data[amount/2]);
    return data[amount/2];
}
double calcMode(double data[], int amount) {
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
    printf("Result of Mode is %f with count %d" , mode, count);
    return mode;
}
double calcMean(double data[], int amount) {
    double total = 0;
    for (int i = 0; i < amount; i++)
    {
        total += data[i];
    }
    printf("Result of Mean is %f" , total/amount);
    return total/amount;
}

void centralTendency(double data[], int amount) {
    printf("Calculating Central Tendencies: Median, Mode, and Mean");
    qsort(data, amount, sizeof(double), compare_function);
    double median = calcMedian(data, amount);
    double mode = calcMode(data, amount);
    double mean = calcMean(data, amount);
    printf("Results: \nMedian: %f \nMode: %f \nMean: %f", median, mode, mean);
}
int main(int argc, char *argv[]) {
    printf("Main");
}
