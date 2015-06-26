#include "head.h"

void Standard(const stu & s)
{
	ifstream in("uhunt\\ana_" + s.ID + ".txt");
	ofstream out("result\\" + s.name + "_" + s.major + ".txt");
	if (!in) { cerr << s.name << "：打开文件失败!" << endl; return; }
	if (!out) { cerr << s.name << "：创建文件失败!" << endl; return; }
	string line;
	while (getline(in, line)){
		line.push_back('\n');
		out << line;
	}
	in.close(); out.close();
	cout << "   " << s.name << "：格式转换完成！" << endl;
}

void files_std()
{
	printf("正在进行文件格式化，请稍候...\n");
	for (size_t i = 0; i < user.size(); i++)
		Standard(user[i]);
	cout << "文件转换完毕！" << endl;
}
