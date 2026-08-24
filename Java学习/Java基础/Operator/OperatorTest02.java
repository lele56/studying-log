package Operator;

import java.util.Scanner;

public class OperatorTest02 {
    public static void main(String[] args) {
        /*
        时间转换
        描述：
            给定秒数 second，将其转换为对应的小时数、分钟数和秒数，使得总时间不变，但是分钟数和秒数不超过 59。
        输入描述：
            在一行中输入一个整数 seconds，表示要转换的秒数，满足 0 <= seconds <= 10^8。
        输出描述：
            一行，包含三个整数，依次为输入整数对应的小时数、分钟数和秒数（可能为零），中间用空格隔开。
            */
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入秒数：");

        // 防止用户输入字母导致报错
        if (sc.hasNextInt()) {
            int seconds = sc.nextInt();

            // 校验输入范围是否有效
            if (seconds < 0 || seconds > 100_000_000) {
                System.out.println("输入错误！请输入 0-10^8 之间的数字。");
                sc.close();
                return;
            }

            // 调用转换方法
            int[] time = convertTime(seconds);
            
            // 打印结果
            System.out.println("转换结果：" + time[0] + " 小时 " + time[1] + " 分钟 " + time[2] + " 秒");
        } else {
            System.out.println("请输入有效的整数！");
            sc.next();
        }
        sc.close();
    }

    // 定义一个方法，用于将秒数转换为小时数、分钟数和秒数
    public static int[] convertTime(int seconds) {
        int second = seconds % 60;
        int minute = seconds / 60 % 60;
        int hour = seconds / 3600;
        /*
        另一种算法：
        int hour = seconds % 3600;
        int minute = (seconds % 3600) / 60;
        int second = (seconds % 3600) % 60;
         */
        return new int[]{hour, minute, second};
    }
}
