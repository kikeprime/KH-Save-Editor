#include <iostream>
#include <fstream>
using namespace std;

#define uint unsigned int
#define byte unsigned char

int CrcPolynomial = 0x04c11db7;
uint CalculateChecksum(byte data[], int offset, int length);

uint CalculateChecksum(byte data[], int offset, int length)
{
    int checksum = 0xFFFFFFFF;

    for (int i = offset; i < offset+length; i++)
    {
        checksum ^= data[i] << 31;
        checksum = checksum << 1 ^ (checksum < 0 ? 0x4c11db7 : 0);
    }

    return (uint)~checksum;
}

int main(int argc, char* argv[])
{
    if (*argv[1] <= '0' || *argv[1] > '9')
    {
        printf("Give me a valid slot!");
        return 1;
    }

    byte data[0x3630] = {0};

    int slot = atoi(argv[1]);
    if (slot > 99)
    {
        printf("Slot must be between 1 and 99!");
        return 1;
    }
    char fajlnev[20];
    sprintf(fajlnev, "BASLUS-21799COM-%02d", slot);
    printf("%s\n", fajlnev);
    fstream fajl(fajlnev);
    if (fajl.fail())
    {
        printf("No file or something's went wrong.");
        return 1;
    }

    for (int i = 0; i < 0x3630; i++)
    {
        data[i] = fajl.get();
        //printf("%02X: %02X\n", i, data[i]);
    }

    uint checksum = *(uint*)(data+0x4);
    printf("%08X\n", checksum);

    checksum = CalculateChecksum(data, 0x10, 0x3620);
    printf("%08X\n", checksum);
    printf("\n");

    fajl.seekp(0x4);
    fajl.write((char*)&checksum,  sizeof(checksum));
    fajl.close();

    //system("PAUSE");
    return 0;
}
