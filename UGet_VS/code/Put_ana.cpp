#include "head.h"

deque<string> decode_tag(string tag){
	deque<string> res;
	string t, x;
	for (auto i : tag.substr(1)){
		if (isalpha(i)) t += " ";
		t += i;
	}
	stringstream ss(t);
	while (ss >> x)
		res.push_back(x);
	return res;
}

Tree & get_tree(deque<string> road, Tree & cur){
	if (road.empty()) return cur;
	Tree & v = cur.next[find_tree(road.front(), cur)];
	road.pop_front();
	return get_tree(road, v);
}

void get_num(Tree & t, const string ID, int & num, double & sc){
	for (auto i = t.pid.begin(); i != t.pid.end(); ++i){
		if (count(i->second.begin(), i->second.end(), ID)){
			++num;
			double add = add_score / i->second.size();
			sc += (fix_score + (add >= fazhi ? add : 0));
		}
	}
}


void put_statistics()
{
	ofstream out("result\\" + file_name + "_statistic.csv");
	if (!out) { cerr << "CSV统计文件创建失败!" << endl; return; }
	out << "姓名,专业,UVaID";
	for (auto it = dict.begin(); it != dict.end(); ++it)
		out << "," << it->first << "," << "分数";
	out << endl;

	for (auto i = user.begin(); i != user.end(); ++i){
		out << i->name << "," << i->major << "," << i->ID;
		for (auto j = dict.begin(); j != dict.end(); ++j){
			int sum = 0; double score = 0;
			for (auto k = j->second.begin(); k != j->second.end(); ++k){
				int num = 0; double sc = 0.0;
				Tree & t = get_tree(decode_tag(*k), root);
				get_num(t, i->ID, num, sc);
				sum += num; score += sc;
			}
			out << "," << sum << "," << score;
		}
		out << endl;
		printf("   %s：算分完毕\n", i->name.c_str());
	}

	out.close();
	cout << "统计完毕，统计文件已经打开！" << endl;
	system(string("start result\\" + file_name + "_statistic.csv").c_str());
}
