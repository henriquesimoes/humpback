#include<iostream>
#include<vector>
#include<utility>
#include<cstring>
#include<cmath>

using namespace std;

#define MAX 7000
#define OFFSET 60

typedef pair<int, int> ii;
typedef pair<vector<ii>, vector<ii>> pvv;

pvv build(int *arr, int off) {
    vector<ii> v, q;
    for (int i = 0; i < MAX; i++)
        if (arr[i]) {
            v.push_back({arr[i], i});
            if (arr[i] > off)
                q.push_back({arr[i], i});
        }

    return {v, q};
}

void histogram(vector<ii> h) {
    int start = h.begin()->second;
    int end = h.rbegin()->second;
    int bin = (int) (end - start) / sqrt(h.size());
    int count;

    auto it = h.begin();
    for (int i = 0; start + i * bin <= end; i++) {
        count = 0;
        while (it != h.end() && it->second < start + (i + 1) * bin) {
            count += it->first;
            it++;
        }

        printf("%4d - %4d | %5d\n", start + i * bin, start + (i + 1) * bin, count);
    }
    putchar('\n');
}

void most_frequent(vector<ii> v) {
    for (auto it = v.begin(); it != v.end(); it++)
        printf("%4d | %5d \n", it->second, it->first);

    printf("\n\n");
}

int main(int argc, char *argv[]) {
    int width, height, occur, widths[MAX], heights[MAX];

    memset(widths, 0, sizeof(widths));
    memset(heights, 0, sizeof(heights));

    scanf("%*[^\n]%*c");

    while (scanf(" (%d, %d) %d ", &width, &height, &occur) != EOF) {
        heights[height] += occur;
        widths[width] += occur;
    }

    const int offset = (argc > 1) ? atoi(argv[1]) : OFFSET;

    auto h = build(heights, offset);
    auto w = build(widths, offset);

    printf("Height distribution\n");
    histogram(h.first);

    printf("Width distribution\n");
    histogram(w.first);

    printf("Heights with more than %d occurrences (Height | Occurrences)\n", offset);
    most_frequent(h.second);

    printf("Widths with more than %d occurrences (Width | Occurrences)\n", offset);
    most_frequent(w.second);

    return 0;
}
