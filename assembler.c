
/* Assembler code fragment for LC-3101 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAXLINELENGTH 1000
#define R_TYPE 1
#define I_TYPE 2
#define J_TYPE 3
#define O_TYPE 4


int readAndParse(FILE *, char *, char *, char *, char *, char *);
int isNumber(char *);
int instr_type(char * );
int R_type_conv(char * ,char * ,char * ,char * ,char * );
int opcode_gen(char * );
void write_bin(FILE * fd, int number, int bits );
void itoa(int num, char * str, int base);
void write_r_instr(FILE*, char*, char*, char*,char*);
void write_i_instr(FILE*, char*, char*, char*,char*);
void write_j_instr(FILE*, char*, char*, char*,char*);
void write_o_instr(FILE*, char*, char*, char*,char*);

int
main(int argc, char *argv[])
{
    char *inFileString, *outFileString;
    FILE *inFilePtr, *outFilePtr;
    char label[MAXLINELENGTH], opcode[MAXLINELENGTH], arg0[MAXLINELENGTH],
            arg1[MAXLINELENGTH], arg2[MAXLINELENGTH];

    if (argc != 3) {
        printf("error: usage: %s <assembly-code-file> <machine-code-file>\n",
            argv[0]);
        exit(1);
    }
    printf("Correct input detected\n");

    inFileString = argv[1];
    outFileString = argv[2];

    inFilePtr = fopen(inFileString, "r");
    if (inFilePtr == NULL) {
        printf("error in opening %s\n", inFileString);
        exit(1);
    }
    outFilePtr = fopen(outFileString, "w");
    if (outFilePtr == NULL) {
        printf("error in opening %s\n", outFileString);
        exit(1);
    }

    /* here is an example for how to use readAndParse to read a line from
        inFilePtr */
    int type = 0;
    int oppies = 0;
    while ( readAndParse(inFilePtr, label, opcode, arg0, arg1, arg2) ) {
        type = instr_type(opcode);
        if (type == R_TYPE) {
            printf("R\n");
            write_r_instr(outFilePtr, opcode, arg0, arg1, arg2);
        }
        else if (type == I_TYPE){
            printf("I\n");
            write_i_instr(outFilePtr, opcode, arg0, arg1, arg2);
        }
        else if (type == O_TYPE){ 
            printf("O\n");
            write_o_instr(outFilePtr, opcode, arg0, arg1, arg2);
        }
        else{
            printf("could be the fil\n");
        }
        printf("%s , %s , %s , %s , %s \n", label, opcode, arg0, arg1, arg2 );
    }

    /* reached end of file */
    printf("reached the end of the file\n");


    /* this is how to rewind the file ptr so that you start reading from the
        beginning of the file */
    rewind(inFilePtr);


    return(0);
}

/* return -1 for error
 * generates opp code number sequence in decimal*/
int
opcode_gen(char * opcode){
    if (!strcmp(opcode, "add")){
        return 0; 
    }
    if (!strcmp(opcode, "nand")){
        return 1; 
    }
    if (!strcmp(opcode, "lw")){
        return 2; 
    }
    if (!strcmp(opcode, "sw")){
        return 3; 
    }
    if (!strcmp(opcode, "beq")){
        return 4; 
    }
    if (!strcmp(opcode, "jalr")){
        return 5; 
    }
    if (!strcmp(opcode, "halt")){
        return 6; 
    }
    if (!strcmp(opcode, "noop")){
        return 7; 
    }
    
    return -1;
}

/* returns 1 for success, 0 for error
 * generates a string of number representing line of assembly
 * into machine code */
int
R_type_conv(char * label,char * opcode,char * arg0,char * arg1,char * arg2){
    int op_trans = opcode_gen(opcode);   
    return 0;
}
void 
write_r_instr(FILE* fd, char*opcode, char* arg0, char* arg1,char* arg2){
    int tempNum = opcode_gen(opcode);
    write_bin(fd,tempNum,11 );
    tempNum = atoi(arg0);
    write_bin(fd, tempNum, 3);
    tempNum = atoi(arg1);
    write_bin(fd, tempNum, 3);
    fprintf(fd,"%0*d", 13, 0);
    tempNum = atoi(arg2);
    write_bin(fd, tempNum, 3);
    fprintf(fd,"\n");

}
void 
write_i_instr(FILE* fd, char*opcode, char* arg0, char* arg1,char* arg2){
    int tempNum = opcode_gen(opcode);
    write_bin(fd,tempNum,11 );
    tempNum = atoi(arg0);
    write_bin(fd, tempNum, 3);
    tempNum = atoi(arg1);
    write_bin(fd, tempNum, 3);
    tempNum = atoi(arg2);
    write_bin(fd, tempNum, 16);
    fprintf(fd,"\n");

}
void 
write_o_instr(FILE* fd, char*opcode, char* arg0, char* arg1,char* arg2){
    int tempNum = opcode_gen(opcode);
    write_bin(fd,tempNum,11 );
    tempNum = atoi(arg0);
    write_bin(fd, tempNum, 3);
    tempNum = atoi(arg1);
    write_bin(fd, tempNum, 3);
    tempNum = 0;
    write_bin(fd, tempNum, 16);
    fprintf(fd,"\n");

}
void 
write_j_instr(FILE* fd, char*opcode, char* arg0, char* arg1,char* arg2){
    int tempNum = opcode_gen(opcode);
    write_bin(fd,tempNum,11 );
    tempNum = 0;
    write_bin(fd, tempNum, 22);
    fprintf(fd,"\n");

}
/* writes a number in binary with bit padding*/
void
write_bin(FILE * fd ,int number, int bits ){
    char buffer[32];
    itoa(number, buffer, 2);
    int binary = atoi(buffer);
    fprintf(fd, "%0*d",bits, binary);
}

void
itoa(int num, char * str, int base){
    int remainder = 0;
    int index = 0;
    int temps[32];
    while(num != 0){
        remainder = num % base; 
        if (remainder > 9){
            str[index] = (remainder-10) + 'a'; 
            temps[index] = str[index];
            index++;
        }
        else{
            str[index] =  remainder + '0'; 
            temps[index] = str[index];
            index++;
        }
        num = num/base; 
    }
    str[index] = '\0';
    int reverse;
    for(int i = 0; i < index; i++){
        reverse = index -1 - i;
        str[i] = temps[reverse];
    }
    return;
}

/* return type of instruction scanned
 * returns 0 when no recognized input 
 */
int
instr_type(char * field){
    if (!strcmp(field, "add") || !strcmp(field, "nand"))
        return R_TYPE;
    if(!strcmp(field, "lw") || !strcmp(field, "sw") || !strcmp(field, "beq") )
        return I_TYPE;
    if(!strcmp(field, "jalr" ))
        return J_TYPE;
    if (!strcmp(field, "halt") || !strcmp(field, "noop"))
        return O_TYPE;
    return 0; 
}

/*
 * Read and parse a line of the assembly-language file.  Fields are returned
 * in label, opcode, arg0, arg1, arg2 (these strings must have memory already
 * allocated to them).
 *
 * Return values:
 *     0 if reached end of file
 *     1 if all went well
 *
 * exit(1) if line is too long.
 */
int
readAndParse(FILE *inFilePtr, char *label, char *opcode, char *arg0,
    char *arg1, char *arg2)
{
    char line[MAXLINELENGTH];
    char *ptr = line;

    /* delete prior values */
    label[0] = opcode[0] = arg0[0] = arg1[0] = arg2[0] = '\0';

    /* read the line from the assembly-language file */
    if (fgets(line, MAXLINELENGTH, inFilePtr) == NULL) {
	/* reached end of file */
        return(0);
    }

    /* check for line too long (by looking for a \n) */
    if (strchr(line, '\n') == NULL) {
        /* line too long */
	printf("error: line too long\n");
	exit(1);
    }

    /* is there a label? */
    ptr = line;
    if (sscanf(ptr, "%[^\t\n ]", label)) {
	/* successfully read label; advance pointer over the label */
        ptr += strlen(label);
    }

    /*
     * Parse the rest of the line.  Would be nice to have real regular
     * expressions, but scanf will suffice.
     */
    sscanf(ptr, "%*[\t\n ]%[^\t\n ]%*[\t\n ]%[^\t\n ]%*[\t\n ]%[^\t\n ]%*[\t\n ]%[^\t\n ]",
        opcode, arg0, arg1, arg2);
    return(1);
}

int
isNumber(char *string)
{
    /* return 1 if string is a number */
    int i;
    return( (sscanf(string, "%d", &i)) == 1);
}
