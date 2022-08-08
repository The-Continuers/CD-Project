//While

int main(){
    int i=0;
    string j="sep";
    while(i<3){
        Print(i);
        i=i+1;
    }

    while(j=="sad"){
        Print("gi zanni mandes");
    }

    i=13;
    while(i>=10){
        Print(i*2);
        i=i-2;
    }

    i=15;
    while(i>0){
        if (i<13){
            Print("breaked");
            break;
        }
        Print(i*10);
        i=i-1;
    }


    i=1500;
    while(i>=0){
        if (i<1495){
            Print("breaked");
            break;
        }
        if (i==1498){
            Print("continued");
            i=i-1;
            continue;
        }
        Print(i);
        i=i-1;
    }
}