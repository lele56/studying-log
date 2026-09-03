package Method;

import java.util.Scanner;

public class Test02 {
    public static void main(String[] args) {
        /*
        计算班级分数
        班主任需要统计 10 名学生的数学成绩（0~100）
        计算及格率，平均分，并找出最高分。
        要求1：键盘录入 10 名学生的成绩，存入数组。超出范围，提示“成绩无效，请重新输入！”
        要求2：定义方法，求及格人数，根据及格人数，求及格率。
        要求3：定义方法求总分，根据总分求平均分。
        要求4：定义方法，求最高分。
        */
        Scanner sc = new Scanner(System.in);
        int[] scores = new int[10];
        for (int i = 0; i < scores.length; i++) {
            System.out.println("请输入第" + (i + 1) + "个学生的成绩：");
            
            if (!sc.hasNextInt()) {
                System.out.println("请输入有效的整数！");
                sc.next();
                i--;
                continue;
            }
            
            scores[i] = sc.nextInt();
            
            if (scores[i] < 0 || scores[i] > 100) {
                System.out.println("成绩不在范围内，请重新输入！");
                i--;
            }
        }
        double passRate = getPassRate(scores);
        int total = getTotal(scores);
        int max = getMax(scores);
        System.out.println("及格率：" + String.format("%.2f", passRate));
        System.out.println("总分：" + total);
        System.out.println("平均分：" + String.format("%.2f", (double) total / scores.length));
        System.out.println("最高分：" + max);
        sc.close();
    }

    // 求及格率
    public static double getPassRate(int[] scores) {
        int passCount = 0;
        for (int i = 0; i < scores.length; i++) {
            if (scores[i] >= 60) {
                passCount++;
            }
        }
        return (double) passCount / scores.length;
    }

    // 求总分
    public static int getTotal(int[] scores) {
        int total = 0;
        for (int i = 0; i < scores.length; i++) {
            total += scores[i];
        }
        return total;
    }

    // 求最高分
    public static int getMax(int[] scores) {
        int max = scores[0];
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] > max) {
                max = scores[i];
            }
        }
        return max;
    }
}