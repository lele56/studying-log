package Array;

import java.util.Scanner;

public class Test01 {
    public static void main(String[] args) {
        /*
        需求：已知数组元素为 {33，5，22，44，55，33}
        键盘录入任意一个数据，查找这个数据在数组中是否存在
        如果数组中要查找的数据出现多次，只要显示第一次的索引即可
        输出要求：
        如果存在打印索引
        如果不存在，提示“该数据不存在”
         */

        // 1. 定义一个数组
        int[] arr = {33, 5, 22, 44, 55, 33};

        // 2. 键盘录入数据
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入要查找的数据：");
        int find = sc.nextInt();

        // 3. 遍历数组，查找数据
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == find) {
                System.out.println("该数据的索引为：" + i);
                sc.close();
                return;
            }
        }
        System.out.println("该数据不存在");
        sc.close();
    }
}
