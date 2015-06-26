#ifndef HEAD_H
#define HEAD_H

#include <algorithm>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <set>
#include <map>
#include <deque>
#include <iterator>
#include <iostream>
#include <numeric>
#include <sstream>
#include <vector>
using namespace std;

struct stu{
	string ID, name, user_name, major;
};
struct Tree{
	string cur;
	map<int, vector<string>> pid;
	vector<Tree> next;
};
extern Tree root;
extern vector<pair<string, vector<string>>> dict;
extern vector<stu> user;
extern double fix_score, add_score, fazhi;
extern string file_name;

void config_score();
void config_chapter();
void put_statistics();
void put_uhunt(const string output_file_name);
void read_uhunt();
void init_user();
void files_std();
void put_accnt(const string output_file_name);
void put_commend(const string output_file_name);
int find_tree(string next_name, Tree & u);

#endif // HEAD_H
