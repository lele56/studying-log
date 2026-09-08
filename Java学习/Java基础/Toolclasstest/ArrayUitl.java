package Toolclasstest;

/**
 * 数组工具类
 * 提供操作数组的静态方法，无需创建对象即可使用
 * 
 * 静态只能调用静态方法，非静态方法调用静态方法需要创建对象
 * 
 * 工具类设计原则：
 * 1. 构造方法私有化，防止外部创建对象
 * 2. 所有方法都定义为静态方法（static）
 * 3. 通过类名直接调用，如 ArrayUtil.printArr(arr)
 * 4. 常见工具类示例：Math、Arrays、Collections
 */
public class ArrayUitl {

    /**
     * 私有化构造方法
     * 目的：工具类不需要创建对象，防止外部 new ArrayUtil()
     */
    private ArrayUitl() {
    }

    /**
     * 遍历数组，格式化为 [a, b, c] 的形式输出
     * @param arr 要遍历的数组
     */
    public static void printArr(int[] arr) {
        // 空数组保护
        if (arr == null || arr.length == 0) {
            System.out.println("[]");
            return;
        }

        System.out.print("[");
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i]);
            if (i < arr.length - 1) {
                System.out.print(", ");  // 最后一个元素后面不加逗号
            }
        }
        System.out.println("]");
    }

    /**
     * 计算数组的平均值
     * @param arr 要计算的数组
     * @return 平均值（double 类型，保留小数）
     */
    public static double getAverage(int[] arr) {
        // 空数组保护，避免除以 0
        if (arr == null || arr.length == 0) {
            return 0;
        }

        double sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum / arr.length;  // 先转为 double 再除，保留小数
    }

    /**
     * 获取数组中的最大值
     * @param arr 要查找的数组
     * @return 数组中的最大值
     */
    public static int getMax(int[] arr) {
        if (arr == null || arr.length == 0) {
            throw new IllegalArgumentException("数组不能为空");
        }

        int max = arr[0];  // 假设第一个是最大值
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }

    /**
     * 获取数组中的最小值
     * @param arr 要查找的数组
     * @return 数组中的最小值
     */
    public static int getMin(int[] arr) {
        if (arr == null || arr.length == 0) {
            throw new IllegalArgumentException("数组不能为空");
        }

        int min = arr[0];  // 假设第一个是最小值
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < min) {
                min = arr[i];
            }
        }
        return min;
    }

    /**
     * 计算数组的总和
     * @param arr 要计算的数组
     * @return 数组元素的总和
     */
    public static int getSum(int[] arr) {
        if (arr == null || arr.length == 0) {
            return 0;
        }

        int sum = 0;
        for (int num : arr) {  // 增强 for 循环，更简洁
            sum += num;
        }
        return sum;
    }
}