#include "head.h"

void put_accnt(const string output_file_name)
{
	auto & all = root.pid;
	ofstream out("result\\" + output_file_name + "-AC-Count.csv");
	if (!out) { cerr << "���󣺴����ļ�ʧ�ܣ�" << endl; return; }
	out << "��Ŀ,AC����" << endl;
	for (auto it = all.begin(); it != all.end(); ++it){
		out << it->first << ",";
		out << it->second.size() << endl;
	}
	out.close();
	system(string("start result\\" + output_file_name + "-AC-Count.csv").c_str());
	cout << "ͳ����ϣ��ļ��Ѿ��򿪣�" << endl;
}

void put_commend(const string output_file_name)
{
	auto & all = root.pid;
	ofstream out("result\\" + output_file_name + "-commend.csv");
	if (!out) { cerr << "���󣺴����ļ�ʧ�ܣ�" << endl; return; }
	out << "����,�Ƽ���Ŀ" << endl;
	for (int i = 0; i != user.size(); ++i){
		out << user[i].name;
		vector<pair<int, int>> res;
		for (auto j : all){
			if (!count(j.second.begin(), j.second.end(), user[i].ID))
				res.push_back(make_pair(j.first, (int)j.second.size()));
		}
		sort(res.begin(), res.end(), [](const pair<int, int> & a, const pair<int, int> & b) {return a.second > b.second;});
		for (int k = 0; k < res.size() && k < 10; ++k)
			out << "," << res[k].first;
		out << endl;
	}
	out.close();
	system(string("start result\\" + output_file_name + "-commend.csv").c_str());
	cout << "ͳ����ϣ��ļ��Ѿ��򿪣�" << endl;
}