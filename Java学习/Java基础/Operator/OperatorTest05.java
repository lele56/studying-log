package Operator;

import java.util.Scanner;

public class OperatorTest05 {
    public static void main(String[] args) {
        /*
        需求：
            键盘录入一个四位整数，判断这个数字是否为回文值。
            回文值：1221、1331、2442等
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入一个四位整数：");
        int num = sc.nextInt();
        if (num < 1000 || num > 9999) {
            System.out.println("输入的四位整数有误");
            sc.close();
            return;
        }
        int a = num / 1000;
        int b = num / 100 % 10;
        int c = num / 10 % 10;
        int d = num % 10;
        if (a == d && b == c) {
            System.out.println("回文值");
        } else {
            System.out.println("不是回文值");
        }
        sc.close();
    }
}

