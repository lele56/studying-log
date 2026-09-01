package Array;

import java.util.Arrays;

public class Test06 {
    public static void main(String[] args) {
        /*
        两数之和
        给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那 两个 整数，并返回它们的数组下标。
        要求：
            1. 只要输出第一对满足要求的情况
            2. 输出所有满足要求的情况
        举例1：
        输入：数组 nums = [2,7,11,15], target = 9
        输出：下标 [0,1]

        举例2：
        输入：数组 nums = [3,2,4], target = 6
        输出：下标 [1,2]
        */
        int nums[] = {3, 2, 4};
        int target = 6;
        
        // 创建二维数组保存原始值和原始下标
        int[][] numsWithIndex = new int[nums.length][2];
        for (int i = 0; i < nums.length; i++) {
            numsWithIndex[i][0] = nums[i];  // 值
            numsWithIndex[i][1] = i;        // 原始下标
        }
        
        // 按值升序排序
        Arrays.sort(numsWithIndex, (a, b) -> a[0] - b[0]);
        
        // 快慢指针
        int slow = 0;
        int fast = nums.length - 1;
        
        while (slow < fast) {
            int sum = numsWithIndex[slow][0] + numsWithIndex[fast][0];
            
            if (sum == target) {
                System.out.println("下标 [" + numsWithIndex[slow][1] + "," + numsWithIndex[fast][1] + "]");
                break;
            } else if (sum < target) {
                slow++;  // 和太小，左指针右移
            } else {
                fast--;  // 和太大，右指针左移
            }
        }
    }    
}