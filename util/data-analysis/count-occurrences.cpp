/**
 * This utilitary program was created to count the number of
 * occurences of the number of examples per whale.
 */

#include <iostream>
#include <climits>
#include <cstring>

using namespace std;

#define MAX 1000000

int main() {
    int n, lower = INT_MAX, upper = 0;
    int occurrences[MAX];

    memset(occurrences, 0, sizeof(occurrences)); // reset occurreces counting

    while (scanf("%d%*[^\n]", &n) != EOF) {
        occurrences[n]++;            // increase the number of occurences

        lower = min(lower, n);
        upper = max(upper, n);
    }

    printf("# examples | occurrences\n");
    for (int i = lower; i <= upper; i++)
        if (occurrences[i])
            printf("%d & %d \\\\\n", i, occurrences[i]);

    return 0;
}
