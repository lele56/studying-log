package Array;

public class Test02 {
    public static void main(String[] args) {
        /*
        需求：已知数组元素为{33，5，22，44，55}
        请找出数组中最大的元素
        */

        // 1. 定义一个数组
        int [] arr = {33, 5, 22, 44, 55};

        // 2. 定义一个变量，保存数组中最大的元素
        int max = arr[0];

        // 3. 遍历数组，查找最大的元素
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        System.out.println("数组中最大的元素为：" + max);

        
    }
}
