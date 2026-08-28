package LoopWhile;

import java.util.Scanner;

public class WhileDome04 {
    public static void main(String[] args) {
        /*
        描述：
        给定一个整数 n，请计算其所有位数之和。若 n 是负数，请先取其绝对值。
        
        示例 1：
        输入：12
        说明：1 + 2 = 3
        输出：3
        
        示例 2：
        输入：-305
        说明：获取绝对值 305，再求和 3 + 0 + 5 = 8
        输出：8
        */
        // 输入一个整数
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入一个整数：");
        int num = sc.nextInt();

        // 取绝对值
        num = Math.abs(num);

        // 计算所有位数之和
        int sum = 0;
        while (num != 0) {
            sum += num % 10;
            num /= 10;
        }
        System.out.println("该整数的所有位数之和为：" + sum);
        sc.close();
    }
}

// 输入：-405
// 输出结果
// 该整数的所有位数之和为：9
