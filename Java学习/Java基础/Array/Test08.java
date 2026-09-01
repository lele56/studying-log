package Array;

public class Test08 {
    public static void main(String[] args) {
        /*
        查找元素
        给定一个递增的有序数组和一个目标值，在数组中查找目标值，打印其索引。
        如果目标值不存在于数组中，打印应插入的位置。
        
        举例1：
        输入: nums = [1,3,5,6], target = 5
        输出: 2

        举例2：
        输入: nums = [1,3,5,6], target = 2
        输出: 1

        举例3：
        输入: nums = [1,3,5,6], target = 7
        输出: 4
        */
        // 1. 定义一个递增有序数组
        int[] arr = {1, 3, 5, 6};
        int target = 7;
        
        // 二分查找
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                System.out.println(mid);
                return;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        // 没找到，返回应插入的位置
        System.out.println(left);
    }
}