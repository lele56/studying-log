package Array;

public class ArrayDemo01 {
    public static void main(String[] args) {
        /*
        数组中元素的访问：
            1.获取数据
            2.修改数据
        */

        // 1. 利用静态初始化创建数组
        int[] arr = {1, 2, 3, 4, 5};

        // 2. 获取数组中的元素
        // 索引：从 0 开始，依次递增
        // 0 1 2 3 4
        System.out.println(arr[0]);

        // 3. 修改数组中的元素
        arr[0] = 100;
        System.out.println(arr[0]);
    }
}
