package Operator;

import java.util.Scanner;

public class OperatorTest06 {
    public static void main(String[] args) {
        /*
        需求：
            寻找7的有缘数，定义一个两位整数，只要该数字包含7或者是7的倍数，就是7的有缘数
        */
       Scanner sc = new Scanner(System.in);
       System.out.println("请输入一个两位整数：");
       int num = sc.nextInt();
       if (num < 10 || num > 99) {
           System.out.println("输入的两位整数有误");
           sc.close();
           return;
       }
       int a = num / 10;
       int b = num % 10;
       if (a == 7 || b == 7 || num % 7 == 0) {
           System.out.println("7的有缘数");
       } else {
           System.out.println("不是7的有缘数");
       }
       sc.close();
    }
}
