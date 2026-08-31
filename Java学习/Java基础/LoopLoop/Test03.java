package LoopLoop;

import java.util.Scanner;

public class Test03 {
    public static void main(String[] args) {
        /*
        打印菱形
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
            System.out.println(" ".repeat(n - i) + "*".repeat(2 * i - 1));
        }
        
        // 下半部分
        for (int i = n - 1; i >= 1; i--) {
            System.out.println(" ".repeat(n - i) + "*".repeat(2 * i - 1));
        }
        
        sc.close();
    }
}