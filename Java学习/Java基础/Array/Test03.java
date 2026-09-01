package Array;

import java.util.Random;

public class Test03 {
    public static void main(String[] args) {
        /*
        需求：已知数组元素为{1，2，3，4，5，6，7，8，9，10}
        要求：打乱数组中的数据

        思路：
            第一步：
                0 索引上的数据，跟随机位置上的数据进行交换

            第二步：
                从第二步开始，重复上面操作
        */
        // 1. 定义一个数组
        int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

        Random random = new Random();

        // 2. 遍历数组
        for (int i = 0; i < arr.length; i++) {
            // 3. 获取随机索引
            int index = random.nextInt(arr.length);
            // 4. 交换数据
            int temp = arr[i];
            arr[i] = arr[index];
            arr[index] = temp;
        }
        // 5. 打印数组
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
    }
}
