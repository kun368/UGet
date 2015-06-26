#include "head.h"

void put_uhunt(const string output_file_name)
{
	ofstream out("uhunt\\" + output_file_name + ".txt");
	if (!out) { cerr << "错误：创建文件失败！" << endl; return; }
	out << user.size() << endl;
	for (size_t i = 0; i < user.size(); i++){
		out << user[i].ID << endl;
		out << user[i].user_name << endl;
	}
	out.close();
	if (output_file_name != "user")
		printf("%s.txt生成成功，请打开uHunt目录下的ut.py,键入\"anaf %s.txt\"命令获取题数信息.\n", output_file_name.c_str(), output_file_name.c_str());
}