#include "head.h"

void Standard(const stu & s)
{
	ifstream in("uhunt\\ana_" + s.ID + ".txt");
	ofstream out("result\\" + s.name + "_" + s.major + ".txt");
	if (!in) { cerr << s.name << "�����ļ�ʧ��!" << endl; return; }
	if (!out) { cerr << s.name << "�������ļ�ʧ��!" << endl; return; }
	string line;
	while (getline(in, line)){
		line.push_back('\n');
		out << line;
	}
	in.close(); out.close();
	cout << "   " << s.name << "����ʽת����ɣ�" << endl;
}

void files_std()
{
	printf("���ڽ����ļ���ʽ�������Ժ�...\n");
	for (size_t i = 0; i < user.size(); i++)
		Standard(user[i]);
	cout << "�ļ�ת����ϣ�" << endl;
}
