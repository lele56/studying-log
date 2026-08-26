package IfDemo;

import java.util.Scanner;

public class IfDemoTest05 {
    public static void main(String[] args) {
        /*
        需求：很多 app 都有不同的优惠卷
        假设，现在有以下优惠卷
            全场商品满 10 减 8
            全场商品满 50 减 30
            全场商品满 100 减 50
            全场商品满 200 减 90

            会员卡：全场 8 折

        请问：会员卡和优惠卷不能同时使用，最优惠的价格是多少？
        */
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.println("请输入商品的价格（输入 0 退出）：");
            double price = sc.nextDouble();
            if (price == 0) {
                System.out.println("感谢使用，再见！");
                break;
            }
            if (price < 0) {
                System.out.println("价格不能为负数，请重新输入！\n");
                continue;
            }
            double minPrice = caculatePrice(price);
            System.out.println("最优惠的价格是：" + minPrice + "\n");
        }
        sc.close();
    }

    public static double caculatePrice(double price) {
        double memberPrice = price * 0.8;
        double discountPrice = price;
        
        // 从高到低判断优惠卷
        if (price >= 200) {
            discountPrice -= 90;
        } else if (price >= 100) {
            discountPrice -= 50;
        } else if (price >= 50) {
            discountPrice -= 30;
        } else if (price >= 10) {
            discountPrice -= 8;
        }
        /*
        if (price < 10) {
            discountPrice = price;          // 不满10元，无优惠
        } else if (price < 50) {
            discountPrice -= 8;             // 满10减8
        } else if (price < 100) {
            discountPrice -= 30;            // 满50减30
        } else if (price < 200) {
            discountPrice -= 50;           // 满100减50
        } else {
            discountPrice -= 90;            // 满200减90
        }
        */
        return Math.min(memberPrice, discountPrice);
    }
}
