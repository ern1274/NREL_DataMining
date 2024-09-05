#include "unity.h"
#include <Methods.h>

void setUp() {}
void tearDown() {}
void test_CalcMedian_should_Median() {
    double test[] = {1, 2, 3, 4, 5};
    TEST_ASSERT_EQUAL_DOUBLE(3, calcMedian(test, 5));
    
    double test2[]= {1, 2, 3, 4};
    TEST_ASSERT_EQUAL_DOUBLE(2.5, calcMedian(test2, 4));
    
    double test3[] = {};
    TEST_ASSERT_EQUAL_DOUBLE(-1, calcMedian(test3, 0));
    
    double test4[] = {1};
    TEST_ASSERT_EQUAL_DOUBLE(1, calcMedian(test4, 1));
    
    double test5[] = {2.63, 5.61, 21.51, 47.31, 49.53, 50.3, 62.23, 78.62, 84.46, 85.74};
    TEST_ASSERT_EQUAL_DOUBLE(49.915, calcMedian(test5, 10));
    
    double test6[] = {5.64, 10.24, 42.35, 58.49, 60.79, 64.2, 66.09, 71.18, 78.29, 85.19, 97.95};
    TEST_ASSERT_EQUAL_DOUBLE(64.2, calcMedian(test6, 11));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_CalcMedian_should_Median);

    return UNITY_END();
}

