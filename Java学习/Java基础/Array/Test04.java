package Array;

import java.util.Random;

public class Test04 {
    public static void main(String[] args) {
        /*
        需求：获取 10 个 1~100 之间的随机数并存入到数组中，要求保证数据是唯一的
        思路：
            如果存在，就不存，继续生成下一个随机数
            如果不存在，就存入到数组当中
        */

        // 1. 定义一个数组
        int[] arr = new int[10];

        // 2. 生成随机数
        Random random = new Random();
        for (int i = 0; i < arr.length; ) {
            // 3. 获取随机数
            int num = random.nextInt(100) + 1;

            // 4. 判断随机数是否存在
            boolean flag = false;
            for (int j = 0; j < i; j++) {
                if (arr[j] == num) {
                    flag = true;
                    break;
                }
            }
            // 只有符合条件的存入才会移动索引
            if (!flag) {
                arr[i] = num;
                i++;
            }
        }
        // 5. 打印数组
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
    }
}
