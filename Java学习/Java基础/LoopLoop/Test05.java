package LoopLoop;

public class Test05 {
    public static void main(String[] args) {
        /*
        打印九九乘法表
        */
        for (int i = 1; i <= 9; i++) {
            for (int j = 1; j <= i; j++) {
                // \t 表示制表符，用于对齐输出
                // 真正的含义是：
                // 在前面的字符后面 补 1~4 个空格，让这个整体的长度凑成 4 的整数倍
                System.out.printf("%d * %d = %2d\t", j, i, i * j);
            }
            System.out.println();
        }
    }
}