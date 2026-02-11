#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;

typedef unsigned int uint;
typedef unsigned char byte;


uint CalculateChecksum(byte data[], int offset, int length);

uint CalculateChecksum(byte data[], int offset, int length)
{
    uint checksum = 0;
    for (int i = offset; i < (offset + length); i+=4)
        checksum += *(uint*)&data[i];

    return checksum;
}

int main()
{
    byte data[0x11E50] = {0};

    fstream fajl("SAVEDATA.DAT");
    if (fajl.fail())
    {
        printf("No file or something's went wrong.");
        return 1;
    }

    for (int i = 0; i < 0x11E50; i++)
    {
        data[i] = fajl.get();
        //printf("%02X: %02X\n", i, data[i]);
    }

//    uint checksum = *(uint*)(data+0xC);
//    printf("%08X\n", checksum);

    printf("SAVEDATA.DAT\n");
    uint checksum = CalculateChecksum(data, 0x10, 0x11E40);
    printf("%08X\n", checksum);
    printf("\n");

    fajl.seekp(0xC);
    fajl.write((char*)&checksum,  sizeof(checksum));
    fajl.close();

//    system("PAUSE");
    return 0;
}
