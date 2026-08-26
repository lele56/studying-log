package IfDemo;

import java.util.Scanner;

public class IfDemoTest06 {
    public static void main(String[] args) {
        /*
        计算电费
        用电量计算采取阶梯计费原则，规则如下：
        1. [0 ~ 100] 度，按 0.5 元/度计费
        2. (100 ~ 200] 度，按 0.8 元/度计费
        3. (超过200] 度，按 1.2 元/度计费
        输入变量 usage 表示实际用电量
        输出总电费 cost。
        示例输入：usage = 150
        示例输出：cost = 100 * 0.5 + 50 * 0.8 = 90
        */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入实际用电量（度）：");
        double usage = sc.nextDouble();
        double cost = caculatePrice(usage);
        System.out.println("总电费是：" + cost + "\n");
        sc.close();
    }
    public static double caculatePrice(double usage) {
        double cost = 0;
        if (usage >= 200) {
            cost = 100 * 0.5 + 50 * 0.8 + (usage - 200) * 1.2;
        } else if (usage >= 100) {
            cost = 100 * 0.5 + (usage - 100) * 0.8;
        } else {
            cost = usage * 0.5;
        }
        return cost;
    }
}
