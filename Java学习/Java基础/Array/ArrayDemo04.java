package Array;

public class ArrayDemo04 {
    public static void main(String[] args) {
        /*
        数组的常见问题：
            索引越界

            针对于任意一个数组而言，索引的范围是从 0 开始，到数组的长度 - 1 结束。
        */

        // 1. 定义一个数组
        int[] arr = {1, 2, 3, 4, 5};
        int index = 10;
        if (index >= 0 && index < arr.length) {
            System.out.println(arr[index]);
        } else {
            System.out.println("索引越界");
        }
    }
}
