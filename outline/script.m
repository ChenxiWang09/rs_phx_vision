query_path='C:\wrs-cx\wcx\outline\data\query12.27\rs\rotate_6.pgm';
template_path='C:\wrs-cx\wcx\outline\data\temp_outline\';
candidate_amount=5;
%box for 4 
% x1=30; x2=189; y1=47; y2=206;
%box for 5
% x1=9; x2=71; y1=3; y2=171;
%box for 8
% x1=8; y1= 9; x2=152; y2=107;
%box for 8 rotate
x1=48; y1=60; x2=140; y2=248;
threshold_of_size=1;
[detection]=chamfermatching_nopic_forpython(query_path,template_path,candidate_amount, x1,x2,y1,y2,threshold_of_size)