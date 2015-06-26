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
	printf(" 1 : 重新读取CSV队员数据\n");
	printf(" 2 : 生成uHunt所需文件\n");
	printf(" 3 : 队员个人数据标准化\n");
	printf(" 4 : 分析整体数据并汇总\n");
	printf(" 5 : 查看每题AC人数\n");
	printf(" 6 : 智能做题推荐\n");
	printf(" 7 : 查看当前系统设置\n");
	printf(" 0 : 退出程序\n");
	printf("****************************\n");
	printf("您的选择 : ");
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
	printf("正在初始化，");
	config_score(); config_chapter(); init_user();
	while (true) Menu();
	return 0;
}
