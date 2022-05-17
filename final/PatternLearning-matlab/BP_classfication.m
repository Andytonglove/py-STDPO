clear;
clc;

% 读入样本图像ROI
exa=imread('beijing-example.tif'); % beijing-roi.png
  % 将样本图像降维
  Re=exa(:,:,1);
  Ge=exa(:,:,2);
  Be=exa(:,:,3);
  % 将灰度值归一化处理
  Re=im2double(Re);
  Ge=im2double(Ge);
  Be=im2double(Be);
  [Me,Ne]=size(Re);
  Pe=[Re;Ge;Be];
  % 处理成单波段123
  exaMt=uint8(zeros(Me,Ne));
  exaMt=exaMt+(exa(:,:,1)/255)*1;
  exaMt=exaMt+(exa(:,:,2)/255)*2;
  exaMt=exaMt+(exa(:,:,3)/255)*3;
  
% 读入待分类遥感图像
I=imread('beijing-band3.tif');
  % 将彩色图像降维
  R=I(:,:,1);
  G=I(:,:,2);
  B=I(:,:,3);
  % 将灰度值归一化处理
  R=im2double(R);
  G=im2double(G);
  B=im2double(B);
  [M,N]=size(R);
  P=[R;G;B];

a1=1;a2=1;a3=1;
for i = 1 : M
    for j = 1 : N
        if (exaMt(i,j)==1)
            T1(:,a1) = I(i,j,:);
            a1=a1+1;
        elseif (exaMt(i,j)==2)
            T2(:,a2) = I(i,j,:);
            a2=a2+1;
        elseif (exaMt(i,j)==3)
            T3(:,a3) = I(i,j,:);
            a3=a3+1;
        end
    end
end

T1 = im2double(T1);
T2 = im2double(T2);
T3 = im2double(T3);

P=[T1,T2,T3];    % 样区数据
T=[];     % 标记结果
TT=[0;0;0];
T=concur(TT,a1-1);
TT=[0.4;0.7;0.7];
TT=concur(TT,a2-1);
T=[T,TT];
TT=[0.6;0.7;0.4];
TT=concur(TT,a3-1);
T=[T,TT];                    

% 建立BP网络，中间层8，输出层3，tansig、purelin分别为中间层、输出层的转换函数，
 echo on
 net=newff(minmax(P),[8,3],{'tansig','purelin'},'trainlm');  
 clc
    % 设置训练参数
    net.trainparam.show=50;        
    net.trainParam.epochs=1000;
    net.trainParam.goal=1e-4;
    net=init(net); % 重新初始化
    [net,tr]=train(net,P,T); 

A4=imread('beijing-band3.tif');
A4=im2double(A4); % 将各波段的灰度值类型转换为人工神经网络可用的类型
RB=A4(:,:,1); % 提取出图像红色波段的灰度值，下面依次为绿、蓝
GB=A4(:,:,2);
BB=A4(:,:,3);
%初始化三个矩阵，确定图像的行数和列数
[m,n]=size(RB);
RB1=reshape(RB,1,n*m);
GB1=reshape(GB,1,m*n);
BB1=reshape(BB,1,m*n);

X=[RB1;GB1;BB1];
OUT=sim(net,X);
IN=sim(net,X); 

clc
[m,n]=size(RB);
r1=OUT(1,:);%将数据还原成原始图像的rgb行列格式
r1=reshape(r1,m,n);
g1=OUT(2,:);
g1=reshape(g1,m,n);
b1=OUT(3,:);
b1=reshape(b1,m,n);
r2=IN(1,:); % 将数据还原成原始图像的rgb行列格式
r2=reshape(r2,m,n);
g2=IN(2,:);
g2=reshape(g2,m,n);
b2=IN(3,:);
b2=reshape(b2,m,n);
R=[];
G=[];
B=[];
for i=1:m
    for j=1:n
        if r1(i,j)<0.9
            R(i,j)=r1(i,j);
            G(i,j)=g1(i,j);
            B(i,j)=b1(i,j);
        else
            R(i,j)=r2(i,j);
            G(i,j)=g2(i,j);
            B(i,j)=b2(i,j);
        end
    end
end
Rr=abs(R)*255; % 还原成图像格式
Gg=abs(G)*255;
Bb=abs(B)*255;
Rr=uint8(Rr);
Gg=uint8(Gg);
Bb=uint8(Bb);
RGB=cat(3,Rr,Gg,Bb);

clc
imshow(RGB);
title('BP神经网络分类');