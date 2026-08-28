package LoopFor;

import java.util.Scanner;

public class ForDemo06 {
    public static void main(String[] args) {
        /*
        描述
        小试试开始学习数列。它想计算以下数列前 n 项的和：
        S(n) = 1 - 2 + 3 - 4 + ...

        示例 1：
        输入：4
        说明：S(4) = 1 - 2 + 3 - 4 = -2
        输出：-2
        */
        // 键盘录入一个数据，表示循环的范围 n
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入一个数字：");
        int num = sc.nextInt();

        // 计算数列的和
        int sum = 0;
        for (int i = 1; i <= num; i++) {
            // 偶数项为负数，奇数项为正数
            sum += (i % 2 == 0 ? -i : i);
        }
        System.out.println("S(" + num + ") = " + sum);
        sc.close();
    }
}
