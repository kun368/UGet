cls
clear screen

sub problem_num
show all our users' submission on specified problem, in time order.
eg : show 11111

cmp problem_num
sort our users' best submission on specified problem.
eg : cmp 310

us user_name
show one user's all submission, and force update cache file.
note that user_name may contain spaces, but Chinese not supported yet.
eg : us liujuan

load csv_file_with_no_extension
load a problem analyze tree from file.
lrj.csv is loaded by default.
eg : load lrj

ana user_id [class_id]
analyze one user
eg : ana 84786
eg : ana 121567 Lists

anaf user_list_file
analyze a group of users
eg : anaf ucmp.txt

