#include <iostream>
#include <fstream>
using namespace std;

#define uint unsigned int
#define byte unsigned char

int CrcPolynomial = 0x04c11db7;
uint CalculateChecksum(byte data[], int offset, int length, unsigned int checksum);
uint crc_table[0x100] = {0};
uint MaxValue = 0xFFFFFFFF;
byte header[8] = {'K', 'H', '2', 'J', 0x3A, 0x00, 0x00, 0x00};

void GetCrcTable(int polynomial)
{
    for (int x = 0; x < 0x100; x++)
    {
        int r = x << 24;
        for (int j = 0; j < 0xff; j++)
        r = r << 1 ^ (r < 0 ? polynomial : 0);
        crc_table[x] = (uint)r;
        //printf("%08X\n", crc_table[x]);
    }
}

uint CalculateChecksum(byte data[], int offset, int length, uint checksum)
{
    for (int i = offset; i < offset + length; i++)
        checksum = crc_table[(checksum >> 24) ^ data[i]] ^ (checksum << 8);

    return checksum ^ MaxValue;
}

int main(int argc, char* argv[])
{
    if (*argv[1] <= '0' || *argv[1] > '9')
    {
        printf("Give me a valid slot!");
        return 1;
    }

    byte data[0x10FC0] = {0};
    GetCrcTable(CrcPolynomial);

    int slot = atoi(argv[1]) - 1;
    char fajlnev[20];
    sprintf(fajlnev, "BISLPM-66675FM-%02d", slot);
    printf("%s\n", fajlnev);
    fstream fajl(fajlnev);
    if (fajl.fail())
    {
        printf("No file or something's went wrong.");
        return 1;
    }

    for (int i = 0; i < 0x10FC0; i++)
    {
        data[i] = fajl.get();
    }

    uint checksum = CalculateChecksum(data, 0, 8, MaxValue);
    printf("%08X\n", checksum);

    checksum = CalculateChecksum(data, 0xC, 0x10FB4, checksum ^ MaxValue);
    printf("%04X\n", checksum);
    printf("\n");

    fajl.seekp(0x8);
    fajl.write((char*)&checksum,  sizeof(checksum));
    fajl.close();

//    system("PAUSE");
    return 0;
}
