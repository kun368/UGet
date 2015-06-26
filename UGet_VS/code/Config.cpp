#include "head.h"

void config_score()
{
	ifstream in("config\\score.ini");
	if (!in) { cerr << "读取成绩配置文件文件失败!" << endl; return; }
	in >> fix_score >> add_score >> fazhi;
	printf("当前设置为");
	printf("每题固定得分：%.2f  价值分：%.2f  阀值：%.2f\n", fix_score, add_score, fazhi);
	in.close();
}

void config_chapter()
{
	dict.clear();
	ifstream in("config\\chapter.ini");
	if (!in) { cerr << "读取章节配置文件文件失败!" << endl; return; }
	string line;
	while (getline(in, line)){
		if (line.back() == '\t') line.pop_back();
		string name = line.substr(0, line.find(","));
		line = line.substr(line.find(",") + 1);
		vector<string> t;
		while (line.find(",") != string::npos){
			t.push_back(line.substr(0, line.find(",")));
			line = line.substr(line.find(",") + 1);
		}
		t.push_back(line);
		dict.push_back(make_pair(name, t));
	}
	in.close();
	cout << "读取章节配置文件成功！" << endl;
}
