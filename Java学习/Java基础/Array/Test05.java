package Array;

public class Test05 {
    public static void main(String[] args) {
        /*
        定义一个递增有序数组，去除其中重复元素
        */
        // 1. 定义一个递增有序数组
        int[] arr = {1, 1, 2, 2, 2, 2, 3, 3, 3, 3};

        // 2. 定义两个指针
        int slow = 0;
        int fast = 1;

        // 3. 利用循环不断的移动快慢指针，找不重复的元素
        while (fast < arr.length) {
            // 判断两个指针指向数据是否相同
            if (arr[slow] != arr[fast]) {
                slow++;
                arr[slow] = arr[fast];
            }
            fast++;
        }
        // 打印去重后的数组
        for (int i = 0; i <= slow; i++) {
            System.out.print(arr[i] + " ");
        }
    }
}
