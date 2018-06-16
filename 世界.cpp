//snow_dll
#define 导出 extern "C" __declspec(dllexport)
#include <map>
#include <iostream>
#include <algorithm>
using namespace std;

typedef tuple<int,int,int> t3;
typedef tuple<int,int> t2;
typedef unsigned char uchar;

void 画顶(uchar id,int x,int y,int z); 
void 画底(uchar id,int x,int y,int z); 
void 画前(uchar id,int x,int y,int z); 
void 画后(uchar id,int x,int y,int z); 
void 画左(uchar id,int x,int y,int z); 
void 画右(uchar id,int x,int y,int z); 


int dv(int a, int b){
    if(a>=0)
        return a/b;
    return -((-a-1)/b+1);
}
int md(int a, int b){
    if(a>=0)
        return a%b;
    return (a+1)%b+b-1;
}
int between(int x,int a,int b){
    return x>a and x<b;
}

class 缓冲{public:
    float*内容=NULL; 
    int 长度=0;
};
缓冲 顶点缓冲区;
缓冲 纹理缓冲区;
缓冲 颜色缓冲区;

void 加入缓冲区(缓冲&缓冲区,initializer_list<float> lst){
    for(auto i:lst){
        缓冲区.内容[缓冲区.长度]=i;
        缓冲区.长度++;
    }
}
void f(float l){
    加入缓冲区(颜色缓冲区,
              {l, l, l,
               l, l, l,
               l, l, l,
               l, l, l});
}
void 写颜色(float a,float b,float c,float d){
    a=pow(a,0.7);
    b=pow(b,0.7);
    c=pow(c,0.7);
    d=pow(d,0.7);
    加入缓冲区(颜色缓冲区,
             {a,a,a,
              b,b,b,
              c,c,c,
              d,d,d});
}
class 区块{public:
    uchar a[16][16][16]={{{0}}};
    bool 最新=true;
    区块(int 默认值=0){
        for(uchar x=0;x<16;x++)
            for(uchar y=0;y<16;y++)
                for(uchar z=0;z<16;z++)
                    a[x][y][z]=默认值;
    }
};
class 世界{public:
    map<t3,区块> 块索引;
    map<t3,区块> 亮度索引;
    map<t2,int> 顶记录;
    int 下界=-16;
    世界(){
    }
    t3 键(int x,int y,int z){
        return t3(dv(x,16),dv(y,16),dv(z,16));
    }
    uchar& 块(int x,int y,int z){
        t3 key=键(x,y,z); 
        if(块索引.find(key)==块索引.end())
            块索引[key]=区块(0);
        return 块索引[key].a[md(x,16)][md(y,16)][md(z,16)];
    }    
    uchar& 亮度(int x,int y,int z){
        t3 key=键(x,y,z);
        if(亮度索引.find(key)==亮度索引.end())
            亮度索引[key]=区块(15);
        return 亮度索引[key].a[md(x,16)][md(y,16)][md(z,16)];
    }    
    int& 顶(int x,int y){
        t2 key=t2(x,y);
        if(顶记录.find(key)==顶记录.end())
            顶记录[key]=下界-1;
        return 顶记录[key];
    }
    void 更新顶(int x,int y){
        for(int i=顶(x,y);i>=下界;i--){
            if(存在(x,y,i)){
                顶(x,y)=i;
                return;
            }
        }
        顶(x,y)=下界-1;
    }
    bool 存在(int x,int y,int z){
        auto key=键(x,y,z);
        if(块索引.find(key)==块索引.end()){
            块索引[key]=区块(0);
            亮度索引[key]=区块(15);
            return false;
        }
        return 块(x,y,z)>0;
    }
    void 放块(int x,int y,int z,int 块号){
        if(存在(x,y,z))
            return ;
        if(顶(x,y)<z)
            顶(x,y)=z;
        块(x,y,z)=块号;

        亮度(x,y,z)=0;

        // 优化，因为侧面的天光块不受降低影响，亮度为0的块不可能此时被更新
        // 好像不对劲2333
        if((0<亮度(x,y,z-1) or
            between(0<亮度(x,y,z+1),0,15) or
            between(0<亮度(x,y+1,z),0,15) or
            between(0<亮度(x,y-1,z),0,15) or
            between(0<亮度(x+1,y,z),0,15) or
            between(0<亮度(x-1,y,z),0,15)))
            更新周边亮度(x,y,z);
        绘图重置(x,y,z);
    }
    uchar 去块(int x,int y,int z){
        if(not 存在(x,y,z))
            return 0;
        uchar t=块(x,y,z);
        块(x,y,z)=0;
        if(顶(x,y)==z)
            更新顶(x,y);
        更新亮度(x,y,z);
        绘图重置(x,y,z);
        return t;
    }
    void 更新亮度(int x,int y,int z){
        if(存在(x,y,z)) 
            return ; 
        if(not(下界<=z and z<=128))
            return ;

        int t;
        if(顶(x,y)<z)
            t=15;
        else
            t=max({
                uchar(1),
                亮度(x,y,z+1),
                亮度(x,y,z-1),
                亮度(x,y+1,z),
                亮度(x,y-1,z),
                亮度(x+1,y,z),
                亮度(x-1,y,z)
            })-1;
        int 原亮度=亮度(x,y,z); 
        if(原亮度!=t){
            亮度(x,y,z)=t;
            更新周边亮度(x,y,z);
            绘图重置(x,y,z);
        }
    }
    void 更新周边亮度(int x,int y,int z){
        更新亮度(x,y,z+1); 
        更新亮度(x,y,z-1); 
        更新亮度(x,y+1,z); 
        更新亮度(x,y-1,z); 
        更新亮度(x+1,y,z); 
        更新亮度(x-1,y,z); 
    }
    void 绘图重置(int x,int y,int z){
        for(int dx=-1;dx<=1;dx++)
            for(int dy=-1;dy<=1;dy++)
                for(int dz=-1;dz<=1;dz++){
                    auto key=键(x+dx,y+dy,z+dz);
                    块索引[key].最新=false;
                }
    }
    int 导出顶点组(t3 key, float*顶点,float*颜色,float*纹理){
        块索引[key].最新=true;
        顶点缓冲区.内容=顶点;
        顶点缓冲区.长度=0;
        颜色缓冲区.内容=颜色;
        颜色缓冲区.长度=0;
        纹理缓冲区.内容=纹理;
        纹理缓冲区.长度=0;
        auto [ox,oy,oz] = key;
        ox*=16; oy*=16; oz*=16;
        int x,y,z,id;
        for(int dx=0;dx<16;dx++)
            for(int dy=0;dy<16;dy++)
                for(int dz=0;dz<16;dz++){
                    x=ox+dx, y=oy+dy, z=oz+dz;
                    if(not 存在(x,y,z)) continue;
                    id=块(x,y,z);
                    if(not 存在(x,y,z+1)) 画顶(id,x,y,z);
                    if(not 存在(x,y,z-1)) 画底(id,x,y,z);
                    if(not 存在(x,y+1,z)) 画前(id,x,y,z);
                    if(not 存在(x,y-1,z)) 画后(id,x,y,z);
                    if(not 存在(x+1,y,z)) 画左(id,x,y,z);
                    if(not 存在(x-1,y,z)) 画右(id,x,y,z);
        }
        return 顶点缓冲区.长度;
    }
};

世界 主世界;

void tex(int x,int y,int 面,int id){
    x=x*16+面*16;
    y=y*16+(id-2)*16;
    y=512-y;
    加入缓冲区(纹理缓冲区, {x/128.0,y/512.0});
}

void 画顶(uchar id,int x,int y,int z){
    加入缓冲区(顶点缓冲区,
              {0+x, 0+y, 1+z,
               1+x, 0+y, 1+z,
               1+x, 1+y, 1+z,
               0+x, 1+y, 1+z});
    uchar a00=主世界.亮度(x-1,y-1,z+1);
    uchar a01=主世界.亮度(x-1,y,z+1);
    uchar a02=主世界.亮度(x-1,y+1,z+1);
    uchar a10=主世界.亮度(x,y-1,z+1);
    uchar a11=主世界.亮度(x,y,z+1);
    uchar a12=主世界.亮度(x,y+1,z+1);
    uchar a20=主世界.亮度(x+1,y-1,z+1);
    uchar a21=主世界.亮度(x+1,y,z+1);
    uchar a22=主世界.亮度(x+1,y+1,z+1);
    float a=(a00+a01+a11+a10)/60.0,
          b=(a10+a11+a20+a21)/60.0,
          c=(a11+a12+a21+a22)/60.0,
          d=(a01+a02+a11+a12)/60.0;
    写颜色(a,b,c,d);
    tex(0,0, 0,id);
    tex(0,1, 0,id);
    tex(1,1, 0,id);
    tex(1,0, 0,id);
}
void 画底(uchar id,int x,int y,int z){
    加入缓冲区(顶点缓冲区,
              {0+x, 0+y, 0+z,
               0+x, 1+y, 0+z,
               1+x, 1+y, 0+z,
               1+x, 0+y, 0+z});
    float l=float(主世界.亮度(x,y,z-1)+1)/16;
    f(l);
    tex(1,0, 5,id);
    tex(1,1, 5,id);
    tex(0,1, 5,id);
    tex(0,0, 5,id);
}
void 画前(uchar id,int x,int y,int z){
    加入缓冲区(顶点缓冲区,
              {0+x, 1+y, 0+z,
               0+x, 1+y, 1+z,
               1+x, 1+y, 1+z,
               1+x, 1+y, 0+z});
    uchar a00=主世界.亮度(x-1,y+1,z-1);
    uchar a01=主世界.亮度(x-1,y+1,z+0);
    uchar a02=主世界.亮度(x-1,y+1,z+1);
    uchar a10=主世界.亮度(x+0,y+1,z-1);
    uchar a11=主世界.亮度(x+0,y+1,z+0);
    uchar a12=主世界.亮度(x+0,y+1,z+1);
    uchar a20=主世界.亮度(x+1,y+1,z-1);
    uchar a21=主世界.亮度(x+1,y+1,z+0);
    uchar a22=主世界.亮度(x+1,y+1,z+1);
    float a=(a00+a01+a11+a10)/60.0,
          b=(a10+a11+a20+a21)/60.0,
          c=(a11+a12+a21+a22)/60.0,
          d=(a01+a02+a11+a12)/60.0;
    写颜色(a,d,c,b);
    tex(1,1, 1,id);
    tex(1,0, 1,id);
    tex(0,0, 1,id);
    tex(0,1, 1,id);
}
void 画后(uchar id,int x,int y,int z){
    加入缓冲区(顶点缓冲区,
              {0+x, 0+y, 0+z,
               1+x, 0+y, 0+z,
               1+x, 0+y, 1+z,
               0+x, 0+y, 1+z});
    uchar a00=主世界.亮度(x-1,y-1,z-1);
    uchar a01=主世界.亮度(x-1,y-1,z+0);
    uchar a02=主世界.亮度(x-1,y-1,z+1);
    uchar a10=主世界.亮度(x+0,y-1,z-1);
    uchar a11=主世界.亮度(x+0,y-1,z+0);
    uchar a12=主世界.亮度(x+0,y-1,z+1);
    uchar a20=主世界.亮度(x+1,y-1,z-1);
    uchar a21=主世界.亮度(x+1,y-1,z+0);
    uchar a22=主世界.亮度(x+1,y-1,z+1);
    float a=(a00+a01+a11+a10)/60.0,
          b=(a10+a11+a20+a21)/60.0,
          c=(a11+a12+a21+a22)/60.0,
          d=(a01+a02+a11+a12)/60.0;
    写颜色(a,b,c,d);
    tex(0,1, 2,id);
    tex(1,1, 2,id);
    tex(1,0, 2,id);
    tex(0,0, 2,id);
}
void 画左(uchar id,int x,int y,int z){
    加入缓冲区(顶点缓冲区,
              {1+x, 0+y, 0+z,
               1+x, 1+y, 0+z,
               1+x, 1+y, 1+z,
               1+x, 0+y, 1+z});
    uchar a00=主世界.亮度(x+1,y-1,z-1);
    uchar a01=主世界.亮度(x+1,y-1,z+0);
    uchar a02=主世界.亮度(x+1,y-1,z+1);
    uchar a10=主世界.亮度(x+1,y+0,z-1);
    uchar a11=主世界.亮度(x+1,y+0,z+0);
    uchar a12=主世界.亮度(x+1,y+0,z+1);
    uchar a20=主世界.亮度(x+1,y+1,z-1);
    uchar a21=主世界.亮度(x+1,y+1,z+0);
    uchar a22=主世界.亮度(x+1,y+1,z+1);
    float a=(a00+a01+a11+a10)/60.0,
          b=(a10+a11+a20+a21)/60.0,
          c=(a11+a12+a21+a22)/60.0,
          d=(a01+a02+a11+a12)/60.0;
    写颜色(a,b,c,d);
    tex(0,1, 3,id);
    tex(1,1, 3,id);
    tex(1,0, 3,id);
    tex(0,0, 3,id);
}
void 画右(uchar id,int x,int y,int z){
    加入缓冲区(顶点缓冲区,
              {0+x, 0+y, 0+z,
               0+x, 0+y, 1+z,
               0+x, 1+y, 1+z,
               0+x, 1+y, 0+z});
    uchar a00=主世界.亮度(x-1,y-1,z-1);
    uchar a01=主世界.亮度(x-1,y-1,z+0);
    uchar a02=主世界.亮度(x-1,y-1,z+1);
    uchar a10=主世界.亮度(x-1,y+0,z-1);
    uchar a11=主世界.亮度(x-1,y+0,z+0);
    uchar a12=主世界.亮度(x-1,y+0,z+1);
    uchar a20=主世界.亮度(x-1,y+1,z-1);
    uchar a21=主世界.亮度(x-1,y+1,z+0);
    uchar a22=主世界.亮度(x-1,y+1,z+1);
    float a=(a00+a01+a11+a10)/60.0,
          b=(a10+a11+a20+a21)/60.0,
          c=(a11+a12+a21+a22)/60.0,
          d=(a01+a02+a11+a12)/60.0;
    写颜色(a,d,c,b);
    tex(1,1, 4,id);
    tex(1,0, 4,id);
    tex(0,0, 4,id);
    tex(0,1, 4,id);
}

导出 void set_block(int x,int y,int z,int 块号){
    主世界.放块(x,y,z,块号);
}
导出 uchar remove_block(int x,int y,int z){
    return 主世界.去块(x,y,z);
}
导出 bool have(int x,int y,int z){
    return 主世界.存在(x,y,z);
}
导出 bool is_new(int x,int y,int z){
    t3 key(x,y,z);
    if(主世界.块索引.find(key)==主世界.块索引.end())
        return true;
    return 主世界.块索引[t3(x,y,z)].最新; 
}
导出 int export_vertex(int x,int y,int z,float*顶点,float*颜色,float*纹理){
    return 主世界.导出顶点组(t3(x,y,z),顶点,颜色,纹理);
}

int main(){
    set_block(3,4,-8,6);
    set_block(0,0,-16,9);

    for(int x=-10;x<16;x++)
        for(int y=-10;y<16;y++)
            for(int z=-10;z<16;z++){
                if (主世界.存在(x,y,z))
                    cout << x << ' ' << y << ' ' << z << endl;
                // cout << 主世界.存在(x,y,z) << endl;
    }
    // int*目标=new int[30000];
    // cout << 主世界.导出顶点组(t3(0,0,0),目标) << endl; 

    // for(int i=0;i<=30;i++)
    //     cout<<目标[i]<<' ';

    // cout << int(主世界.亮度(2,2,-1)) << endl;
    // cout << int(主世界.亮度(0,0,0)) << endl;
    // cout << int(主世界.亮度(0,0,-1)) << endl;
    // cout << int(主世界.亮度(0,0,-5)) << endl;
    // 主世界.放块(1,2,3,9);
    // 主世界.放块(9,9,9,9);
    // 主世界.放块(100,100,-100,9);
}