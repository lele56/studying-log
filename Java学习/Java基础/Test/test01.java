package Test;

public class test01 {
    public static void main(String[] args) {
        /*
        给你一个数组和 nums 和一个值 val，你需要删除所有数组等于 val 的元素
        举例1：
        输入：nums = [3,2,2,3], val = 3
        输出：nums = [2,2] 剩余 2 个元素
        举例2：
        输入：nums = [0,1,2,2,3,0,4,2], val = 2
        输出：nums = [0,1,3,0,4] 剩余 5 个元素
        */
        int[] nums = {0,1,2,2,3,0,4,2};
        int val = 2;
        int newLength = removeElement(nums, val);
        
        System.out.print("剩余元素: [");
        for (int i = 0; i < newLength; i++) {
            System.out.print(nums[i] + (i == newLength - 1 ? "" : ", "));
        }
        System.out.println("] 剩余 " + newLength + " 个元素");
    }

    // 双指针法：删除数组中等于 val 的元素
    public static int removeElement(int[] nums, int val) {
        int slow = 0;  // 慢指针指向下一个要存放的位置
        int fast = 0;  // 快指针遍历数组
        
        while (fast < nums.length) {
            if (nums[fast] != val) {
                nums[slow] = nums[fast];
                slow++;
            }
            fast++;
        }
        
        return slow;  // 返回新数组的长度
    }
}