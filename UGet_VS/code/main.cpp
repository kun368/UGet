#include "head.h"

Tree root;
vector<pair<string, vector<string>>> dict;
vector<stu> user;
double fix_score, add_score, fazhi;
string file_name;

void Menu()
{
	printf("\n");
	printf("*********** MENU ***********\n");
	printf(" 1 : ���¶�ȡCSV��Ա����\n");
	printf(" 2 : ����uHunt�����ļ�\n");
	printf(" 3 : ��Ա�������ݱ�׼��\n");
	printf(" 4 : �����������ݲ�����\n");
	printf(" 5 : �鿴ÿ��AC����\n");
	printf(" 6 : ���������Ƽ�\n");
	printf(" 7 : �鿴��ǰϵͳ����\n");
	printf(" 0 : �˳�����\n");
	printf("****************************\n");
	printf("����ѡ�� : ");
	int cmd; cin >> cmd;
	system("cls");
	if (cmd == 1) init_user();
	if (cmd == 2) put_uhunt(file_name), put_uhunt("user");
	if (cmd == 3) files_std();
	if (cmd == 4) read_uhunt(), put_statistics();
	if (cmd == 5) put_accnt(file_name);
	if (cmd == 6) put_commend(file_name);
	if (cmd == 7) config_score(); 
	if (cmd == 0) exit(0);
}

int main()
{
	system("COLOR 2F");
	printf("*-----------------------------------------------------------------*\n");
	printf("|                            UGet V2.0.2                          |\n");
	printf("|                                                  Powered By KUN |\n");
	printf("*-----------------------------------------------------------------*\n");
	printf("���ڳ�ʼ����");
	config_score(); config_chapter(); init_user();
	while (true) Menu();
	return 0;
}
