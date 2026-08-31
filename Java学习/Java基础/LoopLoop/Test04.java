package LoopLoop;

import java.util.Scanner;

public class Test04 {
    public static void main(String[] args) {
        /*
        打印空心菱形
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入菱形的行数（请输入奇数）：");
        int rows = sc.nextInt();
        
        if (rows <= 0) {
            System.out.println("请输入正整数！");
            sc.close();
            return;
        }
        
        if (rows % 2 == 0) {
            System.out.println("菱形行数应为奇数，已自动调整为：" + (rows + 1));
            rows++;
        }
        
        int n = rows / 2 + 1;  // 上半部分行数
        
        // 上半部分
        for (int i = 1; i <= n; i++) {
            printHollowLine(n, i);
        }
        
        // 下半部分
        for (int i = n - 1; i >= 1; i--) {
            printHollowLine(n, i);
        }
        
        sc.close();
    }

    /**
     * 打印空心菱形的单行
     * @param n 菱形上半部分的行数（中间行行号）
     * @param i 当前行的行号（从1开始）
     */
    public static void printHollowLine(int n, int i) {
        if (i == 1) {
            // 第一行只有一个星号，位于最上方
            System.out.println(" ".repeat(n - i) + "*");
        } else {
            // 其他行：左边空格 + 星号 + 中间空格 + 星号
            System.out.println(" ".repeat(n - i) + "*" + " ".repeat(2 * i - 3) + "*");
        }
    }
}