package Array;

public class Test07 {
    public static void main(String[] args) {
        /*
        合并有序数组
        给你两个有序数组 arr1 和 arr2，
        将两个数组中的数据合并到一个大数组中。
        要求：合并之后的大数组也是有序的
        举例1：
        arr1 = {1, 3, 5, 7, 9}
        arr2 = {2, 4, 6, 8, 10}
        arr3 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        */
        
        // 1. 定义一个大数组，长度为 arr1 和 arr2 的长度之和
        int[] arr1 = {1, 3, 5, 7, 9};
        int[] arr2 = {2, 4, 6, 8, 10};
        int[] arr3 = new int[arr1.length + arr2.length];

        // 2. 定义三个索引，分别指向 arr1、arr2、arr3
        int index1 = 0;
        int index2 = 0;
        int index3 = 0;

        // 3. 遍历 arr1 和 arr2，比较两个数组中的元素，将较小的元素放入 arr3 中
        while (index1 < arr1.length && index2 < arr2.length) {
            if (arr1[index1] < arr2[index2]) {
                arr3[index3] = arr1[index1];
                index1++;
            } else {
                arr3[index3] = arr2[index2];
                index2++;
            }
            index3++;
        }

        // 4. 将剩余的元素放入 arr3 中
        while (index1 < arr1.length) {
            arr3[index3] = arr1[index1];
            index1++;
            index3++;
        }

        while (index2 < arr2.length) {
            arr3[index3] = arr2[index2];
            index2++;
            index3++;
        }

        // 5. 打印合并后的数组
        for (int i = 0; i < arr3.length; i++) {
            System.out.print(arr3[i] + " ");
        }
    }
}
