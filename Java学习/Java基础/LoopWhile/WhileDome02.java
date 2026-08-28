package LoopWhile;

public class WhileDome02 {
    public static void main(String[] args) {
        /*
        假设你在银行投资了 100_000元，银行给出的复利是 1.7%，问多少年后能是实现本金翻倍？
        */
        int year = 0;
        double ratio = 1;
        while (ratio < 2) {
            ratio *= 1.017;
            year++;
        }
        System.out.println("需要 " + year + " 年才能实现本金翻倍");
        System.out.println("最终金额：" + String.format("%.2f", 100000 * ratio) + " 元");
    }
}

// 输出结果
// 需要42年才能实现本金翻倍