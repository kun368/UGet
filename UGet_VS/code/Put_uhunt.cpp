#include "head.h"

void put_uhunt(const string output_file_name)
{
	ofstream out("uhunt\\" + output_file_name + ".txt");
	if (!out) { cerr << "���󣺴����ļ�ʧ�ܣ�" << endl; return; }
	out << user.size() << endl;
	for (size_t i = 0; i < user.size(); i++){
		out << user[i].ID << endl;
		out << user[i].user_name << endl;
	}
	out.close();
	if (output_file_name != "user")
		printf("%s.txt���ɳɹ������uHuntĿ¼�µ�ut.py,����\"anaf %s.txt\"�����ȡ������Ϣ.\n", output_file_name.c_str(), output_file_name.c_str());
}