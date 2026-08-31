package LoopLoop;

import java.util.Scanner;

public class Test02 {
    public static void main(String[] args) {
        /*
        打印正三角形和倒三角形
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入行数：");
        int rows = sc.nextInt();
        for (int i = 1; i <= rows; i++) {
            System.out.println("*".repeat(i));
        }
        // 打印倒三角形
        for (int i = rows - 1; i >= 1; i--) {
            System.out.println("*".repeat(i));
        }
        sc.close();
    }
}
