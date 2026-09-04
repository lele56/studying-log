package Test;

public class test05 {
    public static void main(String[] args) {
        /*
        接雨水
        给定 n 个非负数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少水
        输入：height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
        输出：6
        */
        int[] height = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
        int n = height.length;
        int[] leftMax = new int[n];
        int[] rightMax = new int[n];

        // 初始化边界
        leftMax[0] = height[0];
        rightMax[n - 1] = height[n - 1];

        // 从左往右，记录每个位置左边（含自身）的最大值
        for (int i = 1; i < n; i++) {
            leftMax[i] = Math.max(leftMax[i - 1], height[i]);
        }
        
        // 从右往左，记录每个位置右边（含自身）的最大值
        for (int i = n - 2; i >= 0; i--) {
            rightMax[i] = Math.max(rightMax[i + 1], height[i]);
        }
        
        // 计算能接的雨水
        int water = 0;
        for (int i = 0; i < n; i++) {
            water += Math.min(leftMax[i], rightMax[i]) - height[i];
        }
        System.out.println("能接的雨水为：" + water);
    }
}