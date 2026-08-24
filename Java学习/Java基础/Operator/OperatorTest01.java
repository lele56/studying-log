package Operator;

import java.util.Scanner;

public class OperatorTest01 {
    public static void main(String[] args) {
        /*
        需求：键盘录入一个三位数，将其拆分为个位、十位、百位数字，打印在控制台
        */
        // 创建一个 Scanner 对象，用于从键盘录入数据
        Scanner sc = new Scanner(System.in);
        // 循环录入数据，直到用户输入 0 退出
        while (true) {
            System.out.println("请输入一个三位数（输入 0 退出）：");
        
            // 防止用户输入字母导致报错
            // hasNextInt() 方法用于检查输入是否为整数
            if (sc.hasNextInt()) {
                int num = sc.nextInt();

                // 退出条件
                if (num == 0) {
                    System.out.println("程序退出。");
                    break;
                }
                
                // 检验：确保是三位数
                if (num < 100 || num > 999) {
                    System.out.println("输入错误！请输入 100-999 之间的数字。");
                    continue;
                }

                int[] digits = SplitDigits(num);
                System.out.println("个位数字：" + digits[0]);
                System.out.println("十位数字：" + digits[1]);
                System.out.println("百位数字：" + digits[2]);
            } else{
                System.out.println("请输入有效的整数！");
                // next() 方法用于获取下一个输入项，包括空格、制行符等
                sc.next();
            }
        }
        sc.close();
    }

    // 定义一个方法，用于将一个三位数拆分为个位、十位、百位数字
    public static int[] SplitDigits(int num) {
        int ones = num % 10;          // 个位：123 % 10 = 3
        int tens = (num / 10) % 10;   // 十位：123 / 10 = 12, 12 % 10 = 2
        int hundreds = (num / 100) % 10;     // 百位：123 / 100 = 1, 1 % 10 = 1
        return new int[]{ones, tens, hundreds};
    }
}

