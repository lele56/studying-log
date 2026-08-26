package IfDemo;

import java.util.Scanner;

public class IfDemoTest04 {
    public static void main(String[] args) {
        /*
        卡拉兹函数（Collatz conjecture）定义如下：
            给定正整数 n,
                若 n 是奇数，则 f(n) = 3n + 1
                若 n 是偶数，则 f(n) = n / 2
        示例 1：
            输入：1
            说明：奇数，所以 f(1) = 3 * 1 + 1 = 4
        示例 2：
            输入：2
            说明：偶数，所以 f(2) = 2 / 2 = 1
        */
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("请输入一个正整数（输入 0 退出）：");

            if (sc.hasNextInt()) {
                int n = sc.nextInt();
                // 退出循环
                if (n == 0){
                    break;
                }
                // 输入校验
                if (n < 0){
                    System.out.println("输入的整数不能为负数，请重新输入！");
                    continue;
                }
                
                System.out.println("卡拉兹函数结果：" + n + " ->：" + collatz(n));
            } else {
                System.out.println("输入无效，请输入整数！");
                sc.next(); // 清除无效输入
            }

        }
        sc.close();
    }

    public static int collatz(int n) {
        if (n % 2 == 0) {
            return n / 2;
        } else {
            return 3 * n + 1;
        }
    }
}
