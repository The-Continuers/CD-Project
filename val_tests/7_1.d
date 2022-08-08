// if + recursive function_call + Print
int fact(int n, int temp) {
    if (n == 0 || n == 1) {
        return 1;
    }
    return n * fact( n-1, temp + 1);
}

int main() {
    Print( fact( 7, 0));
}
// expected result: 5040