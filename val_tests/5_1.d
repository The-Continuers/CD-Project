// static scoped function call
// expected result: Semantic Error
void f() {
    Print( x);
}

int main() {
    int x = 5;
    f();
}