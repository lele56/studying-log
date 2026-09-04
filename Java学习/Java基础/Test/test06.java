package Test;

import java.util.Arrays;
import java.util.Random;

public class test06 {
    public static void main(String[] args) {
        /**
         * 大乐透选号规则
         * 基本结构：采用"5+2"双区投注模式，前区35选5与后区12选2
         * 1.前区号码不可重复（01-35 选 5 个）
         * 2.后区号码不可重复（01-12 选 2 个）
         * 3.跨区允许重复（前区选10，后区也可选10）
         * 
         * 中奖规则（前区命中数 + 后区命中数）：
         *     一等奖：5 + 2
         *     二等奖：5 + 1
         *     三等奖：5 + 0 / 4 + 2
         *     四等奖：4 + 1 / 3 + 2
         *     五等奖：4 + 0 / 3 + 1 / 2 + 2
         *     六等奖：3 + 0 / 1 + 2 / 2 + 1 / 0 + 2
         */
        Random random = new Random();

        // ==================== 前区选号：35 选 5 ====================
        // 洗牌算法（Fisher-Yates）：将数组分为"已选区域"和"待选区域"
        // 每次从待选区域随机取一个数，交换到已选区域的末尾
        // 
        // 示例： [1, 2, 3, ..., 35]  →  [12, 28, 5, 33, 7, | ...]
        //                                    ↑ 已选区域         ↑ 待选区域
        //                                    (前 5 个)          (剩余 30 个)

        // 1. 创建号码池 [1, 2, 3, ..., 35]
        int[] pool = new int[35];
        for (int i = 0; i < pool.length; i++) {
            pool[i] = i + 1;
        }

        // 2. 洗牌：只洗前 5 次，每次确定一个号码
        for (int i = 0; i < 5; i++) {
            // 从待选区域 [i, 34] 中随机选一个下标
            // pool.length - i 是待选区域的大小，+ i 是偏移到实际下标
            int randIndex = random.nextInt(pool.length - i) + i;
            // 将选中的号码交换到已定区域（位置 i）
            int temp = pool[i];
            pool[i] = pool[randIndex];
            pool[randIndex] = temp;
        }

        // 3. 前 5 个即为前区号码（不排序，保持随机顺序）
        int[] front = Arrays.copyOf(pool, 5);

        // ==================== 后区选号：12 选 2 ====================
        // 同样使用洗牌算法，逻辑与前区完全一致

        // 1. 创建号码池 [1, 2, 3, ..., 12]
        int[] poolBack = new int[12];
        for (int i = 0; i < poolBack.length; i++) {
            poolBack[i] = i + 1;
        }

        // 2. 洗牌：只洗前 2 次
        for (int i = 0; i < 2; i++) {
            int randIndex = random.nextInt(poolBack.length - i) + i;
            int temp = poolBack[i];
            poolBack[i] = poolBack[randIndex];
            poolBack[randIndex] = temp;
        }

        // 3. 前 2 个即为后区号码
        int[] back = Arrays.copyOf(poolBack, 2);

        // ==================== 输出投注号码 ====================
        System.out.println("您的投注号码：");
        System.out.print("  前区：");
        for (int i = 0; i < front.length; i++) {
            System.out.printf("%02d ", front[i]);  // %02d 保证两位数显示，如 01、09
        }
        System.out.print("\n  后区：");
        for (int i = 0; i < back.length; i++) {
            System.out.printf("%02d ", back[i]);
        }

        // ==================== 生成开奖号码 ====================
        // 复用 generateNumbers 方法，逻辑与投注选号完全一致
        int[] winFront = generateNumbers(random, 35, 5);
        int[] winBack = generateNumbers(random, 12, 2);

        System.out.println("\n\n本期开奖号码：");
        System.out.print("  前区：");
        for (int i = 0; i < winFront.length; i++) {
            System.out.printf("%02d ", winFront[i]);
        }
        System.out.print("\n  后区：");
        for (int i = 0; i < winBack.length; i++) {
            System.out.printf("%02d ", winBack[i]);
        }

        // ==================== 计算中奖结果 ====================
        // 分别统计前区和后区的命中个数
        int frontMatch = countMatch(front, winFront);  // 前区命中数
        int backMatch = countMatch(back, winBack);      // 后区命中数
        String prize = getPrize(frontMatch, backMatch); // 根据命中数判断等级

        System.out.println("\n\n中奖结果：");
        System.out.println("  前区命中 " + frontMatch + " 个，后区命中 " + backMatch + " 个");
        System.out.println("  " + prize);
    }

    /**
     * 洗牌算法生成不重复的随机号码（用于生成开奖号码）
     * 核心原理：将数组分为"已选区域"和"待选区域"，每次从待选区域随机选一个交换到前面
     * 
     * @param random 随机数生成器
     * @param total  号码池总数（如 35 或 12）
     * @param count  需要选取的个数（如 5 或 2）
     * @return 已排序的号码数组
     */
    public static int[] generateNumbers(Random random, int total, int count) {
        // 创建号码池 [1, 2, 3, ..., total]
        int[] pool = new int[total];
        for (int i = 0; i < total; i++) {
            pool[i] = i + 1;
        }

        // 洗牌 count 次
        for (int i = 0; i < count; i++) {
            // 从待选区域 [i, total-1] 中随机选一个下标
            int randIndex = random.nextInt(total - i) + i;
            // 交换到位置 i
            int temp = pool[i];
            pool[i] = pool[randIndex];
            pool[randIndex] = temp;
        }

        // 取前 count 个作为结果，排序后返回
        int[] result = Arrays.copyOf(pool, count);
        Arrays.sort(result);
        return result;
    }

    /**
     * 统计两个数组中相同元素的个数（用于判断命中数）
     * 思路：遍历用户号码，逐个在开奖号码中查找是否匹配
     * 
     * @param user 用户投注的号码
     * @param win  开奖号码
     * @return 命中的个数
     */
    public static int countMatch(int[] user, int[] win) {
        int count = 0;
        for (int u : user) {           // 遍历用户号码
            for (int w : win) {        // 在开奖号码中逐一对比
                if (u == w) {
                    count++;           // 命中，计数 +1
                    break;             // 找到就跳出内层循环，避免重复计数
                }
            }
        }
        return count;
    }

    /**
     * 根据前区和后区命中数判断中奖等级
     * 从高奖到低奖依次判断，命中第一个满足条件的即返回
     * 
     * @param front 前区命中个数（0~5）
     * @param back  后区命中个数（0~2）
     * @return 中奖等级描述
     */
    public static String getPrize(int front, int back) {
        // 一等奖：前区全中 5 个，后区全中 2 个
        if (front == 5 && back == 2) return "一等奖！奖金 1000 万元";
        // 二等奖：前区全中 5 个，后区中 1 个
        if (front == 5 && back == 1) return "二等奖！奖金 50 万元";
        // 三等奖：前区全中 5 个 或 前区中 4 个 + 后区全中 2 个
        if (front == 5 && back == 0) return "三等奖！奖金 1 万元";
        if (front == 4 && back == 2) return "三等奖！奖金 1 万元";
        // 四等奖：前区中 4 个 + 后区中 1 个 或 前区中 3 个 + 后区全中 2 个
        if (front == 4 && back == 1) return "四等奖！奖金 3000 元";
        if (front == 3 && back == 2) return "四等奖！奖金 3000 元";
        // 五等奖：前区中 4 个 或 前区中 3 个 + 后区中 1 个 或 前区中 2 个 + 后区全中 2 个
        if (front == 4 && back == 0) return "五等奖！奖金 300 元";
        if (front == 3 && back == 1) return "五等奖！奖金 300 元";
        if (front == 2 && back == 2) return "五等奖！奖金 300 元";
        // 六等奖：前区中 3 个 或 前区中 1 个 + 后区全中 2 个
        //         或 前区中 2 个 + 后区中 1 个 或 后区全中 2 个
        if (front == 3 && back == 0) return "六等奖！奖金 100 元";
        if (front == 1 && back == 2) return "六等奖！奖金 100 元";
        if (front == 2 && back == 1) return "六等奖！奖金 100 元";
        if (front == 0 && back == 2) return "六等奖！奖金 100 元";
        // 未中奖
        return "未中奖，再接再厉！";
    }
}