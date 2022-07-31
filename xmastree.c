#include <stdio.h>

int du();
void dayin();

int main(void){
	int ceng=du();
	dayin(ceng);
	return 0;
}

int du(void){
	int ceng;
	printf("cengshu: ");
	scanf("%d",&ceng);
	return ceng;
}

void dayin(int ceng){
	for (int i = 1;i < ceng+1; i++){
		for (int k=1;k<ceng-i+1;k++){
			printf(" ");
		}
		for (int j = 1;j<2*i;j++){
			printf("*");
		}
	printf("\n");
	}
}
