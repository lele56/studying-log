package Array;

public class ArrayDemo02 {
    public static void main(String[] args) {
        /*
        数组的遍历：
            定义一个整数数组，里面存储任意数据，并将数组遍历并打印。
        */
        // 1. 定义一个整数数组
        int[] arr = {1, 2, 3, 4, 5};
        // 2. 遍历数组
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
    }
}
