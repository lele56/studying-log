package IfDemo;

import java.util.Scanner;

public class IfDemoTest03 {
    public static void main(String[] args) {
        /*
        需求：小明在每次订外卖都会在多家平台对比，看谁的优惠力度更大
        
        已知：
            饱了么 App：全场 9 折优惠
            美单 App：满 30 减 10
            
        请问 1：
            小明买了一吨烧烤50元，在哪家下单更划算
        请问 2：
            如果价格不确定，数据由键盘录入而来呢？
        */
        Scanner sc = new Scanner(System.in);
        
        while (true) {
            System.out.println("请输入烧烤的价格（输入 0 退出）：");
            
            try {
                double price = sc.nextDouble();
                
                // 退出循环
                if (price == 0) {
                    System.out.println("感谢使用，再见！");
                    break;
                }
                
                // 输入校验
                if (price < 0) {
                    System.out.println("价格不能为负数，请重新输入！\n");
                    continue;
                }
                
                String result = comparePrice(price);
                System.out.println("在 " + result + " 下单更划算\n");
                
            } catch (java.util.InputMismatchException e) {
                System.out.println("输入格式错误，请输入有效的数字！\n");
                sc.next();
            }
        }
        
        sc.close();
    }

    public static String comparePrice(double price) {
        double baoLeMe = price * 0.9;
        double meiDan = price - 10;
        
        // 美单的满减条件
        if (price < 30) {
            return "饱了么 App"; // 美单不满足满减条件
        }

        // 使用差值比较，避免浮点数精度问题
        double diff = baoLeMe - meiDan;
        if (Math.abs(diff) < 0.01) {
            return "两家平台价格相同";
        } else if (diff > 0) {
            return "美单 App";
        } else {
            return "饱了么 App";
        }
    }
}