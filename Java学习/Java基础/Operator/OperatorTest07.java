package Operator;

import java.util.Scanner;

public class OperatorTest07 {
    public static void main(String[] args) {
        /*
        三元运算符：
        格式：
            条件 ? 表达式1 : 表达式2;
            如果条件为 true，执行表达式1；否则执行表达式2。
            
        需求：
            键盘录入两个整数，获取其中的较大值。
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入第一个整数：");
        int a = sc.nextInt();
        System.out.println("请输入第二个整数：");
        int b = sc.nextInt();

        // 如果 a 大于 b，max 为 a；否则 max 为 b
        int max = a > b ? a : b;
        System.out.println("较大值为：" + max);
        sc.close();
    }
}
