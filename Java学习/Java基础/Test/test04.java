package Test;

import java.util.Random;

public class test04 {
    public static void main(String[] args) {
        /*
        学校选举学生会主席，有 5 个候选人
        全校 1000 名同学参与投票（每人一票，可以弃权，或者选 1~5号）
        投票用 Random 模拟
            0：弃权
            1~5：给对应的候选人投票

        要求1：
            统计每个候选人的得票数和得票率，并找出票最多的候选人？
        要求2：
            统计弃票数和弃权率是多少？
        */
        // 定义投票人数为 1000
        int num = 1000;
        // 定义候选人人数为 5
        int candidateNum = 5;
        // 定义投票数组（索引 0 存弃权，1~5 存候选人）
        int[] votes = new int[candidateNum + 1];
        // 定义随机数对象
        Random random = new Random();
        
        // 随机投票
        for (int i = 0; i < num; i++) {
            int vote = random.nextInt(6);  // 0~5
            votes[vote]++;
        }
        
        // 打印候选人得票结果
        System.out.println("投票结果：");
        for (int i = 1; i <= candidateNum; i++) {
            double rate = (double) votes[i] / num * 100;
            System.out.printf("候选人%d：得票 %d 票，得票率 %.2f%%\n", i, votes[i], rate);
        }
        
        // 打印弃票数和弃权率
        System.out.println("\n弃票数：" + votes[0]);
        System.out.printf("弃权率：%.2f%%\n", (double) votes[0] / num * 100);
        
        // 找出票最多的候选人
        int max = 0;
        int maxIndex = 0;
        for (int i = 1; i <= candidateNum; i++) {
            if (votes[i] > max) {
                max = votes[i];
                maxIndex = i;
            }
        }
        System.out.println("\n票最多的候选人是：" + maxIndex + "号，共 " + max + " 票");
    }
}