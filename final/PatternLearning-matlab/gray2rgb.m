% 将灰度图像转为彩色图像
function I = gray2rgb(X)
R = redTransformer(X);
G = greenTransformer(X);
B = blueTransformer(X);
I(:,:,1) = R;
I(:,:,2) = G;
I(:,:,3) = B;
I = uint8(I);
end
% 红色通道映射函数
function R = redTransformer(X)
R = zeros(size(X));
X=X*180;
R(X < 128) = 30;
R(128 <= X & X < 192) = 2*X(128 <= X & X < 192)-150;
R(192 <= X) = 234;
end
% 绿色通道映射函数
function G = greenTransformer(X)
G = zeros(size(X));
X=X*180;
G(X < 90) = 2*X(X < 90)+40;
G(90 <= X & X < 160) = 180;
G(160 <= X) = 0;
end
% 蓝色通道映射函数
function B = blueTransformer(X)
B = zeros(size(X));
X=X*180;
B(X < 64) = 115;
B(64 <= X & X < 128) = 510-4*X(64 <= X & X < 128);
B(128 <= X) = 36;
end