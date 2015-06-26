#include "head.h"


stu get_user_info(string & line)
{
	stu tmp;
	tmp.ID = line.substr(0, line.find_first_of(','));
	line = line.substr(line.find_first_of(',') + 1);
	tmp.name = line.substr(0, line.find_first_of(','));
	line = line.substr(line.find_first_of(',') + 1);
	tmp.user_name = line.substr(0, line.find_first_of(','));
	line = line.substr(line.find_first_of(',') + 1);
	tmp.major = line;
	return tmp;
}

bool user_sort_cmp(const stu & a, const stu & b){
	return a.ID < b.ID;
}

void init_user()
{
	user.clear();
	cout << "�������û���ϢCSV�ļ�����";
	cin >> file_name;
	cout << "���ڶ�ȡ�����Ժ�..." << endl;
	ifstream in("data\\" + file_name + ".csv");
	if (!in) { cerr << file_name << ".csv" << " ��ʧ��!" << endl; return; }
	string line; getline(in, line);
	while (getline(in, line)){
		stu tmp = get_user_info(line);
		user.push_back(tmp);
		cout << "   OK : " << tmp.ID << " - " << tmp.name << " - " << tmp.user_name << " - " << tmp.major << endl;
	}
	in.close();
	sort(user.begin(), user.end(), user_sort_cmp);
	cout << "��ȡ���. �ɹ���ȡ" << user.size() << "��ѧ������" << endl;
}
