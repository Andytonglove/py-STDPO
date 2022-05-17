% 最小马氏距离分类器，可以实现交互式选取图像样本分类数据进行分类
[file,path]=uigetfile({'*.jpg;*.bmp;*.tif;*.png;*.gif','All Image Files';'*.*','All Files'}); % 动态打开文件
image = imread([path,file]);%读取
figure(1);
imshow(image);
image=double(image);
[m,n,bands]=size(image);
k=input('请输入要分类的种类:  '); % 输入要选取的样本类别数
ave=zeros(k,bands); % 申请矩阵空间，用于存储样本数据各类别各波段均值
% 对所选取样本数据进行处理求得各类别均值
for i=1:k % 对选中类别循环
    str=['请在屏幕图像上选择第',num2str(i),'种分类样本,选择完毕请回车确定'];
    disp(str);
    [y,x]=getpts; % 从图像上获取数据点
    A=[round(y),round(x)];
    for band=1:bands % 对图像每个波段进行计算，求取指定类别每个波段均值
        Sum=0;
         for count=1:size(A,1) % 对取得点循环
             temp=image(:,:,band);
            Sum=Sum+temp(A(count,2),A(count,1));
         end
          ave(i,band)=Sum/size(A,1); % 求均值
    end
end
image=reshape(image,m*n,bands); % 将图像数据重塑成为一列为一个波段数据的形式，便于计算
dis=zeros(k,m*n); % 申请矩阵空间存储每个类别图像各个点数据分别到各波段均值的距离的和
% 申请矩阵存储样本数据均值协方差
T=zeros(bands,bands,k);
for t=1:k
	T(:,:,t)=cov(ave);%求取协方差
	tem=image-ave(t,:);
	dis(t,:)=sqrt(sum((tem*T(:,:,t).*tem).'));  %同上
end
[~,index]=min(dis); % 求各距离最小值
index=reshape(index,m,n); % 重塑回原图像排列
re=index/k; % 给各类别赋值指定灰度值便于区分
% 调用灰度转彩色映射到rgb
rgbIamge=gray2rgb(re);
figure(2);
imshow(rgbIamge); % 显示彩色