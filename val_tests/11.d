// nested fors with break

int main(){
    int i;
    int j;
    int k;
    for (i = 0; i < 4; i = i + 1) {
        Print("i");
        Print(i);
        j = 0;
        while (j < 4) {
            if (j == 2) {
                j = j + 1;
                continue;
            }
            Print("j");
            Print(j);
            j = j + 1;
            for (k = 0; k < 10; k = k+1) {
                if (true && (k == 0)) {
                    break;
                }
                Print("k");
                Print(k);
            }
        }
        if (i == 2) {
            break;
        }
    }
}