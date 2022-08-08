//For + FuncCall

int f(int x, string s) {
    int j;
    Print(s);
    for (j = 0; j < 10; j = j + 1) {
        if (j == 2) {
            return x + j;
        }
    }
}

int main(){
    int i;
    int res;
    i = 1;
    res = 12344321;
    for (i = 2; i < 6; i = i + 1) {
        if (i == 5) {
            break;
        }
        res = f(i, "This is a Test");
        Print(res);
    }
}