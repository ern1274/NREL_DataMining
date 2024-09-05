#include "unity.h"
#include <Methods.h>

void setUp() {}
void tearDown() {}
void test_CalcMedian_should_Median() {
    double test[] = {1, 2, 3, 4, 5};
    TEST_ASSERT_EQUAL_INT16(3, calcMedian(test, 5));
    double test2[]= {1, 2, 3, 4};
    TEST_ASSERT_EQUAL_INT16(3, calcMedian(test2, 4));
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_CalcMedian_should_Median);

    return UNITY_END();
}

