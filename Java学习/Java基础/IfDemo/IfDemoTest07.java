package IfDemo;

import java.util.Scanner;

public class IfDemoTest07 {
    public static void main(String[] args) {
        /*
        键盘录入任意三个大于 0 的小数，判断这三个数值构成什么类型的三角形？
        需要判断的类型如下：
        等边、等腰、直角、普通、无效
        三角形的构成条件，任意两边之和大于第三边
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入三个大于 0 的小数，判断它们是否能构成三角形：");
        double a = sc.nextDouble();
        double b = sc.nextDouble();
        double c = sc.nextDouble();
        if (a + b <= c || a + c <= b || b + c <= a) {
            System.out.println("这三个数值不能构成三角形！\n");
            sc.close();
            return;
        }
        if (a == b && b == c) {
            System.out.println("这三个数值构成等边三角形！\n");
        } else if (a == b || a == c || b == c) {
            System.out.println("这三个数值构成等腰三角形！\n");
        } else if (a * a + b * b == c * c || a * a + c * c == b * b || b * b + c * c == a * a) {
            System.out.println("这三个数值构成直角三角形！\n");
        } else {
            System.out.println("这三个数值构成普通三角形！\n");
        }
        sc.close();
    }
}
