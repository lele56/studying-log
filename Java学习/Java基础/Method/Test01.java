package Method;

import java.util.Scanner;

public class Test01 {
    public static void main(String[] args) {       
        /*
        评委打分
        跳水比赛有五个评委打分，分数在 0~100 之间。最终得分会去掉一个最高分，去掉一个最低分，
        剩余的分数再求平均数，改平均数为选手的最终得分。
        要求1：利用键盘录入 5 个整数存入数组当中，如果分数超过范围需要重新录入
        要求2：定义方法分别求数组的最大值和最小值
        要求3：计算五名评委的总分
        要求4：总分 - 最大值 - 最小值，求选手的最终平均分
        */
        Scanner sc = new Scanner(System.in);
        int[] scores = new int[5];
        for (int i = 0; i < scores.length; i++) {
            System.out.println("请输入第" + (i + 1) + "个评委的分数：");
            
            if (!sc.hasNextInt()) {
                System.out.println("请输入有效的整数！");
                sc.next();
                i--;
                continue;
            }
            
            scores[i] = sc.nextInt();
            if (scores[i] < 0 || scores[i] > 100) {
                System.out.println("分数不在范围内，请重新输入！");
                i--;
            }
        }
        
        int max = getMax(scores);
        int min = getMin(scores);
        int total = getTotal(scores);
        double mean = getMean(total, max, min);
        
        System.out.println("总分：" + total);
        System.out.println("最高分：" + max);
        System.out.println("最低分：" + min);
        System.out.println("选手的最终平均分是：" + String.format("%.2f", mean));
        sc.close();
    }
    
    // 求最大值
    public static int getMax(int[] scores) {
        int max = scores[0];
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] > max) {
                max = scores[i];
            }
        }
        return max;
    }
    
    // 求最小值
    public static int getMin(int[] scores) {
        int min = scores[0];
        for (int i = 1; i < scores.length; i++) {
            if (scores[i] < min) {
                min = scores[i];
            }
        }
        return min;
    }
    
    // 求总分
    public static int getTotal(int[] scores) {
        int sum = 0;
        for (int score : scores) {
            sum += score;
        }
        return sum;
    }
    
    // 求平均分（去掉最高分和最低分）
    public static double getMean(int total, int max, int min) {
        return (double) (total - max - min) / 3;
    }
}