package LoopFor;

import java.util.Scanner;

public class ForDemo04 {
    public static void main(String[] args) {
        /*
        需求：键盘录入两个数字，表示一个范围。
              统计这个范围中
              既能被 3 整除，又能被 5 整除数字有多少个。
        */
        int count = 0;
        // 输入两个数
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入第一个数字：");
        int num1 = sc.nextInt();
        System.out.println("请输入第二个数字：");
        int num2 = sc.nextInt();

        // 确认两个数大小
        int start = num1 > num2 ? num2 : num1;
        int end = num1 > num2 ? num1 : num2;

        // 统计范围中能被3和5整除的数字个数
        for (int i = start; i <= end; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                count++;
            }
        }
        System.out.println("在" + start + "到" + end + "之间，既能被3整除，又能被5整除的数字有" + count + "个");
        sc.close();
    }
}
