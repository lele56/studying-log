package LoopWhile;

public class WhileDome01 {
    public static void main(String[] args) {
        /*
        利用 while 循环，实现游戏中连续跳跃10次，用输出语句模拟跳跃的逻辑

        格式：
            初始化语句：
            while（条件判断语句）{
                循环体
                条件控制语句
            }
        */
        int i = 0;
        while (i < 10) {
            System.out.println("跳跃" + (i + 1) + "次");
            i++;
        }
    }
}
