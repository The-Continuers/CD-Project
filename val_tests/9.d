//For

int main(){
    int i;
    for(i=0; i<5; i=i+1){
        Print(2*i);
        i=i+1;
    }

    for(i=0; i<5; i=i+1){
        Print(i);
        if(i==3){
            Print("Broke");
            break;
        }
    }

    for(i=0; i<4; i=i+1){
        if(i==2) {
            Print("Continued");
            continue;
        }
        Print(i);
    }

}