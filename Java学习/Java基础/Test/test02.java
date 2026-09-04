package Test;

import java.util.Random;

public class test02 {
    public static void main(String[] args) {
        /*
        红包问题
        给你两个整数 M 和 N，M 表示红包的总额，N 表示红包的个数
        现在又 N 个人来抽红包，每个人都是随机的，打印每个人领的红包金额
        要求1：每个人最少 1 分钱
        要求2：每个人领完红包之后，至少预留 1 * N 分钱
        要求3：最后一个人是拿剩余的总额
        */
        // 定义红包总额 M 为 20000 分钱
        int money = 20000;

        // 定义红包个数 N 为 5 人
        int num = 5;
        redPacket(money, num);
    }
    
    public static void redPacket(int money, int num) {
        Random random = new Random();
        
        for (int i = 1; i < num; i++) {
            // 当前可抢的最大金额 = 剩余金额 - 后面每人至少留 1 分
            int maxMoney = money - (num - i);
            
            // 限制单次最大金额，避免前面的人抢走太多（不超过剩余的 60%）
            int safeMax = Math.min(maxMoney, money * 6 / 10);
            
            int myMoney = random.nextInt(safeMax) + 1;
            money -= myMoney;
            
            System.out.println("第" + i + "个人领了" + myMoney + "分");
        }
        
        // 最后一个人拿剩余的全部
        System.out.println("第" + num + "个人领了" + money + "分");
    }
}