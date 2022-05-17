clc
clear
tic

[A,R] = readgeoraster('beijing.tif'); % 打开tiff文件
[lines,rows,bands] = size(A); % 读取遥感影像的结构
data = []; % 存储数据，n*p维，n表示样本数，p表示特征，譬如这里特征为7，每个像元都有7个波段
for i = 1:bands % 循环读取每个波段
    data = [data reshape(A(:,:,i),lines*rows,1)]; % 对波段降维
end
data = double(data); % 转为双精度浮点，便于kmeans函数计算
band1 = A(:,:,1); % 读取波段，观察上述过程改变矩阵维度是否正确
band2 = A(:,:,2);
band3 = A(:,:,3);
% 使用kmeans算法聚类，Idx是聚类后的结果，C为质心位置，sumD为该类所有点与质心的距离之和，D为该类的点与质心的距离
% 采用欧氏距离作为距离评判标准，一共分为6类，迭代3次，rep = Replicates 即重复聚类次数（可以理解为重复程序多次取平均）
[Idx,C,sumD,D] = kmeans(data,6,'dist','sqEuclidean','rep',3); 
% Idx为m个整数，且属于1到K之间的数；sumD为1*K的和向量，存储的是类内所有点与该类质心点距离之和；
result = reshape(Idx,lines,rows); % 把样本对应的编号对应到遥感图像上
imagesc(result); % 显示聚类结果
title('kmeans聚类结果');
imwrite(result,'Kmeans.png');  % 输出新图像
% tabulate 是Frequency table函数，显示向量中存在的数及其占比
tabulate(Idx(:)) % 显示各类别的像元总数及所占的百分比
hAxes = gca;
colormap(hAxes , [207/255 165/255 35/255; 170/255 251/255 164/255; 1 1 1;73/255 157/255 250/255; 1 0 0; 32/255 121/255 63/255] )
c = colorbar;
c.Ticks = [1,2,3,4,5,6];

toc % 统计时间