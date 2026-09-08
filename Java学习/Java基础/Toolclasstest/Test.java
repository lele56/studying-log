package Toolclasstest;

/**
 * 测试类：演示 ArrayUtil 工具类的使用
 * 
 * 调用方式：类名.方法名(参数)
 * 如：ArrayUtil.printArr(arr)、ArrayUtil.getAverage(arr)
 * 无需创建对象，直接通过类名调用静态方法
 */
public class Test {
    public static void main(String[] args) {
        // 准备测试数据
        int[] scores = {85, 92, 78, 95, 88, 72, 90};

        // ==================== 演示 printArr() ====================
        System.out.println("==================== 遍历数组 ====================");
        System.out.print("数组内容：");
        ArrayUitl.printArr(scores);  // 通过类名直接调用静态方法

        // ==================== 演示 getAverage() ====================
        System.out.println("\n==================== 计算平均值 ====================");
        double avg = ArrayUitl.getAverage(scores);
        System.out.println("平均分：" + String.format("%.2f", avg));

        // ==================== 演示 getMax() ====================
        System.out.println("\n==================== 查找最大值 ====================");
        int max = ArrayUitl.getMax(scores);
        System.out.println("最高分：" + max);

        // ==================== 演示 getMin() ====================
        System.out.println("\n==================== 查找最小值 ====================");
        int min = ArrayUitl.getMin(scores);
        System.out.println("最低分：" + min);

        // ==================== 演示 getSum() ====================
        System.out.println("\n==================== 计算总和 ====================");
        int sum = ArrayUitl.getSum(scores);
        System.out.println("总分：" + sum);

        // ==================== 演示空数组保护 ====================
        System.out.println("\n==================== 空数组保护测试 ====================");
        int[] emptyArr = {};
        System.out.print("空数组遍历：");
        ArrayUitl.printArr(emptyArr);
        System.out.println("空数组平均值：" + ArrayUitl.getAverage(emptyArr));
        System.out.println("空数组总和：" + ArrayUitl.getSum(emptyArr));
    }
}