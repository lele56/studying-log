package Test;

public class test03 {
    public static void main(String[] args) {
        /*
        给定两个正序数组 arr1 和 arr2，请先合并这两个数组，并找出合并之后的数组中位数
        */
        // 定义两个正序数组 arr1 和 arr2
        int[] arr1 = {1, 3, 5, 7, 9};
        int[] arr2 = {2, 4};
        // 调用方法 FindMedianSortedArrays 找出合并之后的数组中位数
        double median = findMedianSortedArrays(arr1, arr2);
        System.out.println("合并之后的数组中位数为：" + median);
    }

    public static double findMedianSortedArrays(int[] arr1, int[] arr2) {
        // 合并两个有序数组
        int[] merged = new int[arr1.length + arr2.length];
        int i = 0, j = 0, k = 0;
        
        // 比较合并
        while (i < arr1.length && j < arr2.length) {
            if (arr1[i] <= arr2[j]) {
                merged[k++] = arr1[i++];
            } else {
                merged[k++] = arr2[j++];
            }
        }
        
        // 处理剩余元素
        while (i < arr1.length) {
            merged[k++] = arr1[i++];
        }
        while (j < arr2.length) {
            merged[k++] = arr2[j++];
        }
        
        // 找出中位数
        if (merged.length % 2 == 0) {
            return (merged[merged.length / 2 - 1] + merged[merged.length / 2]) / 2.0;
        } else {
            return merged[merged.length / 2];
        }
    }
}