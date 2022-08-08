// function call
int j(int y) {
    int x;
    x = 3;
    return y * x;
}

double k(int y, double x) {
    return 4.0;
}

int main() {
    int x;
    double y;
    x = j( 2);
    y = k( x, y);
    Print( x);
    Print( y);
}