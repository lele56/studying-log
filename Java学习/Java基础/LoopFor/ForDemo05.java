package LoopFor;

import java.util.Scanner;

public class ForDemo05 {
    public static void main(String[] args) {
        /*
        有一组特殊的数字，从第三项开始，每一项都是前两项的数字和
        0，1，1，2，3，5，8，13，21
        */
        Scanner sc = new Scanner(System.in);
        
        while (true) {
            System.out.println("请输入一个数字（输入 -1 退出）：");
            
            // 输入校验
            if (!sc.hasNextInt()) {
                System.out.println("请输入有效的整数！\n");
                sc.next();
                continue;
            }
            
            int num = sc.nextInt();
            
            // 退出循环
            if (num == -1) {
                System.out.println("感谢使用，再见！");
                break;
            }
            
            // 输入校验
            if (num < 0) {
                System.out.println("请输入一个非负整数！\n");
                continue;
            }
            
            printFibonacci(num);
            System.out.println();
        }
        
        sc.close();
    }

    public static void printFibonacci(int n) {
        int a = 0;
        int b = 1;
        
        if (n == 0) {
            System.out.print(a);
            return;
        }
        
        System.out.print(a + ", " + b);
        
        for (int i = 2; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
            System.out.print(", " + c);
        }
    }
}