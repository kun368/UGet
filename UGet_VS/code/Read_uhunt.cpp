#include "head.h"

void init_tree()
{
	root.cur = "R";
	root.pid.clear();
	root.next.clear();
}

int find_tree(string next_name, Tree & u){
	for (int i = 0; i != u.next.size(); ++i)
	if (u.next[i].cur == next_name)
		return i;
	u.next.resize(u.next.size() + 1);
	u.next.back().cur = next_name;
	return u.next.size() - 1;
}

int get_cpt(string str)
{
	str = str.substr(16);
	stringstream ss(str);
	int res; ss >> res;
	return res;
}

vector<int> get_pid(string line){
	line = line.substr(line.find(':') + 1);
	stringstream ss(line);
	int x; vector<int> res;
	while (ss >> x) res.push_back(x);
	return res;
}

deque<string> get_tag(const vector<int> road){
	deque<string> res;
	if (road[1] != 0) res.push_back("B" + to_string(road[1]));
	else return res;
	if (road[2] != -1) res.push_back("C" + to_string(road[2]));
	else return res;
	if (road[3] != 0) res.push_back("U" + to_string(road[3]));
	return res;
}


void add_tree(deque<string> tag, const stu & u, const vector<int> & no, Tree & t){
	for (int i = 0; i != no.size(); ++i)
		if (!count(t.pid[no[i]].begin(), t.pid[no[i]].end(), u.ID))
			t.pid[no[i]].push_back(u.ID);
	if (!tag.empty()){
		string v = tag.front(); tag.pop_front();
		add_tree(tag, u, no, t.next[find_tree(v, t)]);
	}
}

void read_uhunt()
{
	init_tree();
	for (size_t i = 0; i != user.size(); ++i){
		ifstream in("uhunt\\ana_" + user[i].ID + ".txt");
		if (!in) { cerr << user[i].name << "：打开文件失败!" << endl; continue; }
		string line; vector<int> road; road.resize(4);
		while (getline(in, line)){
			if (line.find("AOAPC") != string::npos)
				++road[1], road[2] = -1, road[3] = 0;
			else if (line.find("Chapter") != string::npos)
				road[2] = get_cpt(line), road[3] = 0;
			else if (count(line.begin(), line.end(), '-') == 6 && line.find("Examples") == string::npos && line.find("Exercises") == string::npos && line.find("Extra") == string::npos)
				++road[3];
			else if (line.find("accept") != string::npos) {
				vector<int> pid = get_pid(line);
				add_tree(get_tag(road), user[i], pid, root);
			}
		}
		in.close();
		printf("   %s：uhunt数据读取完毕\n", user[i].name.c_str());
	}
	cout << "所有同学数据读取完毕！" << endl;
}